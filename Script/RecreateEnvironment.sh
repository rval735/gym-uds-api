#!/bin/sh

### This script will set up an environment to run OpenAI gym on a new VM running
### Ubuntu 18.04. It will install all components necessary to replicate an
### environment to run the gym correctly on a VM. Also, it will will install the
### gym-uds dependencies needed to communicate with other executions (C++, Haskell)
### Consider that Python3 is installed along with pip3

### Install OpenAI Gym
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3-dev python3-pip zlib1g-dev libjpeg-dev cmake swig python-pyglet python3-opengl libboost-all-dev libsdl2-dev libosmesa6-dev patchelf ffmpeg xvfb
python3 -m pip3 install --upgrade pip3
pip3 install gym

### Install Protocol Buffers
sudo apt install autoconf automake libtool curl make g++ unzip -y
cd protobuf
git submodule update --init --recursive
./autogen.sh
./configure
make
sudo make install
sudo ldconfig
cd ~

### Install grpcio
pip3 install grpcio --user
pip3 install grpcio-tools --user
sudo apt-get install build-essential autoconf libtool pkg-config -y
git clone -b v1.20.0 https://github.com/grpc/grpc
cd grpc
git submodule update --init
make
sudo make install
sudo ldconfig
cd ~

### Install gym-uds-api
git clone https://github.com/rval735/gym-uds-api/l
cd gym-uds-api
git checkout MultipleActions
cd ~

### install Zweifel library
git clone https://github.com/zweifel/zweifel.git
cd zweifel/src
./create_all_libs.sh
cd ..
PATH_TO_ZWEIFEL_LIBRARY=$(pwd)/lib
cd ~

### install BiSUNA
git clone git@bitbucket.org:rval735/suna.git
