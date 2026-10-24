# Guided bootstrap tool — design proposal

Status: retained design proposal, not implemented tooling. `forge-relay` is a
working command name; neither the project name nor an organization rename is
decided. This proposal does not authorize implementation or GitHub changes.

The goal is one guided setup, followed by ordinary tagged releases. Use `gh`
for GitHub configuration and verification, and `git` for reviewable repository
changes. Keep the existing narrow credential boundaries.

## 1. Start setup locally

```text
forge-relay setup
```

Ask for the deployment owner, coordinator and publication repository names,
local configuration/credential directory, and initial package targets. Start
with Debian; add OpenWrt after the first successful publication.

Detect existing repositories and configuration. Do not overwrite them
automatically. Personal-account deployment is a proposed capability requiring
validation; the currently documented deployment supports an organization.

## 2. Check GitHub access

Check `git`, `gh`, and the current GitHub login. If authentication is missing,
offer `gh auth login`. The browser opens for GitHub authentication; the user
signs in and returns to the terminal. Check access and report missing
permissions before proceeding. Install no missing tools automatically.

## 3. Show the deployment plan

Show the exact repositories, file changes, Apps, variables, and secrets needed.
The user approves the concrete plan. Existing-feed deletion is a separate,
explicit operation; ordinary setup never clears a feed. Existing-system
replacement and old-writer retirement have a separate procedure.

## 4. Create and install the three Apps

Explain each App's purpose, permissions, and repository selection. Open the
relevant GitHub App setup page in the browser. Where supported, an App manifest
supplies the configuration; the user reviews and submits it.

Guide installation on the required repositories. Any manual private-key
download goes into the deployment owner's protected local credential directory.
After each step, verify App identity, permissions, installation scope, and
private-key identity before continuing. Do not collapse the three Apps into a
single broadly privileged source credential.

## 5. Configure the observer token

Open GitHub's fine-grained PAT creation page. Give the exact owner, repository
coverage, read-only permissions, and expiration requirements. The user creates
the PAT and supplies it through a hidden terminal prompt or the indicated
local file. Verify access without displaying or logging the token.

## 6. Configure signing

Offer existing signing keys or preparation of new keys through a separately
approved step. Check that private and public keys match. Configure private keys
as coordinator secrets and prepare public files for publication. A browser is
normally unnecessary. Never silently rotate existing keys.

## 7. Prepare repositories

Use `git` to prepare reviewable configuration changes and `gh` to configure
approved variables and secrets. Present the diff and offer PR creation. Open
the browser only when the user chooses browser review. Merging is an explicit
stage, with the coordinator integrated before its sources.

## 8. Add source projects

```text
forge-relay add-project
```

Ask for a repository, package targets, dependencies, and build-hook template.
Prepare the thin workflow and source-owned package definition. Custom build
commands remain the maintainer's responsibility.

If an App installation needs extending, open that installation's settings in
the browser for the user, then verify the resulting repository selection.

## 9. Verify and activate

```text
forge-relay doctor
```

Check configuration, credential access, signing keys, workflows, and feed
state. Report actionable errors with direct settings links. Distinguish checks
of secret metadata from actual authentication/signing proofs: GitHub secret
contents cannot be read back.

When ready, explain the first activation tag. The user creates it or separately
authorizes the tool to do so. Monitor the release and provide links to real
jobs, status pages, and package directories. Configuration success alone is
not proof of successful builds or installability.

## Resuming and local storage

On rerun, compare saved configuration with actual GitHub state and resume at
the unfinished step. Verify completed steps rather than recreating Apps,
credentials, or repositories. Browser windows need not stay open after a step
is complete; a newly generated PAT must be saved before leaving its result
page because GitHub does not reveal it again.

Keep credentials outside Git, for example in a locally ignored directory:

```text
.local-credentials/
├── SNodeC/
└── VOC-Experiments/
```

Use mode `0700` for directories and `0600` for files. Keep separate credentials
and configuration records for each deployment owner. Never print secrets,
commit them, or upload the credential directory. Keep an encrypted backup;
Git ignore rules are not encryption. Before deleting a temporary checkout,
relocate any credentials stored under it.

## Scope and outstanding design work

Required user interactions on GitHub remain explicit and guided. Automation
prepares, configures, and verifies; it does not bypass authentication, approval,
or permission decisions. Browser opening should be offered, with the same URL
available for users working from a terminal without a local browser.

Before implementation, trace existing setup mechanisms and define the exact
resume record, supported owner types, App-manifest flow, credential handling,
and mutation approvals. This document proposes no new runtime controller,
scheduler, or CI authority. The running CI must not depend on the bootstrap
machine after setup.
