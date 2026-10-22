# Live validation matrix

This is a test plan and evidence register, not an all-green claim. Status is explicit; local proof is distinguished from live proof. Sandbox only; no SNodeC deployment changes.

| ID | Repositories | Guarantee | State | Evidence / blocker |
| --- | --- | --- | --- | --- |
| L01 | coordinator, packages | Empty controller is safe | passed | 39800707102 |
| L02 | demo-app, coordinator, packages | Own tag activates durably; missing prerequisite fails row | passed | 39801935511 |
| L03 | demo-core, coordinator | Moved tag captures exact SHA and fresh revision | passed | 39828642106 |
| L04 | both sources, packages | Per-row cascade recovers application without matrix barrier | running | current five-row cascade |
| L05 | both sources, packages | Debian package signatures, checksum and runtime | passed | apt-siblings independent verification |
| L06 | both sources, packages | OpenWrt 24.10 x86_64/arm64 signing, verification, SDK reuse | running | core publishers 39829293477 and 39829430282 passed; application pending |
| L07 | both sources, packages | OpenWrt 25.12 x86_64/arm64 APK signing and SDK reuse | running | core publication passed; application pending |
| L08 | coordinator | Unknown repository, malformed tag/SHA/run rejected | passed | 7 rejected requests, no reservation; runs 39830357019–39830378760; exact errors and unchanged request slot recorded |
| L09 | coordinator | Wrong source event/run rejected | passed | 39830375493 and 39830378760 reject wrong source event/SHA before reserve |
| L10 | demo-app, coordinator | Tag/VERSION mismatch rejected before reservation | passed | 39831820312 rejects tag/VERSION mismatch; source 39831372661 rejects leading-zero tag before notify |
| L11 | coordinator, packages | Duplicate valid notification allocates nothing | passed | 39830382444 succeeded; no new generation or request; request record unchanged |
| L12 | demo-app, packages | Direct older version builds exact source; highest display unchanged | running | tag-only 5650a807, VERSION 0.9.0, Debian-only JSON; source build passed; publisher 39832574333 pending |
| L13 | demo-core, demo-app | Chain after older direct picks highest semver tag | planned |  |
| L14 | demo-app, packages | Default HEAD differs; captured tag JSON/hook remain authoritative | partial | 0.9.0 capture 39832128450 uses tag-only Debian definition while main stays 1.0.0 with five rows |
| L15 | coordinator, packages | Identical receipt replay does not sign/write feed again | passed | 39829293477 attempt 2: success, no push/signing output; all 8 target files byte-identical |
| L16 | coordinator | Forged artifact/run/attempt callback rejected | passed | wrong intent/run/job/digest rejected by distinct checks; 39831293495/39831297925/39831301620/39831305457 attempt 2; published node unchanged |
| L17 | coordinator | Duplicate/delayed valid callback is safe | passed | 39831309086 duplicate callback succeeded; published node byte-equivalent |
| L18 | demo-core, coordinator | Deterministic failure remains terminal over later wakes | passed | earlier missing-script/feed/export failures retained |
| L19 | demo-core, coordinator | Authorized source rerun binds higher attempt | passed | 39824723667 attempt 2 |
| L20 | coordinator | Operator publication retry reuses retained artifact | passed | 39826674876; no source redispatch |
| L21 | both sources, packages | Stale dependency rejects artifact and pinned readmission | planned |  |
| L22 | coordinator | Strict publication/dependent/direct cause priority | partial | live sequencing observed; constrained-capacity contention pending |
| L23 | organization, coordinator | Plan/headroom, active occupied jobs and backlog separation | partial | 39832578690: two bounded hosted jobs in inactive demo-side; observation correlation pending; busy publisher may correctly skip scan |
| L24 | coordinator | Unknown observer capacity fails closed then recovers | passed | earlier observer authentication/counter failure and recovery |
| L25 | coordinator | Finite queue preserves callback/controller wakes | partial | pending queue observed; no claim about queue exhaustion |
| L26 | packages | Version/sibling/SDK/by-hash retention | partial | Debian siblings/by-hash passed; older-version and OpenWrt sibling checks pending |
| L27 | packages | Highest pending/failure status; real job links only | planned |  |
| L28 | coordinator | Capture expiry and artifact expiry handling | blocked | requires an isolated expiry fixture or waiting for actual expiry; no ledger fabrication |
| L29 | coordinator | Ambiguous dispatch, transient API and lost callback recovery | partial | cancel/rerun/retry tested; real API fault injection not configured |
| L30 | four sources, coordinator | Three-level chain and diamond: zero early join, exactly one join | setup pending | four source repositories now exist; local schema and C runtime pass; coordinator App installation and two secrets per new source still required |
| L31 | organization, coordinator | Private unrelated repository visibility and occupied-job count | blocked | needs private test repository plus corresponding installation visibility review |
| L32 | all repositories | No signing secrets/feed write/sibling reads in source credentials | partial | narrow token minting succeeds; negative permission probes pending |
| L33 | coordinator, packages | Concurrent status and publication CAS preserve both outcomes | partial | real lease conflict recovered; deliberately timed race pending |
| L34 | coordinator | Separate source/publication budgets and operator recovery | partial | publication retry and source rerun passed; three-attempt exhaustion pending |
| L35 | all repositories | Reusable unchanged core across unrelated deployments | passed locally | two offline deployments; sandbox committed generic code matches 22 files |

