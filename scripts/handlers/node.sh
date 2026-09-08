#!/data/data/com.termux/files/usr/bin/bash

node_install() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1

    echo "=== NODE INSTALL ==="

    if [ ! -f "package.json" ]; then
        echo "[ERROR] package.json not found"
        return 1
    fi

    npm install
}

node_test() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1

    echo "=== NODE TEST ==="

    if grep -q '"test"[[:space:]]*:' package.json 2>/dev/null; then
        npm test
    else
        echo "[INFO] No test script found"
        echo "[DONE]"
    fi
}

node_run() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1

    echo "=== NODE RUN ==="

    if [ -f "package.json" ]; then
        if grep -q '"start"' package.json; then
            start_process "$project" npm start
            return $?
        fi
    fi

    if [ -f "index.js" ]; then
        start_process "$project" node index.js
        return $?
    fi

    echo "[ERROR] No start script or index.js found"
    return 1
}

node_stop() {
    stop_process "$1"
}

node_logs() {
    process_logs "$1"
}
