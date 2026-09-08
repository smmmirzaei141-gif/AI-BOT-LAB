#!/data/data/com.termux/files/usr/bin/bash

REGISTRY_DIR="$LAB_DIR/configs"
REGISTRY_FILE="$REGISTRY_DIR/projects.db"

registry_init() {
    mkdir -p "$REGISTRY_DIR"
    touch "$REGISTRY_FILE"
}

registry_add() {
    local name="$1"
    local type="$2"

    registry_init

    if grep -q "^${name}|" "$REGISTRY_FILE" 2>/dev/null; then
        return 1
    fi

    printf '%s|%s|%s\n' "$name" "$type" "$PROJECTS_DIR/$name" >> "$REGISTRY_FILE"
}

registry_get_type() {
    local name="$1"

    registry_init

    awk -F'|' -v n="$name" '$1 == n {print $2; exit}' "$REGISTRY_FILE"
}

registry_get_path() {
    local name="$1"

    registry_init

    awk -F'|' -v n="$name" '$1 == n {print $3; exit}' "$REGISTRY_FILE"
}

registry_remove() {
    local name="$1"
    local tmp="$REGISTRY_FILE.tmp"

    registry_init

    awk -F'|' -v n="$name" '$1 != n' "$REGISTRY_FILE" > "$tmp"
    mv "$tmp" "$REGISTRY_FILE"
}

registry_list() {
    registry_init

    if [ ! -s "$REGISTRY_FILE" ]; then
        echo "(empty)"
        return 0
    fi

    cat "$REGISTRY_FILE"
}
