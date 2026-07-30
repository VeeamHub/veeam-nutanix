#!/usr/bin/env python3
"""vbrcli -- Veeam Backup & Replication CLI, Nutanix AHV-first.

Single stdlib-only file, no pip (Python 3.7+, any OS). TSV output by default,
-j / --json for raw JSON. Talks to two APIs and hides the difference:

  * PUBLIC  VBR REST   https://<host>:9419/api/v1/...   (x-api-version header)
        - platform-agnostic: sessions, backups, restore points, credentials,
          managed servers, repositories, backup copy jobs, file-level restore.
  * PRIVATE plugin API https://<host>/extension/<instanceId>/api/<ver>/...
        - the per-platform workhorse (AHV/Proxmox/Xen/...): clusters, prism
          centrals, workers, jobs, restore, instant recovery, sessions. The
          API version differs per platform (AHV = v10, the newer
          Virtualization Plug-ins = v1); vbrcli prepends it for you. Reached
          through the VBR reverse proxy on 443 after a 3-step token dance
          (password -> extensions list -> per-plugin vbr_extension token).

Config: ~/.vbrcli.json (Windows: %USERPROFILE%\\.vbrcli.json), see
config.example.json. Token cache: ~/.vbrcli.tokens.json (auto-managed;
delete it to force re-login).

The public :9419 login has anti-bruteforce lockout (~14 min after a few bad
tokens), so tokens are cached and reused until shortly before expiry. Do not
loop-retry a failed login.

TLS certificates are verified by default. A VBR server uses a self-signed
certificate out of the box, so a host whose certificate is not in the local
trust store needs --insecure (or "insecure": true in the config).
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSION = "0.4.0"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".vbrcli.json")
TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".vbrcli.tokens.json")
DEFAULT_REST_API = "1.3-rev0"
# Nutanix Prism / Prism Central UI+API port.
DEFAULT_NUTANIX_PORT = 9440

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


class CliError(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg)
        self.code = code


# ---------------------------------------------------------------------- #
# config + token cache

def load_config():
    """~/.vbrcli.json, overridable per-key by VBRCLI_* env vars."""
    path = os.environ.get("VBRCLI_CONFIG", CONFIG_PATH)
    cfg = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as f:
            cfg = json.load(f)
    for env, key in (("VBRCLI_URL", "url"),
                     ("VBRCLI_USERNAME", "username"),
                     ("VBRCLI_PASSWORD", "password"),
                     ("VBRCLI_PLATFORM", "platform")):
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    for key in ("url", "username", "password"):
        if not cfg.get(key):
            raise CliError(
                "no '%s' in %s (and no VBRCLI_%s env). Create the config from "
                'config.example.json: {"url": "https://<vbr-host>", '
                '"username": "HOST\\\\Administrator", "password": "...", '
                '"rest_port": 9419, "platform": "AHV"}'
                % (key, path, key.upper()), 2)
    cfg.setdefault("rest_port", 9419)
    cfg.setdefault("platform", "AHV")
    cfg.setdefault("rest_api_version", DEFAULT_REST_API)
    cfg.setdefault("insecure", False)
    return cfg


def _load_tokens():
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_tokens(tok):
    tmp = TOKEN_PATH + ".tmp"
    # create 0600 from the start: the file holds bearer tokens, and on POSIX
    # a plain open() would briefly leave it world-readable before chmod.
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(tok, f)
    os.replace(tmp, TOKEN_PATH)
    try:
        os.chmod(TOKEN_PATH, 0o600)
    except Exception:
        pass


# ---------------------------------------------------------------------- #
# core client

class Vbr:
    def __init__(self, cfg):
        self.cfg = cfg
        self.base = cfg["url"].rstrip("/")
        self.rest_base = "%s:%s" % (self.base, cfg["rest_port"])
        self.rest_api = cfg["rest_api_version"]
        # Verification stays on unless it is switched off explicitly, and the
        # same context serves both the public REST port and the plugin API
        # behind the 443 reverse proxy.
        self.insecure = bool(cfg.get("insecure"))
        self.ctx = ssl.create_default_context()
        if self.insecure:
            self.ctx.check_hostname = False
            self.ctx.verify_mode = ssl.CERT_NONE
        # vbrcli always dials the VBR host directly; never route through a
        # system/env proxy (macOS urllib picks one up from System Settings,
        # which silently breaks private network addresses).
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=self.ctx))
        self._tokens = _load_tokens()
        self._ext_cache = None
        self._api_ver_cache = {}

    # -- low level ---------------------------------------------------- #
    def _raw(self, url, method="GET", headers=None, data=None,
             ctype="application/json", timeout=180):
        req = urllib.request.Request(url, data=data, method=method)
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        if data is not None and "Content-Type" not in (headers or {}):
            req.add_header("Content-Type", ctype)
        try:
            with self.opener.open(req, timeout=timeout) as r:
                payload = r.read()
                ct = r.headers.get("Content-Type", "")
                if "json" in ct and payload:
                    return json.loads(payload.decode("utf-8-sig"))
                if not payload:
                    return {}
                return payload
        except urllib.error.HTTPError as e:
            body = e.read()
            msg = ""
            try:
                d = json.loads(body.decode("utf-8-sig"))
                msg = (d.get("message") or d.get("detail") or d.get("title")
                       or json.dumps(d))
                if d.get("errors"):
                    msg += " | " + json.dumps(d["errors"])
            except Exception:
                text = body[:500].decode("utf-8", "replace")
                msg = ("(HTML page returned — token invalid/expired?)"
                       if "<html" in text.lower() else text)
            raise CliError("HTTP %d %s\n%s" % (e.code, url, msg[:800]))
        except urllib.error.URLError as e:
            if isinstance(e.reason, ssl.SSLCertVerificationError):
                raise CliError(
                    "TLS certificate verification failed: %s\n%s\nA VBR "
                    "server uses a self-signed certificate out of the box; "
                    "either trust it locally or re-run with --insecure "
                    '(equivalent to "insecure": true in the config).'
                    % (url, e.reason))
            raise CliError("connection failed: %s (%s)" % (url, e.reason))

    @staticmethod
    def _form(d):
        return urllib.parse.urlencode(d).encode()

    def _cache_key(self, key):
        # Cached tokens are namespaced per target host: plugin instanceIds are
        # per-platform constants, not per-server, so an unqualified key would
        # let a second VBR reuse the first one's token.
        return "%s|%s" % (self.base, key)

    def _cache_get(self, key):
        t = self._tokens.get(self._cache_key(key))
        if t and t.get("exp", 0) > time.time() + 60:
            return t["token"]
        return None

    def _cache_put(self, key, token, expires_in):
        self._tokens[self._cache_key(key)] = {
            "token": token, "exp": time.time() + int(expires_in or 900)}
        # Keys without a host prefix can never be looked up; drop them as we
        # go so the cache file does not accumulate unreachable entries.
        for stale in [k for k in self._tokens if "|" not in k]:
            del self._tokens[stale]
        _save_tokens(self._tokens)

    # -- auth: public REST :9419 ------------------------------------- #
    def public_token(self, force=False):
        if not force:
            t = self._cache_get("public")
            if t:
                return t
        r = self._raw(
            self.rest_base + "/api/oauth2/token", "POST",
            {"x-api-version": self.rest_api,
             "Content-Type": "application/x-www-form-urlencoded"},
            self._form({"grant_type": "password",
                        "username": self.cfg["username"],
                        "password": self.cfg["password"]}))
        self._cache_put("public", r["access_token"], r.get("expires_in"))
        return r["access_token"]

    def pub(self, path, method="GET", body=None, api=None, timeout=180):
        url = self.rest_base + path
        headers = {"x-api-version": api or self.rest_api,
                   "Authorization": "Bearer " + self.public_token(),
                   "Accept": "application/json"}
        data = json.dumps(body).encode() if body is not None else None
        return self._raw(url, method, headers, data, timeout=timeout)

    # -- auth: private base :443 ------------------------------------- #
    def private_base_token(self, force=False):
        if not force:
            t = self._cache_get("private_base")
            if t:
                return t
        r = self._raw(
            self.base + "/private-api/oauth2/token", "POST",
            {"Content-Type": "application/x-www-form-urlencoded"},
            self._form({"grant_type": "password",
                        "username": self.cfg["username"],
                        "password": self.cfg["password"]}))
        self._cache_put("private_base", r["access_token"], r.get("expires_in"))
        return r["access_token"]

    def priv(self, path, method="GET", body=None, timeout=180):
        url = self.base + path
        headers = {"Authorization": "Bearer " + self.private_base_token(),
                   "Accept": "application/json"}
        data = json.dumps(body).encode() if body is not None else None
        return self._raw(url, method, headers, data, timeout=timeout)

    # -- extensions + per-plugin token ------------------------------- #
    def extensions(self):
        if self._ext_cache is None:
            r = self.priv("/private-api/v1/vbrinfo/extensions")
            self._ext_cache = r.get("data", r)
        return self._ext_cache

    def extension(self, platform):
        for e in self.extensions():
            if e.get("type", "").lower() == platform.lower():
                return e
        avail = ", ".join(e.get("type") for e in self.extensions())
        raise CliError("no '%s' plugin installed on this VBR. Available: %s"
                       % (platform, avail), 4)

    def plugin_token(self, platform, force=False):
        ext = self.extension(platform)
        key = "plugin_" + ext["instanceId"]
        if not force:
            t = self._cache_get(key)
            if t:
                return t, ext
        r = self._raw(
            self.base + "/private-api/oauth2/vbr_extension", "POST",
            {"Authorization": "Bearer " + self.private_base_token(),
             "Content-Type": "application/x-www-form-urlencoded"},
            self._form({"grant_type": "vbr_common_auth",
                        "type": ext["type"],
                        "instance_id": ext["instanceId"]}))
        self._cache_put(key, r["access_token"], r.get("expires_in"))
        return r["access_token"], ext

    def plugin(self, path, method="GET", body=None, platform=None,
               timeout=180):
        platform = platform or self.cfg["platform"]
        token, ext = self.plugin_token(platform)
        # typed commands pass version-less paths ("/clusters"); the plugin's
        # API version differs per platform (AHV = v10, the newer
        # Virtualization Plug-ins = v1), so prepend it here. A caller that
        # already spells "/api/..." (the raw escape hatch) is passed through
        # untouched.
        if not path.startswith("/api/"):
            path = "/api/%s%s" % (self.plugin_api_version(platform), path)
        url = self.base + ext["uri"].rstrip("/") + path
        headers = {"Authorization": "Bearer " + token,
                   "Accept": "application/json"}
        ctype = "application/json;charset=UTF-8"
        data = json.dumps(body).encode() if body is not None else None
        return self._raw(url, method, headers, data, ctype=ctype,
                         timeout=timeout)

    # Confirmed plugin API versions; anything else is probed once and cached.
    _KNOWN_API_VERSION = {"ahv": "v10", "proxmox": "v1", "xen": "v1",
                          "scp": "v1", "hpevme": "v1", "sfr": "v1"}

    def plugin_api_version(self, platform):
        key = platform.lower()
        override = (self.cfg.get("plugin_api_versions") or {}).get(platform)
        if override:
            return override
        if key in self._KNOWN_API_VERSION:
            return self._KNOWN_API_VERSION[key]
        if key not in self._api_ver_cache:
            self._api_ver_cache[key] = self._detect_api_version(platform)
        return self._api_ver_cache[key]

    def _detect_api_version(self, platform):
        """Newer Virtualization Plug-ins answer /api/v1; older plug-ins
        answer only /api/v10."""
        for ver in ("v1", "v10"):
            try:
                self.plugin("/api/%s/clusters" % ver, platform=platform)
                return ver
            except CliError:
                continue
        return "v1"

    def plugin_all(self, path, platform=None, page=500):
        """GET a paged plugin collection, following offset until totalCount.

        List endpoints answer {results, offset, limit, totalCount} and cap a
        page at their own default (100 on the Virtualization Plug-ins), so a
        single GET silently truncates a big inventory - a VM that exists then
        "is not found" by name resolution. Non-paged shapes fall through to
        as_list.
        """
        sep = "&" if "?" in path else "?"
        items, offset = [], 0
        while True:
            r = self.plugin("%s%slimit=%d&offset=%d" % (path, sep, page,
                                                        offset),
                            platform=platform)
            if not isinstance(r, dict) or "results" not in r:
                return as_list(r)
            batch = r["results"]
            items.extend(batch)
            offset += len(batch)
            total = r.get("totalCount")
            if not batch:
                break
            if total is not None and offset >= total:
                break
            if total is None and len(batch) < page:
                break
        return items

    def plugin_first(self, paths, platform=None):
        """Try each version-less path, return the first that answers.

        Some resources live under different paths per platform (e.g. cluster
        networks: /clusters/{id}/networks on AHV, /workers/clusters/{id}/
        networks on the newer Virtualization Plug-ins). Raises the last error
        if all 404.
        """
        last = None
        for p in paths:
            try:
                return self.plugin(p, platform=platform)
            except CliError as e:
                last = e
        raise last

    # -- convenience: credentials (public Credentials Manager) ------- #
    def find_or_create_cred(self, username, password, description=None,
                            cred_type="Standard"):
        """Reuse a matching Credentials Manager record or create one.

        cred_type "Standard" (AHV/Prism) or "Linux" (SSH, for Proxmox &
        other Linux-authenticated hosts).

        A record is reused only on an exact username + type + description
        match: the same username on two hosts usually means two different
        passwords, so a bare username match silently pairs a server with a
        stale secret.
        """
        description = description or ("vbrcli: " + username)
        existing = self.pub("/api/v1/credentials").get("data", [])
        for c in existing:
            if (c.get("username") == username
                    and c.get("type") == cred_type
                    and c.get("description") == description):
                return c["id"]
        body = {"type": cred_type, "username": username, "password": password,
                "description": description}
        if cred_type == "Linux":
            body["authenticationType"] = "Password"
        return self.pub("/api/v1/credentials", "POST", body)["id"]


# ---------------------------------------------------------------------- #
# output helpers

def cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, dict):
        v = v.get("name") or v.get("displayName") or json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        v = "; ".join(cell(x) for x in v)
    return " ".join(str(v).split())


def out(*cols):
    print("\t".join(cell(c) for c in cols))


def jprint(obj):
    print(json.dumps(obj, indent=1, ensure_ascii=False))


def as_list(r):
    """Plugin collections come as {results:[...]} or a bare list."""
    if isinstance(r, dict) and "results" in r:
        return r["results"]
    if isinstance(r, list):
        return r
    if isinstance(r, dict) and "data" in r:
        return r["data"]
    return [r]


# ---------------------------------------------------------------------- #
# server (Prism Central + cluster) commands

# Servers use one of two trust flows. Most platforms (AHV/Xen/SCP/HPE) present
# just a TLS certificate over a Standard credential; Proxmox additionally pins
# an SSH host key over a Linux/SSH credential. Default management ports differ.
_SSH_TRUST_PLATFORMS = {"proxmox"}
# Platforms whose top-level server is a manager registered via
# /clusterOrchestrators (HPE Morpheus VME and Sangfor aSV; POST /clusters is
# 501 on both). HPE additionally picks a backup snapshot storage per cluster;
# Sangfor takes the bare manager.
_ORCHESTRATOR_PLATFORMS = {"hpevme", "sfr"}
# Sangfor validates on /api/v2 and wraps the probe in a "clusterConnection"
# envelope, unlike every other plugin's flat /clusters/validateConnection.
_WRAPPED_VALIDATE_PLATFORMS = {"sfr"}
_PLUGIN_DEFAULT_PORT = {"ahv": DEFAULT_NUTANIX_PORT, "proxmox": 8006,
                        "sfr": 4430}


def _default_port(platform, given):
    if given:
        return given
    return _PLUGIN_DEFAULT_PORT.get(platform.lower(), 443)


def _server_cred(vbr, args, cred_type):
    if args.creds:
        return args.creds
    if not (args.username and args.password):
        raise CliError("need --creds <id> OR --username/--password", 2)
    # Default description is per-host so records never leak across servers
    # that happen to share a username (root@pve vs root@xcp, ...).
    desc = args.creds_desc or ("vbrcli: %s@%s" % (args.username, args.address))
    cid = vbr.find_or_create_cred(args.username, args.password,
                                  desc, cred_type=cred_type)
    sys.stderr.write("# credentials record: %s\n" % cid)
    return cid


def _resolve_thumbprint(vbr, platform, address, port, cred_id, given):
    if given:
        return given
    probe = {"ipOrDnsName": address, "port": port, "credentialsTag": cred_id}
    if platform.lower() in _WRAPPED_VALIDATE_PLATFORMS:
        path, probe = "/api/v2/clusters/validateConnection", {
            "clusterConnection": probe}
    else:
        path = "/clusters/validateConnection"
    res = vbr.plugin(path, "POST", probe, platform=platform)
    if res.get("errorType") == "Other":
        raise CliError("connection validation failed: "
                       + (res.get("errorMessage") or json.dumps(res)[:300]))
    info = res.get("certificateInfo") or {}
    tb = info.get("thumbprint")
    if not tb:
        raise CliError("validateConnection returned no thumbprint: "
                       + json.dumps(res)[:400])
    sys.stderr.write("# presented certificate: %s (%s) thumbprint %s\n"
                     % (info.get("subject", "?"), info.get("issuer", "?"), tb))
    return tb


def _submit_server(vbr, args, platform, endpoint, body):
    if args.dry_run:
        return jprint(body)
    r = vbr.plugin(endpoint, "POST", body, platform=platform)
    if args.json:
        jprint(r)
    else:
        out("session", r.get("sessionId"))
        sys.stderr.write("# submitted; poll 'vbrcli %s list' for state\n"
                         % ("prismcentral" if "prism" in endpoint
                            else "cluster"))
    return r


def _add_server_ssh(vbr, args, platform):
    """Proxmox-style add: Linux/SSH credential, SSH host key + TLS cert."""
    port = _default_port(platform, args.port)
    cred_id = _server_cred(vbr, args, "Linux")
    ssh_fp = args.ssh_fingerprint
    if not ssh_fp:
        r1 = vbr.plugin("/%s/validateSshConnection" % platform.lower(),
                        "POST",
                        {"credentialsTag": cred_id, "port": port,
                         "ipOrDnsName": args.address,
                         "certificateThumbprint": "",
                         "sshKeyFingerprint": ""}, platform=platform)
        if r1.get("errorType") == "Other":
            raise CliError("SSH validation failed: "
                           + (r1.get("errorMessage") or json.dumps(r1)[:300]))
        ssh_fp = r1.get("certificateBase64")
        sys.stderr.write("# SSH host key fingerprint: %s\n" % ssh_fp)
    thumb = args.thumbprint
    if not thumb:
        r2 = vbr.plugin("/%s/validateConnection" % platform.lower(), "POST",
                        {"credentialsTag": cred_id, "port": port,
                         "ipOrDnsName": args.address,
                         "certificateThumbprint": "",
                         "sshKeyFingerprint": ssh_fp}, platform=platform)
        if r2.get("errorType") == "Other":
            raise CliError("connection validation failed: "
                           + (r2.get("errorMessage") or json.dumps(r2)[:300]))
        info = r2.get("certificateInfo") or {}
        thumb = info.get("thumbprint")
        if not thumb:
            raise CliError("validateConnection returned no thumbprint: "
                           + json.dumps(r2)[:300])
        sys.stderr.write("# certificate %s thumbprint %s\n"
                         % (info.get("subject", "?"), thumb))
    adv = {"sshKeyFingerprint": ssh_fp}
    if args.snapshot_storage:
        adv["defaultBackupSnapshotStorage"] = args.snapshot_storage
    body = {"ip": args.address, "port": port, "credentialsTag": cred_id,
            "certificateThumbprint": thumb, "advancedSettings": adv,
            # Description is a REQUIRED field on the Virtualization Plug-ins'
            # POST /clusters (they 400 without it), optional elsewhere.
            "description": args.description or "Added by vbrcli"}
    return _submit_server(vbr, args, platform, "/clusters", body)


def _add_server(vbr, args, endpoint, addr_key):
    platform = args.platform or vbr.cfg["platform"]
    if platform.lower() in _SSH_TRUST_PLATFORMS:
        return _add_server_ssh(vbr, args, platform)
    if platform.lower() in _ORCHESTRATOR_PLATFORMS:
        return _add_orchestrator(vbr, args, platform)
    port = _default_port(platform, args.port)
    cred_id = _server_cred(vbr, args, "Standard")
    thumb = _resolve_thumbprint(vbr, platform, args.address, port, cred_id,
                                args.thumbprint)
    body = {addr_key: args.address, "port": port,
            "credentialsTag": cred_id, "certificateThumbprint": thumb,
            "description": args.description or "Added by vbrcli"}
    return _submit_server(vbr, args, platform, endpoint, body)


def _add_orchestrator(vbr, args, platform):
    """HPE Morpheus VME / Sangfor aSV add: the manager ('cluster
    orchestrator') is the registered entity, not the cluster. POST /clusters
    answers 501 on both; the flow is validateConnection -> POST
    /clusterOrchestrators (note: `address`, not `ip`). HPE inserts two extra
    steps in between — retrieveClusters, then pick a backup snapshot storage
    per cluster. Sangfor has no snapshot-storage choice: its sub-clusters
    come with the manager, so the bare manager body is the whole request."""
    port = _default_port(platform, args.port)
    cred_id = _server_cred(vbr, args, "Standard")
    thumb = _resolve_thumbprint(vbr, platform, args.address, port, cred_id,
                                args.thumbprint)
    body = {"address": args.address, "port": port, "credentialsTag": cred_id,
            "certificateThumbprint": thumb,
            "description": args.description or "Added by vbrcli"}
    if platform.lower() == "sfr":
        return _submit_server(vbr, args, platform, "/clusterOrchestrators",
                              body)
    probe = {"ipOrDnsName": args.address, "port": port,
             "credentialsTag": cred_id, "certificateThumbprint": thumb}
    clusters = as_list(vbr.plugin("/clusterOrchestrators/retrieveClusters",
                                  "POST", probe, platform=platform))
    if not clusters:
        raise CliError("orchestrator reports no clusters")
    storages_map = {}
    for c in clusters:
        cid = c["id"]
        if args.snapshot_storage:
            storages_map[cid] = args.snapshot_storage
            continue
        st = as_list(vbr.plugin(
            "/clusterOrchestrators/clusters/%s/backupSnapshotStorages" % cid,
            "POST", probe, platform=platform))
        if not st:
            raise CliError("no snapshot storages reported for cluster %s (%s)"
                           % (c.get("name"), cid))
        best = max(st, key=lambda s: s.get("freeSpace") or 0)
        storages_map[cid] = best["id"]
        sys.stderr.write("# cluster %s: snapshot storage -> %s (%s)\n"
                         % (c.get("name"), best.get("name"), best["id"]))
    body["advancedSettings"] = {"backupSnapshotStorages": storages_map}
    return _submit_server(vbr, args, platform, "/clusterOrchestrators", body)


def _orchestrator_ids(vbr, platform):
    try:
        r = as_list(vbr.plugin("/clusterOrchestrators", platform=platform))
    except Exception:
        return {}
    return {(e.get("settings") or e).get("id"): e for e in r}


def cmd_prismcentral(vbr, args):
    if args.action == "list":
        r = vbr.plugin("/prismCentrals", platform=args.platform)
        rows = as_list(r)
        if args.json:
            return jprint(r)
        out("id", "name", "address", "port", "state", "version")
        for e in rows:
            s = e.get("settings", e)
            out(s.get("id"), s.get("name"), s.get("address"), s.get("port"),
                e.get("state"), e.get("version"))
    elif args.action == "add":
        _add_server(vbr, args, "/prismCentrals", "address")
    elif args.action == "remove":
        r = vbr.plugin("/prismCentrals/" + args.id, "DELETE",
                       platform=args.platform)
        jprint(r) if args.json else out("removed", args.id)
    elif args.action == "rescan":
        r = vbr.plugin("/prismCentrals/%s/refreshAsync" % args.id,
                       "POST", platform=args.platform)
        jprint(r) if args.json else out("rescan", r.get("sessionId", "ok"))
    elif args.action == "clusters":
        r = vbr.plugin("/prismCentrals/%s/clusters" % args.id,
                       platform=args.platform)
        _print_clusters(r, args)
    elif args.action == "vms":
        r = vbr.plugin_all("/prismCentrals/%s/vms" % args.id,
                           platform=args.platform)
        _print_vms(r, args)


def _print_clusters(r, args):
    if args.json:
        return jprint(r)
    out("id", "name", "address", "port", "state", "version")
    for c in as_list(r):
        out(c.get("id"), c.get("name"), c.get("address"), c.get("port"),
            c.get("state"), c.get("version"))


def _print_vms(r, args):
    if args.json:
        return jprint(r)
    out("id", "name", "cluster", "sizeGiB")
    for v in as_list(r):
        size = v.get("vmSize") or 0
        out(v.get("id"), v.get("name"), v.get("clusterName"),
            round(size / (1024 ** 3), 1) if size else "")


def _is_orchestrator_platform(vbr, args):
    platform = args.platform or vbr.cfg["platform"]
    return platform.lower() in _ORCHESTRATOR_PLATFORMS


def cmd_cluster(vbr, args):
    if args.action == "list":
        if _is_orchestrator_platform(vbr, args):
            for o in _orchestrator_ids(vbr, args.platform
                                       or vbr.cfg["platform"]).values():
                s = o.get("settings") or o
                sys.stderr.write("# orchestrator %s (%s) state=%s\n"
                                 % (s.get("name"), s.get("id"),
                                    o.get("state")))
        r = vbr.plugin("/clusters", platform=args.platform)
        _print_clusters(r, args)
    elif args.action == "add":
        _add_server(vbr, args, "/clusters", "ip")
    elif args.action == "remove":
        path = "/clusters/"
        if _is_orchestrator_platform(vbr, args) and args.id in \
                _orchestrator_ids(vbr, args.platform or vbr.cfg["platform"]):
            path = "/clusterOrchestrators/"
        r = vbr.plugin(path + args.id, "DELETE", platform=args.platform)
        jprint(r) if args.json else out("removed", args.id)
    elif args.action == "rescan":
        path = "/clusters/%s/refreshAsync"
        if _is_orchestrator_platform(vbr, args) and args.id in \
                _orchestrator_ids(vbr, args.platform or vbr.cfg["platform"]):
            path = "/clusterOrchestrators/%s/refreshAsync"
        r = vbr.plugin(path % args.id, "POST",
                       platform=args.platform)
        jprint(r) if args.json else out("rescan", r.get("sessionId", "ok"))
    elif args.action == "hosts":
        r = vbr.plugin("/clusters/%s/hosts" % args.id,
                       platform=args.platform)
        if args.json:
            return jprint(r)
        out("id", "name")
        for h in as_list(r):
            out(h.get("id"), h.get("name"))
    elif args.action == "networks":
        r = vbr.plugin("/clusters/%s/networks" % args.id,
                       platform=args.platform)
        if args.json:
            return jprint(r)
        out("id", "name")
        for n in as_list(r):
            out(n.get("id"), n.get("name"))
    elif args.action == "storagecontainers":
        r = vbr.plugin("/clusters/%s/storageContainers" % args.id,
                       platform=args.platform)
        if args.json:
            return jprint(r)
        out("id", "name")
        for s in as_list(r):
            out(s.get("id"), s.get("name"))
    elif args.action == "vms":
        r = vbr.plugin_all("/clusters/%s/vms" % args.id,
                           platform=args.platform)
        _print_vms(r, args)


# ---------------------------------------------------------------------- #
# worker commands

def cmd_worker(vbr, args):
    if args.action == "list":
        r = vbr.plugin("/workersWithLocal", platform=args.platform)
        if args.json:
            return jprint(r)
        out("id", "name", "cluster", "enabled", "status", "updateStatus")
        for w in as_list(r):
            c = w.get("configuration", w)
            out(w.get("id") or c.get("id"), c.get("name"),
                c.get("clusterName") or c.get("clusterId"),
                w.get("enabled"), w.get("status"), w.get("updateStatus"))
    elif args.action == "get":
        r = vbr.plugin("/workers/%s/configuration" % args.id,
                       platform=args.platform)
        jprint(r)
    elif args.action == "defaults":
        cluster = args.cluster or args.id
        if not cluster:
            raise CliError("worker defaults needs a cluster id", 2)
        r = vbr.plugin("/workers/defaultConfiguration?clusterId="
                       + cluster, platform=args.platform)
        jprint(r)
    elif args.action == "test":
        r = vbr.plugin("/workers/%s/test" % args.id, "POST",
                       platform=args.platform)
        jprint(r) if args.json else out("test", r.get("sessionId", "ok"))
    elif args.action == "enable":
        r = vbr.plugin("/workers/%s/enable" % args.id, "POST",
                       platform=args.platform)
        jprint(r) if args.json else out("enabled", args.id)
    elif args.action == "disable":
        r = vbr.plugin("/workers/%s/disable" % args.id, "POST",
                       platform=args.platform)
        jprint(r) if args.json else out("disabled", args.id)
    elif args.action == "remove":
        r = vbr.plugin("/workers/" + args.id, "DELETE",
                       platform=args.platform)
        jprint(r) if args.json else out("removed", args.id)
    elif args.action == "add":
        body = _worker_spec(vbr, args)
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/workers", "POST", body,
                       platform=args.platform)
        if args.json:
            jprint(r)
        else:
            wid = r.get("id") or r.get("sessionId")
            out("worker", wid)
            sys.stderr.write("# worker record created (status Configured); "
                             "'vbrcli worker test %s' deploys+checks the VM\n"
                             % wid)


def _worker_spec(vbr, args):
    """Worker body: --spec verbatim, or defaults for --cluster + overrides."""
    if args.spec:
        return _read_spec(args.spec)
    if not (args.cluster and args.name):
        raise CliError(
            "worker add needs --spec @file.json OR --cluster <id> --name <n> "
            "[--container <id>] [--network <id|name>] [--tasks N] [--cpu N] "
            "[--memory N] [--description <d>]", 2)
    body = vbr.plugin("/workers/defaultConfiguration?clusterId="
                      + args.cluster, platform=args.platform)
    body["name"] = args.name
    if args.description:
        body["description"] = args.description
    if args.container:
        body["storageContainerId"] = args.container
    if args.network:
        nets = _cluster_networks(vbr, args.platform, args.cluster)
        match = next((n for n in nets
                      if args.network in (n.get("id"), n.get("name"))), None)
        if not match:
            raise CliError("network '%s' not on the cluster; see "
                           "'vbrcli cluster networks %s'"
                           % (args.network, args.cluster), 2)
        # Some plugins (Sangfor) hand back defaultConfiguration with the key
        # already present and the list EMPTY, so setdefault alone yields [] --
        # seed the first NIC explicitly instead of indexing into it blindly.
        nics = body.setdefault("networkSettings", {}).setdefault("networks", [])
        if not nics:
            nics.append({})
        nic = nics[0]
        nic.update(index=0, networkId=match["id"],
                   networkName=match.get("name"))
        nic.setdefault("obtainIpAutomatically", True)
    if args.tasks:
        body["maxConcurrentTasks"] = args.tasks
    if args.cpu:
        body["cpuCount"] = args.cpu
    if args.memory:
        body["memoryGb"] = args.memory
    return body


def _read_spec(spec):
    if spec.startswith("@"):
        with open(spec[1:], encoding="utf-8") as f:
            return json.load(f)
    return json.loads(spec)


# ---------------------------------------------------------------------- #
# job commands (plugin API)

def _resolve_vms(vbr, args, spec):
    """Comma-separated VM ids/names -> JobSourceObject list."""
    wanted = [w.strip() for w in spec.split(",") if w.strip()]
    clusters = as_list(vbr.plugin("/clusters", platform=args.platform))
    if args.cluster:
        clusters = [c for c in clusters if c.get("id") == args.cluster]
        if not clusters:
            raise CliError("cluster %s not found" % args.cluster, 2)
    found = {}
    for c in clusters:
        if len(found) == len(wanted):
            break
        vms = vbr.plugin_all("/clusters/%s/vms" % c["id"],
                             platform=args.platform)
        for v in vms:
            for w in wanted:
                if w not in found and w in (v.get("id"), v.get("name")):
                    found[w] = {"id": v["id"], "clusterId": c["id"],
                                "type": "VirtualMachine"}
    missing = [w for w in wanted if w not in found]
    if missing:
        raise CliError("VM(s) not found: %s (searched %d cluster(s); "
                       "names are case-sensitive)"
                       % (", ".join(missing), len(clusters)), 2)
    return [found[w] for w in wanted]


def _resolve_categories(vbr, args, spec):
    """Comma-separated Prism Central category ids (name:value) ->
    JobSourceObject list. Category sources hang off a Prism Central, not a
    cluster; the id IS the name:value pair."""
    wanted = [w.strip() for w in spec.split(",") if w.strip()]
    for w in wanted:
        if ":" not in w:
            raise CliError("category must be name:value (got %r)" % w, 2)
    pc_id = args.pc
    if not pc_id:
        pcs = as_list(vbr.plugin("/prismCentrals", platform=args.platform))
        if len(pcs) != 1:
            raise CliError("--categories needs --pc <id> (%d Prism Centrals "
                           "registered; see 'vbrcli pc list')" % len(pcs), 2)
        pc_id = pcs[0].get("settings", pcs[0]).get("id")
    known, offset = set(), 0
    while True:
        page = vbr.plugin("/prismCentrals/%s/categories?offset=%d"
                          % (pc_id, offset), platform=args.platform)
        rows = as_list(page)
        if not rows:
            break
        known.update(r.get("id") for r in rows)
        offset += len(rows)
        if offset >= (page.get("totalCount") or 0):
            break
    missing = [w for w in wanted if w not in known]
    if missing:
        raise CliError("category(ies) not found on Prism Central %s: %s"
                       % (pc_id, ", ".join(missing)), 2)
    # The published OpenAPI spec names prismCentralId, but the server's
    # validator expects masterServerId (400 otherwise); send what it expects.
    return [{"id": w, "masterServerId": pc_id, "type": "Category"}
            for w in wanted]


_BUS_NAMES = {"scsi": "Scsi", "ide": "Ide", "sata": "Sata", "pci": "Pci"}


def _apply_disk_rules(vbr, body, args):
    """--disks <vm>=<bus>.<index>[,...] (repeatable, one per VM) ->
    diskFilterSettings entry with mode Selected: ONLY the listed disks of
    that VM are backed up."""
    if not args.disks:
        return
    filters = []
    for rule in args.disks:
        vm_spec, _, disks = rule.partition("=")
        if not disks.strip():
            raise CliError("--disks takes <vm>=<bus>.<index>[,...] "
                           "(e.g. VM2=scsi.2)", 2)
        obj = _resolve_vms(vbr, args, vm_spec)[0]
        entries = []
        for d in disks.split(","):
            bus, _, idx = d.strip().partition(".")
            bus_name = _BUS_NAMES.get(bus.strip().lower())
            if not bus_name or not idx.strip().isdigit():
                raise CliError("bad disk %r; format <bus>.<index>, bus = "
                               "scsi|ide|sata|pci" % d.strip(), 2)
            entries.append({"busType": bus_name, "index": int(idx)})
        filters.append({"object": obj,
                        "filter": {"mode": "Selected", "disks": entries,
                                   "volumeGroups": []}})
    body.setdefault("diskFilterSettings", {})["filters"] = filters


def _expand_days(spec):
    """Day spec -> full day names: everyday | weekdays | weekend |
    mon,fri | mon-fri (ranges wrap: fri-mon)."""
    s = spec.strip().lower()
    order = list(_DAY_NAMES.values())
    if s in ("everyday", "every", "all"):
        return order
    if s in ("weekdays", "workdays"):
        return order[:5]
    if s == "weekend":
        return order[5:]
    days = []
    for tok in s.split(","):
        tok = tok.strip()
        if "-" in tok:
            a, _, b = tok.partition("-")
            ia = order.index(_expand_names(a, _DAY_NAMES, "day")[0])
            ib = order.index(_expand_names(b, _DAY_NAMES, "day")[0])
            idxs = (range(ia, ib + 1) if ia <= ib
                    else list(range(ia, 7)) + list(range(0, ib + 1)))
            days += [order[i] for i in idxs]
        else:
            days += _expand_names(tok, _DAY_NAMES, "day")
    return days


def _apply_backup_window(body, args):
    """--backup-window '<days>@<h1>-<h2>[;...]' | off -> the permitted-hours
    grid on scheduleSettings.periodic (the only schedule flavor the plugin
    API windows). Hour granularity, h2 exclusive, ranges wrap (22-06)."""
    if not args.backup_window:
        return
    sched = body.setdefault("scheduleSettings", {})
    spec = args.backup_window.strip().lower()
    if spec == "off":
        sched.setdefault("periodic", {})["backupWindow"] = None
        return
    grid = {d: [False] * 24 for d in _DAY_NAMES.values()}
    for seg in re.split(r"[; ]+", spec):
        if not seg:
            continue
        days_part, at, hours_part = seg.partition("@")
        if not at:  # bare "22-06" = every day
            days_part, hours_part = "everyday", seg
        m = re.match(r"^(\d{1,2})-(\d{1,2})$", hours_part.strip())
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 24:
            raise CliError("--backup-window hours must be <h1>-<h2> with "
                           "h1 0-23, h2 1-24 (got %r); minutes are not "
                           "supported" % hours_part, 2)
        h1, h2 = int(m.group(1)), int(m.group(2))
        hours = (range(h1, h2) if h1 < h2
                 else list(range(h1, 24)) + list(range(0, h2)))
        for day in _expand_days(days_part):
            for h in hours:
                grid[day][h] = True
    per = sched.setdefault("periodic", {})
    per["backupWindow"] = {"days": [{"day": d, "hours": grid[d]}
                                    for d in _DAY_NAMES.values()]}
    if sched.get("type") != "Periodic":
        raise CliError("--backup-window applies to the periodic schedule "
                       "only; add --schedule periodic --every <N>h", 2)


def _apply_periodic_full(body, key, spec, flag):
    """activeFullSettings / syntheticFullSettings from
    on | off | <days>[@HH:MM] (e.g. thu@17:32, mon,fri@06:00)."""
    val = (spec or "").strip().lower()
    st = body.setdefault(key, {})
    if val == "off":
        st["enabled"] = False
        return
    st["enabled"] = True
    st.setdefault("type", "Weekly")
    if val in ("", "on"):
        return
    days, _, at = val.partition("@")
    weekly = st.setdefault("weekly", {})
    if days:
        weekly["configuredDays"] = "SelectedDays"
        weekly["selectedDays"] = _expand_names(days, _DAY_NAMES, "day")
    if at:
        if not re.match(r"^\d{1,2}:\d{2}$", at):
            raise CliError("%s time must be HH:MM (got %r)" % (flag, at), 2)
        weekly["startTime"] = at


def _job_spec(vbr, args):
    """Compose the job body.

    Starts from the server's own `jobs/defaultSettings` -- the exact template
    the web UI edits -- and overlays the requested fields, so a CLI-created
    job is structurally identical to a UI-created one. `--spec` bypasses this
    and sends your JSON verbatim.
    """
    if args.spec:
        return _read_spec(args.spec)
    if not (args.name and (args.vms or args.categories)):
        raise CliError(
            "job create needs --spec @file.json OR --name <n> plus --vms "
            "<id|name,...> and/or --categories <name:value,...> "
            "[--cluster <id>] [--repo <id>] [--description <d>]",
            2)
    body = vbr.plugin("/jobs/defaultSettings?jobMode=Backup",
                      platform=args.platform)
    body["name"] = args.name
    if args.description:
        body["description"] = args.description
    if args.repo:
        body["repositoryId"] = args.repo
    body.setdefault("includes", {})["objects"] = (
        _resolve_vms(vbr, args, args.vms) if args.vms else [])
    _apply_job_overrides(vbr, body, args)
    return body


# Live-probed enums (PVE/Xen/HpeVme 13.x + AHV v10), all case-insensitive:
#   scheduleSettings.type: Weekly | Monthly | Periodic (UI "Daily" = Weekly)
#   weekly.configuredDays: EveryDay | WeekDays | SelectedDays
#   monthly.configuredWeekOrDay: First/Second/Third/Fourth/LastWeek|DayOfMonth
#   periodic.mode: EveryHour | EveryMinute (+ backupWindow.days[7].hours[24])
_DAY_NAMES = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday",
              "thu": "Thursday", "fri": "Friday", "sat": "Saturday",
              "sun": "Sunday"}
_MONTH_NAMES = {"jan": "January", "feb": "February", "mar": "March",
                "apr": "April", "may": "May", "jun": "June", "jul": "July",
                "aug": "August", "sep": "September", "oct": "October",
                "nov": "November", "dec": "December"}


def _expand_names(csv, table, what):
    names = []
    for tok in csv.split(","):
        t = tok.strip().lower()
        full = table.get(t[:3])
        if not full:
            raise CliError("unknown %s: %r" % (what, tok), 2)
        names.append(full)
    return names


def _apply_schedule(body, args):
    sched = body.setdefault("scheduleSettings", {})
    mode = (args.schedule or "").lower()
    if mode == "off":
        sched["enabled"] = False
        return
    if args.schedule:
        sched["enabled"] = True
    if mode in ("daily", "weekly"):
        sched["type"] = "Weekly"
    elif mode == "monthly":
        sched["type"] = "Monthly"
    elif mode == "periodic":
        sched["type"] = "Periodic"
    elif mode not in ("", "on"):
        raise CliError("--schedule takes on|off|daily|monthly|periodic", 2)
    if args.days:
        sched["type"] = "Weekly"
        sched["enabled"] = True
        weekly = sched.setdefault("weekly", {})
        d = args.days.strip().lower()
        if d in ("everyday", "every", "all"):
            weekly["configuredDays"] = "EveryDay"
        elif d in ("weekdays", "workdays"):
            weekly["configuredDays"] = "WeekDays"
        else:
            weekly["configuredDays"] = "SelectedDays"
            weekly["selectedDays"] = _expand_names(args.days, _DAY_NAMES,
                                                   "day")
    if args.at:
        sched["enabled"] = True
        if sched.get("type") == "Monthly":
            sched.setdefault("monthly", {})["startTime"] = args.at
        else:
            sched.setdefault("type", "Weekly")
            if sched["type"] == "Weekly":
                weekly = sched.setdefault("weekly", {})
                weekly["startTime"] = args.at
                weekly.setdefault("configuredDays", "EveryDay")
    if args.every:
        sched["type"] = "Periodic"
        sched["enabled"] = True
        m = re.match(r"^(\d+)\s*([hm])$", args.every.strip().lower())
        if not m:
            raise CliError("--every takes <N>h or <N>m (e.g. 4h, 30m)", 2)
        per = sched.setdefault("periodic", {})
        per["interval"] = int(m.group(1))
        per["mode"] = "EveryHour" if m.group(2) == "h" else "EveryMinute"
    if args.months:
        sched["type"] = "Monthly"
        sched["enabled"] = True
        sched.setdefault("monthly", {})["months"] = _expand_names(
            args.months, _MONTH_NAMES, "month")
    if args.month_day:
        sched["type"] = "Monthly"
        sched["enabled"] = True
        monthly = sched.setdefault("monthly", {})
        md = args.month_day.strip()
        if md.isdigit():
            monthly["configuredWeekOrDay"] = "DayOfMonth"
            monthly["dayOfMonth"] = int(md)
        else:
            week, _, day = md.partition(":")
            monthly["configuredWeekOrDay"] = week.capitalize() + "Week"
            if day:
                monthly["dayOfWeek"] = _expand_names(day, _DAY_NAMES,
                                                     "day")[0]


def _vss_backup_type(vbr, args):
    """Same setting, two spellings: AHV v10 says Copy, the Virtualization
    Plug-ins (Proxmox/Xen/SCP/HpeVme) say CopyOnly. Accept either and
    translate."""
    val = args.vss.strip().lower()
    names = {"none": "None", "full": "Full", "copy": "Copy",
             "copyonly": "Copy"}
    if val not in names:
        raise CliError("--vss takes none|full|copy", 2)
    canonical = names[val]
    if canonical == "Copy":
        platform = (args.platform or vbr.cfg["platform"]).lower()
        return "Copy" if platform == "ahv" else "CopyOnly"
    return canonical


def _apply_job_overrides(vbr, body, args):
    """Overlay the common backup settings onto the defaults template."""
    if args.compression:
        body["compression"] = args.compression
    if args.block_size:
        body["backupBlockSize"] = args.block_size
    if args.keep is not None:
        ret = body.setdefault("retentionSettings", {})
        ret["restorePointsToKeep"] = args.keep
        ret["daysToKeep"] = args.keep
    if args.categories:
        inc = body.setdefault("includes", {}).setdefault("objects", [])
        inc.extend(_resolve_categories(vbr, args, args.categories))
    if args.exclude_vms:
        body.setdefault("excludes", {})["objects"] = _resolve_vms(
            vbr, args, args.exclude_vms)
    _apply_disk_rules(vbr, body, args)
    _apply_schedule(body, args)
    _apply_backup_window(body, args)
    if args.active_full:
        _apply_periodic_full(body, "activeFullSettings", args.active_full,
                             "--active-full")
    if args.synthetic_full:
        _apply_periodic_full(body, "syntheticFullSettings",
                             args.synthetic_full, "--synthetic-full")
    adv = body.setdefault("advancedSettings", {})
    if args.quiesce:
        adv.setdefault("guestToolsSettings", {})["guestQuiescenceEnabled"] = \
            args.quiesce == "on"
    if args.ngt:
        adv.setdefault("nutanixGuestToolsSettings", {})["enabled"] = \
            args.ngt == "on"
    if args.vss:
        ngt = adv.setdefault("nutanixGuestToolsSettings", {})
        ngt["vssBackupType"] = _vss_backup_type(vbr, args)
        if not args.ngt:
            ngt["enabled"] = True
    _apply_guest_processing(vbr, body, args)


def _cred_type(vbr, cred_id):
    """Map a Credentials Manager record to a GuestProcessingCredentialsType."""
    for c in vbr.pub("/api/v1/credentials").get("data", []):
        if c.get("id") == cred_id:
            return "Linux" if c.get("type") == "Linux" else "Standard"
    raise CliError("credentials record %s not found (see 'vbrcli creds list')"
                   % cred_id, 2)


def _db_log_blocks(args):
    """Per-DB log shipping settings from flags (UI-default shapes).
    A custom DB account (--pg-creds/--oracle-creds) sets
    useGuestCredentials=false + credentialsId; MS SQL has no separate
    account -- it rides the guest OS credentials."""
    blocks = {}
    if args.pg_log_backup or args.pg_creds:
        pg = {"enabled": True, "useGuestCredentials": not args.pg_creds,
              "userType": "DbUserWithPassword",
              "backupLogsEnabled": bool(args.pg_log_backup),
              "backupMinutesCount": args.pg_log_every or 15,
              "retentionLogsType": "UntilBackupDeleted", "keepDaysCount": 15,
              "logsTemporaryLocation": "/tmp",
              "shippingLogSettings": {"autoSelection": True,
                                      "shippingServerIds": []}}
        if args.pg_creds:
            pg["credentialsId"] = args.pg_creds
        blocks["postgreSqlSettings"] = pg
    if args.oracle_log_backup or args.oracle_creds:
        ora = {"enabled": True,
               "useGuestCredentials": not args.oracle_creds,
               "archivedLogsType": "DoNotDelete",
               "deleteLogsHoursCount": 24, "deleteLogsGBsCount": 20,
               "backupLogsEnabled": bool(args.oracle_log_backup),
               "backupMinutesCount": args.oracle_log_every or 15,
               "retentionLogsType": "UntilBackupDeleted", "keepDaysCount": 15,
               "shippingLogSettings": {"autoSelection": True,
                                       "shippingServerIds": []}}
        if args.oracle_creds:
            ora["credentialsId"] = args.oracle_creds
        blocks["oracleSettings"] = ora
    if args.sql_log_backup:
        blocks["msSqlSettings"] = {
            "enabled": True, "shippingLogsMode": "Periodically",
            "backupMinutesCount": args.sql_log_every or 15,
            "retentionLogsType": "UntilBackupDeleted", "keepDaysCount": 15,
            "shippingLogSettings": {"autoSelection": True,
                                    "shippingServerIds": []}}
    return blocks


def _apply_guest_processing(vbr, body, args):
    """Build guestProcessingSettings for every VM in the job from flags:
    --app-aware, --guest-creds, DB log shipping flags, --index."""
    db_blocks = _db_log_blocks(args)
    want = (args.app_aware or args.guest_creds or args.index or db_blocks)
    if not want:
        return
    objects = body.get("includes", {}).get("objects", [])
    if not objects:
        raise CliError("app-aware needs at least one VM (--vms)", 2)
    if not args.guest_creds:
        raise CliError("app-aware needs --guest-creds <id> (guest OS "
                       "credentials record; see 'vbrcli creds list')", 2)
    ctype = _cred_type(vbr, args.guest_creds)
    is_linux = ctype == "Linux"

    aa = []
    for o in objects:
        el = {"object": dict(o), "isIncluded": True,
              "applicationAwareProcessingMode": "RequireSuccess",
              "usePersistentGuestAgent": False,
              "vssMode": "ProcessTransactionLogs"}
        for key, block in db_blocks.items():
            el[key] = json.loads(json.dumps(block))
        aa.append(el)

    idx = []
    for o in objects:
        idx.append({
            "object": dict(o), "isIncluded": True,
            "linuxIndexingSettings": {
                "enabled": args.index in ("linux", "all"),
                "type": "IndexAll" if args.index in ("linux", "all")
                else "Disabled", "indexingList": []},
            "windowsIndexingSettings": {
                "enabled": args.index in ("windows", "all"),
                "type": "IndexAll" if args.index in ("windows", "all")
                else "Disabled", "indexingList": []}})

    creds = [{"object": dict(o), "isIncluded": True,
              "credentials": {
                  "linuxCredentialsId": args.guest_creds if is_linux else None,
                  "windowsCredentialsId": None if is_linux
                  else args.guest_creds}}
             for o in objects]

    body["guestProcessingSettings"] = {
        "enabled": True,
        "applicationAwareProcessing": {"enabled": True, "settings": aa},
        "indexingSettings": {"enabled": bool(args.index), "settings": idx},
        "credentials": {"credentialsId": args.guest_creds,
                        "credentialsType": ctype, "credentials": creds},
        "guestInteractionProxySettings": {"enabled": False,
                                          "autoSelectEnabled": True,
                                          "preferredProxyIds": []}}


def _print_jobs(r, args):
    if args.json:
        return jprint(r)
    out("id", "name", "status", "enabled", "objects", "nextRun", "target")
    for j in as_list(r):
        primary = next((t for t in j.get("targets") or []
                        if t.get("isPrimary")), {})
        out(j.get("id"), j.get("name"), j.get("status"), j.get("enabled"),
            j.get("objects"), j.get("nextRunInfo"),
            primary.get("displayName"))


def cmd_job(vbr, args):
    if args.action == "list":
        r = vbr.plugin("/jobs", platform=args.platform)
        _print_jobs(r, args)
    elif args.action == "get":
        jprint(vbr.plugin("/jobs/" + args.id,
                          platform=args.platform))
    elif args.action == "settings":
        jprint(vbr.plugin("/jobs/%s/settings" % args.id,
                          platform=args.platform))
    elif args.action == "defaults":
        jprint(vbr.plugin("/jobs/defaultSettings?jobMode=Backup",
                          platform=args.platform))
    elif args.action in ("create", "validate"):
        body = _job_spec(vbr, args)
        if args.action == "create" and args.dry_run:
            return jprint(body)
        v = vbr.plugin("/jobs/validate", "POST", body,
                       platform=args.platform)
        if args.action == "validate" or _validation_failed(v):
            return jprint(v)
        r = vbr.plugin("/jobs", "POST", body,
                       platform=args.platform)
        if args.json:
            jprint(r)
        else:
            out("job", r.get("id") or r.get("sessionId"))
    elif args.action == "edit":
        if not args.id:
            raise CliError("job edit needs a job id", 2)
        if args.spec:
            body = _read_spec(args.spec)
        else:
            body = vbr.plugin("/jobs/%s/settings" % args.id,
                              platform=args.platform)
            if args.name:
                body["name"] = args.name
            if args.description:
                body["description"] = args.description
            if args.repo:
                body["repositoryId"] = args.repo
            if args.vms:
                body.setdefault("includes", {})["objects"] = _resolve_vms(
                    vbr, args, args.vms)
            _apply_job_overrides(vbr, body, args)
            # GET /settings returns computed gfs beginTimeUtc fields that PUT
            # rejects ("must be empty"); drop them before sending back.
            for sub in ("weekly", "monthly", "yearly"):
                g = (body.get("gfsSettings") or {}).get(sub)
                if isinstance(g, dict):
                    g.pop("beginTimeUtc", None)
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/jobs/%s/settings" % args.id, "PUT", body,
                       platform=args.platform)
        jprint(r) if args.json else out("edited", args.id)
    elif args.action == "remove":
        r = vbr.plugin("/jobs/" + args.id, "DELETE",
                       platform=args.platform)
        jprint(r) if args.json else out("removed", args.id)
    else:  # start / stop / retry / enable / disable
        r = vbr.plugin("/jobs/%s/%s" % (args.id, args.action),
                       "POST", platform=args.platform)
        if args.json:
            jprint(r)
        else:
            out(args.action, r.get("sessionId") or args.id)


def _validation_failed(v):
    """True if POST /jobs/validate reports a problem worth aborting on."""
    if not isinstance(v, dict):
        return False
    if v.get("isValid") is False or v.get("valid") is False:
        return True
    for key in ("errors", "validationErrors", "messages", "results"):
        val = v.get(key)
        if isinstance(val, list) and val:
            return True
    return False


# ---------------------------------------------------------------------- #
# restore commands (plugin API); restore point ids are shared with the
# public REST, so feed ids straight from 'vbrcli rp list'

def _rp_disks(vbr, args):
    return as_list(vbr.plugin("/restorePoints/%s/disks" % args.id,
                              platform=args.platform))


def _rp_meta(vbr, args):
    return vbr.plugin("/restorePoints/%s/metadata" % args.id,
                      platform=args.platform)


def _target_cluster(args, meta):
    """Restore target: --cluster if given, else the restore point's own host.
    On Proxmox/HPE the host is a node (subClusterId); elsewhere it's the
    cluster itself."""
    return (args.cluster or meta.get("subClusterId")
            or meta.get("clusterId"))


def _disk_settings(disks, base=None, container=None):
    """diskSettings array: keep each disk's bus type; renumber slots from
    `base` if given; send `container` for every disk or keep the original."""
    return [{"diskId": d["id"], "busType": d.get("busType"),
             "index": (base + n if base is not None else d.get("index")),
             "storageContainerId": container or d.get("storageContainerId")}
            for n, d in enumerate(disks)]


def _adapters_from_rp(vbr, platform, rp_id):
    """Restore-point NICs wrapped as networkAdapters entries (no remap)."""
    src = as_list(vbr.plugin("/restorePoints/%s/networkAdapters" % rp_id,
                             platform=platform))
    return [{"originalMacAddress": a.get("macAddress", ""), "value": a}
            for a in src] or None


def _cluster_networks(vbr, platform, cluster_id):
    return as_list(vbr.plugin_first(
        ["/clusters/%s/networks" % cluster_id,
         "/workers/clusters/%s/networks" % cluster_id], platform=platform))


def _cluster_storages(vbr, platform, cluster_id):
    return as_list(vbr.plugin_first(
        ["/clusters/%s/storageContainers" % cluster_id,
         "/workers/clusters/%s/storages" % cluster_id], platform=platform))


def _resolve_container(vbr, platform, cluster_id, wanted, rp_disks):
    """Target storage container: --container by id or name, else the source
    disk's own container. Names are resolved against the target cluster."""
    if wanted and cluster_id:
        conts = _cluster_storages(vbr, platform, cluster_id)
        match = next((c for c in conts
                      if wanted in (c.get("id"), c.get("name"))), None)
        if match:
            return match["id"]
        if not any(c.get("id") == wanted for c in conts):
            raise CliError("storage container '%s' not on the cluster; see "
                           "'vbrcli cluster storagecontainers %s'"
                           % (wanted, cluster_id), 2)
    if wanted:
        return wanted
    return rp_disks[0].get("storageContainerId") if rp_disks else None


def _network_remap(vbr, platform, rp_id, cluster_id, spec, vlan_spec):
    """Positional NIC remap: --network bridge1,bridge2 maps the VM's 1st,2nd
    adapter; --vlan 40 (or 40,0) tags them (0 = no VLAN). Target networks are
    resolved by id or name against the cluster."""
    names = [n.strip() for n in spec.split(",") if n.strip()]
    vlans = [v.strip() for v in (vlan_spec or "").split(",") if v.strip()]
    for v in vlans:
        if not (v.isdigit() and 0 <= int(v) <= 4094):
            raise CliError("--vlan values must be integers 0-4094 (0 = no "
                           "VLAN tag); got '%s'" % v, 2)
    nets = _cluster_networks(vbr, platform, cluster_id)
    src = as_list(vbr.plugin("/restorePoints/%s/networkAdapters" % rp_id,
                             platform=platform))
    adapters = []
    for i, token in enumerate(names):
        net = next((n for n in nets
                    if token in (n.get("id"), n.get("name"))), None)
        if not net:
            raise CliError("network '%s' not on the cluster; see "
                           "'vbrcli cluster networks %s'"
                           % (token, cluster_id), 2)
        if vlans:
            vlan = int(vlans[i]) if i < len(vlans) else int(vlans[0])
        else:
            vlan = 0
        value = dict(src[i]) if i < len(src) else {}
        value.update(networkId=net["id"], networkName=net.get("name"),
                     vlan=vlan)
        value.setdefault("ipAddresses", [])
        adapters.append({"originalMacAddress": value.get("macAddress", ""),
                         "value": value})
    if len(names) > len(src) and src:
        sys.stderr.write("# note: %d networks given but the VM has %d "
                         "adapter(s); extras are ignored by the plug-in\n"
                         % (len(names), len(src)))
    return adapters


def cmd_restore(vbr, args):
    platform = args.platform
    if args.what == "vm":
        body = {"restorePointId": args.id,
                "restoreToOriginal": bool(args.original),
                "powerOnVmAfterRestore": bool(args.power_on)}
        if args.disk_format:
            body["diskFormat"] = args.disk_format
        if args.original:
            body["forceDeleteExistingVm"] = True
        else:
            if not args.target_name:
                raise CliError("restore vm needs --target-name <newVmName> "
                               "(or --original to overwrite the source VM)", 2)
            meta = _rp_meta(vbr, args)
            cluster = _target_cluster(args, meta)
            body["targetVmName"] = args.target_name
            if cluster:
                body["targetVmClusterId"] = cluster
            container = _resolve_container(vbr, platform, cluster,
                                           args.container, _rp_disks(vbr, args))
            if not container:
                raise CliError("restore to a new location needs --storage "
                               "<container id or name>", 2)
            body["storageContainerId"] = container
            if args.network:
                if not cluster:
                    raise CliError("--network needs a target cluster/host to "
                                   "resolve networks (--cluster)", 2)
                body["networkAdapters"] = _network_remap(
                    vbr, platform, args.id, cluster, args.network, args.vlan)
                body["disconnectNetworksAfterRestore"] = False
        if args.reason:
            body["reason"] = args.reason
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/restorePoints/restore", "POST", body,
                       platform=platform)
        _print_async(r, args)
    elif args.what == "disk":
        if not args.target_vm:
            raise CliError("restore disk needs --target-vm <vmId>", 2)
        disks = _rp_disks(vbr, args)
        if args.disk:
            want = [w.strip() for w in args.disk.split(",")]
            disks = [d for d in disks
                     if d.get("id") in want or d.get("diskLabel") in want]
            if not disks:
                raise CliError("no matching disks; see "
                               "'vbrcli rp disks %s'" % args.id, 2)
        container = _resolve_container(vbr, platform, args.cluster,
                                       args.container, None)
        body = {"restorePointId": args.id, "targetVmId": args.target_vm,
                "powerOnVmAfterRestore": bool(args.power_on),
                "diskSettings": _disk_settings(disks, args.index, container)}
        if args.cluster:
            body["targetVmClusterId"] = args.cluster
        if args.reason:
            body["reason"] = args.reason
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/restorePoints/diskRestore", "POST", body,
                       platform=platform)
        _print_async(r, args)


