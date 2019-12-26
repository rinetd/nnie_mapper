#!/bin/bash

#install anaconda3
echo "install anaconda3"
ANACONDA3_HOME=$HOME/anaconda3
wget --no-check-certificate https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh
sh ./Anaconda3-5.2.0-Linux-x86_64.sh

#Get installation location
ANACONDA3_HOME_ORIG=$ANACONDA3_HOME
read -e -p "Enter installation location (default: $ANACONDA3_HOME, press enter for default location): " ANACONDA3_HOME
ANACONDA3_HOME=${ANACONDA3_HOME:-$ANACONDA3_HOME_ORIG}
echo $ANACONDA3_HOME

echo "add anaconda lib path to /etc/ld.so.conf.d/anaconda3.conf"
echo "$ANACONDA3_HOME/lib" >> /etc/ld.so.conf.d/anaconda3.conf
echo "export ANACONDA3_HOME="${ANACONDA3_HOME} >> $HOME/.bashrc
