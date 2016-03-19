#!/bin/bash



echo "link /private/tmp/lnk0 ..."
ln -s "/private/tmp/lnk0" "/tmp/lnkdest/$(basename '/private/tmp/lnk0')" || {
    exit 1
}

echo "link /private/tmp/lnk1 ..."
ln -s "/private/tmp/lnk1" "/tmp/lnkdest/$(basename '/private/tmp/lnk1')" || {
    exit 1
}


