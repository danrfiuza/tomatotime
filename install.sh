#!/bin/bash

export SUDO_USER_HOME=$(eval echo ~${SUDO_USER})

apt install libappindicator3-dev python3 python3-gi openvpn3 -y --no-install-recommends

mkdir -p /usr/share/applications /usr/share/tomatotime

cp ./usr/bin/openvpn3-manager-applet /usr/bin/tomatotime
cp ./usr/share/applications/tomatotime.desktop /usr/share/applications/tomatotime.desktop
cp ./usr/share/tomatotime/tomato.png /usr/share/tomatotime/tomato.png
cp ./usr/share/tomatotime/run.py /usr/share/tomatotime/run.py

update-desktop-database