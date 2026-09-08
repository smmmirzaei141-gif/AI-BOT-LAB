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

        run)
            cmd_run "$@"
            ;;

        stop)
            cmd_stop "$@"
            ;;

        logs)
            cmd_logs "$@"
            ;;

        *)
            echo "ERROR: Unknown V2 command: $command"
            return 1
            ;;
    esac
}
