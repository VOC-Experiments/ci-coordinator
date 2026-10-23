# Live validation matrix

This is a test plan and evidence register, not an all-green claim. Status is explicit; local proof is distinguished from live proof. Sandbox only; no SNodeC deployment changes.

| ID | Repositories | Guarantee | State | Evidence / blocker |
| --- | --- | --- | --- | --- |
| L01 | coordinator/packages | Empty controller safe | passed, retained | 39800707102; empty-feed local CAS guard |
| L02 | app/coordinator/packages | Own activation/missing prerequisite | passed, retained | 39801935511; durable request and row failure |
| L03 | core/coordinator | Moved tag exact SHA/fresh revision | passed | 39828642106 and moved Core39878350568; immutable old bundles |
| L04 | four sources/packages | Per-row cascade and useful feed | passed scheduling and x86_64 clients | All five rows converge; signed feed/index evidence and both x86_64 client installations/runtime pass. No aarch64 runtime claim. |
| L05 | four sources/packages | Debian signatures/checksum/runtime | passed in sampled Debian feed | Downloaded/extracted four binaries:42,42,43,42+43; no host installation |
| L06 | four sources/packages | 24.10 signing/membership/SDK reuse | passed x86_64 client; aarch64 runtime untested | Official 24.10.8 x86_64: opkg signature check,4 exact package installs and runtime pass;6 installed payload hashes match IPKs. Both architecture indexes/IPK controls and import checks passed; fixtures may rebuild prerequisites. No aarch64 execution. |
| L07 | four sources/packages | 25.12 APK signing/reuse | passed x86_64 client; aarch64 runtime untested | Official 25.12.5 x86_64: signed-index APK update/add,4 exact package installs/runtime pass;6 installed payload hashes match APK metadata. Both APK index signatures and 11 identities per architecture verified; no aarch64 execution. |
| L08 | coordinator | Malformed/unknown intake | passed, retained | Seven exact rejection errors/no reservation,39830357019–39830378760 |
| L09 | coordinator | Wrong source event/run | passed, retained | 39830375493/39830378760 reject before reserve |
| L10 | app/coordinator | Strict tag/VERSION | passed, retained | 39831820312 mismatch;39831372661 rejects leading zero |
| L11 | coordinator/packages | Duplicate notification | passed, retained | 39830382444 no new generation/slot/allocation |
| L12 | app/packages | Older direct/highest display | passed | 39832574333/39833699291,14 lifecycle snapshots preserve visible highest bytes |
| L13 | core/app | Highest chain after older direct | passed | 39832292873 chooses highest; later multi-version audit preserves cause distinction |
| L14 | app/side/join | Tag differs from main by real digests | passed for inspected captures | Side39866493931/Join39868922328 captured after sentinel main; ZIP JSON/hook/source digests match tag. Healthy main restored afterwards |
| L15 | coordinator/packages | Non-empty replay no package write | passed | 39859263723 attempt2, full manifest/files unchanged; authored refresh/status commits separate |
| L16 | coordinator | Forged callback | passed, retained | Intent/run/job/digest negatives39831293495/39831297925/39831301620/39831305457 attempt2 |
| L17 | coordinator | Delayed/duplicate callback | passed, retained | 39831309086 preserves published node; offline wake-on-rejection guard |
| L18 | sources/coordinator | Terminal retention | passed | Wrong-version Join failed artifact stays byte-identical after new Core event; no budget reset |
| L19 | sources/coordinator | Authorized source rerun | passed | 39824723667 attempt2; Side39881285597 attempt2 operator recovery |
| L20 | coordinator | Publication retry artifact reuse | passed, retained | 39826674876 no source redispatch |
| L21 | core/arms/join | Stale work gate/pinned recovery | passed in bounded live sequence and offline | live-stale-conversion-proof; terminal negative; independent raw baseline audit; direct still presence-only |
| L22 | coordinator | Strict cause priority | passed in bounded window | Capacity6:11 observations/3publisher/0newbuildcapture, exact config restored1c269c0 |
| L23 | organization/coordinator | Org capacity/occupied/backlog | partial | Observer39871717858 counts2unrelated jobs;35endpoint invocations/12.273478893s. Full saturation/private/pool arithmetic not certified |
| L24 | coordinator | Unknown capacity fails closed/recovery | passed, retained | Earlier observer auth/private-counter failure and fixed recovery |
| L25 | coordinator | Finite queue wake retention | partial | Pending queue observed; overflow/exhaustion not forced |
| L26 | packages | Siblings/versions/SDK/by-hash | passed sampled retention/indexes and x86_64 clients | Both 24.10 rows retain all 4 products/versions; both 25.12 signed indexes match all 11 package controls per architecture. SDK own-only and Debian by-hash evidence retained. Actual opkg/APK clients select highest versions; aarch64 runtime untested. |
| L27 | packages | Highest failure visible | passed in inspected failure | 040ae335 shows highestSide1.2-r10 failure/real job link, no older fallback; render transaction lag qualified |
| L28 | coordinator | Expiry/uncertain run | blocked for live deletion/expiry injection | 404/403 preservation and new-event recovery proven offline; no live deletion without S3 |
| L29 | coordinator | Ambiguity/transient/lost callback | partial | Rerun/recovery exercised; actual dispatch transport fault injection needs S3 |
| L30 | four sources/coordinator | Diamond capture/build/publication | certified for deliberately sequenced row; sampled others | composite-certified: zero early joins,1freshcapture/1source/1publication after outside-lineage App and failed Side/operator retry; full raw/artifact audits |
| L31 | organization | Private unrelated visibility | blocked | No private fixture/permission setup authorized |
| L32 | all sources | Least-privilege source boundary | partial | Narrow token minting/workflow contract succeeds; no new permission-negative probes without S3 |
| L33 | coordinator/packages | Status/publication/graph CAS | partial live; passed offline | Real lease conflict recovery; actual-shell concurrent graph negatives offline; no deliberate live highest-graph race |
| L34 | coordinator | Separate budgets/operator | partial | Operator source/publication recovery passes; forced exhaustion not authorized |
| L35 | both offline deployments/sandbox | Reusable same coordinator | passed locally and deployed hash identity | 288-test final suite;22 identical generic hashes across SNodeC/ExampleOrg/final sandbox |
| L36 | core/coordinator/packages | Namespace spoof every format | passed six real publisher negatives | Corev0.7.43 capture 39879842831, Debian/RPM/opkgx2/APKx2; exact push trees only status/presentation changes. Executed1491260; additional filename guard offline/e86 |
| L37 | coordinator/packages | Current key authority | passed sampled key identities plus offline rotation regression | Every inspected exact publication snapshot matches all 3 authority keys; family mismatch fails before signing; no rotation performed |
| L38 | coordinator/child sources | Registered child during aggregate lag | passed offline; live aggregate lag not observed | Public tick regression passes. Three parent-running ledger samples were observation lag: parent API updated_at precedes child creation by22–29seconds; no positive aggregate-lag claim |

