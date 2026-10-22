<a id="banner"></a>
# Debian test feed

Only use a disposable Debian trixie test container. The feed base is
`https://raw.githubusercontent.com/VOC-Experiments/packages/main/debian`.
Use the `keys/apt.asc` key from this repository and `signed-by` in the source entry.
Both `InRelease` and `Release.gpg` must verify before installation.
