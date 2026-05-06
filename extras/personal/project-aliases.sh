##
## === FREQUENTLY VISITED DIRECTORIES
##

create_alias_if_present() {
    local var_name=""
    local alias_name=""
    local dir_path=""

    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --var)
                var_name="$2"
                shift 2
                ;;
            --alias)
                alias_name="$2"
                shift 2
                ;;
            --dir)
                dir_path="$2"
                shift 2
                ;;
            *)
                echo "create_alias_if_present: unknown argument: $1" >&2
                return 2
                ;;
        esac
    done

    if [[ -z "$var_name" || -z "$alias_name" || -z "$dir_path" ]]; then
        echo "create_alias_if_present: requires --var <name> --alias <name> --dir <path>" >&2
        return 2
    fi

    [[ -d "$dir_path" ]] || return 0

    export "$var_name=$dir_path"
    alias "$alias_name=cd \"\$$var_name\""
}

create_alias_if_present --var DDOC --alias ddoc --dir "$HOME/Documents"
create_alias_if_present --var DSYS --alias dsys --dir "$DDOC/SetupFramework"
create_alias_if_present --var DNOTES --alias dnotes --dir "$DDOC/ProjectNotes"

create_alias_if_present --var DPROJ --alias dproj --dir "$DHOME/Projects"
create_alias_if_present --var DDOT --alias ddot --dir "$DPROJ/DotFiles"
create_alias_if_present --var DASGARD --alias dasgard --dir "$DPROJ/Asgard"
create_alias_if_present --var DQUOKKA --alias dquokka --dir "$DPROJ/quokka"

## .
