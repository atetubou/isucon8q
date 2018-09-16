#!/bin/bash
cd $(dirname $0)

HOSTNAME=$(hostname)

# Do not add '/'
ruby stat.rb '^/room/\w+$' \
             '^/room/$' \
             '^/images/' \
             '^/ws/\w+$' \
             '^/ws/$' \
             < /var/log/nginx/main_access.log | tee stat_$HOSTNAME.txt

go tool pprof -list='main.*' /tmp/cpuprofile | tee cpuprofile_$HOSTNAME.txt | python parse_cpuprofile.py | tee stat_go_$HOSTNAME.txt
# /usr/local/go/bin/go tool pprof ~/isubata/webapp/go/isubata /tmp/cpuprof <<EOF
# list main.* > prof.txt
# EOF