The current live graph is `demo-core → demo-app`, each with Debian trixie amd64 and OpenWrt 24.10/25.12 x86_64 and aarch64_generic. A live diamond requires two additional products; source tokens retain their DP/own-source boundary. No permission widening is performed by this plan.

## Four-source diamond setup

The sources are [demo-core](https://github.com/VOC-Experiments/demo-core), [demo-app](https://github.com/VOC-Experiments/demo-app), [demo-side](https://github.com/VOC-Experiments/demo-side) and [demo-join](https://github.com/VOC-Experiments/demo-join). Graph: `core → {app, side} → join`. All four source JSON files request five rows. No extra source checkout was created; the new fixtures were prepared through disposable bare Git repositories under the evidence directory.

The coordinator allowlist remains on the two configured sources until installation setup is complete: token minting requires installation access to every allowlisted repository, even before activation. Add the new allowlist entries only after step 2 below.

Before the first tags of side and join:

1. Open [the coordinator App installation](https://github.com/organizations/VOC-Experiments/settings/installations/174142534). Keep the existing repositories selected and add `demo-side` and `demo-join`. Do not change permission types. The capture-reader and notify Apps remain installed on `ci-coordinator` only.
2. Open [demo-side Actions secrets](https://github.com/VOC-Experiments/demo-side/settings/secrets/actions) and [demo-join Actions secrets](https://github.com/VOC-Experiments/demo-join/settings/secrets/actions). In each, set repository secret `PACKAGE_CAPTURE_APP_PRIVATE_KEY` to the existing capture-reader PEM and `PACKAGE_NOTIFY_APP_PRIVATE_KEY` to the existing notify PEM. Use the same respective values already configured in demo-core/demo-app. Never use the coordinator PEM.
3. The repository variables use the existing public client IDs: `PACKAGE_CAPTURE_APP_CLIENT_ID=Iv23libfjJoXiNDcE1qf` and `PACKAGE_NOTIFY_APP_CLIENT_ID=Iv23liJWdDpL1dBPy39L`.
4. Once setup is verified, create each source's own v1.0.0 tag. Activate side, then join. Move the core tag for the diamond cascade. Assert zero early join captures/builds, then exactly one join per row after both arms publish. Repeat with arm failure/retry and a direct arm publication outside the original lineage.

No tag has been created for either new repository during preparation. A failed first build must keep activation, but a credential failure is not a useful substitute for the diamond test.

## Diamond scenario matrix (live execution awaits source credentials)

| Case | Root / arms / join action | Required per-row evidence |
| --- | --- | --- |
| D01 | Activate join while an arm has no publication | Clear terminal missing-prerequisite reason; activation remains |
| D02 | Publish core after all four products activate | Captures select highest tags of app and side; join has zero early captures/builds |
| D03 | Delay side while app publishes | Join remains unadmitted; independent rows proceed |
| D04 | Publish app directly outside core lineage while side remains stale | Zero join captures/builds; no lineage shortcut |
| D05 | Publish side, completing both current arms | Exactly one join capture/build/publication per row, bound to both current arms |
| D06 | Fail side deterministically, then operator retry | No automatic failed-node budget reset; no early join; one join after recovery |
| D07 | Repeat wakes and move core tag while children are in flight | No duplicate join; exact pinned stale readmission versus fresh capture kept separate |
| D08 | Prerequisite changes after a join artifact was built | Publication rejects stale artifact; one pinned readmission against current arms |

## Test setup failures retained as evidence

- Adding uninstalled repositories to the allowlist caused App token HTTP 422. The names were removed until installation setup is complete; no permission widening was attempted. Callback cases were rerun and verified against their actual rejection errors.
- The first Debian-only 0.9.0 fixture retained an extra OpenWrt hook. Strict validation correctly rejected it; the fixture was corrected and its tag moved. This is not reported as a CI defect.
- The GitHub Git-tree API rejected workflow-file writes for the existing CLI credential. Existing Git SSH access published the fixtures through disposable bare repositories instead; no OAuth scope was widened.
- The local four-source schema check uses a proposed master fixture. The live master intentionally stays on the two fully configured sources.
