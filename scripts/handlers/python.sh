#!/data/data/com.termux/files/usr/bin/bash

python_install() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    if [ ! -d "$path" ]; then
        echo "[ERROR] Project not found: $project"
        return 1
    fi

    cd "$path" || return 1

    echo "=== PYTHON INSTALL ==="
    echo "Project: $project"

    if [ ! -f "requirements.txt" ]; then
        echo "[INFO] No requirements.txt"
        echo "[DONE]"
        return 0
    fi

    if [ ! -s "requirements.txt" ]; then
        echo "[INFO] requirements.txt is empty"
        echo "[DONE]"
        return 0
    fi

    python -m pip install -r requirements.txt
}

python_test() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    if [ ! -d "$path" ]; then
        echo "[ERROR] Project not found: $project"
        return 1
    fi

    cd "$path" || return 1

    echo "=== PYTHON TEST ==="
    echo "Project: $project"

    if [ -d "tests" ] && find tests -type f -name 'test_*.py' | grep -q .; then
        python -m pytest
    else
        echo "[INFO] No pytest tests found"
        echo "[DONE]"
    fi
}

python_run() {
    local project="$1"
    local path="$PROJECTS_DIR/$project"

    if [ ! -d "$path" ]; then
        echo "[ERROR] Project not found: $project"
        return 1
    fi

    cd "$path" || return 1

    echo "=== PYTHON RUN ==="
    echo "Project: $project"

    if [ -f "main.py" ]; then
        start_process "$project" python main.py
        return $?
    fi

    if [ -f "app.py" ]; then
        start_process "$project" python app.py
        return $?
    fi

    if [ -f "bot.py" ]; then
        start_process "$project" python bot.py
        return $?
    fi

    echo "[ERROR] No main.py, app.py or bot.py found"
    return 1
}

python_stop() {
    local project="$1"
    stop_process "$project"
}

python_logs() {
    local project="$1"
    process_logs "$project"
}
