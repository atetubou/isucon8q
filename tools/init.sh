#!/bin/bash
set -xe
which python36 ||  sudo yum install python36-devel
which pip3 || sudo python3 -m ensurepip
which virtualenv || pip3 install virtualenv

rsync -av flask/ ~/flask/

cd ~/flask
if [ ! -f env ]; then
    virtualenv env
fi
source env/bin/activate
pip install -r requirements.txt
sudo cp negainoido.profile.service /usr/lib/systemd/system/negainoido.profile.service
sudo systemctl enable negainoido.profile.service
sudo systemctl restart negainoido.profile.service