The current live graph is `demo-core → {demo-app, demo-side} → demo-join`, with Debian trixie amd64 and OpenWrt 24.10/25.12 x86_64 and aarch64_generic. Workflow configuration limits source readers to coordinator/own-source paths. Negative permission/private-visibility probes remain partial (L32); readers can access other captures held by the coordinator. All six repositories are configured; installation minting and both new source notification paths succeeded.

## Historical four-source diamond setup

The sources are [demo-core](https://github.com/VOC-Experiments/demo-core), [demo-app](https://github.com/VOC-Experiments/demo-app), [demo-side](https://github.com/VOC-Experiments/demo-side) and [demo-join](https://github.com/VOC-Experiments/demo-join). Graph: `core → {app, side} → join`. All four source JSON files request five rows. No extra source checkout was created; the new fixtures were prepared through disposable bare Git repositories under the evidence directory.

The coordinator allowlist now contains all four sources. Setup below has been completed and verified by control run 39835348765; token minting requires installation access to every allowlisted repository, even before activation.

Before the first tags of side and join:

1. Open [the coordinator App installation](https://github.com/organizations/VOC-Experiments/settings/installations/174142534). Keep the existing repositories selected and add `demo-side` and `demo-join`. Do not change permission types. The capture-reader and notify Apps remain installed on `ci-coordinator` only.
2. Open [demo-side Actions secrets](https://github.com/VOC-Experiments/demo-side/settings/secrets/actions) and [demo-join Actions secrets](https://github.com/VOC-Experiments/demo-join/settings/secrets/actions). In each, set repository secret `PACKAGE_CAPTURE_APP_PRIVATE_KEY` to the existing capture-reader PEM and `PACKAGE_NOTIFY_APP_PRIVATE_KEY` to the existing notify PEM. Use the same respective values already configured in demo-core/demo-app. Never use the coordinator PEM.
3. The repository variables use the existing public client IDs: `PACKAGE_CAPTURE_APP_CLIENT_ID=Iv23libfjJoXiNDcE1qf` and `PACKAGE_NOTIFY_APP_CLIENT_ID=Iv23liJWdDpL1dBPy39L`.
4. Once setup is verified, create each source's own v1.0.0 tag. Activate side, then join. Move the core tag for the diamond cascade. Assert zero early join captures/builds, then exactly one join per row after both arms publish. Repeat with arm failure/retry and a direct arm publication outside the original lineage.

No tag has been created for either new repository during preparation. A failed first build must keep activation, but a credential failure is not a useful substitute for the diamond test.

## Diamond scenario matrix — inspected evidence

| Case | State | Evidence and limit |
| --- | --- | --- |
| D01 | passed, retained | Join39835546673,5missing-Side terminal rows, activation kept |
| D02 | passed for inspected fixed sequence | Core39878350568,highest App/Side pins; raw capture/build audit |
| D03 | passed | Side20-minute hold; zero early Join; independent rows publish |
| D04 | passed | App39881613016 outside Core lineage publishes inside Side hold; zero Join captures/builds |
| D05 | passed | After Side recovery: exactly1Joincapture 39885172814/source 39885255474/publisher39886643960; raw resolved arms/ZIP/receipt checked |
| D06 | passed | Failed source 39881285597 attempt1; one operator rerun attempt2, old budgets retained, one Join after publish |
| D07 | passed for sampled moved-root/stale-recovery sequences | Fresh captures versus pinned re-admissions independently classified; no universal timing/exact-once claim outside observed identities |
| D08 | passed offline; live gate subclaim not certified | Mandatory publication arm gate negative passes offline. Old publisher39861949839 attempt2 is receipt no-op, not gate reach; natural stale-identity live rejection separately recorded |

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

## Historical four-source setup and D01

[Control run 39835348765](https://github.com/VOC-Experiments/ci-coordinator/actions/runs/39835348765) passed after the installation update. Source notifications and captures passed for join and side, proving their reader/notify credentials authenticate. D01 passed via capture 39835546673: five `unsatisfiable`/`blocked` nodes naming missing demo-side, no admitted source request, activation still eligible. Side activation capture is 39835779276. The overlapping moved-root capture is 39836077535, pinned to core commit 89852e2e8bc4b7f78abcb0fda75b58417b4596a0.

The initial external auditor checked join builds against coordinator-derived identity fingerprints. That evidence was insufficient to certify captures, exactly-once behavior or publication-time correctness. The independent raw-manifest and package-byte audits in the current correction supersede that limited conclusion; all earlier evidence remains.

## Historical independent review, 22 October 2026

Verdict: **changes required**, not whole-system acceptance. Confirmed blocker:
OpenWrt 24.10 indexes contain two newline bytes and no package entries. Usign
verification proves the signature, not completeness or installability. The
publication deletion/reindex boundary is under investigation. Other findings
cover OpenWrt metadata validation, the arm gate after stale direct-work
conversion, concurrent graph validation and public-key authority. Offboarding
semantics remain outside scope.

At that review, the external live auditor checked join source admission against pinned
feed identities and arm bindings. Five admissions had passed; that does not
certify zero early captures, exact-once joins or publication-time correctness.
Those gaps remain explicit. All four Debian packages were downloaded at one feed
commit, checked against manifest SHA-256, extracted without installation and run:
core 42; app uses core 42; side 43; join core 42, side 43.

Actual negative captures rejected an unsupported distro (39837395135), a
self-cycle (39837331084), and an unknown registered dependency (39837323639).
The side v0.9.0 two-row capture published trixie and closed bookworm with a
missing-core reason. These lower test tags do not replace the highest graph.

## Historical intermediate correction evidence

The fixed coordinator is byte-identical to the locally verified canonical production files (configuration, keys, site content and sandbox-only workflows excluded). The frozen offline run passed285 tests (284 passed, one missing-OpenWrt-tools skip), plus28 additional checks and 22 static checks. It includes25 review methods, including the reproduced IPK control-paragraph injection regression. These counts do not prove live client installability.

| ID | Scope | Current outcome |
| --- | --- | --- |
| L36 | Namespace spoof, lower fixture tags; Debian/RPM/opkg/APK | Passed: six real publisher rejections for core v0.7.43; package manifests unchanged (RPM subtree stays absent). Join v0.7.42 wrong-version artifact also rejected. Extra control-paragraph rejection is a new reader regression. |
| L37 | Feed public keys versus deployed default-branch authority | Offline key-regression checks pass; verify after each new publication |
| L38 | Registered child during aggregate lag | Passed offline only; three ledger samples were observation lag, with parent API completion 22–29seconds before child creation. No positive live aggregate-lag claim. |

D02–D08 require deliberate sequencing and an independent audit of held capture intents, child builds, raw arm facts, artifact contents and exact publisher snapshots. Prior convergence is not exactly-once certification. The auditor includes duplicate and stale-arm negative self-tests. Local mocks do not certify real signatures or package installation. At that intermediate stage S2 approval was pending; the approved client results below supersede that gap. Run/artifact deletion, forced budget exhaustion and new permissions still need S3.

Read-only observer accounting reports actual API commands/rate limits separately from the coordinator's static cost formula. N5 retains an unobservable request and its commitments; a new verified source push for the same tag replaces the request through CAS. A 404 alone never proves absence. N10 probes baseline commits by exact SHA and measured age, without changing the accepted parentless writer.

## Historical reader follow-up

The trusted reader now rejects malformed controls and extra body paragraphs; one IPK cannot inject an unvalidated second index entry. Both publisher-boundary subtests failed before the predicate correction; all16 inspected real SDK IPKs are accepted by the actual reader. This adds one net canonical production line to the approved correction. Earlier sandbox generations retain their captured tooling; the new deployment is recorded separately from7cd30df and its config-only descendants.

The first side1.2 source rerun succeeded, but its original row was superseded by a fresh capture after a concurrent framework baseline change. This is not called isolated operator-only recovery. The next D06 fixture keeps the framework steady; the later D03/D04 fixture holds only one cascade arm while independent rows continue. No CI controller timer or ledger field is added.

The first capacity fixture put capacity at the top level and was rejected before ledger processing. It was restored, then settings.capacity=6 was validated and tested for eight minutes, then restored byte for byte. Those failures remain evidence rather than being counted as passing contention checks.

Existing sandbox-only live-capacity-check.yml now instruments the actual capacity function with REST call counts, elapsed time and shared-PAT rate observations. It remains a fixture excluded from canonical code identity, and still asserts both unrelated probe jobs are counted. No parallel observer or permission change is introduced.

## Historical intermediate evidence, 23 October 2026

Publisher ownership regressions include omitted sibling facts, a poisoned historical sibling namespace, foreign SDK filenames and a missing expected-version owner. Valid own publication succeeds while foreign files are excluded and sibling entries remain unchanged. The final287-test offline run passed286 tests with one missing-OpenWrt-tools skip;28 runner checks and 22 static checks also passed. Evidence is kept under `review-fixes-20261022T202117Z/owner2-*` on the development machine.

Observer measurement run39871717858 issued35 endpoint invocations in12.273478893 seconds and counted both unrelated capacity-probe jobs. The shared PAT rate counters changed by32; that is not equated to invocation count or total reconciliation cost. This is a bounded sandbox observation, not a universal plan/rate guarantee.

A separate deliberately sequenced Core-move/direct-App/failed-Side/operator-rerun test follows. Earlier direct Side failures and convergence are retained but are not relabeled as the required failed in-cascade arm proof. No run cancellation, ledger repair, permission change or credential rotation is involved.

## Current verified correction

**Changes complete for the tested scope (23 October 2026); no production go-live claim.**
The empty OpenWrt 24.10 index defect is corrected: indexes now derive from verified own and retained package controls. Both architecture indexes, raw signatures, every indexed IPK checksum/size and control identity were independently checked. Live negatives cover internal-name spoofs across Debian/RPM/opkg/APK; version and architecture negatives are offline tests (APK controls synthetic). Approved S2 tests now prove signed-feed installation and runtime of all four products in official OpenWrt 24.10.8 and 25.12.5 x86_64 containers. The aarch64 rows have metadata/index evidence; native aarch64 installation and execution remain untested.

The deliberately held/failed-arm diamond passed: direct App published outside Core lineage while Side was stale, with zero early Join captures/builds. One operator Side rerun was followed by exactly one Join capture 39885172814, source 39885255474 and publication. The final raw admission audit covers89 generations / 114 observations with zero errors;37 Join artifact/publication records were inspected with zero errors. Auditors use raw sources, revisions and owned checksums, including duplicate/stale negative self-tests. Counts are bounded evidence, not a universal timing claim.

The final frozen offline suite ran 288 tests: 287 passed, zero failures/errors, one skipped because local OpenWrt signer tools are absent. All 28 runner and 22 static checks passed. Both complete unrelated offline deployments and the deployed coordinator match 22 generic files. No new CI state/schema/controller/workflow/permission was introduced.

Healthy current source hooks are restored after the deliberate fixtures. Side v1.3.0@ccd1ff10e3f079dc3d3b327b34e966dae8977df8 capture 39889290108 published all five rows; exactly one corresponding healthy Join child per row published on final coordinator code e86bbe8. Previous tag commits, failed runs, bundles and negative fixtures remain immutable evidence. See the [item-by-item live matrix](live-validation.md) for partial/blocked cases and the exact scope.

The shared reader/validator rejects malformed control paragraphs and control characters in own/retained package identities. Public-key overlay, fresh prospective CAS graph validation, terminal retention, observation uncertainty and source credential boundaries are preserved. The earlier six live namespace negatives ran on 1491260; the last one-line filename guard was additionally reproduced/fixed offline and deployed on e86bbe8. No malformed live index was created.

S2 image/client work is approved and completed for the stated x86_64 scope. S3 destructive/exhaustion/permission experiments remain unapproved. Do not interpret partial/blocked rows as passed. The D08 operator rerun returned an identical-receipt no-op; publication arm-currency rejection is mandatory offline proof, not a claimed live gate reach. The source fixtures and capacity setting are restored; no SNodeC external change occurred.

## OpenWrt client installation proof

The user approved S2 on 23 October 2026. Both official SHA-verified x86_64 root filesystems installed all four products directly from the signed feed frozen at `9bc93ab2a8c88c43c581cbb8f75bb969b5f7e94d`:

| Product | OpenWrt 24.10.8 / opkg | OpenWrt 25.12.5 / APK |
| --- | --- | --- |
| demo-core | 1.1.0-r10 | 1.1.0-r10 |
| demo-app | 1.2.0-r26 | 1.2.0-r26 |
| demo-side | 1.3.0-r19 | 1.3.0-r19 |
| demo-join | 1.1.0-r29 | 1.1.0-r30 |

Each client ran all four installed programs and produced exactly:

```text
demo-core 42
demo-app uses core 42
demo-side 43
demo-join core 42, side 43
```

`opkg` used `option check_signature` and reported `Signature check passed.` APK used only the sandbox public key directory and frozen repository; native `apk verify` also verified both architecture indexes. No untrusted/signature or TLS bypass was used. No upstream dependency feed was needed: the official rootfs already contained base dependencies.

The certificate covers 2 client cases,8 package installs,8 runtime outputs and12 installed executable/library SHA256 comparisons. Both APK indexes contain exactly 11 verified identities each: internal owner/version/architecture, archive SHA256, file size and dependencies match the frozen manifest/native package metadata. Installed x86_64 file hashes match their published IPK data or APK file metadata. The APK repository index is signed; standalone unsigned APK extraction correctly rejects without a bypass. This is not a failure of signed-repository installation.

Architecture limits: no aarch64 emulation was installed. The aarch64 APK index/control/archive checks pass; native installation/execution and APK ELF extraction are not claimed. Earlier IPK architecture/extraction evidence remains separate. This closes the x86_64 client gap, not every S3/private/fault/queue hypothesis in the matrix.

Tests used existing rootless Podman 5.8.6 with dedicated storage/runroot/tmp under `/tmp/codex/build/snodec/package-ci/review-fixes-20261022T202117Z/s2-clients-20261023T062911Z/`. Containers were disposable, unprivileged and removed on exit; images/logs/storage remain for review. No host packages, signing keys, permissions, source tags, CI code or SNodeC external state changed. The initial boot-directory/BusyBox/heredoc harness failures and exact package-proof qualifications are retained beside `certificate.json`; they are not CI defects. The pre-existing 288-test suite was not rerun for container/documentation-only work.

## Prepared boundary-fix retest (not yet executed)

The proposed shared correction adds four production lines: rerun the existing SDK import conflict check after `compile`,
and require the artifact directory inventory to equal the checksum manifest plus `build.json` before publication.
The SDK check rejects changed bytes/links; missing ordinary files are restored, and byte-identical rebuilds pass.
It does not certify that the dependent avoided a prerequisite rebuild. Source hooks must suppress such rebuilds.

| Case | Preparation and pass criteria | Current status |
| --- | --- | --- |
| BF01 | Permanent real `.tar.zst` import tests: unchanged/path rewrites, changed bytes, links/type, missing-file repair | Passed locally: 292 tests, 291 passed, one host signer skip |
| BF02 | Publisher boundary: extra file/package/nested/hidden/link rejected; flat and nested RPM inventories admitted | Passed locally: 292 tests, 291 passed, one host signer skip |
| BF03 | Fresh tagged dependent builds on 24.10 and 25.12 x86_64; post-compile check, receipt, signed index and payload evidence | Not run |
| BF04 | Lower-tag negative appends an undeclared harmless file after stage; publisher rejects before package/index changes | Not run |

A failed negative publication can update the execution ledger and rendered failure status. Acceptance requires unchanged
package manifests, indexes, signatures and package payloads, rather than an unchanged whole feed ref.
All SNodeC GitHub repositories, production tags and feeds are outside this sandbox retest.

## Revision-sharing and recovery validation (current stage)

All new cases below are pending live evidence until their run/capture/artifact identities are recorded. SNodeC GitHub remains untouched. Coordinator tooling remains constant during each live wave.

| ID | Scope | Expected | State |
|---|---|---|---|
| R01 | callback/control | One verified source-pair download per capture in one callback+tick pass | local regression passed; live pending |
| R02 | core→app/side→join, five rows | Matching fresh cascade provenance shares row revisions, with zero early or duplicate joins | pending |
| R03 | older core direct tag | Exact requested source publishes; highest display unchanged; no cascade | pending |
| R04 | identical publisher replay | No signing/package/index/receipt mutation | pending |
| R05 | older app direct, then framework move | Exact older direct; subsequent chain selects highest app tag; matching rows share where eligible | pending |
| R06 | failed highest source and repaired moved tag | Failure remains visible; old failure/budgets retained; new valid event recovers and cascades | pending |
| R07 | artifact/feed audit | Controls, namespace, row revisions, signatures/checksums and actual package payloads agree | pending |
| R08 | delivered schedule and empty-input wake | Backoff respected; automatic schedule observed separately from operator recovery | pending |

The ten-minute cron is staggered to UTC minutes 3,13,23,33,43,53. It is best effort. No external scheduler, self-trigger loop, extra retry authority or bound on GitHub wake delivery is claimed. Existing schedules show long gaps; comparing the offset requires a quiet observation window and is not certified by a few live samples.
