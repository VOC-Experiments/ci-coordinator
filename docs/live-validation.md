# Live validation matrix

This is a test plan and evidence register, not an all-green claim. Status is explicit; local proof is distinguished from live proof. Sandbox only; no SNodeC deployment changes.

| ID | Repositories | Guarantee | State | Evidence / blocker |
| --- | --- | --- | --- | --- |
| L01 | coordinator, packages | Empty controller is safe | passed | 39800707102 |
| L02 | demo-app, coordinator, packages | Own tag activates durably; missing prerequisite fails row | passed | 39801935511 |
| L03 | demo-core, coordinator | Moved tag captures exact SHA and fresh revision | passed | 39828642106 |
| L04 | both sources, packages | Per-row cascade recovers application without matrix barrier | partial | two-product cascade published all rows; index completeness and signatures now pass; real OpenWrt client installation still awaits S2 |
| L05 | both sources, packages | Debian package signatures, checksum and runtime | passed | apt-siblings independent verification |
| L06 | four sources, packages | OpenWrt 24.10 x86_64/arm64 signing, verification, SDK reuse | partial | fixed indexes contain every IPK, including retained versions; independent raw-index signature/hash/gzip checks pass on both architectures;16 own-only SDK exports checked; real client installation awaits S2 |
| L07 | both sources, packages | OpenWrt 25.12 x86_64/arm64 APK signing and SDK reuse | partial | real APK signing and publisher verification passed; independent index content/install verification remains pending |
| L08 | coordinator | Unknown repository, malformed tag/SHA/run rejected | passed | 7 rejected requests, no reservation; runs 39830357019–39830378760; exact errors and unchanged request slot recorded |
| L09 | coordinator | Wrong source event/run rejected | passed | 39830375493 and 39830378760 reject wrong source event/SHA before reserve |
| L10 | demo-app, coordinator | Tag/VERSION mismatch rejected before reservation | passed | 39831820312 rejects tag/VERSION mismatch; source 39831372661 rejects leading-zero tag before notify |
| L11 | coordinator, packages | Duplicate valid notification allocates nothing | passed | 39830382444 succeeded; no new generation or request; request record unchanged |
| L12 | demo-app, packages | Direct older version builds exact source; highest display unchanged | passed | publisher 39832574333 succeeded; second older lifecycle 39833699291 left all rendered Markdown and highest projection unchanged in 14 samples |
| L13 | demo-core, demo-app | Chain after older direct picks highest semver tag | passed | chain capture 39832292873 selected highest v1.0.0 after direct v0.9.0 publication |
| L14 | app, side, join, packages | Default HEAD differs; captured tag JSON/hook remain authoritative | passed in inspected captures | side child39866493931 and join child39868922328 captured after deliberately divergent main commits; source-pair ZIP/checksums and JSON/hook digests match the tag; earlier initial-capture proof alone was insufficient |
| L15 | coordinator, packages | Identical receipt replay does not sign/write packages again | passed | 39859263723 attempt2 succeeded with a non-empty24.10 index; package files and complete manifest unchanged, no package push; concurrent status commits are separate |
| L16 | coordinator | Forged artifact/run/attempt callback rejected | passed | wrong intent/run/job/digest rejected by distinct checks; 39831293495/39831297925/39831301620/39831305457 attempt 2; published node unchanged |
| L17 | coordinator | Duplicate/delayed valid callback is safe | passed | 39831309086 duplicate callback succeeded; published node byte-equivalent |
| L18 | demo-core, coordinator | Deterministic failure remains terminal over later wakes | passed | earlier missing-script/feed/export failures retained |
| L19 | demo-core, coordinator | Authorized source rerun binds higher attempt | passed | 39824723667 attempt 2 |
| L20 | coordinator | Operator publication retry reuses retained artifact | passed | 39826674876; no source redispatch |
| L21 | both sources, packages | Stale dependency rejects artifact and pinned readmission | planned |  |
| L22 | coordinator | Strict publication/dependent/direct cause priority | passed in bounded window | six-slot window:11 snapshots,3 publisher admissions,0 new build/capture intents while direct work waited; existing jobs were not preempted; exact config restored in1c269c0 |
| L23 | organization, coordinator | Plan/headroom, active occupied jobs and backlog separation | partial | observer 39833080328 attempt 2 counted both inactive demo-side jobs, app and itself; unsaturated observation only, not full admission arithmetic |
| L24 | coordinator | Unknown observer capacity fails closed then recovers | passed | earlier observer authentication/counter failure and recovery |
| L25 | coordinator | Finite queue preserves callback/controller wakes | partial | pending queue observed; no claim about queue exhaustion |
| L26 | packages | Version/sibling/SDK/by-hash retention | partial | Debian siblings/by-hash passed; older-version and OpenWrt sibling checks pending |
| L27 | packages | Highest pending/failure status; real job links only | passed in inspected failure | feed040ae335 renders side1.2.0-r10 failed with its real job link, no older success fallback; ledger/render transaction timing recorded separately |
| L28 | coordinator | Capture expiry and artifact expiry handling | blocked | requires an isolated expiry fixture or waiting for actual expiry; no ledger fabrication |
| L29 | coordinator | Ambiguous dispatch, transient API and lost callback recovery | partial | cancel/rerun/retry tested; real API fault injection not configured |
| L30 | four sources, coordinator | Three-level chain and diamond: zero early join, exactly one join | converged, not certified | all five rows converged under root 39836077535, with six join source admissions; captures/artifacts/publication audit and deliberate scenarios remain pending |
| L31 | organization, coordinator | Private unrelated repository visibility and occupied-job count | blocked | needs private test repository plus corresponding installation visibility review |
| L32 | all repositories | No signing secrets/feed write/sibling reads in source credentials | partial | narrow token minting succeeds; negative permission probes pending |
| L33 | coordinator, packages | Concurrent status and publication CAS preserve both outcomes | partial | real lease conflict recovered; deliberately timed race pending |
| L34 | coordinator | Separate source/publication budgets and operator recovery | partial | publication retry and source rerun passed; three-attempt exhaustion pending |
| L35 | all repositories | Reusable unchanged core across unrelated deployments | passed locally | two offline deployments; sandbox committed generic code matches 22 files |

