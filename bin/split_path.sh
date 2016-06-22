#!/usr/bin/env bash

# See: http://stackoverflow.com/a/18139746
# SYNOPSIS
#   split_path path varDirname [varBasename [varBasenameRoot [varSuffix]]] 
# DESCRIPTION
#   Splits the specified input path into its components and returns them by assigning
#   them to variables with the specified *names*.
#   Specify '' or throw-away variable _ to skip earlier variables, if necessary.
#   The filename suffix, if any, always starts with '.' - only the *last*
#   '.'-prefixed token is reported as the suffix.
#   As with `dirname`, varDirname will report '.' (current dir) for input paths
#   that are mere filenames, and '/' for the root dir.
#   As with `dirname` and `basename`, a trailing '/' in the input path is ignored.
#   A '.' as the very first char. of a filename is NOT considered the beginning
#   of a filename suffix.
# EXAMPLE
#   splitPath '/home/jdoe/readme.txt' parentpath fname fnameroot suffix
#   echo "$parentpath" # -> '/home/jdoe'
#   echo "$fname" # -> 'readme.txt'
#   echo "$fnameroot" # -> 'readme'
#   echo "$suffix" # -> '.txt'
#   ---
#   splitPath '/home/jdoe/readme.txt' _ _ fnameroot
#   echo "$fnameroot" # -> 'readme'  

split_path () {
    local _sp_dirname= _sp_basename= _sp_basename_root= _sp_suffix=
    # simple argument validation
    (( $# >= 2 )) || {
        echo "$FUNCNAME: ERROR: Specify an input path and" \
            "at least 1 output variable name." >&2; exit 2
    }
    # extract dirname (parent path) and basename (filename)
    _sp_dirname=$(dirname "$1")
    _sp_basename=$(basename "$1")
    # determine suffix, if any
    _sp_suffix=$([[ $_sp_basename = *.* ]] \
        && printf %s ".${_sp_basename##*.}" || printf '')
    # determine basename root (filemane w/o suffix)
    if [[ "$_sp_basename" == "$_sp_suffix" ]]
    then # does filename start with '.'?
        _sp_basename_root=$_sp_basename
        _sp_suffix=''
    else # strip suffix from filename
        _sp_basename_root=${_sp_basename%$_sp_suffix}
    fi
    # assign to output vars.
    [[ -n $2 ]] && printf -v "$2" "$_sp_dirname"
    [[ -n $3 ]] && printf -v "$3" "$_sp_basename"
    [[ -n $4 ]] && printf -v "$4" "$_sp_basename_root"
    [[ -n $5 ]] && printf -v "$5" "$_sp_suffix"
    return 0
}
