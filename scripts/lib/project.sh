#!/data/data/com.termux/files/usr/bin/bash

project_exists() {
    local name="$1"
    [ -d "$PROJECTS_DIR/$name" ]
}

project_path() {
    local name="$1"
    echo "$PROJECTS_DIR/$name"
}

project_type() {
    local name="$1"
    local dir="$PROJECTS_DIR/$name"
    local file="$dir/PROJECT.md"

    # Explicit metadata
    if [ -f "$file" ]; then
        local type
        type="$(grep '^Type:' "$file" 2>/dev/null |
            head -n 1 |
            sed 's/^Type:[[:space:]]*//')"

        if [ -n "$type" ]; then
            echo "$type"
            return 0
        fi
    fi

    # Automatic Android detection
    if [ -f "$dir/settings.gradle" ] ||
       [ -f "$dir/settings.gradle.kts" ] ||
       [ -f "$dir/gradlew" ] ||
       [ -f "$dir/app/build.gradle" ] ||
       [ -f "$dir/app/build.gradle.kts" ]; then
        echo "android"
        return 0
    fi

    # Automatic Node detection
    if [ -f "$dir/package.json" ]; then
        echo "node"
        return 0
    fi

    # Automatic Python detection
    if [ -f "$dir/requirements.txt" ] ||
       [ -f "$dir/pyproject.toml" ] ||
       [ -f "$dir/setup.py" ]; then
        echo "python"
        return 0
    fi

    # Automatic Shell detection
    if find "$dir" -maxdepth 2 -type f \
        \( -name '*.sh' -o -name '*.bash' \) 2>/dev/null |
        grep -q .; then
        echo "shell"
        return 0
    fi

    echo "unknown"
}

validate_project_name() {
    case "$1" in
        ""|*[!a-zA-Z0-9._-]*)
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

list_project_names() {
    for dir in "$PROJECTS_DIR"/*; do
        [ -d "$dir" ] || continue
        basename "$dir"
    done
}