def _print_async(r, args):
    if args.json:
        return jprint(r)
    sid = r.get("sessionId") or r.get("id")
    out("session", sid)
    sys.stderr.write("# async; poll 'vbrcli session get %s'\n" % sid)


# ---------------------------------------------------------------------- #
# instant recovery (plugin API)

def cmd_ir(vbr, args):
    platform = args.platform
    if args.action == "start":
        if not args.target_name:
            raise CliError("ir start needs --target-name <newVmName>", 2)
        meta = _rp_meta(vbr, args)
        disks = _rp_disks(vbr, args)
        cluster = _target_cluster(args, meta)
        container = _resolve_container(vbr, platform, cluster,
                                       args.container, disks)
        if args.network:
            adapters = _network_remap(vbr, platform, args.id, cluster,
                                      args.network, args.vlan)
        else:
            adapters = _adapters_from_rp(vbr, platform, args.id)
        body = {"restorePointId": args.id,
                "restoreToOriginal": False,
                "targetVmId": meta.get("id"),
                "sourceVmName": meta.get("name"),
                "targetVmName": args.target_name,
                "targetVmClusterId": cluster,
                "powerOnVmAfterRestore": bool(args.power_on),
                "disconnectNetworksAfterRestore": False,
                "networkAdapters": adapters,
                "diskSettings": _disk_settings(disks, container=container)}
        if args.disk_format:
            body["diskFormat"] = args.disk_format
        if args.reason:
            body["reason"] = args.reason
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/instantRecovery", "POST", body, platform=platform)
        _print_async(r, args)
    elif args.action == "disks":
        # instant disk recovery: publish the restore point's disks and
        # attach them to an existing VM
        if not args.target_vm:
            raise CliError("ir disks needs --target-vm <vmId>", 2)
        meta = _rp_meta(vbr, args)
        disks = _rp_disks(vbr, args)
        container = _resolve_container(vbr, platform,
                                       _target_cluster(args, meta),
                                       args.container, None)
        body = {"restorePointId": args.id,
                "targetVmId": args.target_vm,
                "targetVmName": args.target_name,
                "sourceVmName": meta.get("name"),
                "targetVmClusterId": _target_cluster(args, meta),
                "locationPreference": None,
                "diskSettings": _disk_settings(disks, args.index, container)}
        if args.reason:
            body["reason"] = args.reason
        if args.dry_run:
            return jprint(body)
        r = vbr.plugin("/instantDiskRecovery", "POST", body,
                       platform=platform)
        _print_async(r, args)
    elif args.action == "get":
        jprint(vbr.plugin("/instantRecovery/sessions/" + args.id,
                          platform=args.platform))
    elif args.action == "stop":
        r = vbr.plugin("/instantRecovery/sessions/%s/stop" % args.id,
                       "POST", platform=args.platform)
        jprint(r) if args.json else out("stopped", args.id)
    elif args.action == "migrate":
        r = vbr.plugin("/instantRecovery/sessions/%s/startMigration"
                       % args.id, "POST", platform=args.platform)
        _print_async(r, args)
    elif args.action == "migration":
        jprint(vbr.plugin("/instantRecovery/migrations/" + args.id,
                          platform=args.platform))
    elif args.action == "stop-migration":
        r = vbr.plugin("/instantRecovery/migrations/%s/stop"
                       % args.id, "POST", platform=args.platform)
        jprint(r) if args.json else out("stopped", args.id)


