#!/bin/sh

relative_path=$(dirname $0)
absolute_path=$(python3 -c "import os,sys; print(os.path.realpath('${relative_path}'))")
awk "{sub(\"{}\",\"${absolute_path}\"); print}" "${relative_path}/url2phash.service" > /etc/systemd/system/url2phash.service