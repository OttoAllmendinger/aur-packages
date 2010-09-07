#!/bin/bash
if !(which cronkite > /dev/null); then
    echo "get the cronkite"
    exit 1
fi

aur_data=($(cronkite -info grooveshark-desktop))
aur_version=${aur_data[3]%-*}

air_xmlns="http://ns.adobe.com/air/framework/update/description/1.0"
grooveshark_version_url="http://preview.grooveshark.com/desktop/version.php"
latest_version=$(curl -so- ${grooveshark_version_url} | \
    xml sel -N x=${air_xmlns} -t -v "/x:update/x:version")

if [ ${latest_version} != ${aur_version} ]; then
    echo "new version - mailing message"
    echo "new grooveshark version: ${latest_version}" | mail otto
else
    echo "aur version is latest version"
fi
