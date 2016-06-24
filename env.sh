#!/usr/bin/env bash

# See: http://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
i_am_sourced ()
{ case ${0} in ("${BASH_SOURCE}") return 1 ;; (*) return 0 ;; esac; }

if ! i_am_sourced
then
    echo "sorry: '${0}' must be sourced" 1>&2
    echo "aborting" 1>&2
    exit 1
fi

# Put API key for meetup.com into environment.
export MEETUP_API_KEY=$( cat ~/.meetup/apikey )

prepend_to_path ()
# $1 - path env var
# $2 - dir
{
    local path_var=${1?}
    local dir=${2?}
    case :${!path_var}: in
    (*:${dir}:*) ;;
    (*) eval "${path_var}=\${dir}:\${!path_var}" ;;
    esac
    eval export "${path_var}"
}

# Prepend ./bin to PATH.
prepend_to_path PATH "$(pwd)/bin"

# Prepend louvain/python-louvain/community to PYTHONPATH.
prepend_to_path PYTHONPATH "$(pwd)/louvain/python-louvain"
