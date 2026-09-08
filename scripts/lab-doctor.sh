#!/data/data/com.termux/files/usr/bin/bash

echo "================================"
echo "       AI-BOT-LAB DOCTOR"
echo "================================"
echo

check() {
    NAME="$1"
    CMD="$2"

    if command -v "$CMD" >/dev/null 2>&1; then
        echo "[OK]   $NAME -> $(command -v "$CMD")"
    else
        echo "[MISS] $NAME"
    fi
}

check "Git" git
check "Python" python
check "Pip" pip
check "Node.js" node
check "NPM" npm
check "Java" java
check "Javac" javac
check "Gradle" gradle
check "ADB" adb
check "AAPT" aapt
check "AAPT2" aapt2
check "ApkSigner" apksigner
check "ZipAlign" zipalign
check "Curl" curl
check "Wget" wget

echo
echo "----- Android Environment -----"

if [ -n "$ANDROID_HOME" ]; then
    echo "[OK]   ANDROID_HOME=$ANDROID_HOME"
else
    echo "[INFO] ANDROID_HOME is not set"
fi

if [ -n "$ANDROID_SDK_ROOT" ]; then
    echo "[OK]   ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"
else
    echo "[INFO] ANDROID_SDK_ROOT is not set"
fi

echo
echo "----- Git -----"
cd "$(dirname "$0")/.." || exit 1
echo "Branch: $(git branch --show-current)"
echo "Remote: $(git remote get-url origin 2>/dev/null || echo NOT_SET)"
echo "Status:"
git status --short

echo
echo "AI-BOT-LAB DOCTOR COMPLETE"
