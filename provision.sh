#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y build-essential python-dev python-setuptools \
                     python-numpy python-scipy python-pip \
                     libatlas-dev libatlas3gf-base
sudo update-alternatives --set libblas.so.3 \
    /usr/lib/atlas-base/atlas/libblas.so.3
sudo update-alternatives --set liblapack.so.3 \
    /usr/lib/atlas-base/atlas/liblapack.so.3

sudo pip install -U scikit-learn
sudo pip install flask
#setup virtualenv for the python environment
#sudo pip install virtualenv
#cd /vagrant && sudo pip install -r requirements.txt
#sudo pip install numpy

#http://stackoverflow.com/questions/5844869/comprehensive-beginners-virtualenv-tutorial
#http://scikit-learn.org/stable/developers/advanced_installation.html#advanced-installation
