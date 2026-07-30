# vbrcli — a CLI for the Veeam Backup & Replication hypervisor plug-ins

`vbrcli` drives the whole backup lifecycle of the VBR hypervisor plug-ins —
**Nutanix AHV, Proxmox VE, XenServer / XCP-ng, Scale Computing HyperCore, HPE
Morpheus VM Essentials and Sangfor aSV** — from the command line: register
servers, deploy workers (the VMs that move the data — the plug-ins' backup
proxies), create and run backup jobs, restore VMs and disks. It talks to an
existing Veeam Backup & Replication server over HTTPS and offers the same
commands and flags on every platform.

It is built first and foremost as an **integration surface for AI agents** that
operate a VBR server, and works just as well as a human-facing CLI. One Python
file, standard library only — no pip, no dependencies — on Windows, macOS and
Linux with Python 3.7+. Output is tab-separated by default, raw JSON with `-j`;
failures print an `error: …` message on stderr and set a documented
[exit code](#exit-codes). A ready-made
[Claude Code skill](.claude/skills/vbrcli/SKILL.md) ships in
`.claude/skills/vbrcli/`, so an agent picks up the command surface and the known
traps without reading the source.

**What you need.** Requires **Veeam Backup & Replication 13.1**. Other VBR
releases are not supported and will not work: vbrcli pins the public REST API
version (`1.3-rev0`) and the per-platform plug-in API versions (AHV `v10`, the
other plug-ins `v1`). You also need the VBR host's local administrator account
in `HOST\Administrator` form — domain and appliance accounts are rejected — and
Python 3.7+. Run it from anywhere that can reach the VBR host; the first command
is `vbrcli login`, which prints the server name, its build and the installed
plug-ins. See [Setup](#setup).

Two version numbers, two meanings: the folder name (`vbrcli_13.1`) is the only
supported VBR release, while `vbrcli --version` reports the utility's own
version (0.4.0).

## Why a CLI and not an MCP server

Both give an agent access to VBR. The CLI costs less to run and less to use:

* **Fewer tokens.** No tool schemas sitting in the context window — one skill
  file plus `--help` on demand — and TSV rows instead of nested JSON envelopes.
  `-j` is there for when the structure is actually needed.
* **Nothing to host.** A single file you copy next to the agent, not a server
  process to install, run and keep alive alongside the session.
* **Predictable failures.** Every run ends in one of five documented
  [exit codes](#exit-codes), so an agent can branch on the code instead of
  parsing prose.
* **Composable and reproducible.** Commands pipe into `grep`/`jq`, run from CI
  or a scheduler, paste into a bug report, and can be replayed by a human
  as-is. The commands that compose a request body — `cluster`/`pc add`,
  `worker add`, `job create`/`edit`, `restore`, `ir`, `repo add`,
  `copyjob create` — take `--dry-run`, which prints that body instead of
  sending it.

## Two APIs behind one CLI

VBR exposes these plug-ins through two different APIs, and vbrcli hides the
difference behind one consistent CLI:

| API | What it covers |
|-----|----------------|
| Public REST (`:9419/api/v1`) | platform-agnostic: sessions, backups, restore points, credentials, repositories, backup copy jobs, file-level restore. |
| Private plug-in API (reverse proxy on 443) | the per-platform workhorse: clusters/servers, workers, jobs, restore, instant recovery. |

The plug-in API needs a 3-step token exchange and uses a different version per
platform (AHV is `v10`, the newer plug-ins are `v1`); vbrcli handles both and
caches tokens for you. You just run commands.

## Scope — what works on which platform

Everything is driven by the same commands; the differences below come from the
plug-ins themselves.

| Capability | AHV | Proxmox | Xen | Scale | HPE VME | Sangfor |
|------------|:---:|:-------:|:---:|:-----:|:-------:|:-------:|
| Add server, workers, backup jobs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| VM restore (full) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Disk restore | ✓ | ✓ | — | — | — | — |
| Instant recovery | ✓ | ✓ | — | — | — | — |
| Backup copy, file-level restore, repositories | ✓ (public REST — platform-agnostic) ||||||

`-P` takes the platform ID the server reports, not the friendly name used above:
`AHV`, `Proxmox`, `Xen`, `SCP` (Scale Computing HyperCore), `HpeVme` (HPE
Morpheus VM Essentials), `SFR` (Sangfor aSV). Matching is case-insensitive, and
`vbrcli extensions` lists the ones actually installed on your server.

Platform notes: **Proxmox** authenticates with SSH credentials and pins both
the SSH host key and the TLS certificate (`--snapshot-storage` pins its default
backup snapshot storage); the others use standard credentials and a single TLS
trust. **HPE Morpheus VME** registers the Morpheus manager
(a "cluster orchestrator") rather than a bare cluster — `cluster add` detects
this, discovers the clusters behind the manager, picks a backup snapshot
storage for each (override with `--snapshot-storage`) and registers the
orchestrator in one go. **Sangfor aSV** is a manager too, but a simpler one:
its sub-clusters arrive with the manager, so `cluster add` validates and
registers in two calls; the default port is 4430. Sangfor ships no web UI, so
the CLI (or the desktop console) is the only way to register it. Target
**storage** is one container per VM (Scale
HyperCore has a single pool, so no choice). **Networks** can be remapped per
NIC, and **VLAN tags** and **disk format** are supported where the platform
does (VLAN and disk format on Proxmox).

Guest quiescence and the guest-tools VSS mode are part of the job model on
every platform (`--quiesce`, `--ngt`, `--vss`); only the AHV web UI exposes
them as a wizard tab, so on the other platforms the CLI (or the desktop
console) is the way to set them. Note the VSS enum spelling differs between
AHV (`Copy`) and the other plug-ins (`CopyOnly`) — `--vss copy` translates
automatically.

## Setup

Copy `config.example.json` to `~/.vbrcli.json` and fill it in:

```json
{
  "url": "https://<vbr-host>",
  "rest_port": 9419,
  "username": "<VBR-HOST>\\Administrator",
  "password": "...",
  "platform": "AHV",
  "rest_api_version": "1.3-rev0"
}
```

`username` must be the local administrator of the VBR host in `HOST\Administrator`
form (domainless / appliance accounts are rejected). `platform` is the default
plug-in; every command takes `-P/--platform` to target another (list the
installed ones with `vbrcli extensions`). `rest_api_version` is the
`x-api-version` header sent to the public REST API; `1.3-rev0` is the value VBR
13.1 expects, so leave it alone — it is exposed only so a hotfix build that
demands a different header can be reached without editing the code.

No config file is needed when the environment supplies the same values, which is
the usual path for CI and for agents: `VBRCLI_URL`, `VBRCLI_USERNAME`,
`VBRCLI_PASSWORD` and `VBRCLI_PLATFORM` override the matching keys, and
`VBRCLI_CONFIG` points at a config file somewhere other than `~/.vbrcli.json`.
There is no environment variable for `rest_port` or `rest_api_version` — they
fall back to `9419` and `1.3-rev0` — and certificate checking is switched off
with `--insecure` rather than through the environment.

### TLS certificates

Certificates are verified by default. A VBR server uses a self-signed
certificate out of the box, so unless a trusted certificate is installed — or
the self-signed one has been added to the local trust store — verification
fails with a message pointing at the escape hatch:

```sh
vbrcli --insecure login
```

`"insecure": true` in `~/.vbrcli.json` makes that permanent. Either form
applies to both APIs (the public REST port and the plug-in API behind 443).
Trusting the certificate is the better fix; `--insecure` is for labs and
first-contact troubleshooting.

### Windows

```powershell
Copy-Item config.example.json "$env:USERPROFILE\.vbrcli.json"
notepad "$env:USERPROFILE\.vbrcli.json"    # fill in url / username / password
$env:PATH += ";$PWD"                       # or just call .\vbrcli.cmd
vbrcli login
```

`vbrcli.cmd` is the Windows launcher. Arguments such as `--spec @job.json` use a
leading `@` to mean "read the JSON body from this file" (without `@` the value is
parsed as inline JSON); in PowerShell quote them — `--spec '@job.json'` —
because a bare `@` is the splat operator there.

### macOS / Linux

```sh
git clone https://github.com/VeeamHub/veeam-nutanix.git
cd veeam-nutanix/vbrcli_13.1
chmod +x vbrcli vbrcli.py
ln -s "$PWD/vbrcli" ~/bin/vbrcli        # any directory on your PATH
cp config.example.json ~/.vbrcli.json
chmod 600 ~/.vbrcli.json                # it holds the VBR password
vbrcli login
```

## Commands

```
vbrcli login                         check connectivity, show server + plug-ins
vbrcli extensions                    installed plug-ins and their -P names

# servers
vbrcli prismcentral list | add | remove <id> | rescan <id> | clusters <id> | vms <id>   (alias: pc)
vbrcli cluster     list | add | remove <id> | rescan <id>
vbrcli cluster     hosts <id> | networks <id> | storagecontainers <id> | vms <id>

# workers (backup proxies)
vbrcli worker list | get <id> | defaults <clusterId> | test <id>
vbrcli worker enable <id> | disable <id> | remove <id>
vbrcli worker add --cluster <id> --name <n> [--network <id|name>] [--container <id>]
                  [--cpu N] [--memory N] [--tasks N] [--dry-run]

# backup jobs
vbrcli job list | get <id> | settings <id> | defaults
vbrcli job create --name <n> --vms <name|id,...> [--cluster <id>] [--repo <id>]
                  [--categories name:value,...] [--pc <pcId>]     (AHV: Prism Central categories)
                  [--exclude-vms <name|id,...>]
                  [--disks "<vm>=<bus>.<index>[,...]"]...          (back up ONLY those disks)
                  [--keep N] [--compression None|Rle|Lz4|Zstd3|Zstd9]
                  [--block-size Kb256|Kb512|Kb1024|Kb4096]
                  [--schedule [on|off|daily|monthly|periodic]] [--at HH:MM]
                  [--days everyday|weekdays|Mon,Fri,...] [--every 4h|30m]
                  [--backup-window "weekdays@22-06;weekend@0-24"]   (periodic schedule)
                  [--months Jan,Jul,...] [--month-day 15|fourth:sat]
                  [--active-full [thu@17:32|off]] [--synthetic-full wed@14:22|on|off]
                  [--quiesce on|off] [--ngt on|off] [--vss none|full|copy]
                  [--app-aware --guest-creds <id> [--index linux|windows|all]
                   [--pg-log-backup     [--pg-log-every N]     [--pg-creds <id>]]
                   [--oracle-log-backup [--oracle-log-every N] [--oracle-creds <id>]]
                   [--sql-log-backup    [--sql-log-every N]]]
                  [--dry-run]                              (or --spec @job.json)
vbrcli job validate ...same flags...
vbrcli job edit <id> [same flags]                          (or --spec @job.json)
vbrcli job start <id> | stop <id> | retry <id> | enable <id> | disable <id> | remove <id>

# restore
vbrcli restore vm   <rpId> --target-name <n> [--cluster <hostId>] [--storage <id|name>]
                    [--network <id|name,...>] [--vlan <n,...>] [--disk-format Raw|Qcow2|Vmdk]
                    [--power-on] [--reason <r>] [--dry-run]
vbrcli restore vm   <rpId> --original                      # overwrite the source VM
vbrcli restore disk <rpId> --target-vm <vmId> [--disk <id|label,...>] [--index N]
vbrcli ir start <rpId> --target-name <n> [--storage ...] [--network ...] [--vlan ...]
vbrcli ir disks <rpId> --target-vm <vmId>
vbrcli ir get <sid> | stop <sid> | migrate <sid> | migration <mid> | stop-migration <mid>

# backups, restore points, file-level restore (public REST)
vbrcli backup list [--name] [--job] [--after] [--before] | get <id> | objects [<backupId>] | files <id>
vbrcli backup remove <id>            DESTRUCTIVE: deletes the backup and its restore points, no prompt
vbrcli rp   list [--object] [--backup] [--name] [--after] [--before] | get <id> | disks <id>
vbrcli flr  mount <rpId> --os Windows|Linux | list | browse <sid> [--path <p>] | unmount <sid>

# repositories + backup copy (public REST)
vbrcli repo    list | states | get <id> | add --name <n> --path <folder> | rescan <id> | remove <id>
vbrcli copyjob list | get <id> | create --name <n> --source-job <jobId> --repo <repoId>
vbrcli copyjob start <id> [--sync All|Latest] | stop <id> | enable <id> | disable <id> | remove <id>

# helpers
vbrcli creds   list | add --username <u> --password <p> [--desc <d>]
vbrcli session list [--limit N] [--public] | get <id> | logs <id> | stop <id>
vbrcli raw <METHOD> <path> [--body @body.json] [--public | --private]
```

## Examples

Add a Nutanix Prism Central, then back up a VM:

```sh
vbrcli pc add --address <prism-central-ip> --username admin --password '***'
vbrcli cluster vms <clusterId>                       # find the VM
vbrcli job create --name nightly --vms myvm --cluster <clusterId> \
                  --keep 14 --schedule --at 22:00
vbrcli job start <jobId>
```

Add a Proxmox host (SSH + TLS trust handled automatically) and back up a VM:

```sh
vbrcli -P Proxmox cluster add --address pve01 --username root --password '***'
vbrcli -P Proxmox job create --name pve-nightly --vms myvm --cluster <nodeId>
vbrcli -P Proxmox job start <jobId>
```

Schedules and guest quiescence, same flags on every platform:

```sh
vbrcli job edit <jobId> --schedule daily --at 21:30 --days Mon,Fri
vbrcli job edit <jobId> --schedule monthly --months Jan,Jul --month-day fourth:sat
vbrcli job edit <jobId> --schedule periodic --every 4h
vbrcli -P Xen job edit <jobId> --quiesce on --vss full     # VSS: none|full|copy
```

Back up everything tagged with a Prism Central category, minus one VM, keep
only one disk of another VM, and schedule active + synthetic fulls:

```sh
vbrcli raw GET /api/v10/prismCentrals/<pcId>/categories    # browse name:value pairs
vbrcli job create --name env-prod --categories Environment:Production \
       --exclude-vms <vm-uuid> --disks "<vm2-uuid>=scsi.2" \
       --schedule --at 22:00 \
       --active-full thu@17:32 --synthetic-full wed@14:22
```

Categories are dynamic: VMs tagged later join the job automatically. A disk
rule (`--disks`, repeatable per VM) limits the backup to the listed disks
(`scsi|ide|sata|pci`.`index`). Note for `--spec` users: the category source
object wants `masterServerId` (the Prism Central id), not the `prismCentralId`
named in the published OpenAPI spec.

Restore a VM to a new name, on a chosen storage and network with a VLAN tag:

```sh
vbrcli rp list --name myvm                           # pick a restore point
vbrcli restore vm <rpId> --target-name myvm-restored \
       --storage local-lvm --network vmbr0 --vlan 40 --power-on
```

Back up a PostgreSQL VM with log backup, custom guest credentials and indexing —
one command:

```sh
vbrcli creds add --username postgres --password '***' --desc 'pg guest'   # -> <credId>
vbrcli job create --name pg-nightly --vms pgvm --cluster <clusterId> \
       --app-aware --guest-creds <credId> --pg-log-backup --index linux
```

Oracle and MS SQL log shipping work the same way; `--oracle-creds` /
`--pg-creds` set a dedicated DB account (default is the guest OS credentials;
MS SQL always uses those). A periodic schedule can be fenced with a backup
window — hour-granular, `<days>@<from>-<to>` segments, ranges wrap midnight:

```sh
vbrcli job create --name ora-nightly --vms oravm --cluster <clusterId> \
       --schedule periodic --every 4h --backup-window "weekdays@22-06;weekend@0-24" \
       --app-aware --guest-creds <guestCredId> \
       --oracle-log-backup --oracle-creds <oraCredId> --sql-log-backup
```

For richer application-aware setups (log retention tuning, per-VM differences)
build the job body with `--spec` — see
[`examples/job-guest-processing.json`](examples/job-guest-processing.json):
take `vbrcli job defaults`, merge a `guestProcessingSettings` block, then
`vbrcli job validate --spec @body.json` and `vbrcli job create --spec @body.json`.

`job create` and `job edit` start from the server's own default settings and
overlay your flags, so a job made from the CLI is structurally identical to one
made in the web UI. `--dry-run` prints the request without sending it.

## Notes

* **VBR 13.1 only.** The plug-in API is private — not a published, supported
  interface — and it is versioned per platform, while the public REST version is
  pinned as well. Another VBR release, or a plug-in update that moves its API
  version, will break these calls, so treat a VBR upgrade as needing a new
  vbrcli rather than expecting this copy to keep working.
* TLS certificates are verified by default. `--insecure` (or `"insecure": true`
  in the config) turns the check off for a server still presenting its
  self-signed certificate; it covers both APIs.
* `backup remove` and `restore vm --original` are destructive and ask for no
  confirmation — the first deletes a backup, the second overwrites the source
  VM.
* The public login has an anti-bruteforce lockout after several bad attempts —
  tokens are cached, so fix the credentials and reuse the cache rather than
  retrying in a loop.
* Instant recovery and replica are available only where the plug-in supports
  them (AHV and Proxmox).
* A Scale Computing HyperCore cluster that accepts only TLS 1.3 cannot be
  added when the VBR server's Windows has no TLS 1.3 client support — the
  plug-in's handshake fails with "Authentication failed ... The function
  requested is not supported". Nothing vbrcli can do about it; use an OS with
  TLS 1.3 (Windows Server 2022+) or allow TLS 1.2 on the cluster.
* `raw` is an escape hatch to any endpoint: it defaults to the current
  platform's plug-in API; add `--public` for `:9419/api/v1` or `--private` for
  the `/private-api` on 443.

### Exit codes

| Code | Meaning |
|-----:|---------|
| 0 | success |
| 1 | the request failed against the server or the network did: HTTP error, connection failure, TLS verification failure |
| 2 | bad usage — a missing or invalid flag, a name that could not be resolved, an incomplete config |
| 4 | the plug-in selected with `-P` is not installed on that VBR server |
| 130 | interrupted (Ctrl+C) |

## Requests and issues

vbrcli covers what was needed for these six plug-ins, and the command set is
meant to grow. Missing commands, extra platforms and additional output formats
are all fair game — please
[open an issue](https://github.com/VeeamHub/veeam-nutanix/issues/new/choose) or
send a pull request (see the repository
[Contributing Guide](../CONTRIBUTING.md)).

Distributed under the MIT License — see [LICENSE](../LICENSE) in the repository
root. This is a VeeamHub community project: it is not part of the Veeam product
and is not covered by Veeam Support.
