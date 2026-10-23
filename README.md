# Canonical package CI — VOC-Experiments

This organization is a disposable **first deployment** of the canonical package CI.
It uses its own repositories, credentials, signing keys and fresh package feed.
It does not read or migrate the SNodeC feed, and it does not use SNodeC credentials.

The [live test matrix](docs/live-validation.md) tracks guarantees across all sandbox repositories, evidence and unresolved setup.

## Current validation verdict

**Changes complete for the tested scope (23 October 2026); no production go-live claim.**
The empty OpenWrt 24.10 index defect is corrected: indexes now derive from verified own and retained package controls. Both architecture indexes, raw signatures, every indexed IPK checksum/size and control identity were independently checked. The trusted publisher rejects namespace/version/architecture spoofs across Debian/RPM/opkg/APK. Real OpenWrt client installation still requires the separate S2 approval for the rootfs/tool stage; signing and metadata checks alone do not prove it.

The deliberately held/failed-arm diamond passed: direct App published outside Core lineage while Side was stale, with zero early Join captures/builds. One operator Side rerun was followed by exactly one Join capture 39885172814, source 39885255474 and publication. The final raw admission audit covers89 generations / 114 observations with zero errors;37 Join artifact/publication records were inspected with zero errors. Auditors use raw sources, revisions and owned checksums, including duplicate/stale negative self-tests. Counts are bounded evidence, not a universal timing claim.

The final frozen offline suite ran 288 tests: 287 passed, zero failures/errors, one skipped because local OpenWrt signer tools are absent. All 28 runner and 22 static checks passed. Both complete unrelated offline deployments and the deployed coordinator match 22 generic files. No new CI state/schema/controller/workflow/permission was introduced.

Healthy current source hooks are restored after the deliberate fixtures. Side v1.3.0@ccd1ff10e3f079dc3d3b327b34e966dae8977df8 capture 39889290108 published all five rows; exactly one corresponding healthy Join child per row published on final coordinator code e86bbe8. Previous tag commits, failed runs, bundles and negative fixtures remain immutable evidence. See the [item-by-item live matrix](docs/live-validation.md) for partial/blocked cases and the exact scope.

## What you need to do now

The organization and six repositories exist, and the coordinator workflows,
dummy sources and fresh publication state are pushed. All three Apps and the
expected repository credential entries are configured. Secret contents were
checked manually by the operator; runtime authentication and signing are tested
separately below.

**Prepared sandbox: configuration is complete; do not recreate its Apps or keys.**
Tag activation, missing-prerequisite closure, moved-tag capture, highest-only status, direct older releases, source reruns, sibling/version/SDK retention, callback verification and the deliberately sequenced diamond have bounded live evidence. Rootfs/client installation and unapproved fault/permission probes remain incomplete. The current verdict and [live matrix](docs/live-validation.md) are authoritative; earlier evidence counts are historical.

The observer PAT authenticates, reads the organization plan, and lists all six
repositories. The approved policy accepts the complete paginated inventory when
GitHub omits optional private-repository counters, relying on mandatory
**All repositories** scope (section 3). Known counter mismatches and API/listing
failures still block admission. Capacity admission has now succeeded live.

