#!/data/data/com.termux/files/usr/bin/bash

shell_install() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    echo "=== SHELL INSTALL ==="
    echo "[INFO] No package installation required"
    echo "[DONE]"
}

shell_test() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1

    echo "=== SHELL TEST ==="

    local failed=0

    for file in scripts/*.sh; do
        [ -f "$file" ] || continue

        if bash -n "$file"; then
            echo "[OK] $file"
        else
            echo "[FAIL] $file"
            failed=1
        fi
    done

    return "$failed"
}

shell_run() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1

    echo "=== SHELL RUN ==="

    if [ -f "main.sh" ]; then
        chmod +x main.sh
        start_process "$project" ./main.sh
        return $?
    fi

    if [ -f "run.sh" ]; then
        chmod +x run.sh
        start_process "$project" ./run.sh
        return $?
    fi

    echo "[ERROR] No main.sh or run.sh found"
    return 1
}

shell_stop() {
    stop_process "$1"
}

shell_logs() {
    process_logs "$1"
}
