#!/data/data/com.termux/files/usr/bin/bash

android_prepare() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    if [ ! -d "$path" ]; then
        echo "[ERROR] Project not found: $project"
        return 1
    fi

    source "$LAB_DIR/scripts/lib/android_env.sh"
    android_env_init

    cd "$path" || return 1
}

android_gradle() {
    if [ -f "gradlew" ]; then
        chmod +x gradlew
        ./gradlew "$@"
    else
        gradle "$@"
    fi
}

android_install() {
    local project="$1"
    android_prepare "$project" || return 1

    echo "=== ANDROID DEPENDENCIES ==="
    echo "Project: $project"

    android_gradle dependencies
}

android_test() {
    local project="$1"
    android_prepare "$project" || return 1

    echo "=== ANDROID TEST ==="
    android_gradle test
}

android_build() {
    local project="$1"
    android_prepare "$project" || return 1

    echo "=== ANDROID BUILD ==="
    echo "Project: $project"

    android_gradle --offline --no-daemon assembleDebug
}

android_clean() {
    local project="$1"
    android_prepare "$project" || return 1

    echo "=== ANDROID CLEAN ==="
    android_gradle clean
}

android_find_apk() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    find "$path/app/build/outputs/apk" \
        -type f \
        -name '*.apk' \
        2>/dev/null |
        sort |
        head -n 1
}

android_install_apk() {
    local project="$1"
    android_prepare "$project" || return 1

    local apk
    apk="$(android_find_apk "$project")"

    if [ -z "$apk" ]; then
        echo "[ERROR] APK not found."
        echo "[INFO] Run: build $project"
        return 1
    fi

    echo "=== INSTALL APK ==="
    echo "APK: $apk"

    android_adb install -r "$apk"
}

android_get_package() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    if [ -f "$path/app/build.gradle" ]; then
        grep -E 'applicationId[[:space:]]+' \
            "$path/app/build.gradle" 2>/dev/null |
            head -n 1 |
            sed -E 's/.*applicationId[[:space:]]+["'\'']([^"'\'']+)["'\''].*/\1/'
    fi
}

android_run() {
    local project="$1"
    android_prepare "$project" || return 1

    local package
    package="$(android_get_package "$project")"

    if [ -z "$package" ]; then
        echo "[ERROR] applicationId not found."
        return 1
    fi

    echo "=== ANDROID RUN ==="
    echo "Package: $package"

    if ! android_adb get-state >/dev/null 2>&1; then
        echo "[ERROR] No Android device connected."
        echo
    android_adb devices
        return 1
    fi

    local activity
    activity="$(android_adb shell cmd package resolve-activity \
        --brief "$package" 2>/dev/null |
        tail -n 1 |
        tr -d '\r')"

    if [ -z "$activity" ] || [ "$activity" = "No activity found" ]; then
        echo "[ERROR] Launcher activity not found."
        return 1
    fi

    echo "Activity: $activity"
    android_adb shell am start -n "$activity"
}

android_stop() {
    local project="$1"

    local package
    package="$(android_get_package "$project")"

    if [ -z "$package" ]; then
        echo "[ERROR] applicationId not found."
        return 1
    fi

    echo "=== ANDROID STOP ==="
    echo "Package: $package"

    android_adb shell am force-stop "$package"
}

android_logs() {
    local project="${1:-}"

    echo "=== ANDROID LOGCAT ==="

    if [ -n "$project" ]; then
        local package
        package="$(android_get_package "$project")"

        if [ -n "$package" ]; then
    android_adb logcat -d -t 300 | grep "$package" || true
            return 0
        fi
    fi

    android_adb logcat -d -t 300
}

android_run_all() {
    local project="$1"

    android_build "$project" || return 1
    android_install_apk "$project" || return 1
    android_run "$project"
}
