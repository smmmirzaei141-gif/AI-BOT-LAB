#!/data/data/com.termux/files/usr/bin/bash

generic_install() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    echo "=== GENERIC INSTALL ==="
    echo "Project: $project"
    echo "[INFO] No generic package manager configured"
    echo "[DONE]"
}

generic_test() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1
    echo "=== GENERIC TEST ==="

    if [ -d "tests" ] && find tests -type f | grep -q .; then
        echo "[INFO] Test files found"
        find tests -type f -maxdepth 2 -print
    else
        echo "[INFO] No generic tests found"
    fi

    echo "[DONE]"
}

generic_build() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1
    echo "=== GENERIC BUILD ==="

    if [ -x "./build.sh" ]; then
        ./build.sh
        return $?
    fi

    if [ -f "Makefile" ]; then
        make
        return $?
    fi

    echo "[INFO] No generic build system detected"
    echo "[DONE]"
}

generic_run() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    cd "$path" || return 1
    echo "=== GENERIC RUN ==="

    if [ -x "./run.sh" ]; then
        start_process "$project" ./run.sh
        return $?
    fi

    if [ -x "./main.sh" ]; then
        start_process "$project" ./main.sh
        return $?
    fi

    echo "[ERROR] No executable run.sh or main.sh found"
    return 1
}

generic_stop() {
    stop_process "$1"
}

generic_logs() {
    process_logs "$1"
}

generic_clean() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    [ -d "$path" ] || {
        echo "[ERROR] Project not found: $project"
        return 1
    }

    find "$path" -type f \
        \( -name '*.log' -o -name '*.tmp' \) -delete

    echo "[CLEANED] $project"
}
