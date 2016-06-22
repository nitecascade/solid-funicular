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

# Prepend ./bin to PATH.
bin=$(pwd)/bin
case :${PATH}: in
(*:${bin}:*) ;;
(*) PATH=${bin}:${PATH} ;;
esac
export PATH
