# Source integration contract

The coordinator's [bootstrap README](../README.md) gives complete credential and
first-deployment steps. This file describes what a product repository owns.

A source has root `VERSION`, `ci/packages.json`, packaging hooks, and the thin
`.github/workflows/build-distribution-packages.yml` wrapper. The **selected tag's
exact commit** owns all four. No branch HEAD or previous published source is
substituted.

Example definition:

```json
{
  "title": "Demo application",
  "package": "demo-app",
  "depends_on": ["demo-core"],
  "build": {
    "native": "ci/package/native.sh",
    "openwrt": "ci/package/openwrt.sh"
  },
  "matrix": {
    "linux": [
      {
        "distribution": "debian",
        "suite": "trixie",
        "image": "debian:trixie",
        "architectures": ["amd64"]
      }
    ],
    "openwrt": {
      "releases": ["24.10.8", "25.12.5"],
      "targets": {"x86_64": "x86/64", "aarch64_generic": "armsr/armv8"}
    }
  }
}
```

`depends_on` references permitted repository basenames. Namespace `package` must
be unique and valid. Definitions validate rows, hooks, supported tooling,
registered dependencies and cycles. The master allowlist does not duplicate
this matrix, graph or build commands.

Native hooks run inside the target distribution against captured source and
already verified prerequisite packages. They receive `BUILD_PROJECT`,
`DISTRIBUTION`, `SUITE`, `ARCH` and `PACKAGE_RELEASE`. Write packages under
`/work/packages`, plus `<package>.packages` listing the package component names.
Versions/architectures/names are checked from package metadata against the
captured version, revision and ownership. Product-specific prerequisites and
build commands belong in the source hook. CPack is optional; demo sources use
GCC/dpkg without CMake.

OpenWrt hooks run from the captured archive in the selected SDK, supply the
recipe and `compile()` function, and use the existing `sdk-export` contract for
development files needed by dependents. A dependent imports the matching
published SDK export, with identity/checksum verification. Hooks must not rebuild or replace imported
prerequisites; suppress `package/feeds/package_ci/<dependency>/compile` in their `make` command.
The post-compile import conflict check rejects changed bytes/links; missing ordinary files are restored.
Byte-identical rebuilds pass, so this check alone does not prove that no rebuild occurred. Source jobs never
sign packages or acquire feed write/signing credentials.

The source wrapper calls this deployment's `notify-release.yml@main` on tag
push and `build-packages.yml@main` on coordinator workflow dispatch. It forwards
only the capture-reader and notify secrets. The notification includes the full
JSON and source run/tag/SHA. Intake verifies those claims before durable
activation/reservation. Until its own valid notification a source is inactive.

To add another supported product: add its basename to the allowlist, commit its
own definition/hooks/wrapper/VERSION, grant its two narrow source credentials,
validate integration, then create its own matching version tag. No coordinator
code/workflow/central target inventory change is required.
