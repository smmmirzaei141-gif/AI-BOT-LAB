#!/data/data/com.termux/files/usr/bin/bash

android_env_init() {
    export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
    export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT:-$ANDROID_HOME}"

    export PATH="$ANDROID_HOME/platform-tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/34.0.0:$PATH"
}

android_env_check() {
    android_env_init

    echo "=== ANDROID ENVIRONMENT ==="
    echo "ANDROID_HOME=$ANDROID_HOME"
    echo "ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"

    echo
    echo "--- Tools ---"

    command -v adb >/dev/null 2>&1 \
        && echo "[OK] adb" \
        || echo "[FAIL] adb"

    command -v sdkmanager >/dev/null 2>&1 \
        && echo "[OK] sdkmanager" \
        || echo "[INFO] sdkmanager unavailable"

    command -v aapt >/dev/null 2>&1 \
        && echo "[OK] aapt" \
        || echo "[FAIL] aapt"

    command -v apksigner >/dev/null 2>&1 \
        && echo "[OK] apksigner" \
        || echo "[FAIL] apksigner"

    command -v zipalign >/dev/null 2>&1 \
        && echo "[OK] zipalign" \
        || echo "[FAIL] zipalign"

    echo
    echo "--- SDK ---"

    [ -d "$ANDROID_HOME/platforms/android-35" ] \
        && echo "[OK] Android 35" \
        || echo "[FAIL] Android 35"

    [ -d "$ANDROID_HOME/build-tools/34.0.0" ] \
        && echo "[OK] Build Tools 34.0.0" \
        || echo "[FAIL] Build Tools 34.0.0"
}