# ---------------------------------------------------------------------- #
# public REST: backups, restore points, file-level restore

def _query(pairs):
    q = {k: v for k, v in pairs if v not in (None, "")}
    return ("?" + urllib.parse.urlencode(q)) if q else ""


def cmd_backup(vbr, args):
    if args.action == "list":
        q = _query([("nameFilter", args.name), ("jobIdFilter", args.job),
                    ("platformIdFilter", args.platform_id),
                    ("createdAfterFilter", args.after),
                    ("createdBeforeFilter", args.before),
                    ("limit", args.limit), ("skip", args.skip)])
        r = vbr.pub("/api/v1/backups" + q)
        if args.json:
            return jprint(r)
        out("id", "name", "jobId", "repository", "created")
        for b in r.get("data", []):
            out(b.get("id"), b.get("name"), b.get("jobId"),
                b.get("repositoryName"), b.get("creationTime"))
    elif args.action == "get":
        jprint(vbr.pub("/api/v1/backups/" + args.id))
    elif args.action == "objects":
        if args.id:
            r = vbr.pub("/api/v1/backups/%s/objects" % args.id)
        else:
            q = _query([("nameFilter", args.name),
                        ("platformIdFilter", args.platform_id),
                        ("limit", args.limit), ("skip", args.skip)])
            r = vbr.pub("/api/v1/backupObjects" + q)
        if args.json:
            return jprint(r)
        out("id", "name", "type", "restorePoints", "platform")
        for o in r.get("data", []):
            out(o.get("id"), o.get("name"), o.get("type"),
                o.get("restorePointsCount"), o.get("platformName"))
    elif args.action == "files":
        jprint(vbr.pub("/api/v1/backups/%s/backupFiles" % args.id))
    elif args.action == "remove":
        r = vbr.pub("/api/v1/backups/" + args.id, "DELETE")
        jprint(r) if args.json else out("removed", args.id)


