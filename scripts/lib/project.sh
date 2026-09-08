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
    local file="$PROJECTS_DIR/$name/PROJECT.md"

    if [ -f "$file" ]; then
        grep '^Type:' "$file" 2>/dev/null | head -n 1 | sed 's/^Type:[[:space:]]*//'
    else
        echo "unknown"
    fi
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
