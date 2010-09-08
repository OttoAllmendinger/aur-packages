#!/bin/bash

OPT_MAIL=0
OPT_DOWNLOAD=0

while getopts :md option; do
    case ${option} in
        m)  OPT_MAIL=1 ;;
        d)  OPT_DOWNLOAD=1 ;;
    esac
done

echo "mail: ${OPT_MAIL}"


if !(which cronkite > /dev/null); then
    echo "get the cronkite"
    exit 1
fi

aur_data=($(cronkite -info grooveshark-desktop))
aur_version=${aur_data[3]%-*}

air_xmlns="http://ns.adobe.com/air/framework/update/description/1.0"
gs_version_url="http://preview.grooveshark.com/desktop/version.php"
gs_version_file="/tmp/gs_info.xml"
curl -s -o${gs_version_file} ${gs_version_url}
gs_latest_version=$(xml sel -N x=${air_xmlns} -t -v "/x:update/x:version" \
    $gs_version_file)
gs_download_url=$(xml sel -N x=${air_xmlns} -t -v "/x:update/x:url" \
    $gs_version_file)

if [ "${gs_latest_version}" != "${aur_version}" ]; then
    msg="New grooveshark version ${latest_version}"
    echo ${msg}

    if [ ! -z "${OPT_DOWNLOAD}" ]; then 
        wget "${gs_download_url}"
    fi

    if [ "${OPT_MAIL}" != "0" ]; then
        echo "mailing message..."
        echo "${msg}" | mail -s "grooveshark-desktop update" otto
    fi

else
    echo "aur version is latest version"
fi
