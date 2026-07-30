---
name: vbrcli
description: Work with a Veeam Backup & Replication server's hypervisor plug-ins (Nutanix AHV, Proxmox VE, XenServer/XCP-ng, Scale Computing HyperCore, HPE Morpheus VME, Sangfor aSV) via the vbrcli CLI — servers (add with Standard or Proxmox SSH+TLS trust, remove/rescan/list, child hosts/networks/storage/vms), workers (add with real VM deploy, test/enable/disable/remove), backup jobs (create with UI-identical settings/validate/start/stop/…), VM restore + disk restore + instant recovery (storage/network/VLAN remap), backups + restore points with filters, file-level restore (mount/browse/unmount), repositories, backup copy jobs, Credentials Manager records, sessions + logs, and a raw REST escape hatch over BOTH the public REST (:9419) and the private plugin API (443 reverse proxy, per-platform version). Use for ANY task against a VBR box's AHV/Proxmox/Xen/Scale/HPE/Sangfor infrastructure. Triggers - VBR, Veeam Backup, Nutanix, AHV, Proxmox, PVE, Xen, Scale Computing, HPE VME, Sangfor, SFR, aSV, Prism Central, cluster, worker, backup job, restore, instant recovery, restore point, FLR, backup copy, repository, add server, rescan, plugin API, extension token.
---

# vbrcli — Veeam B&R CLI (Nutanix AHV-first)

Source: https://github.com/VeeamHub/veeam-nutanix, folder `vbrcli_13.1`.
Credentials/target: `~\.vbrcli.json` (`url`, `rest_port`, `username` = `HOST\Administrator`, `password`, `platform`, optional `insecure`).
Token cache: `~\.vbrcli.tokens.json` (auto-managed; delete to force re-login).
TLS: certificates are verified by default. A VBR server presents a self-signed
certificate out of the box, so add `--insecure` (or set `"insecure": true` in the
config) unless the certificate is trusted locally; it covers both APIs.

## Invocation — ALWAYS this form

Run from the tool folder, or point one variable at it:

```powershell
$vc = "<path-to-clone>\veeam-nutanix\vbrcli_13.1\vbrcli.py"
python $vc <command> ...
```

Global flags: `-j` = raw JSON (default TSV → pipe to `Select-String`); `-P PLATFORM`
targets another installed plugin (default from config, e.g. `AHV`); `--insecure`
skips TLS certificate verification. `python $vc extensions` lists the platform IDs
the server itself reports, and the `-P` value comes from that list (`AHV`,
`Proxmox`, `Xen`, `RHV`, `SCP`, `HpeVme`, `SFR`, `AWS`, `Azure`, `Kasten`, and
whatever else is installed).

## Two APIs, handled for you

* **Public REST** `:9419/api/v1` — platform-agnostic (sessions, backups, restore
  points, credentials, managed servers, generic jobs). NO Nutanix job/restore verbs.
* **Private plugin API** `https://<host>/extension/<instanceId>/api/v10` (reverse
  proxy 443) — the Nutanix workhorse. Reached via a 3-step token dance the CLI does
  automatically (password → `/private-api/v1/vbrinfo/extensions` → `/private-api/oauth2/vbr_extension`).

**Anti-bruteforce:** the `:9419` login locks ~14 min after a few bad tokens. Tokens are
cached; NEVER loop-retry a login — fix creds and reuse the cache.

**Multi-host:** cached tokens are namespaced by target host (plugin
`instanceId`s are per-platform constants, not per-server), so pointing
`VBRCLI_URL` at a second VBR just works. Worth knowing as a symptom: if the
public REST calls succeed and `login` looks healthy while EVERY plugin-API call
answers `HTTP 401 ... System error.`, suspect a token cached for a different
host before you suspect the credentials.

## Common commands

