#!/data/data/com.termux/files/usr/bin/bash

android_env_init() {
    export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
    export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$ANDROID_HOME}"

    # Termux ADB is native ARM64 on Android.
    # SDK platform-tools may contain a desktop x86_64 binary.
    if [ -x "$PREFIX/bin/adb" ]; then
        export ADB="$PREFIX/bin/adb"
    else
        export ADB="$ANDROID_HOME/platform-tools/adb"
    fi

    export PATH="$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/34.0.0:$PREFIX/bin:$PATH"
}

android_env_check() {
    android_env_init

    echo "=== ANDROID ENVIRONMENT ==="
    echo "ANDROID_HOME=$ANDROID_HOME"
    echo "ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"
    echo "ADB=$ADB"

    if [ -x "$ADB" ]; then
        echo "ADB_BINARY:"
        file "$ADB"
    else
        echo "[ERROR] ADB not found"
        return 1
    fi

    echo
    echo "ADB_VERSION:"
    "$ADB" version
}

android_adb() {
    android_env_init
    "$ADB" "$@"
}