The current live graph is `demo-core → {demo-app, demo-side} → demo-join`, with Debian trixie amd64 and OpenWrt 24.10/25.12 x86_64 and aarch64_generic. Source tokens retain their coordinator/own-source boundary. All six repositories are configured; installation minting and both new source notification paths succeeded.

## Four-source diamond setup

The sources are [demo-core](https://github.com/VOC-Experiments/demo-core), [demo-app](https://github.com/VOC-Experiments/demo-app), [demo-side](https://github.com/VOC-Experiments/demo-side) and [demo-join](https://github.com/VOC-Experiments/demo-join). Graph: `core → {app, side} → join`. All four source JSON files request five rows. No extra source checkout was created; the new fixtures were prepared through disposable bare Git repositories under the evidence directory.

The coordinator allowlist now contains all four sources. Setup below has been completed and verified by control run 39835348765; token minting requires installation access to every allowlisted repository, even before activation.

Before the first tags of side and join:

1. Open [the coordinator App installation](https://github.com/organizations/VOC-Experiments/settings/installations/174142534). Keep the existing repositories selected and add `demo-side` and `demo-join`. Do not change permission types. The capture-reader and notify Apps remain installed on `ci-coordinator` only.
2. Open [demo-side Actions secrets](https://github.com/VOC-Experiments/demo-side/settings/secrets/actions) and [demo-join Actions secrets](https://github.com/VOC-Experiments/demo-join/settings/secrets/actions). In each, set repository secret `PACKAGE_CAPTURE_APP_PRIVATE_KEY` to the existing capture-reader PEM and `PACKAGE_NOTIFY_APP_PRIVATE_KEY` to the existing notify PEM. Use the same respective values already configured in demo-core/demo-app. Never use the coordinator PEM.
3. The repository variables use the existing public client IDs: `PACKAGE_CAPTURE_APP_CLIENT_ID=Iv23libfjJoXiNDcE1qf` and `PACKAGE_NOTIFY_APP_CLIENT_ID=Iv23liJWdDpL1dBPy39L`.
4. Once setup is verified, create each source's own v1.0.0 tag. Activate side, then join. Move the core tag for the diamond cascade. Assert zero early join captures/builds, then exactly one join per row after both arms publish. Repeat with arm failure/retry and a direct arm publication outside the original lineage.

No tag has been created for either new repository during preparation. A failed first build must keep activation, but a credential failure is not a useful substitute for the diamond test.

## Diamond scenario matrix (prior convergence; independent recertification pending)

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
- The local four-source schema check uses a proposed master fixture. The master was expanded to four sources after the operator confirmed installation and secret setup.

Operator confirmed installation setup on 22 October 2026. Both new repositories expose the expected secret names and client-ID variables. Actual token minting and source callbacks are verified by their first live tag runs; secret values are never read back or logged. The missing-arm test intentionally activates join before side.

## Historical setup failure (resolved)

Operator supplied both source secret names (metadata verified), but [control run 39834797076](https://github.com/VOC-Experiments/ci-coordinator/actions/runs/39834797076) still failed coordinator App-token minting with HTTP 422: at least one requested repository is inaccessible to the parent installation. Client ID is the expected `Iv23liMgaVixcN2WcIoU`. The master was returned to the two configured sources to preserve operation. Neither new source has an activation tag.

The operator resolved this by opening [coordinator App installation 174142534](https://github.com/organizations/VOC-Experiments/settings/installations/174142534), and selecting both `demo-side` and `demo-join` in addition to the existing four repositories, then saving. This is the coordinator App, not the capture-reader or notify App. No permission types or PAT scope need changing.

The completed older-tag lifecycle was sampled 14 times: notification/pending/publishing/published. All rendered Markdown blobs and highest display projection stayed identical; raw ledger and publication advanced. Source run/build and publication completed normally.

The operator subsequently confirmed saving the coordinator App repository selection for both new sources. The allowlist is restored to four sources for a fresh token-minting verification, followed by missing-arm activation and diamond execution. The prior HTTP 422 record remains historical evidence.

## Verified four-source setup and D01

[Control run 39835348765](https://github.com/VOC-Experiments/ci-coordinator/actions/runs/39835348765) passed after the installation update. Source notifications and captures passed for join and side, proving their reader/notify credentials authenticate. D01 passed via capture 39835546673: five `unsatisfiable`/`blocked` nodes naming missing demo-side, no admitted source request, activation still eligible. Side activation capture is 39835779276. The overlapping moved-root capture is 39836077535, pinned to core commit 89852e2e8bc4b7f78abcb0fda75b58417b4596a0.

The external auditor checks every actual join build at `request.publication`, independently reconstructing identity fingerprints from exact sources, revisions and owned file hashes. Both arm nodes must be bound to that baseline. It retains raw snapshots and records each admission. This is sandbox test tooling, not a new CI controller or state store. Existing capture nodes may predate a newer root publication; their build admission must still wait after the baseline changes.

## Independent review, 22 October 2026

Verdict: **changes required**, not whole-system acceptance. Confirmed blocker:
OpenWrt 24.10 indexes contain two newline bytes and no package entries. Usign
verification proves the signature, not completeness or installability. The
publication deletion/reindex boundary is under investigation. Other findings
cover OpenWrt metadata validation, the arm gate after stale direct-work
conversion, concurrent graph validation and public-key authority. Offboarding
semantics remain outside scope.

The external live auditor currently checks join source admission against pinned
feed identities and arm bindings. Five admissions have passed; that does not
certify zero early captures, exact-once joins or publication-time correctness.
Those gaps remain explicit. All four Debian packages were downloaded at one feed
commit, checked against manifest SHA-256, extracted without installation and run:
core 42; app uses core 42; side 43; join core 42, side 43.

Actual negative captures rejected an unsupported distro (39837395135), a
self-cycle (39837331084), and an unknown registered dependency (39837323639).
The side v0.9.0 two-row capture published trixie and closed bookworm with a
missing-core reason. These lower test tags do not replace the highest graph.

## Review correction and new evidence requirements

The fixed coordinator is byte-identical to the locally verified canonical production files (configuration, keys, site content and sandbox-only workflows excluded). The frozen offline run passed285 tests (284 passed, one missing-OpenWrt-tools skip), plus28 additional checks and22 static checks. It includes25 review methods, including the reproduced IPK control-paragraph injection regression. These counts do not prove live client installability.

| ID | Scope | Current outcome |
| --- | --- | --- |
| L36 | Namespace spoof, lower fixture tags; Debian/RPM/opkg/APK | Passed: six real publisher rejections for core v0.7.43; package manifests unchanged (RPM subtree stays absent). Join v0.7.42 wrong-version artifact also rejected. Extra control-paragraph rejection is a new reader regression. |
| L37 | Feed public keys versus deployed default-branch authority | Offline key-regression checks pass; verify after each new publication |
| L38 | Registered child while parent aggregate run lags | Offline public tick regression passes; live observation pending |

D02–D08 require deliberate sequencing and an independent audit of held capture intents, child builds, raw arm facts, artifact contents and exact publisher snapshots. Prior convergence is not exactly-once certification. The auditor includes duplicate and stale-arm negative self-tests. Local mocks do not certify real signatures or package installation. Official disposable OpenWrt client rootfs tests need the work order's separate S2 approval; run/artifact deletion, forced budget exhaustion and new permissions need S3.

Read-only observer accounting reports actual API commands/rate limits separately from the coordinator's static cost formula. N5 retains an unobservable request and its commitments; a new verified source push for the same tag replaces the request through CAS. A 404 alone never proves absence. N10 probes baseline commits by exact SHA and measured age, without changing the accepted parentless writer.

## Verified reader follow-up

The trusted reader now rejects malformed controls and extra body paragraphs; one IPK cannot inject an unvalidated second index entry. Both publisher-boundary subtests failed before the predicate correction; all16 inspected real SDK IPKs are accepted by the actual reader. This adds one net canonical production line to the approved correction. Earlier sandbox generations retain their captured tooling; the new deployment is recorded separately from7cd30df and its config-only descendants.

The first side1.2 source rerun succeeded, but its original row was superseded by a fresh capture after a concurrent framework baseline change. This is not called isolated operator-only recovery. The next D06 fixture keeps the framework steady; the later D03/D04 fixture holds only one cascade arm while independent rows continue. No CI controller timer or ledger field is added.

The first capacity fixture put capacity at the top level and was rejected before ledger processing. It was restored, then settings.capacity=6 was validated and tested for eight minutes, then restored byte for byte. Those failures remain evidence rather than being counted as passing contention checks.

Existing sandbox-only live-capacity-check.yml now instruments the actual capacity function with REST call counts, elapsed time and shared-PAT rate observations. It remains a fixture excluded from canonical code identity, and still asserts both unrelated probe jobs are counted. No parallel observer or permission change is introduced.
