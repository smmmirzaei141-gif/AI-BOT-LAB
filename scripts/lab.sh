#!/data/data/com.termux/files/usr/bin/bash

LAB_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECTS_DIR="$LAB_DIR/projects"

usage() {
    echo ""
    echo "AI-BOT-LAB"
    echo "=========="
    echo "Usage:"
    echo "  ./scripts/lab.sh list"
    echo "  ./scripts/lab.sh create <project-name> <type>"
    echo "  ./scripts/lab.sh status"
    echo "  ./scripts/lab.sh backup"
    echo ""
    echo "Types:"
    echo "  python"
    echo "  node"
    echo "  android"
    echo "  shell"
    echo "  generic"
    echo ""
}

create_project() {
    NAME="$1"
    TYPE="$2"

    if [ -z "$NAME" ] || [ -z "$TYPE" ]; then
        usage
        exit 1
    fi

    TARGET="$PROJECTS_DIR/$NAME"

    if [ -e "$TARGET" ]; then
        echo "ERROR: Project already exists: $NAME"
        exit 1
    fi

    mkdir -p "$TARGET"

    cat > "$TARGET/PROJECT.md" <<EOT
# $NAME

Type: $TYPE

Created by AI-BOT-LAB.

## Status
Development

## Notes
EOT

    case "$TYPE" in
        python)
            mkdir -p "$TARGET/src" "$TARGET/tests" "$TARGET/config"
            touch "$TARGET/src/.gitkeep"
            touch "$TARGET/tests/.gitkeep"
            cat > "$TARGET/requirements.txt" <<EOT
EOT
            ;;
        node)
            mkdir -p "$TARGET/src" "$TARGET/tests"
            cat > "$TARGET/package.json" <<EOT
{
  "name": "$NAME",
  "version": "0.1.0",
  "private": true
}
EOT
            ;;
        android)
            mkdir -p "$TARGET/app"
            ;;
        shell)
            mkdir -p "$TARGET/scripts" "$TARGET/tests"
            ;;
        generic)
            mkdir -p "$TARGET/src" "$TARGET/tests" "$TARGET/docs"
            ;;
        *)
            echo "ERROR: Unknown project type: $TYPE"
            rm -rf "$TARGET"
            exit 1
            ;;
    esac

    echo "Created project: $NAME"
    echo "Type: $TYPE"
    echo "Location: $TARGET"
}

list_projects() {
    echo ""
    echo "Projects:"
    echo "---------"

    found=0

    for dir in "$PROJECTS_DIR"/*; do
        if [ -d "$dir" ]; then
            found=1
            name="$(basename "$dir")"
            echo "- $name"
        fi
    done

    if [ "$found" -eq 0 ]; then
        echo "No projects yet."
    fi
}

status() {
    cd "$LAB_DIR" || exit 1

    echo ""
    echo "AI-BOT-LAB STATUS"
    echo "================="
    echo "Location: $LAB_DIR"
    echo ""

    git branch --show-current
    git status --short
    echo ""

    git log -1 --oneline
}

backup() {
    cd "$LAB_DIR" || exit 1

    git add .

    if git diff --cached --quiet; then
        echo "Nothing new to backup."
    else
        git commit -m "AI-BOT-LAB automatic backup"
        git push
    fi
}

case "$1" in
    list)
        list_projects
        ;;
    create)
        create_project "$2" "$3"
        ;;
    status)
        status
        ;;
    backup)
        backup
        ;;
    *)
        usage
        ;;
esac