def cmd_rp(vbr, args):
    if args.action == "list":
        q = _query([("backupObjectIdFilter", args.object),
                    ("backupIdFilter", args.backup),
                    ("nameFilter", args.name),
                    ("createdAfterFilter", args.after),
                    ("createdBeforeFilter", args.before),
                    ("platformIdFilter", args.platform_id),
                    ("limit", args.limit), ("skip", args.skip)])
        r = vbr.pub("/api/v1/restorePoints" + q)
        if args.json:
            return jprint(r)
        out("id", "name", "type", "created", "malware", "allowedOps")
        for p in r.get("data", []):
            out(p.get("id"), p.get("name"), p.get("type"),
                p.get("creationTime"), p.get("malwareStatus"),
                p.get("allowedOperations"))
    elif args.action == "get":
        jprint(vbr.pub("/api/v1/restorePoints/" + args.id))
    elif args.action == "disks":
        jprint(vbr.pub("/api/v1/restorePoints/%s/disks" % args.id))


def cmd_flr(vbr, args):
    if args.action == "mount":
        if not (args.id and args.os):
            raise CliError("flr mount needs <restorePointId> and "
                           "--os Windows|Linux", 2)
        body = {"restorePointId": args.id, "type": args.os,
                "mountMode": "Automatic",
                "autoUnmount": {"isEnabled": True,
                                "noActivityPeriodInMinutes": 30}}
        if args.reason:
            body["reason"] = args.reason
        r = vbr.pub("/api/v1/restore/flr", "POST", body)
        if args.json:
            return jprint(r)
        out("session", r.get("sessionId"))
        src = r.get("sourceProperties") or {}
        out("machine", src.get("machineName"))
        for e in r.get("mountErrors") or []:
            out("mountError", e.get("type"), e.get("message"))
        sys.stderr.write("# browse with 'vbrcli flr browse %s --path /'\n"
                         % r.get("sessionId"))
    elif args.action == "list":
        r = vbr.pub("/api/v1/backupBrowser/flr")
        if args.json:
            return jprint(r)
        out("sessionId", "type", "machine", "restorePoint")
        for m in r.get("data", []):
            src = m.get("sourceProperties") or {}
            out(m.get("sessionId"), m.get("type"), src.get("machineName"),
                src.get("restorePointName"))
    elif args.action == "get":
        jprint(vbr.pub("/api/v1/backupBrowser/flr/" + args.id))
    elif args.action == "browse":
        path = args.path
        if path is None:
            info = vbr.pub("/api/v1/backupBrowser/flr/" + args.id)
            path = "C:\\" if info.get("type") == "Windows" else "/"
        r = vbr.pub("/api/v1/backupBrowser/flr/%s/browse" % args.id, "POST",
                    {"path": path})
        if args.json:
            return jprint(r)
        out("type", "size", "modified", "state", "name")
        for i in r.get("items", []):
            out(i.get("type"), i.get("size"), i.get("modifiedDate"),
                i.get("itemState"), i.get("displayName") or i.get("name"))
    elif args.action == "unmount":
        r = vbr.pub("/api/v1/restore/flr/%s/unmount" % args.id, "POST")
        jprint(r) if args.json else out("unmounted", args.id)