For a new deployment, follow [the credential steps below](#2-create-the-three-github-apps)
from the beginning. In this prepared sandbox, do not recreate the existing Apps.

The historical assisted setup used
[the temporary local setup page](http://127.0.0.1:18765/). When running, it pre-fills the three
App manifests, accepts GitHub's one-time creation callbacks, and saves the App
keys in a private local directory. **Install each App with the exact repository
selection below after creating it.** The page also links the observer-token
form. Do not paste keys or tokens into chat. This local helper is temporary
operator tooling; the CI does not depend on it. The manual procedure below is
complete without that helper.

| Repository | Purpose | Role |
| --- | --- | --- |
| [ci-coordinator](https://github.com/VOC-Experiments/ci-coordinator) | Capture, scheduling, verification, central signing/publication | Canonical coordinator deployed; live validation underway |
| [packages](https://github.com/VOC-Experiments/packages) | Public signed feed and status | Isolated signed feed and runtime ledger |
| [demo-core](https://github.com/VOC-Experiments/demo-core) | Tiny C library and executable | Diamond root; source-owned JSON and Debian/OpenWrt hooks |
| [demo-app](https://github.com/VOC-Experiments/demo-app) | Tiny C executable linked to demo-core | First diamond arm, depends on demo-core |
| [demo-side](https://github.com/VOC-Experiments/demo-side) | Library and executable using demo-core | Second diamond arm |
| [demo-join](https://github.com/VOC-Experiments/demo-join) | Executable using both arms | Diamond join; depends on demo-app and demo-side |

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

When preparing a coordinator deployment, ignore only root build/checkouts
directories (`/build/` and `/checkouts/`). A bare `build/` ignore pattern also
hides `ci/build/`, preventing its scripts from being committed. Before pushing,
check that `git ls-files ci/build` lists all four platform scripts; verify the
committed tree, not just files present in the working directory.

No product matrix or dependency graph belongs in the coordinator master JSON:

```json
{
  "repositories": ["demo-core", "demo-app", "demo-side", "demo-join"],
  "feed": {"repository": "packages", "branch": "main"}
}
```

Omitted settings use plan-derived capacity, headroom 2, and automatic pinned
stale-dependency re-admission. Optional supported settings are `capacity` (a
positive integer or `"plan"`), `headroom`, and `rebuild_overlap` (boolean).
Cascades always select the highest semantic-version tag; there is no
`dependent_version` mode. Unknown settings are rejected.

## 2. Create the three GitHub Apps

Create **three separate Apps**, one for each role. Start with the coordinator.
Open [New organization GitHub App](https://github.com/organizations/VOC-Experiments/settings/apps/new).

### Fill in the “Create GitHub App” form

If you are on the form with the long permissions list, use this table. You do
not need to fill every section.

| Field or section on GitHub | What to enter or select |
| --- | --- |
| **GitHub App name** | Coordinator: `VOC Experiments CI Coordinator`. Later repeat with `VOC Experiments CI Capture Reader` and `VOC Experiments CI Notify`. Names must be unique; a different name does not change the role. |
| **Description** | Optional; for example `Isolated package CI coordinator for VOC-Experiments`. |
| **Homepage URL** | Use `https://github.com/VOC-Experiments/ci-coordinator` for **all three Apps**: Coordinator, Capture Reader and Notify. |
| **Redirect URL / callback URLs** | Leave empty. This CI does not use user OAuth authorization. |
| **Allow mismatching** | Leave unchecked. |
| **Expire user authorization tokens** | Leave the default; this CI does not use these tokens. |
| **Request user authorization (OAuth) during installation** | Leave unchecked. |
| **Enable Device Flow** | Leave unchecked. |
| **Post installation → Setup URL** | Leave empty; leave redirect-on-update unchecked. |
| **Webhook → Active** | **Uncheck it.** No webhook endpoint is required. |
| **Webhook URL / Secret** | Leave empty after disabling Active. If GitHub still requires a webhook URL, check that **Active is unchecked**. |
| **Permissions → Repository permissions** | Change only the Actions/Contents rows listed in the role table below. Leave **Metadata** at its mandatory read-only value. |
| **Organization, Account and Enterprise permissions** | Leave unchanged, with no optional permissions granted. The observer token is configured separately in section 3. |
| **Subscribe to events** | Leave **every event unchecked**, including Workflow dispatch. These are webhook subscriptions; they are not needed to dispatch an Actions workflow. |
| **Where can this GitHub App be installed?** | Select **Only on this account** (`VOC-Experiments`), not Any account. |

**All three Apps use the same Homepage URL:**
`https://github.com/VOC-Experiments/ci-coordinator`. This is an informational
link. Each App's permissions and installation selection determine its role;
there is no separate homepage for the reader or notify App.

### Before you start: three Apps, three different roles

**Do not repeat the coordinator credentials in every repository.** You will
create these three App registrations, each with its own Client ID and private
key. All four source repositories share the capture-reader credentials and share
the notify credentials.

| App to create | Actions permission | Contents permission | Install on | Save its credentials in |
| --- | --- | --- | --- | --- |
| `VOC Experiments CI Coordinator` | Read and write | Read and write | All six named repositories | ci-coordinator only |
| `VOC Experiments CI Capture Reader` | Read-only | Read-only | ci-coordinator only | all four source repositories |
| `VOC Experiments CI Notify` | Read and write | No access | ci-coordinator only | all four source repositories |

**Installation selection and credential destination are different.** The two
source Apps are installed only on `ci-coordinator`, because they let source
workflows read captures from, and send notifications to, the coordinator. Their
private keys are saved in all four source repositories, where those workflows run.

**All entries below are repository-level Actions entries.** Do not create an
Environment. A Client ID goes under **Variables → New repository variable**.
The private key goes under **Secrets → New repository secret**: paste the whole
PEM file, including its BEGIN/END lines and line breaks, not its filename.
Never paste a private key into chat or commit it to Git.

To return to an existing App, open
[VOC-Experiments → Settings → Developer settings → GitHub Apps](https://github.com/organizations/VOC-Experiments/settings/apps)
and click **Edit** next to its name. An App registration can exist before it
appears in the installed-Apps list. Do not recreate an App you already created.

### 2.1 Coordinator App — create, install, then save in ci-coordinator

If you already completed this App and saved both repository entries, continue
to **2.2 Capture Reader**. Keep the coordinator credentials where they are.

1. Open [New organization GitHub App](https://github.com/organizations/VOC-Experiments/settings/apps/new).
2. Enter **GitHub App name:** `VOC Experiments CI Coordinator`.
3. Use the common form fields above: Homepage URL
   `https://github.com/VOC-Experiments/ci-coordinator`, **Webhook Active unchecked**,
   callback/setup URLs empty, **Only on this account** selected.
4. Under **Repository permissions**, set **Actions → Read and write** and
   **Contents → Read and write**. Metadata stays mandatory read-only. Leave every
   other optional permission at No access, including **Workflows**. Select no events.
5. Click **Create GitHub App**. On its General page, copy the **Client ID**
   (`Iv...`), not the numeric App ID. No OAuth Client secret is needed.
6. Click **Generate a private key** and save the downloaded `.pem` securely.
   For the CLI examples below, this is `bootstrap-private/coordinator.pem`.
7. Click **Install App** in the App's sidebar, choose **VOC-Experiments**, choose
   **Only select repositories**, and select exactly `ci-coordinator`, `packages`,
   `demo-core`, `demo-app`, `demo-side`, and `demo-join`. Click **Install** and finish the confirmation.
8. Open [ci-coordinator Actions Variables](https://github.com/VOC-Experiments/ci-coordinator/settings/variables/actions).
   Click **New repository variable**. Name: `PACKAGES_APP_CLIENT_ID`.
   Value: this **Coordinator App's Client ID**. Save it.
9. Open [ci-coordinator Actions Secrets](https://github.com/VOC-Experiments/ci-coordinator/settings/secrets/actions).
   Click **New repository secret**. Name: `PACKAGES_APP_PRIVATE_KEY`.
   Value: the entire **Coordinator App's PEM**. Save it.

**Checkpoint:** ci-coordinator now has one App Client ID variable and one App
private-key secret. Do not put either coordinator credential in the source
repositories. Creating this App does not create the other two Apps.

### 2.2 Capture Reader App — create, install, then save in all four sources

This is a **new, separate App**, not another key generated for the Coordinator App.
It lets source workflows read coordinator captures and tooling.

1. Open [New organization GitHub App](https://github.com/organizations/VOC-Experiments/settings/apps/new).
2. Enter **GitHub App name:** `VOC Experiments CI Capture Reader`.
3. Set **Homepage URL:** `https://github.com/VOC-Experiments/ci-coordinator`. Use
   **Webhook Active unchecked**, empty callback/setup URLs, and **Only on this account**.
4. Set **Actions → Read-only** and **Contents → Read-only**. Leave other optional
   permissions at No access, including Workflows; leave all events unchecked.
5. Click **Create GitHub App**. Copy this **Capture Reader App's Client ID**.
6. Click **Generate a private key**. Save this App's downloaded PEM separately
   from the coordinator PEM. In the CLI examples: `bootstrap-private/capture-reader.pem`.
7. Click **Install App** → **VOC-Experiments** → **Only select repositories** →
   select **ci-coordinator only** → **Install**. Do not select any source repository or packages.
8. Open [demo-core Actions Variables](https://github.com/VOC-Experiments/demo-core/settings/variables/actions).
   Create repository variable `PACKAGE_CAPTURE_APP_CLIENT_ID` with this
   **Capture Reader App's Client ID**.
9. Open [demo-core Actions Secrets](https://github.com/VOC-Experiments/demo-core/settings/secrets/actions).
   Create repository secret `PACKAGE_CAPTURE_APP_PRIVATE_KEY` with this
   **Capture Reader App's entire PEM**.
10. Open [demo-app Actions Variables](https://github.com/VOC-Experiments/demo-app/settings/variables/actions).
    Create repository variable `PACKAGE_CAPTURE_APP_CLIENT_ID` with the **same
    Capture Reader Client ID** you used in demo-core.
11. Open [demo-app Actions Secrets](https://github.com/VOC-Experiments/demo-app/settings/secrets/actions).
    Create repository secret `PACKAGE_CAPTURE_APP_PRIVATE_KEY` with the **same
    Capture Reader PEM** you used in demo-core.

12. Repeat the same repository-variable and repository-secret entries in
    [demo-side variables](https://github.com/VOC-Experiments/demo-side/settings/variables/actions) /
    [secrets](https://github.com/VOC-Experiments/demo-side/settings/secrets/actions), and
    [demo-join variables](https://github.com/VOC-Experiments/demo-join/settings/variables/actions) /
    [secrets](https://github.com/VOC-Experiments/demo-join/settings/secrets/actions). Use the same
    Capture Reader Client ID and PEM as in demo-core and demo-app.

**Checkpoint:** all four source repositories now have their capture variable and
secret. Their names and values match each other. They do not match the
coordinator's credentials. Now create the third App below.

### 2.3 Notify App — create, install, then save in all four sources

This is a **third App** with its own Client ID and PEM. It lets source workflows
notify and call back to the coordinator.

1. Open [New organization GitHub App](https://github.com/organizations/VOC-Experiments/settings/apps/new).
2. Enter **GitHub App name:** `VOC Experiments CI Notify`.
3. Set **Homepage URL:** `https://github.com/VOC-Experiments/ci-coordinator`. Use
   **Webhook Active unchecked**, empty callback/setup URLs, and **Only on this account**.
4. Set **Actions → Read and write**. Leave **Contents → No access** and every other
   optional permission at No access, including Workflows. Select no events.
5. Click **Create GitHub App**. Copy this **Notify App's Client ID**.
6. Click **Generate a private key**. Save this App's PEM separately from the
   other two. In the CLI examples: `bootstrap-private/notify.pem`.
7. Click **Install App** → **VOC-Experiments** → **Only select repositories** →
   select **ci-coordinator only** → **Install**. Do not select any source repository or packages.
8. Open [demo-core Actions Variables](https://github.com/VOC-Experiments/demo-core/settings/variables/actions).
   Create repository variable `PACKAGE_NOTIFY_APP_CLIENT_ID` with this
   **Notify App's Client ID**.
9. Open [demo-core Actions Secrets](https://github.com/VOC-Experiments/demo-core/settings/secrets/actions).
   Create repository secret `PACKAGE_NOTIFY_APP_PRIVATE_KEY` with this
   **Notify App's entire PEM**.
10. Open [demo-app Actions Variables](https://github.com/VOC-Experiments/demo-app/settings/variables/actions).
    Create repository variable `PACKAGE_NOTIFY_APP_CLIENT_ID` with the **same
    Notify Client ID** you used in demo-core.
11. Open [demo-app Actions Secrets](https://github.com/VOC-Experiments/demo-app/settings/secrets/actions).
    Create repository secret `PACKAGE_NOTIFY_APP_PRIVATE_KEY` with the **same
    Notify PEM** you used in demo-core.

12. Repeat the same repository-variable and repository-secret entries in
    [demo-side variables](https://github.com/VOC-Experiments/demo-side/settings/variables/actions) /
    [secrets](https://github.com/VOC-Experiments/demo-side/settings/secrets/actions), and
    [demo-join variables](https://github.com/VOC-Experiments/demo-join/settings/variables/actions) /
    [secrets](https://github.com/VOC-Experiments/demo-join/settings/secrets/actions). Use the same
    Notify Client ID and PEM as in demo-core and demo-app.

### 2.4 Check the completed App setup

These are the exact repository entries after all three App procedures:

| Repository | Repository variable and its value | Repository secret and its value |
| --- | --- | --- |
| ci-coordinator | `PACKAGES_APP_CLIENT_ID` = Coordinator Client ID | `PACKAGES_APP_PRIVATE_KEY` = Coordinator PEM |
| demo-core | `PACKAGE_CAPTURE_APP_CLIENT_ID` = Capture Reader Client ID | `PACKAGE_CAPTURE_APP_PRIVATE_KEY` = Capture Reader PEM |
| demo-core | `PACKAGE_NOTIFY_APP_CLIENT_ID` = Notify Client ID | `PACKAGE_NOTIFY_APP_PRIVATE_KEY` = Notify PEM |
| demo-app | `PACKAGE_CAPTURE_APP_CLIENT_ID` = same Capture Reader Client ID | `PACKAGE_CAPTURE_APP_PRIVATE_KEY` = same Capture Reader PEM |
| demo-app | `PACKAGE_NOTIFY_APP_CLIENT_ID` = same Notify Client ID | `PACKAGE_NOTIFY_APP_PRIVATE_KEY` = same Notify PEM |
| demo-side | Both `PACKAGE_CAPTURE_APP_CLIENT_ID` and `PACKAGE_NOTIFY_APP_CLIENT_ID`, as above | Both matching `PACKAGE_*_APP_PRIVATE_KEY` secrets, as above |
| demo-join | Both `PACKAGE_CAPTURE_APP_CLIENT_ID` and `PACKAGE_NOTIFY_APP_CLIENT_ID`, as above | Both matching `PACKAGE_*_APP_PRIVATE_KEY` secrets, as above |
| packages | None | None |

There must be **three Apps created and installed**, **one App variable and one
App secret in ci-coordinator**, and **two App variables and two App secrets in
each source**. No environment entries are required. The observer and signing
secrets are separate steps in sections 3 and 4; App setup alone is not the
complete CI setup.

The coordinator key has the installation's full authority. Per-step token
narrowing does not reduce what someone holding its PEM can do. Neither source
App may be installed on the feed or another product repository. The notify App
retains a residual ability to cancel coordinator runs/delete artifacts; it has
no publication or signing authority.

If you use the optional local manifest setup page instead of GitHub's manual
form, it saves each App's key privately. You still need to install each App
with the exact selection above and configure the repository entries. The manual
procedure above works without that helper.

### Optional: CLI instead of entering the repository entries in the browser

CLI equivalent, run locally with private keys in an ignored/protected directory:

```sh
gh variable set PACKAGES_APP_CLIENT_ID --repo VOC-Experiments/ci-coordinator --body 'COORDINATOR_CLIENT_ID'
gh secret set PACKAGES_APP_PRIVATE_KEY --repo VOC-Experiments/ci-coordinator < bootstrap-private/coordinator.pem

for repo in demo-core demo-app demo-side demo-join; do
    gh variable set PACKAGE_CAPTURE_APP_CLIENT_ID --repo "VOC-Experiments/$repo" --body 'READER_CLIENT_ID'
    gh secret set PACKAGE_CAPTURE_APP_PRIVATE_KEY --repo "VOC-Experiments/$repo" < bootstrap-private/capture-reader.pem
    gh variable set PACKAGE_NOTIFY_APP_CLIENT_ID --repo "VOC-Experiments/$repo" --body 'NOTIFY_CLIENT_ID'
    gh secret set PACKAGE_NOTIFY_APP_PRIVATE_KEY --repo "VOC-Experiments/$repo" < bootstrap-private/notify.pem
done
```

Replace the three Client ID placeholders; do not use them literally. If you
used the agent-assisted manifest page, its keys are already saved privately and
the agent can configure these repository entries after App installation. If you
used GitHub's manual form, use its downloaded PEM files with the UI or CLI steps
above. No private key needs to be sent through chat.

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

**All repositories is mandatory for the observer PAT in every deployment.**
It includes current and future private repositories automatically. With
**Only select repositories**, a private repository must be explicitly selected
or it is invisible to the observer: its running jobs are ignored entirely in
capacity accounting. This can cause excess admissions and queueing. The CI
cannot independently detect that omission when GitHub provides no private
repository counter. Keep All repositories selected when editing or renewing
the token. This requirement concerns the observer PAT, not the three Apps or
the product allowlist in `ci/projects.json`.

The CI always reads every repository-listing page. It cross-checks repository
counts when supplied, but does not require the optional private counter or
assume a missing counter means zero private repositories. API errors, failed
pages, unknown plans and unknown runner allocations still block admission.

Paste **only the generated token string**, on one line, into
`PACKAGES_OBSERVER_TOKEN`. Do not paste its name, the creation-page URL, an
`Authorization:` header, a shell command, quotes, or a PEM file. Avoid leading
or trailing spaces and line breaks. A runtime error saying **invalid header
field value for Authorization** means the stored token text must be corrected;
it is not proof of a permission failure. The observer fails closed until fixed.

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
committed to the coordinator. Generate usign pairs with `usign -G` as below; do
not hand-serialize them. A locally consistent Ed25519 seed/public check does not
replace an actual usign sign-and-verify check. Feed keys come from the coordinator default branch. Before signing, the capture-pinned key for that family must match the deployed key byte for byte; after an authorized key correction, create fresh captures rather than rewriting old bundles. Re-signing existing rows is a separate operator procedure.

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

## Four-source live diamond setup record

The operator has configured `demo-side` and `demo-join` with the existing capture-reader/notify repository secrets. Their public client-ID variables are set. The coordinator App installation was updated to include all six sandbox repositories: `ci-coordinator`, `packages`, `demo-core`, `demo-app`, `demo-side`, `demo-join`. Actual four-source token minting is checked before activation; the result is tracked in the [live matrix](docs/live-validation.md).

For onboarding, save the coordinator App installation selection **before** adding the source to `ci/projects.json`. Merely setting source secrets does not grant the coordinator access. Capture-reader and notify remain installed on `ci-coordinator` only; the source receives their narrow reader/notify credentials, never the coordinator key. Each new source activates only through its own valid version tag.

The six-repository installation is now verified: [control run 39835348765](https://github.com/VOC-Experiments/ci-coordinator/actions/runs/39835348765) succeeded. Both new source notifications and captures succeeded. The join-first test retained activation while all five rows failed explicitly for missing side publications. The side was then activated, and the moved-root diamond/overlap tests have the bounded proof described above.

## Review correction model

The coordinator validates internal package namespace, version/revision and architecture before signing every own or retained package. OpenWrt 24.10 indexes are regenerated from verified package controls, including retained siblings; 25.12 indexes must cover every verified identity. New publications and independent index/package checks verify complete indexes; actual client installation remains a distinct S2 gap.

The CAS reservation validates the prospective highest requested graph. Stale direct artifacts pass the same dependent arm gate after conversion; terminal failures keep their budgets. A registered child is no longer held by aggregate run lag. Invalid callbacks still allow reconciliation before the run fails. An unobservable capture stays reserved; recovery needs a new valid same-tag push event, not a rerun of the same source run. Failed build/publish jobs remain terminal until an operator acts or a separate new event creates new work.

Do not remove a source with request records: offboarding is out of scope. Source ZIPs have origin/digest/path checks but no expanded-size quota. Availability of orphaned baseline commits is measured separately; no retention mechanism is added. Sandbox-only `live-capacity-check.yml` and demo-side's historical `capacity-probe.yml` are fixtures, excluded from canonical hash comparisons and retained until user-directed cleanup.

All four source hooks were updated to export only their own SDK staging-record files and own provides record, retaining legitimate prerequisite export/import. See the [live matrix](docs/live-validation.md) for current proof and remaining gaps.

The latest reader correction and live evidence are recorded in [the validation matrix](docs/live-validation.md#current-verified-correction). Official OpenWrt client-rootfs tests require the work order's separate S2 approval; package/index validation and real signing alone do not establish installation.

## Trusted ownership and key boundaries

Incoming facts identify only the releasing product; sibling facts come from pinned published entries. Omitted or poisoned sibling facts cannot claim overlapping-prefix binary or SDK files. The one metadata validator requires an expected owner/version and rejects control characters in binary filenames/internal names, before signing. Native staging uses published baseline versions plus the captured own version.

Feed keys come from the current default-branch overlay. The captured signing-family key must equal that authority before signing; otherwise a fresh capture is required. Drain prepared publishers before rotation, and re-sign existing rows through the documented operator procedure. No key rotation occurred in this correction.

Evidence is retained on the development machine under `/tmp/codex/build/snodec/package-ci/review-fixes-20261022T202117Z/`: frozen tests/hashes, red-before regressions, exact live snapshots/artifacts, composite certificate, final audits, accounting and handover. Public run links are in the matrix; no secrets are logged.