```powershell
python $vc login                       # refresh + show server/build/plugins
python $vc extensions                  # installed plugins + which -P value to use
# servers
python $vc prismcentral list           # alias: pc  (AHV / HPE VME)
python $vc cluster list | cluster networks <id> | cluster vms <id>
python $vc cluster add --address <ip> --username <u> --password '<pw>' [--dry-run]
python $vc -P Proxmox cluster add --address <pve> --username root --password '<pw>'  # SSH+TLS double trust
# workers
python $vc worker defaults <clusterId>       # needs a cluster id
python $vc worker add --cluster <id> --name <vmName> [--network <id|name>] [--container <id>] [--dry-run]
python $vc worker test <workerId>            # DEPLOYS the worker VM + checks (~8 min)
# jobs (model == UI: server defaultSettings + your flags)
python $vc job create --name <n> --vms <vmName|id,...> --cluster <id> [--keep N] [--compression Lz4] [--schedule] [--at 22:00] [--dry-run]
python $vc job edit <jobId> [same flags]     # PUT /settings; overlays flags on current settings (or --spec)
# scope beyond --vms: PC categories (AHV, dynamic membership), excludes, per-VM disk rules
python $vc job create --name <n> --categories Environment:Production [--pc <pcId>] `
    --exclude-vms <vmName|uuid,...> --disks "<vm|uuid>=scsi.2[,ide.0]" [--vms ...]
# periodic fulls: on | off | <days>[@HH:MM]  (weekly; monthly flavors via --spec)
python $vc job edit <id> --active-full thu@17:32 --synthetic-full wed@14:22
# backup window (PERIODIC schedule only; hour-granular, ranges wrap midnight)
python $vc job edit <id> --schedule periodic --every 4h --backup-window "weekdays@22-06;weekend@0-24"
# schedule flavors (all platforms): daily / monthly / periodic / off
python $vc job edit <id> --schedule daily --at 21:30 --days Mon,Fri     # or --days everyday|weekdays
python $vc job edit <id> --schedule monthly --at 03:00 --months Jan,Jul --month-day 15   # or --month-day fourth:sat
python $vc job edit <id> --schedule periodic --every 4h                 # or 30m
python $vc job edit <id> --schedule off
# guest quiescence / guest-tools VSS (all plugin platforms)
python $vc job edit <id> --quiesce on --vss full     # --vss none|full|copy; --ngt on|off
python $vc job start <jobId>                 # -> sessionId; poll 'session get <id>'
# restore / instant recovery (plugin)
python $vc restore vm <rpId> --target-name <n> [--storage <id|name>] [--network vmbr0,vmbr1] [--vlan 40] [--disk-format Qcow2] [--dry-run]
python $vc restore disk <rpId> --target-vm <vmId> [--index N]
python $vc ir start <rpId> --target-name <n> ; python $vc ir stop <sessionId>   # AHV / Proxmox
# public REST
python $vc backup list --name <glob>   # filters: --job --after --before --platform-id
python $vc backup remove <backupId>    # DESTRUCTIVE: deletes the backup + its restore points, no prompt
python $vc rp list --name <vmName>     # --object --backup --after --before
python $vc flr mount <rpId> --os Windows ; python $vc flr browse <sid> ; python $vc flr unmount <sid>
python $vc repo list ; python $vc repo add --name <n> --path C:\repo
python $vc copyjob create --name <n> --source-job <jobId> --repo <repoId> ; python $vc copyjob start <id> --sync Latest
python $vc session logs <sessionId>    # plugin events, or --public for VBR-core /logs
python $vc raw GET /api/v10/clusters/<id>/vms          # plugin escape hatch (use full /api/<ver>/ path)
python $vc raw GET /api/v1/backups --public            # public REST escape hatch
```

**Server add.** `--creds <id>` OR `--username/--password` (auto reuse-or-create a
Credentials Manager record; reuse requires exact username+type+description match,
default description is per-host `vbrcli: user@address`, so same-named users on
different hosts never share a record). AHV/Xen/Scale = Standard creds, single
TLS-cert trust. **Proxmox = Linux/SSH creds, double trust** (SSH host key + TLS
cert both accepted for you; SSH fingerprint pinned in advancedSettings).
**HPE Morpheus VME = orchestrator, not cluster**: `cluster add` transparently does
validate → `clusterOrchestrators/retrieveClusters` → picks a backup snapshot
storage per cluster (most free space; override with `--snapshot-storage <id>`) →
`POST /clusterOrchestrators` (`address`, not `ip`; plain `POST /clusters` is 501
on HPE). **Sangfor aSV (`-P SFR`) = orchestrator too**, with two quirks of its
own: it validates on `/api/v2/clusters/validateConnection` with the probe wrapped
in a `clusterConnection` envelope, and it has no snapshot-storage step (the
sub-clusters arrive with the manager), so the flow is validate →
`POST /clusterOrchestrators`. Sangfor ships no Web UI bundle and no
cmdlets, so this CLI is the only way to register it. `cluster list/remove/rescan`
understand orchestrator ids on both HPE and Sangfor.
`description` is REQUIRED by the Virtualization Plug-ins' POST /clusters — sent automatically
(`--description` to customize). Ports default to 9440 (AHV) / 8006 (Proxmox) /
4430 (Sangfor) / 443 (others). Adds are async → poll `... list` for
`state: Available`. On Proxmox the node id (for workers/restore) comes from
`raw GET /api/v1/proxmox/clusters/<clusterId>/nodes`. On Proxmox judge health by
the NODE state, not the cluster row: the parent cluster object stays
`state: Unknown` (no address, port 0) even with every node of the cluster
registered and `Available` — it is a synthetic parent, not a probe result.

**Compose vs verbatim.** `worker add` / `job create` build the body from the
server's `defaultConfiguration`/`defaultSettings` + your flags → structurally
identical to the UI; `--dry-run` prints it, `--spec @file.json` bypasses. `job
create` resolves VM names to ids and `validate`s before creating; new jobs have
the scheduler off unless `--schedule`/`--at`.

**Application-aware / log backup / indexing / per-VM guest creds.** The common
case is one command:

```powershell
python $vc job create --name pg1 --vms myvm --cluster <id> `
    --app-aware --guest-creds <credId> --pg-log-backup --index linux
```