# ---------------------------------------------------------------------- #
# public REST: repositories + backup copy jobs

def _backup_server_id(vbr):
    for s in vbr.pub("/api/v1/backupInfrastructure/managedServers"
                     ).get("data", []):
        if s.get("isBackupServer"):
            return s["id"]
    raise CliError("could not find the backup server in managedServers")


def cmd_repo(vbr, args):
    base = "/api/v1/backupInfrastructure/repositories"
    if args.action == "list":
        q = _query([("nameFilter", args.name), ("limit", args.limit)])
        r = vbr.pub(base + q)
        if args.json:
            return jprint(r)
        out("id", "name", "type", "host", "path")
        for rep in r.get("data", []):
            out(rep.get("id"), rep.get("name"), rep.get("type"),
                rep.get("hostName") or rep.get("hostId"),
                (rep.get("repository") or {}).get("path"))
    elif args.action == "states":
        r = vbr.pub(base + "/states")
        if args.json:
            return jprint(r)
        out("id", "name", "type", "capacityGB", "freeGB", "online")
        for s in r.get("data", []):
            out(s.get("id"), s.get("name"), s.get("type"),
                s.get("capacityGB"), s.get("freeGB"), s.get("isOnline"))
    elif args.action == "get":
        jprint(vbr.pub(base + "/" + args.id))
    elif args.action == "add":
        if not (args.name and args.path):
            raise CliError("repo add needs --name and --path "
                           "(WinLocal folder on the VBR server)", 2)
        host = args.host or _backup_server_id(vbr)
        body = {"name": args.name,
                "description": args.description or "created by vbrcli",
                "type": "WinLocal", "isDisabled": False, "hostId": host,
                "repository": {"path": args.path,
                               "taskLimitEnabled": True,
                               "maxTaskCount": args.tasks or 4},
                "mountServer": {
                    "mountServerSettingsType": "windows",
                    "windows": {
                        "mountServerId": host,
                        "writeCacheFolder":
                            "C:\\ProgramData\\Veeam\\Backup\\IRCache\\",
                        "vPowerNFSEnabled": True}}}
        if args.dry_run:
            return jprint(body)
        r = vbr.pub(base, "POST", body)
        if args.json:
            return jprint(r)
        out("session", r.get("id"))
        sys.stderr.write("# async; poll 'vbrcli session get %s --public', "
                         "then 'vbrcli repo list --name %s'\n"
                         % (r.get("id"), args.name))
    elif args.action == "rescan":
        r = vbr.pub(base + "/rescan", "POST", {"repositoryIds": [args.id]})
        jprint(r) if args.json else out("rescan", r.get("id", "ok"))
    elif args.action == "remove":
        vbr.pub(base + "/" + args.id, "DELETE")
        out("removed", args.id)


