#!/bin/bash
cd $(dirname $0)

HOSTNAME=$(hostname)

export $(cat /home/isucon/torb/webapp/env.sh)

# Do not add '/'
ruby stat.rb '^/api/events/\d+/actions/reserve$' \
             '^/api/users/\d+$' \
             '^/api/events/\d+/sheets/./\d+/reservation$' \
             '^/admin/api/reports/events/\d+/sales$' \
             '^/api/events/\d+/sheets/\s/\d+/reserve$' \
             '^/api/events/\d+$' \
             < /var/log/nginx/main_access.log | tee stat_$HOSTNAME.txt
go tool pprof -list='main.*' /tmp/cpuprofile | tee cpuprofile_$HOSTNAME.txt | python parse_cpuprofile.py | tee stat_go_$HOSTNAME.txt
# /usr/local/go/bin/go tool pprof ~/isubata/webapp/go/isubata /tmp/cpuprof <<EOF
# list main.* > prof.txt
# EOF
