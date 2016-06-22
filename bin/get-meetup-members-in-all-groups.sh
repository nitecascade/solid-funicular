#!/usr/bin/env bash

usage='"
Usage: ${progname} [--dry-run] [-v] groups-file

Description
    Read groups-file for a list of group_id values (first token on each line).
    Run meetup-members-in-group.py with each group_id and stash the data
    in big_data/members_in_group_/ using the big_data/stash_it.sh program.

Options
    --dry-run   Just show what would happen.
    -v          Increase verbosity.
"'

progname=$( basename "${0}" )
msg () { echo "${progname}:" "${@}"; }
emsg () { msg "${@}" 1>&2; }
vecho () { case ${verbose} in (v*) echo "${@}" ;; esac; }
vvecho () { case ${verbose} in (vv*) echo "${@}" ;; esac; }

unset errs
unset dry_run
unset verbose
while case ${#} in (0) break ;; esac
do
    case ${1} in
    (--)
        shift; break ;;
    (-h|--h*)
        eval echo "${usage}"; exit ;;
    (--dry-run)
        dry_run= ;;
    (-*)
        errmsg "unknown flag: ${1}"; errs= ;;
    (*)
        break ;;
    esac
    shift
done

case ${#} in
(0)
    emsg "missing groups-file!"; errs= ;;
(*)
    groups_file=${1}; shift ;;
esac

case ${#} in
(0)
    ;;
(*)
    emsg "extra args: ${@}"; errs= ;;
esac

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

prefix=big_data

awk '{ print $1 }' "${groups_file}" \
| while read group_id
do
    echo "group_id: ${group_id}"
    target=members_in_group_${group_id}.json
    if stash.sh --prefix="${prefix}" exists "${target}"
    then
        echo "    exists: '${target}'"
    else
        echo "    downloading member data for group ${group_id}"
        run meetup-members-in-group.py --group-id "${group_id}" \
            "${prefix}/${target}"
        echo "    installing member data for group ${group_id} into '${prefix}'"
        run stash.sh --prefix="${prefix}" install "${prefix}/${target}"
    fi
done

echo
echo "stash ${prefix}/members_in_group_:"
(cd "${prefix}"; find "members_in_group_" -type f -exec wc -l {} \;)
