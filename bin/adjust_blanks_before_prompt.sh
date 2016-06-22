#!/usr/bin/env bash

usage='"
Usage: eval \"\$(${progstr} add|remove)\"

Description
    Add/remove one newline to/from the beginning of PS1. Writes new prompt to
    stdout. To change the prompt of the invoking shell use:

        \$ eval \"\$(${progstr} add)\"
    or
        \$ eval \"\$(${progstr} remove)\"
"'

progstr=${BASH_SOURCE##*/}
msg () { echo "${progstr}:" "${@}"; }
emsg () { msg "${@}" 1>&2; }

unset errs
while case ${#} in (0) break ;; esac
do
    case ${1} in
    (-h|--help)
        eval echo "${usage}" 1>&2; exit ;;
    (-*)
        emsg "unknown flag: ${1}"; errs= ;;
    (*)
        break ;;
    esac
    shift
done

case ${#} in
(0)
    emsg "missing add/remove!"; errs= ;;
(*)
    adjustment=${1}; shift ;;
esac

case ${#} in
(0)
    ;;
(*)
    emsg "extra args: ${*}"; errs= ;;
esac

case ${errs+isset} in
(isset)
    emsg "aborting, run with -h for help"; exit 1 ;;
esac

case ${adjustment} in
(r*)
    echo "echo '>>> remove one prefix newline from PS1, if it has one' 1>&2"
    echo "echo '>>> if there is no change to your prompt, re-run with --help' 1>&2"
    echo "PS1=\"\${PS1#\\\n}\""
    ;;
(a*)
    echo "echo '>>> prepend newline to PS1' 1>&2"
    echo "echo '>>> if there is no change to your prompt, re-run with --help' 1>&2"
    echo "PS1=\"\\\n\${PS1}\""
    ;;
(*)
    echo "echo '>>> unknown arg: ${adjustment}' 1>&2"
    echo "echo '>>> re-run with --help' 1>&2"
    ;;
esac
