#/bin/bash

function log(){
        local msg=${1}

        [ -z "$msg" ] && exit -1

        local logfile=${2:-"syslog"}

        if [[ $logfile =~ ^[Ss][Yy][Ss][Ll][Oo][Gg]$ ]]; then
            logger -t "$0" "$msg"
        else

        echo "`date '+%x %X'` $msg" >> $logfile
        fi
        return 0
}
