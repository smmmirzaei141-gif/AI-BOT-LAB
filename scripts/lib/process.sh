#!/data/data/com.termux/files/usr/bin/bash

RUNTIME_DIR="$LAB_DIR/.runtime"
PID_DIR="$RUNTIME_DIR/pids"
LOG_DIR="$RUNTIME_DIR/logs"

runtime_init() {
    mkdir -p "$PID_DIR" "$LOG_DIR"
}

pid_file() {
    echo "$PID_DIR/$1.pid"
}

log_file() {
    echo "$LOG_DIR/$1.log"
}

is_running() {
    local name="$1"
    local pf
    pf="$(pid_file "$name")"

    [ -f "$pf" ] || return 1

    local pid
    pid="$(cat "$pf" 2>/dev/null)"

    [ -n "$pid" ] || return 1

    kill -0 "$pid" 2>/dev/null
}

start_process() {
    local name="$1"
    shift

    runtime_init

    if is_running "$name"; then
        echo "[RUNNING] $name"
        return 1
    fi

    local log
    local pf
    log="$(log_file "$name")"
    pf="$(pid_file "$name")"

    nohup "$@" >> "$log" 2>&1 &
    local pid=$!

    echo "$pid" > "$pf"

    echo "[STARTED] $name"
    echo "PID: $pid"
    echo "LOG: $log"
}

stop_process() {
    local name="$1"
    local pf
    pf="$(pid_file "$name")"

    if ! is_running "$name"; then
        rm -f "$pf"
        echo "[NOT RUNNING] $name"
        return 0
    fi

    local pid
    pid="$(cat "$pf")"

    kill "$pid" 2>/dev/null || true
    sleep 1

    if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm -f "$pf"

    echo "[STOPPED] $name"
}

process_status() {
    local name="$1"

    if is_running "$name"; then
        local pid
        pid="$(cat "$(pid_file "$name")")"
        echo "[RUNNING] $name PID=$pid"
    else
        echo "[STOPPED] $name"
    fi
}

process_logs() {
    local name="$1"
    local log
    log="$(log_file "$name")"

    if [ -f "$log" ]; then
        cat "$log"
    else
        echo "[NO LOG] $name"
    fi
}