`--guest-creds <id>` is REQUIRED with `--app-aware` (guest OS credentials
record; its type Linux/Standard is detected automatically). DB log shipping is
a flag triple per engine: `--pg-log-backup` / `--oracle-log-backup` /
`--sql-log-backup` (+ `--*-log-every <min>`, default 15); `--pg-creds` /
`--oracle-creds <id>` set a dedicated DB account (`useGuestCredentials:false`
+ `credentialsId`; omitted = guest OS creds; MS SQL has no separate account).
`--index linux|windows|all` turns on guest file indexing. These apply to every
VM in `--vms`. For anything richer (log retention tuning, per-VM different
settings) build the body via `--spec`: take `job defaults`, add
`includes.objects`, add a `guestProcessingSettings` block. Working template at
`examples/job-guest-processing.json` (PostgreSQL log backup + custom Linux
creds + Linux indexing). It has FOUR sub-blocks, all keyed to
the same `{id,clusterId,type}` object:
`applicationAwareProcessing.settings[]` (per-VM app settings incl.
`postgreSqlSettings`/`msSqlSettings`/`oracleSettings`),
`indexingSettings.settings[]`, `credentials` (an OBJECT, see traps), and
`guestInteractionProxySettings`. Gotchas that cost real 400/500s:
1. `credentials` is an **object** `{credentialsId, credentialsType, credentials:[…]}` — NOT an array. Per-VM entries live in the inner `credentials.credentials[]`, each with a nested `credentials:{linuxCredentialsId, windowsCredentialsId}`.
2. `credentialsType` must not be `Unknown`; `"Ssh"` is rejected (wrong enum) — use `"Linux"` for a Linux/SSH record, `"Standard"` for Windows.
3. Every object enabled for app-aware needs a credential — an empty per-VM `credentials[]` → 400 "guest credentials ID cannot be empty".
4. Indexing needs BOTH `linuxIndexingSettings` AND `windowsIndexingSettings` present (even if one is `enabled:false, type:"Disabled"`) — one alone → 500.
5. `postgreSqlSettings.useGuestCredentials:false` = use the custom creds above; `true` = guest-OS default. Log backup toggle is `backupLogsEnabled:true`.
Enums: mode `RequireSuccess`/`IgnoreFailures`/`Disabled`; `vssMode`
`ProcessTransactionLogs`/`PerformCopyOnly`; postgre `userType`
`DbUserWithPassword`/`DbUserWithPasswordFile`/`SystemUserWithoutPassword`;
`retentionLogsType` `UntilBackupDeleted`/`KeepOnlyDays`; indexing `type`
`IndexAll`/`IndexAllExcept`/`IndexOnly`/`Disabled`. Always `job validate --spec`
first, then `job create --spec`.

**Restore.** Target host defaults to the restore point's own host (Proxmox/HPE =
node), so `--cluster` is optional for same-host. `--storage` = container id or
name (one per VM; Scale has none). `--network a,b` remaps NICs positionally,
`--vlan 40` tags (0 = untagged, 0-4094). `--disk-format` Proxmox-only. Disk
restore all platforms; instant recovery AHV/Proxmox only.