def cmd_copyjob(vbr, args):
    if args.action == "list":
        q = _query([("typeFilter", "BackupCopy"), ("nameFilter", args.name)])
        r = vbr.pub("/api/v1/jobs/states" + q)
        if args.json:
            return jprint(r)
        out("id", "name", "status", "lastResult", "repository", "objects")
        for j in r.get("data", []):
            out(j.get("id"), j.get("name"), j.get("status"),
                j.get("lastResult"), j.get("repositoryName"),
                j.get("objectsCount"))
    elif args.action == "get":
        jprint(vbr.pub("/api/v1/jobs/" + args.id))
    elif args.action == "create":
        if not (args.name and args.source_job and args.repo):
            raise CliError("copyjob create needs --name, --source-job <jobId> "
                           "and --repo <targetRepositoryId>", 2)
        body = {"name": args.name,
                "description": args.description or "created by vbrcli",
                "type": "BackupCopy", "mode": args.mode,
                "sourceObjects": {"includes": {
                    "jobs": [{"id": args.source_job}]}},
                "target": {"backupRepositoryId": args.repo,
                           "retentionPolicy": {"type": "RestorePoints",
                                               "quantity": args.keep or 7}}}
        if args.dry_run:
            return jprint(body)
        r = vbr.pub("/api/v1/jobs", "POST", body)
        jprint(r) if args.json else out("job", r.get("id"))
    elif args.action == "remove":
        vbr.pub("/api/v1/jobs/" + args.id, "DELETE")
        out("removed", args.id)
    elif args.action == "start":
        body = {"performActiveFull": False}
        if args.sync:
            body["syncRestorePoints"] = args.sync
        r = vbr.pub("/api/v1/jobs/%s/start" % args.id, "POST", body)
        _print_async(r, args)
    elif args.action == "stop":
        r = vbr.pub("/api/v1/jobs/%s/stop" % args.id, "POST",
                    {"gracefulStop": True})
        _print_async(r, args)
    elif args.action in ("enable", "disable"):
        r = vbr.pub("/api/v1/jobs/%s/%s" % (args.id, args.action), "POST")
        jprint(r) if args.json else out(args.action + "d", args.id)


