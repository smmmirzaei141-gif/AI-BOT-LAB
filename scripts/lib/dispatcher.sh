#!/data/data/com.termux/files/usr/bin/bash

dispatch_command() {
    local command="$1"
    shift

    case "$command" in
        install)
            cmd_install "$@"
            ;;
        test)
            cmd_test "$@"
            ;;
        build)
            cmd_build "$@"
            ;;
        run)
            cmd_run "$@"
            ;;
        stop)
            cmd_stop "$@"
            ;;
        logs)
            cmd_logs "$@"
            ;;
        clean)
            cmd_clean "$@"
            ;;
        *)
            echo "ERROR: Unknown command: $command"
            return 1
            ;;
    esac
}
