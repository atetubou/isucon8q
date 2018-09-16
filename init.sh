#!/bin/bash
set -eux

cd $(dirname $0)

(
    cd webapp/go && make
)

# sudo systemctl stop cco.golang.service
# rm -rf ~/webapp/go/app
# cp webapp/go/app ~/webapp/go/app
# rsync -av webapp/public/ ~/webapp/public/
# cp env.sh ~/env.sh

#(
#    source env.sh;
#    mysql -h $ISU_DB_HOST -u $ISU_DB_USER -p$ISU_DB_PASSWORD < adding_column.sql || true
#)


sudo rsync -av etc/nginx/ /etc/nginx/
# sudo rsync -av etc/my.cnf /etc/my.cnf
# sudo rsync -av etc/my.cnf.d/ /etc/my.cnf.d/
# rsync -av etc/sysctl.conf /etc/
# rsync -av etc/security/ /etc/security/

# sudo service mariadb restart
# sudo rm -rf /var/log/nginx/main_access.log
sudo systemctl disable h2o.service
sudo systemctl stop h2o.service
sudo systemctl enable nginx.service
sudo systemctl restart nginx.service

# sudo systemctl restart cco.golang.service
# time curl localhost/initialize
