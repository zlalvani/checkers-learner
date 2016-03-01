#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y build-essential

#setup virtualenv for the python environment
sudo pip install virtualenv
cd /vagrant/ && sudo pip install requirements.txt
#sudo pip install numpy

#http://stackoverflow.com/questions/5844869/comprehensive-beginners-virtualenv-tutorial