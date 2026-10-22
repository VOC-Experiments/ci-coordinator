<a id="banner"></a>
# OpenWrt test feed

Only use disposable test targets. Feed paths are `openwrt/24.10/<arch>/`
and `openwrt/25.12/<arch>/`, for `x86_64` and `aarch64_generic`.
Verify 24.10 Packages signatures with `keys/opkg.pub`, and 25.12 APK
signatures with `keys/apk.pem`, before installing demo-core/demo-app.
