#!/usr/bin/env bash

usage='"
Usage: ${progname} [--dry-run] [--prefix=pre] [-v] {cmd} file ...

Description
    Each file can be a full or relative path ending with the final filename
    component matching \"blah_12345.ext\".

Options
    --dry-run       Do not install any files into the stash, just show what
                    would happen.

    --prefix=pre    Use pre as the prefix to put in front of the destination
                    file names; (default ${dflt_prefix}).

    -v              Verbose; may be repeated for more verbosity.
    
Commands

    install     Moves each file to \"pre/blah_/1/2/1234.ext\".

    exists      Only checks to see if the destination files exist. Exits 0 if
                they all do, 1 if one or more do not.
"'

progname=$( basename "${0}" )
msg () { echo "${progname}:" "${@}"; }
emsg () { msg "${@}" 1>&2; }
vecho () { case ${verbose} in (v*) echo "${@}" ;; esac; }
vvecho () { case ${verbose} in (vv*) echo "${@}" ;; esac; }

source split_path.sh

dflt_prefix=$( dirname "${0}" )

unset errs
unset dry_run
prefix=${dflt_prefix}
unset verbose
while case ${#} in (0) break ;; esac
do
    case ${1} in
    (--)
        shift; break ;;
    (-h|--help)
        eval echo "${usage}"; exit ;;
    (--dry-run)
        dry_run= ;;
    (--verbose|-v)
        verbose=${verbose}v ;;
    (--prefix=*)
        prefix=${1#*=} ;;
    (-*)
        emsg "unknown flag: ${1}"; errs= ;;
    (*)
        break ;;
    esac
    shift
done

case ${errs+isset} in
(isset)
    emsg "aborting, run with -h for help"; exit 1 ;;
esac

run ()
{
    echo "${@}"
    case ${dry_run+isset} in
    (isset)
        ;;
    (*)
        "${@}" ;;
    esac
}

parse_filename ()
# $1 - filename
# sets: store_name group_id ext first_digit second_digit stash_path
{
    local file=${1:?"parse_filename: missing file!"}
    split_path "${file}" parentpath filename basename ext
    store_name=${basename%%[0-9]*}
    group_id=${basename##*_}
    first_digit=${group_id:0:1}
    second_digit=${group_id:1:1}
    stash_path=${store_name}/${first_digit}/${second_digit}
    vvecho "parentpath=${parentpath}"
    vvecho "filename=${filename}"
    vvecho "basename=${basename}"
    vvecho "ext=${ext}"
    vvecho "store_name=${store_name}"
    vvecho "group_id=${group_id}"
    vvecho "first_digit=${first_digit}"
    vvecho "second_digit=${second_digit}"
    vvecho "stash_path=${stash_path}"
}

check_exists ()
# $1 - file
{
    parse_filename "${1}"
    case ${stash_path} in
    (${store_name}/[0-9]/[0-9])
        if [ ! -f "${prefix}/${stash_path}/${group_id}${ext}" ]
        then
            vecho "does not exist: ${prefix}/${stash_path}/${group_id}${ext}"
            status=1
        else
            vecho "exists: ${prefix}/${stash_path}/${group_id}${ext}"
        fi
        ;;
    (*)
        emsg "bad stash path: '${stash_path}'"
        errs=
        ;;
    esac

}

stash_file ()
# $1 - file
{
    parse_filename "${1}"
    if [ -f "${1}" ]
    then
        case ${stash_path} in
        (${store_name}/[0-9]/[0-9])
            run mkdir -p "${prefix}/${stash_path}"
            run mv "${f}" "${prefix}/${stash_path}/${group_id}${ext}"
            ;;
        (*)
            emsg "bad stash path: '${stash_path}'"
            errs=
            ;;
        esac
    else
        emsg "not a file: '${1}'"
        errs=
    fi
}

case ${#} in
(0)
    emsg "missing command (exists|install)!"; errs= ;;
(*)
    cmd=${1}; shift ;;
esac

case ${#} in
(0)
    emsg "no files!"; errs= ;;
esac

case ${errs+isset} in
(isset)
    emsg "aborting, run with -h for help"; exit 1 ;;
esac

status=0
for f
do
    case ${cmd} in
    (exists)
        check_exists "${f}" ;;
    (install)
        stash_file "${f}" ;;
    (parse)
        parse_filename "${f}"
        echo "parentpath=${parentpath}"
        echo "filename=${filename}"
        echo "basename=${basename}"
        echo "ext=${ext}"
        echo "store_name=${store_name}"
        echo "group_id=${group_id}"
        echo "first_digit=${first_digit}"
        echo "second_digit=${second_digit}"
        echo "stash_path=${stash_path}"
        ;;
    (*)
        emsg "unknown command: '${cmd}'"; errs= ;;
    esac
done

case ${errs+isset} in
(isset)
    status=1 ;;
esac

exit ${status}