# ---------------------------------------------------------------------- #
# credentials, sessions, misc

def cmd_creds(vbr, args):
    if args.action == "list":
        r = vbr.pub("/api/v1/credentials")
        if args.json:
            return jprint(r)
        out("id", "type", "username", "description")
        for c in r.get("data", []):
            out(c.get("id"), c.get("type"), c.get("username"),
                c.get("description"))
    elif args.action == "add":
        cid = vbr.find_or_create_cred(args.username, args.password, args.desc)
        out("id", cid)


def cmd_session(vbr, args):
    if args.action == "list":
        if args.public:
            r = vbr.pub("/api/v1/sessions?limit=%d" % args.limit)
            if args.json:
                return jprint(r)
            out("id", "name", "type", "state", "result", "created")
            for s in r.get("data", []):
                out(s.get("id"), s.get("name"), s.get("sessionType"),
                    s.get("state"), (s.get("result") or {}).get("result"),
                    s.get("creationTime"))
            return
        r = vbr.plugin("/sessions?limit=%d" % args.limit,
                       platform=args.platform)
        if args.json:
            return jprint(r)
        out("id", "name", "type", "state", "result", "start")
        for s in as_list(r):
            out(s.get("id"), s.get("name"), s.get("sessionType"),
                s.get("state"), s.get("result"), s.get("startTimeUtc"))
    elif args.action == "get":
        if args.public:
            return jprint(vbr.pub("/api/v1/sessions/" + args.id))
        jprint(vbr.plugin("/sessions/" + args.id,
                          platform=args.platform))
    elif args.action == "logs":
        if not args.public:
            # plugin sessions carry their log as progressState.events
            try:
                r = vbr.plugin("/sessions/" + args.id,
                               platform=args.platform)
                if args.json:
                    return jprint(r)
                out("severity", "start", "message")
                for e in (r.get("progressState") or {}).get("events", []):
                    out(e.get("severity"), e.get("startTimeUtc"),
                        e.get("message"))
                return
            except CliError:
                sys.stderr.write("# not a plugin session; trying public "
                                 "/sessions/{id}/logs\n")
        r = vbr.pub("/api/v1/sessions/%s/logs" % args.id)
        if args.json:
            return jprint(r)
        out("status", "start", "title")
        for rec in r.get("records", []):
            out(rec.get("status"), rec.get("startTime"), rec.get("title"))
    elif args.action == "stop":
        if args.public:
            r = vbr.pub("/api/v1/sessions/%s/stop" % args.id, "POST")
        else:
            r = vbr.plugin("/sessions/%s/stop" % args.id, "POST",
                           platform=args.platform)
        jprint(r) if args.json else out("stopped", args.id)


def cmd_extensions(vbr, args):
    r = vbr.extensions()
    if args.json:
        return jprint(r)
    out("type", "name", "instanceId", "uri")
    for e in r:
        out(e.get("type"), e.get("name"), e.get("instanceId"), e.get("uri"))


def cmd_login(vbr, args):
    vbr.public_token(force=True)
    vbr.private_base_token(force=True)
    info = vbr.pub("/api/v1/serverInfo")
    out("server", info.get("name"))
    out("build", info.get("buildVersion"))
    out("plugins", ", ".join(e.get("type") for e in vbr.extensions()))


def cmd_raw(vbr, args):
    body = _read_spec(args.body) if args.body else None
    if args.public:
        r = vbr.pub(args.path, args.method, body)
    elif args.private:
        r = vbr.priv(args.path, args.method, body)
    else:
        r = vbr.plugin(args.path, args.method, body, platform=args.platform)
    jprint(r)


# ---------------------------------------------------------------------- #
# argparse