**FLR** works on `Full` restore points (`allowedOps: StartFlrRestore`); `--os
Windows` uses the default Windows mount server, `--os Linux` needs a Linux mount
host via `raw POST /api/v1/restore/flr --public` (`mountServer.helperHost.hostId`
or `mountServer.originalHost.credentialsId`).

**UI parity (verified by round-trip create+edit).** Every setting in the AHV
web-UI backup-job wizard maps to a body field and survives create→`job settings`
read-back: Job Info (name/description), Sources (`includes`/`excludes` +
Backup Filters = `diskFilterSettings`; a Category source is `{id:
"name:value", masterServerId: <pcId>, type: "Category"}` — the server DEMANDS
`masterServerId` though the published OpenAPI spec names `prismCentralId`,
otherwise 400),
Storage (`repositoryId`, retention, GFS
`Configure`=`gfsSettings`, `Map backup`=`jobs/attachBackup`) with Advanced
Settings tabs → Maintenance=`deletedVmRetention`, Storage=`compression`
+`backupBlockSize`, **Nutanix AHV tab=`advancedSettings.nutanixGuestToolsSettings`
{enabled, vssBackupType: `None`|`Full` (=truncate/VSS_BT_FULL)|`Copy`
(=VSS_BT_COPY)} + `guestToolsSettings.guestQuiescenceEnabled`**, Notifications=
`emailSettings`; Guest Processing → `guestProcessingSettings`; Schedule →
`scheduleSettings`/`activeFullSettings`/`syntheticFullSettings`/
`healthCheckSettings`. `job edit` drops the server-computed
`gfsSettings.*.beginTimeUtc` before PUT (server rejects it on write).

**Guest quiescence per platform (live-probed on PVE/Xen/HPE, create+edit
round-trips).** ALL plugin platforms share the same two advanced blocks:
`advancedSettings.guestToolsSettings.guestQuiescenceEnabled` (bool; SCP defaults
to `true`, everyone else `false`) and `advancedSettings.nutanixGuestToolsSettings
{enabled, vssBackupType}`. The vssBackupType enum SPELLING differs: AHV v10 =
`None|Full|Copy`, Virtualization Plug-ins (Proxmox/Xen/SCP/HpeVme v1) = `None|Full|CopyOnly`
— `--vss copy` translates per platform automatically. Only AHV shows these in the
web UI (Advanced Settings → "Nutanix AHV" tab); the Proxmox wizard has NO
platform tab (Storage+Notifications only, `withAhvSettings:false` in its bundle)
and Xen/SCP/HPE have no web job wizard at all — on those platforms the fields
are API/Console-settable only, and a PVE backup runs fine with quiescence on
(effect depends on the VM's QEMU guest agent).

**Schedule enums (live-probed, case-insensitive).** `scheduleSettings.type`:
`Weekly` | `Monthly` | `Periodic` — nothing else (the UI's "Daily" IS Weekly +
`configuredDays`; no after-job/chained type in the plugin API).
`weekly.configuredDays`: `EveryDay|WeekDays|SelectedDays` (+`selectedDays[]`).
`monthly.configuredWeekOrDay`: `FirstWeek..FourthWeek|LastWeek|DayOfMonth`
(+`dayOfWeek`/`dayOfMonth`/`months[]`). `periodic`: `{interval, mode:
EveryHour|EveryMinute, startTimeWithinAnHour 0-59, backupWindow:{days:[{day,
hours:[24 bools]}]}}` — the window round-trips and drives nextRun. Unknown JSON
keys are silently swallowed (a typo'd field just disappears — read back and
diff, which is what `job settings` is for).

## Support matrix

**VBR 13.1 only.** Other Veeam Backup & Replication releases are not supported
and will not work: the public REST version (`1.3-rev0`) and the per-platform
plug-in API versions (AHV `v10`, the others `v1`) are pinned to that release.

| Capability | AHV | Proxmox | Xen | Scale | HPE VME | Sangfor |
|------------|:---:|:-------:|:---:|:-----:|:-------:|:-------:|
| Server / cluster add, workers, backup jobs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| VM restore, disk restore | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Instant recovery | ✓ | ✓ | — | — | — | — |
| Backups, restore points, FLR, repositories, backup copy | ✓ (public REST — platform-agnostic) ||||||

Known platform limitation: a Scale Computing HyperCore cluster that accepts only
TLS 1.3 cannot be added when the VBR host's Windows has no TLS 1.3 client
support — the Schannel handshake fails with "The function requested is not
supported". Use an OS with TLS 1.3 support or allow TLS 1.2 on the cluster.
