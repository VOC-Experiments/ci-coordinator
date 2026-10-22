# Canonical package CI — VOC-Experiments

This organization is a disposable **first deployment** of the canonical package CI.
It uses its own repositories, credentials, signing keys and fresh package feed.
It does not read or migrate the SNodeC feed, and it does not use SNodeC credentials.

## What you need to do now

The organization and four repositories already exist. The dummy sources and the
empty publication state are pushed. The coordinator implementation is staged
locally while final offline verification completes.

**Your remaining setup is three GitHub Apps and one read-only observer token.**
Follow [the credential steps below](#2-create-the-three-github-apps). Do not move
version tags until the coordinator workflows and all credentials are ready.

In the current assisted setup session you may use
[the temporary local setup page](http://127.0.0.1:18765/). It pre-fills the three
App manifests, accepts GitHub's one-time creation callbacks, and saves the App
keys in a private local directory. **Install each App with the exact repository
selection below after creating it.** The page also links the observer-token
form. Do not paste keys or tokens into chat. This local helper is temporary
operator tooling; the CI does not depend on it. The manual procedure below is
complete without that helper.

| Repository | Purpose | Initial state |
| --- | --- | --- |
| [ci-coordinator](https://github.com/VOC-Experiments/ci-coordinator) | Capture, scheduling, verification, central signing/publication | Bootstrap documentation; verified implementation follows |
| [packages](https://github.com/VOC-Experiments/packages) | Public signed feed and status | Fresh `status.json`, no product active |
| [demo-core](https://github.com/VOC-Experiments/demo-core) | Tiny C library and executable | Source-owned JSON and Debian/OpenWrt hooks, no activation tag yet |
| [demo-app](https://github.com/VOC-Experiments/demo-app) | Tiny C executable linked to demo-core | Source-owned JSON and hooks, depends on demo-core |

Each source requests Debian trixie/amd64 and OpenWrt x86_64 and
`aarch64_generic` (`armsr/armv8`). OpenWrt 24.10.8 tests opkg/usign;
25.12.5 tests apk. There are five target rows per source. Builds use native
GCC/dpkg and OpenWrt SDK recipes; CMake is not required by the product hooks.

## 1. Deployment boundaries and preparation

Use a GitHub.com **organization**. Coordinator, sources and public feed live
under that owner. This deployment does not claim cross-owner, personal-account,
GitHub Enterprise Server or private-feed support.

An organization owner needs permission to create/install its Apps, manage the
repositories, and set repository Actions secrets/variables. For optional CLI
commands, authenticate `gh` and Git as that owner. Do not put a personal GitHub
login token in source workflows.

When deploying elsewhere, copy the same coordinator code/workflows. Change only:

- `ci/projects.json`: permitted repository basenames, feed identity/branch and
  supported settings;
- source wrappers' reusable-workflow repository/ref literals;
- source-owned definitions, hooks and `VERSION`;
- deployment content under `site/`, `install/`, and the public `keys/`;
- the new deployment's credentials.

No product matrix or dependency graph belongs in the coordinator master JSON:

```json
{
  "repositories": ["demo-core", "demo-app"],
  "feed": {"repository": "packages", "branch": "main"}
}
```

Omitted settings use plan-derived capacity, headroom 2, and automatic pinned
stale-dependency re-admission. Optional supported settings are `capacity` (a
positive integer or `"plan"`), `headroom`, and `rebuild_overlap` (boolean).
Cascades always select the highest semantic-version tag; there is no
`dependent_version` mode. Unknown settings are rejected.

## 2. Create the three GitHub Apps

Open [New organization GitHub App](https://github.com/organizations/VOC-Experiments/settings/apps/new)
for each role below. Use distinct names, for example `VOC Experiments CI
coordinator`, `VOC Experiments CI capture-reader` and `VOC Experiments CI notify`.
GitHub may require a different name if a name is already taken.

For each App:

1. Set its homepage to this repository URL.
2. Disable webhooks. These workflows use authenticated dispatches, not webhooks.
3. Set only the permissions listed below; Metadata read is implicit. No user
   permissions, webhook subscriptions or OAuth user authorization are needed.
4. Make it private to the organization.
5. Create it, note its **Client ID**, and generate/download its private-key PEM.
   The workflow uses the Client ID (`Iv...`), not the numeric App ID.
6. Choose **Install App → VOC-Experiments → Only select repositories**, and select
   exactly the repositories listed below.
7. Retain the PEM privately. Never commit it, upload it as a build artifact,
   publish it in an issue, or paste it into a command argument/chat.

| App role | Repository permissions | Install on | Who holds its private key |
| --- | --- | --- | --- |
| Coordinator | Actions **read/write**, Contents **read/write** | ci-coordinator, packages, demo-core, demo-app | ci-coordinator only |
| Capture reader | Actions **read**, Contents **read** | ci-coordinator **only** | demo-core and demo-app |
| Notify | Actions **read/write** | ci-coordinator **only** | demo-core and demo-app |

The coordinator key has the installation's full authority. Per-step token
narrowing does not reduce what someone holding that private key can do. Never
share it with the source repositories. Neither source App may be installed on
the feed or another product repository. The notify role retains a residual
ability to cancel coordinator runs/delete artifacts; it has no publication or
signing authority.

### Set the App variables and secrets

Use each repository's **Settings → Secrets and variables → Actions**. Client IDs
are **Variables**; PEM private keys are **Secrets**.

| Repository | Variable | Secret |
| --- | --- | --- |
| ci-coordinator | `PACKAGES_APP_CLIENT_ID` = coordinator App Client ID | `PACKAGES_APP_PRIVATE_KEY` = coordinator App PEM |
| demo-core | `PACKAGE_CAPTURE_APP_CLIENT_ID` = capture-reader Client ID | `PACKAGE_CAPTURE_APP_PRIVATE_KEY` = capture-reader PEM |
| demo-core | `PACKAGE_NOTIFY_APP_CLIENT_ID` = notify Client ID | `PACKAGE_NOTIFY_APP_PRIVATE_KEY` = notify PEM |
| demo-app | `PACKAGE_CAPTURE_APP_CLIENT_ID` = capture-reader Client ID | `PACKAGE_CAPTURE_APP_PRIVATE_KEY` = capture-reader PEM |
| demo-app | `PACKAGE_NOTIFY_APP_CLIENT_ID` = notify Client ID | `PACKAGE_NOTIFY_APP_PRIVATE_KEY` = notify PEM |

CLI equivalent, run locally with private keys in an ignored/protected directory:

```sh
gh variable set PACKAGES_APP_CLIENT_ID --repo VOC-Experiments/ci-coordinator --body 'COORDINATOR_CLIENT_ID'
gh secret set PACKAGES_APP_PRIVATE_KEY --repo VOC-Experiments/ci-coordinator < bootstrap-private/coordinator.pem

for repo in demo-core demo-app; do
    gh variable set PACKAGE_CAPTURE_APP_CLIENT_ID --repo "VOC-Experiments/$repo" --body 'READER_CLIENT_ID'
    gh secret set PACKAGE_CAPTURE_APP_PRIVATE_KEY --repo "VOC-Experiments/$repo" < bootstrap-private/capture-reader.pem
    gh variable set PACKAGE_NOTIFY_APP_CLIENT_ID --repo "VOC-Experiments/$repo" --body 'NOTIFY_CLIENT_ID'
    gh secret set PACKAGE_NOTIFY_APP_PRIVATE_KEY --repo "VOC-Experiments/$repo" < bootstrap-private/notify.pem
done
```

Replace the three Client ID placeholders; do not use them literally. The
agent-assisted manifest flow already saves the keys privately, so you can ask
the agent to perform these repository-secret writes after installing the Apps.
No private key needs to be sent through chat.

## 3. Create the read-only organization observer token

The coordinator must see **all organization repositories and Actions jobs**, not
only these package builds. It must also read the organization's plan.

1. Open [the prefilled fine-grained token form](https://github.com/settings/personal-access-tokens/new?name=VOC-Experiments-CI-observer&target_name=VOC-Experiments&expires_in=7&actions=read&organization_plan=read).
2. Confirm **Resource owner: VOC-Experiments**.
3. Choose **All repositories** in that organization, including future repositories.
   This is needed for complete capacity accounting.
4. Repository permissions: **Actions: read**; Metadata read is implicit.
5. Organization permissions: **Plan: read**. Do not grant Contents write, Actions
   write, administration write, or access to another organization.
6. Use a short expiry for this experiment (the link proposes seven days). Approve
   the token for the organization if GitHub requires owner approval.
7. Save it directly as the **ci-coordinator repository secret**
   `PACKAGES_OBSERVER_TOKEN`. Do not store it in a source repository or Git.

The token is a secret, not a Variable. Renew it before expiry. Its ability to
return plan and complete inventory fields is verified by actual capacity
observation; a missing/inaccessible field is not assumed to mean zero jobs.

The default headroom of two slots is best effort. Queued unrelated jobs are
reported as backlog, not occupied capacity. Known queued admitted runs retain
commitments until observed start/terminal execution. Unknown capacity pauses
new admissions and leaves built artifacts intact; it is not permission to make
capacity unlimited. Counting and dispatching are not atomic.

## 4. Configure isolated package-signing keys

All private signing keys exist in **ci-coordinator Secrets only**:

| Secret | Public verification file in coordinator `keys/` |
| --- | --- |
| `APT_SIGNING_KEY` | `apt.asc` |
| `OPENWRT_USIGN_KEY` | `opkg.pub` |
| `OPENWRT_APK_KEY` | `apk.pem` |

The current assisted experiment already has newly generated test keys. They are
separate from SNodeC keys and stored privately; the agent can upload them after
App setup. Its OpenPGP key expires after seven days. Only public keys are
committed to the coordinator.

For a new deployment, generate your own keys with existing operator tools:

```sh
umask 077
mkdir -p bootstrap-private keys
# Use a dedicated empty GNUPGHOME outside Git, owned by you with mode 0700.
export GNUPGHOME=/absolute/private/path/to/deployment-gnupg
mkdir -p "$GNUPGHOME"
chmod 700 "$GNUPGHOME"
gpg --quick-generate-key 'Package CI <packages@example.invalid>' rsa3072 sign 7d
# Replace KEY_FINGERPRINT with the generated key fingerprint.
gpg --armor --export KEY_FINGERPRINT > keys/apt.asc
gpg --armor --export-secret-keys KEY_FINGERPRINT > bootstrap-private/apt.asc
usign -G -s bootstrap-private/opkg.key -p keys/opkg.pub
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out bootstrap-private/apk.key
openssl pkey -in bootstrap-private/apk.key -pubout -out keys/apk.pem

gh secret set APT_SIGNING_KEY --repo VOC-Experiments/ci-coordinator < bootstrap-private/apt.asc
gh secret set OPENWRT_USIGN_KEY --repo VOC-Experiments/ci-coordinator < bootstrap-private/opkg.key
gh secret set OPENWRT_APK_KEY --repo VOC-Experiments/ci-coordinator < bootstrap-private/apk.key
```

These are explicit operator examples, not commands run automatically by the CI.
Replace the identity, directory and expiry policy for your deployment. Use a
noninteractive-compatible OpenPGP signing key; publication cannot prompt for a
passphrase. The `.gitignore` excludes `bootstrap-private/`, but check `git status`
before committing. Never distribute signing secrets to a source repository.

## 5. Initialize the feed and deploy in order

For a **new empty** feed repository, its first normal commit contains:

```json
{
  "repository": "VOC-Experiments/packages",
  "branch": "main",
  "counters": {},
  "allocations": {},
  "requests": {},
  "runs": {}
}
```

This is already pushed to [packages/main](https://github.com/VOC-Experiments/packages/blob/main/status.json).
It activates no product. There is no historical import or old-CI trigger.

Complete the following order:

1. Create the repositories and initial fresh feed.
2. Configure and verify the three App installations, repository variables and
   secrets, observer access, and matching public/private signing keys.
3. Push the verified coordinator workflows/core/config/content to `main`. The
   scheduled control workflow and workflow-completion wakes can then run.
4. Push the source wrappers, JSON, hooks and `VERSION` to each default branch.
   Sources already have this integration; no version tag has been created yet.
5. Verify the wrappers point to
   `VOC-Experiments/ci-coordinator/.github/workflows/...@main`.
6. Only then create the first source version tags as described below.

Do not replace the observer by a broad source credential, install source Apps on
all repositories, or bypass failed verification. The coordinator implementation
must stay identical to the verified canonical code; deployment configuration,
content and wrapper literals are the intended differences.

## 6. Activate sources with their own version tags

A permitted repository is inactive until its **own** valid tag notification.
Each tag's exact commit must contain `VERSION`, `ci/packages.json`, its build
hooks and the workflow integration. Tags must be strict `vMAJOR.MINOR.PATCH`
(no leading zeros or prereleases), and root `VERSION` must match without `v`.

For the ordinary startup sequence, run in the relevant **sandbox source** clone:

```sh
# demo-core: VERSION is 1.0.0; integration is committed on main.
git tag v1.0.0 main
git push origin refs/tags/v1.0.0
# Wait for matching core targets to be signed and published.

# demo-app: VERSION is 1.0.0; integration is committed on main.
git tag v1.0.0 main
git push origin refs/tags/v1.0.0
```

Check `git remote -v` first: these commands are for **VOC-Experiments**, not SNodeC.
A source tag triggers its own notification; no manual coordinator dispatch is
needed for normal releases.

Expected behavior:

- Core's first tag activates/builds/signs/publishes core only. The inactive app is
  not read or cascaded merely because it is allowlisted.
- App's own first tag activates it. It builds each row only against matching
  published core prerequisites. Missing rows fail clearly; activation persists.
- A later core publication cascades recursively to active matching dependents at
  their **highest semantic-version tag**, pinning the resolved source and JSON.
- A direct app tag builds that exact version, including an older version.
  Moving an older tag does not make cascades choose it.
- Versions coexist in the feed. Status shows the highest version; older build
  activity does not replace its state, timestamps or real source-job log link.
- Each row progresses independently; there is no full-matrix barrier.

Moved tags are allowed. To move a sandbox tag, first commit a source change with
matching `VERSION`, then explicitly move/push that tag. This creates a fresh
capture/revision. Never move a production tag while testing this experiment.

## 7. Verify actual behavior

Use the repositories' **Actions** tabs, real job links from the feed status pages,
and the internal `packages/status.json` ledger. Do not infer success only from a
green notification or a rendered page.

```sh
gh run list --repo VOC-Experiments/ci-coordinator --limit 30
gh run list --repo VOC-Experiments/demo-core --limit 20
gh run list --repo VOC-Experiments/demo-app --limit 20
gh api repos/VOC-Experiments/packages/contents/status.json --jq .content | base64 --decode
```

Record capture IDs, source run/attempt/job IDs, artifact digests, target rows and
publication receipts. Verify all requested rows, not just the first one:

- `debian-trixie-amd64`;
- `openwrt-24.10-x86_64`, `openwrt-24.10-aarch64_generic`;
- `openwrt-25.12-x86_64`, `openwrt-25.12-aarch64_generic`.

Check APT InRelease/Release.gpg, OpenWrt 24.10 Packages usign signatures, and
OpenWrt 25.12 APK signatures against this deployment's public keys. Install/run
packages only in disposable test containers/targets, not on the workstation or
production devices.

The live experiment must also cover app-before-core missing-prerequisite
failure, later recovery, moved tags, older direct releases versus highest chain
selection, callback/replay safety, stale overlap and retry behavior. A full
chain/diamond test needs additional dummy products; the same coordinator must
handle them through allowlist/own definitions only. Do not claim diamond proof
from a two-product graph or claim mocked capacity timing as a live measurement.

## 8. Recovery and common setup errors

| Symptom | Check / supported action |
| --- | --- |
| Missing Client ID/private-key input | Correct repository-level Variable versus Secret names; verify source caller has both reader and notify roles |
| App cannot access repository | Check installation selection and permissions, not only per-step token narrowing |
| Capacity unknown | Verify observer resource owner, all-repository coverage, Plan/Actions read permissions and expiry; retain ledger and inspect reason/backoff |
| Missing prerequisite | Publish matching core row; the failed direct node stays closed, while a later genuine cascade can select the highest app tag |
| Deterministic build/publication failure | Repair cause, then authorized operator retry or a new valid source event; no endless automatic retries |
| Expired build artifact | Operator retry rebuilds after discarding expired artifact |
| Expired immutable capture | New valid source release notification is required; never silently recapture different bytes |
| Retried held capture under old root | It retires with an actionable reason; current root re-evaluates the dependent |
| Observer cannot see a known queued run | Commitment stays fail-closed; repair access before deliberately retrying and potentially duplicating execution |

Authorized operators use **Coordinate package builds** to retry
`capture/project/target`, or wake without retry after repairing access. Retry
resets only that node's budgets and may reuse a valid artifact. Inspect the
node's category/reason/backoff. A 404 may mean inaccessible or expired; it does
not prove absence. `queue: max` is finite; reconciliation recovers callbacks,
not a lost manual operator request.

Strict priority is ready publication, then dependent/overlap/capture work, then
direct releases. There is no fairness/root injection or preemption; drain claims
assume bounded arrivals/retries. Headroom is best effort, not reserved runners.

## 9. Cleanup and promoting fixes

Keep the experiment's run IDs, logs, receipts, hashes and failure cases before
cleanup. Revoke/delete only **sandbox** credentials and repositories when their
owner authorizes that cleanup. Never rotate or reuse SNodeC credentials here.

Sandbox deployment does not authorize merging the SNodeC task PRs, wiping its
feed, or moving its tags. Any canonical fix found live must return to the task
worktree, pass its relevant tests, and be deployed back here as identical core
code. Do not patch a sandbox-only coordinator implementation and call that
reusability.

More integration detail: [ci/README.md](ci/README.md).
