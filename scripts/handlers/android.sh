#!/data/data/com.termux/files/usr/bin/bash

android_prepare() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    source "$LAB_DIR/scripts/lib/android_env.sh"
    android_env_init

    cd "$path" || return 1
}

android_install() {
    local project="$1"

    android_prepare "$project" || return 1

    echo "=== ANDROID INSTALL ==="
    echo "Project: $project"

    if [ -f "gradlew" ]; then
        chmod +x gradlew
        ./gradlew dependencies
    else
        gradle dependencies
    fi
}

android_test() {
    local project="$1"

    android_prepare "$project" || return 1

    echo "=== ANDROID TEST ==="

    if [ -f "gradlew" ]; then
        chmod +x gradlew
        ./gradlew test
    else
        gradle test
    fi
}

android_build() {
    local project="$1"

    android_prepare "$project" || return 1

    echo "=== ANDROID BUILD ==="

    if [ -f "gradlew" ]; then
        chmod +x gradlew
        ./gradlew assembleDebug
    else
        gradle assembleDebug
    fi
}

android_install_apk() {
    local project="$1"

    android_prepare "$project" || return 1

    local path="$PROJECTS_DIR/$project"
    local apk
    apk="$(find "$path/app/build/outputs/apk" -type f -name '*.apk' 2>/dev/null | head -n 1)"

    if [ -z "$apk" ]; then
        echo "[ERROR] APK not found"
        return 1
    fi

    adb install -r "$apk"
}

android_run() {
    local project="$1"

    android_prepare "$project" || return 1

    echo "[INFO] Android run requires a connected device/emulator."

    adb devices

    echo
    echo "[INFO] Use android_install_apk after a successful build."
}

android_stop() {
    local project="$1"
    echo "[INFO] Android apps are stopped through ADB/package manager."
    echo "Project: $project"
}

android_logs() {
    echo "=== ANDROID LOGCAT ==="
    adb logcat -d -t 200
}

android_clean() {
    local project="$1"

    android_prepare "$project" || return 1

    echo "=== ANDROID CLEAN ==="

    if [ -f "gradlew" ]; then
        chmod +x gradlew
        ./gradlew clean
    else
        gradle clean
    fi
}