def build_parser():
    p = argparse.ArgumentParser(
        prog="vbrcli", description="Veeam B&R CLI (Nutanix AHV-first).")
    p.add_argument("-j", "--json", action="store_true",
                   help="raw JSON output instead of TSV")
    p.add_argument("-P", "--platform", default=None,
                   help="plugin platform (default from config, e.g. AHV)")
    p.add_argument("--insecure", action="store_true",
                   help="skip TLS certificate verification; needed while the "
                        "VBR server still uses its out-of-the-box self-signed "
                        'certificate (same as "insecure": true in the config)')
    p.add_argument("--version", action="version", version="vbrcli " + VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("login", help="refresh tokens and show server info")
    sub.add_parser("extensions", help="list installed platform plugins")

    # prism central
    pc = sub.add_parser("prismcentral", aliases=["pc"],
                        help="manage Nutanix Prism Centrals")
    pc.add_argument("action", choices=["list", "add", "remove", "rescan",
                                       "clusters", "vms"])
    pc.add_argument("id", nargs="?")
    _add_server_args(pc)

    cl = sub.add_parser("cluster", help="manage clusters (standalone / under PC)")
    cl.add_argument("action", choices=["list", "add", "remove", "rescan",
                                       "hosts", "networks", "storagecontainers",
                                       "vms"])
    cl.add_argument("id", nargs="?")
    _add_server_args(cl)

    wk = sub.add_parser("worker", help="manage backup/restore workers")
    wk.add_argument("action", choices=["list", "get", "defaults", "test",
                                       "enable", "disable", "remove", "add"])
    wk.add_argument("id", nargs="?")
    wk.add_argument("--spec", help="worker JSON spec or @file.json (for add)")
    wk.add_argument("--cluster", help="cluster id (defaults/add)")
    wk.add_argument("--dry-run", action="store_true", dest="dry_run",
                    help="print the composed worker spec, do not submit")
    wk.add_argument("--name", help="worker VM name (add)")
    wk.add_argument("--container", help="storage container id")
    wk.add_argument("--network", help="cluster network id or exact name")
    wk.add_argument("--tasks", type=int, help="maxConcurrentTasks")
    wk.add_argument("--cpu", type=int, help="vCPU count")
    wk.add_argument("--memory", type=int, help="memory GB")
    wk.add_argument("--description")

    jb = sub.add_parser("job", help="platform backup jobs (plugin API)")
    jb.add_argument("action", choices=["list", "get", "settings", "defaults",
                                       "create", "validate", "edit", "start",
                                       "stop", "retry", "enable", "disable",
                                       "remove"])
    jb.add_argument("id", nargs="?")
    jb.add_argument("--spec", help="job JSON spec or @file.json")
    jb.add_argument("--name", help="job name (create)")
    jb.add_argument("--vms", help="comma-separated VM ids or exact names")
    jb.add_argument("--categories",
                    help="comma-separated Prism Central categories "
                         "name:value (dynamic include; AHV only)")
    jb.add_argument("--pc",
                    help="Prism Central id for --categories (default: the "
                         "only registered one)")
    jb.add_argument("--exclude-vms", dest="exclude_vms",
                    help="comma-separated VM ids or exact names to EXCLUDE "
                         "from the job scope")
    jb.add_argument("--disks", action="append",
                    help="per-VM disk rule <vm>=<bus>.<index>[,...] "
                         "(e.g. VM2=scsi.2) -- back up ONLY the listed "
                         "disks; repeat the flag for more VMs")
    jb.add_argument("--cluster", help="limit VM lookup to this cluster id")
    jb.add_argument("--repo", help="repository id (default from defaults)")
    jb.add_argument("--description")
    jb.add_argument("--keep", type=int,
                    help="restore points / days to keep (retention)")
    jb.add_argument("--compression",
                    choices=["None", "Rle", "Lz4", "Zstd3", "Zstd9"],
                    help="compression level (default Lz4)")
    jb.add_argument("--block-size", dest="block_size",
                    choices=["Kb256", "Kb512", "Kb1024", "Kb4096"],
                    help="backup block size (default Kb1024)")
    jb.add_argument("--schedule", nargs="?", const="on",
                    help="on|off|daily|monthly|periodic -- enable the run "
                         "schedule and pick its type (bare flag = enable)")
    jb.add_argument("--at", help="scheduled start time HH:MM (daily/monthly)")
    jb.add_argument("--days",
                    help="everyday|weekdays|Mon,Fri,... (daily schedule)")
    jb.add_argument("--every",
                    help="periodic schedule interval: <N>h or <N>m "
                         "(e.g. 4h, 30m)")
    jb.add_argument("--months", help="Jan,Jul,... (monthly schedule)")
    jb.add_argument("--month-day", dest="month_day",
                    help="monthly flavor: day number (15) or week:day "
                         "(fourth:sat, last:sun)")
    jb.add_argument("--quiesce", choices=["on", "off"],
                    help="advancedSettings.guestToolsSettings."
                         "guestQuiescenceEnabled")
    jb.add_argument("--ngt", choices=["on", "off"],
                    help="platform guest tools block (nutanixGuestTools"
                         "Settings.enabled; present on ALL plugin platforms)")
    jb.add_argument("--vss", choices=["none", "full", "copy"],
                    help="guest tools VSS backup type; full = truncate "
                         "logs, copy = copy-only (spelling per platform "
                         "handled automatically)")
    jb.add_argument("--active-full", nargs="?", const="on",
                    dest="active_full", metavar="DAYS[@HH:MM]",
                    help="active full backups: bare flag = weekly on the "
                         "default day, or thu@17:32 / mon,fri@06:00 / off")
    jb.add_argument("--synthetic-full", dest="synthetic_full",
                    metavar="DAYS[@HH:MM]",
                    help="synthetic full backups: on|off|<days>[@HH:MM] "
                         "(e.g. wed@14:22)")
    jb.add_argument("--app-aware", action="store_true", dest="app_aware",
                    help="enable application-aware processing (needs "
                         "--guest-creds)")
    jb.add_argument("--guest-creds", dest="guest_creds",
                    help="guest OS credentials record id for app-aware "
                         "(see 'vbrcli creds list')")
    jb.add_argument("--pg-log-backup", action="store_true",
                    dest="pg_log_backup",
                    help="enable PostgreSQL transaction log backup")
    jb.add_argument("--pg-log-every", type=int, dest="pg_log_every",
                    help="PostgreSQL log backup interval, minutes (default 15)")
    jb.add_argument("--pg-creds", dest="pg_creds",
                    help="credentials record id for the PostgreSQL account "
                         "(default: guest OS credentials)")
    jb.add_argument("--oracle-log-backup", action="store_true",
                    dest="oracle_log_backup",
                    help="enable Oracle archived log backup (log shipping)")
    jb.add_argument("--oracle-log-every", type=int, dest="oracle_log_every",
                    help="Oracle log backup interval, minutes (default 15)")
    jb.add_argument("--oracle-creds", dest="oracle_creds",
                    help="credentials record id for the Oracle account "
                         "(default: guest OS credentials)")
    jb.add_argument("--sql-log-backup", action="store_true",
                    dest="sql_log_backup",
                    help="enable MS SQL transaction log backup (uses the "
                         "guest OS credentials)")
    jb.add_argument("--sql-log-every", type=int, dest="sql_log_every",
                    help="MS SQL log backup interval, minutes (default 15)")
    jb.add_argument("--backup-window", dest="backup_window", metavar="SPEC",
                    help="permitted start hours for the periodic schedule: "
                         "'<days>@<h1>-<h2>[;...]' (e.g. "
                         "'weekdays@22-06;weekend@0-24') or off")
    jb.add_argument("--index", choices=["linux", "windows", "all"],
                    help="enable guest file system indexing")
    jb.add_argument("--dry-run", action="store_true", dest="dry_run",
                    help="print the composed job spec, do not submit")

    rs = sub.add_parser("restore",
                        help="restore VM / disks from a restore point")
    rs.add_argument("what", choices=["vm", "disk"])
    rs.add_argument("id", help="restore point id (from 'vbrcli rp list')")
    rs.add_argument("--target-name", dest="target_name",
                    help="new VM name (vm restore to a new location)")
    rs.add_argument("--original", action="store_true",
                    help="restore over the ORIGINAL VM (destructive)")
    rs.add_argument("--cluster", help="target cluster / host id")
    rs.add_argument("--storage", "--container", dest="container",
                    help="target storage container id or name (one per VM)")
    rs.add_argument("--network",
                    help="target network(s), comma-separated, mapped to the "
                         "VM's NICs positionally (id or name)")
    rs.add_argument("--vlan",
                    help="VLAN tag(s) for --network, comma-separated 0-4094 "
                         "(0 = untagged); a single value applies to all")
    rs.add_argument("--disk-format", dest="disk_format",
                    help="target disk format (e.g. Raw/Qcow2/Vmdk for "
                         "Proxmox); default: same as source")
    rs.add_argument("--target-vm", dest="target_vm",
                    help="target VM id (disk restore)")
    rs.add_argument("--disk",
                    help="disk id(s) or label(s), comma-separated "
                         "(default: all disks of the restore point)")
    rs.add_argument("--index", type=int,
                    help="target bus slot for the first restored disk "
                         "(next disks increment; default: original index)")
    rs.add_argument("--power-on", action="store_true", dest="power_on",
                    help="power the VM on after restore")
    rs.add_argument("--reason", help="restore reason for the audit log")
    rs.add_argument("--dry-run", action="store_true", dest="dry_run",
                    help="print the composed body, do not submit")

    ir = sub.add_parser("ir", help="instant recovery (plugin API)")
    ir.add_argument("action", choices=["start", "disks", "get", "stop",
                                       "migrate", "migration",
                                       "stop-migration"])
    ir.add_argument("id", help="restore point id (start/disks) / IR session "
                               "id / migration id")
    ir.add_argument("--target-name", dest="target_name",
                    help="name for the published VM (start)")
    ir.add_argument("--target-vm", dest="target_vm",
                    help="existing VM id to attach disks to (disks)")
    ir.add_argument("--cluster", help="target cluster / host id")
    ir.add_argument("--storage", "--container", dest="container",
                    help="target storage container id or name")
    ir.add_argument("--network",
                    help="target network(s), comma-separated, mapped to NICs "
                         "positionally (id or name)")
    ir.add_argument("--vlan",
                    help="VLAN tag(s) for --network, comma-separated 0-4094")
    ir.add_argument("--disk-format", dest="disk_format",
                    help="target disk format (e.g. Raw/Qcow2/Vmdk)")
    ir.add_argument("--index", type=int,
                    help="target bus slot for the first mounted disk (disks)")
    ir.add_argument("--power-on", action="store_true", dest="power_on")
    ir.add_argument("--reason")
    ir.add_argument("--dry-run", action="store_true", dest="dry_run")

    bk = sub.add_parser("backup",
                        help="backups + backup objects (public REST); "
                             "'remove' DELETES a backup (destructive)")
    bk.add_argument("action", choices=["list", "get", "objects", "files",
                                       "remove"],
                    help="remove: DELETE the backup and its restore points "
                         "(destructive, no confirmation prompt)")
    bk.add_argument("id", nargs="?")
    bk.add_argument("--name", help="name filter")
    bk.add_argument("--job", help="job id filter")
    bk.add_argument("--platform-id", dest="platform_id",
                    help="platform (plugin instance) id filter")
    bk.add_argument("--after", help="createdAfter (ISO date)")
    bk.add_argument("--before", help="createdBefore (ISO date)")
    bk.add_argument("--limit", type=int)
    bk.add_argument("--skip", type=int)

    rp = sub.add_parser("rp", aliases=["restorepoint"],
                        help="restore points (public REST)")
    rp.add_argument("action", choices=["list", "get", "disks"])
    rp.add_argument("id", nargs="?")
    rp.add_argument("--object", help="backup object id filter")
    rp.add_argument("--backup", help="backup id filter")
    rp.add_argument("--name", help="name filter")
    rp.add_argument("--platform-id", dest="platform_id")
    rp.add_argument("--after")
    rp.add_argument("--before")
    rp.add_argument("--limit", type=int)
    rp.add_argument("--skip", type=int)

    fl = sub.add_parser("flr", help="file-level restore (public REST)")
    fl.add_argument("action", choices=["mount", "list", "get", "browse",
                                       "unmount"])
    fl.add_argument("id", nargs="?",
                    help="restore point id (mount) / flr session id (rest)")
    fl.add_argument("--os", choices=["Windows", "Linux"],
                    help="guest OS type (mount)")
    fl.add_argument("--path", default=None,
                    help="folder to browse (default: C:\\ for Windows "
                         "sessions, / for Linux)")
    fl.add_argument("--reason", help="restore reason for the audit log")

    rq = sub.add_parser("repo", help="backup repositories (public REST)")
    rq.add_argument("action", choices=["list", "states", "get", "add",
                                       "rescan", "remove"])
    rq.add_argument("id", nargs="?")
    rq.add_argument("--name", help="repo name (add) / name filter (list)")
    rq.add_argument("--path", help="folder on the VBR server (WinLocal add)")
    rq.add_argument("--host", help="host id (default: the backup server)")
    rq.add_argument("--tasks", type=int, help="maxTaskCount (default 4)")
    rq.add_argument("--description")
    rq.add_argument("--limit", type=int)
    rq.add_argument("--dry-run", action="store_true", dest="dry_run")

    cj = sub.add_parser("copyjob", help="backup copy jobs (public REST)")
    cj.add_argument("action", choices=["list", "get", "create", "start",
                                       "stop", "enable", "disable", "remove"])
    cj.add_argument("id", nargs="?")
    cj.add_argument("--name", help="job name (create) / name filter (list)")
    cj.add_argument("--source-job", dest="source_job",
                    help="source backup job id (plugin job ids work)")
    cj.add_argument("--repo", help="target repository id")
    cj.add_argument("--keep", type=int, help="restore points to keep (7)")
    cj.add_argument("--mode", choices=["Immediate", "Periodic"],
                    default="Immediate")
    cj.add_argument("--sync", choices=["All", "Latest"],
                    help="sync restore points on start")
    cj.add_argument("--description")
    cj.add_argument("--dry-run", action="store_true", dest="dry_run")

    cr = sub.add_parser("creds", help="Veeam Credentials Manager records")
    cr.add_argument("action", choices=["list", "add"])
    cr.add_argument("--username")
    cr.add_argument("--password")
    cr.add_argument("--desc")

    se = sub.add_parser("session", help="plugin / VBR-core sessions")
    se.add_argument("action", choices=["list", "get", "logs", "stop"])
    se.add_argument("id", nargs="?")
    se.add_argument("--limit", type=int, default=25)
    se.add_argument("--public", action="store_true",
                    help="target VBR-core sessions (public REST) instead of "
                         "the platform plugin's")

    rw = sub.add_parser("raw", help="raw REST escape hatch")
    rw.add_argument("method")
    rw.add_argument("path")
    rw.add_argument("--body", help="JSON string or @file.json")
    g = rw.add_mutually_exclusive_group()
    g.add_argument("--public", action="store_true", help="hit public :9419 REST")
    g.add_argument("--private", action="store_true",
                   help="hit /private-api on 443")
    return p


def _add_server_args(sp):
    sp.add_argument("--address", help="IP / DNS name of PC or cluster")
    sp.add_argument("--port", type=int,
                    help="default 9440 (AHV) / 8006 (Proxmox) / 443 (others)")
    sp.add_argument("--creds", help="existing credentials record id")
    sp.add_argument("--username", help="creds username (auto-creates record)")
    sp.add_argument("--password", help="creds password")
    sp.add_argument("--creds-desc", dest="creds_desc",
                    help="description for an auto-created creds record")
    sp.add_argument("--thumbprint", help="pre-accepted certificate thumbprint")
    sp.add_argument("--ssh-fingerprint", dest="ssh_fingerprint",
                    help="pre-accepted SSH host key fingerprint (Proxmox)")
    sp.add_argument("--snapshot-storage", dest="snapshot_storage",
                    help="backup snapshot storage id: the default storage on "
                         "Proxmox, or the per-cluster storage to use when "
                         "registering an HPE Morpheus VME manager (default "
                         "there: the one with the most free space). Sangfor "
                         "aSV has no snapshot-storage step")
    sp.add_argument("--description", help="description for the added server")
    sp.add_argument("--dry-run", action="store_true", dest="dry_run",
                    help="print the composed body, do not submit")


DISPATCH = {
    "login": cmd_login,
    "extensions": cmd_extensions,
    "prismcentral": cmd_prismcentral,
    "pc": cmd_prismcentral,
    "cluster": cmd_cluster,
    "worker": cmd_worker,
    "job": cmd_job,
    "restore": cmd_restore,
    "ir": cmd_ir,
    "backup": cmd_backup,
    "rp": cmd_rp,
    "restorepoint": cmd_rp,
    "flr": cmd_flr,
    "repo": cmd_repo,
    "copyjob": cmd_copyjob,
    "creds": cmd_creds,
    "session": cmd_session,
    "raw": cmd_raw,
}


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        cfg = load_config()
        if args.insecure:
            cfg["insecure"] = True
        vbr = Vbr(cfg)
        DISPATCH[args.cmd](vbr, args)
    except CliError as e:
        sys.stderr.write("error: %s\n" % e)
        return e.code
    except BrokenPipeError:
        # a downstream pipe (| head) closed early; silence the interpreter's
        # final stdout flush too, so POSIX shells don't print a noisy trace.
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except Exception:
            pass
        return 0
    except KeyboardInterrupt:
        sys.stderr.write("\ninterrupted\n")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
