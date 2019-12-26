#!/bin/bash

#The ubuntu version should be 1404
echo "Linux distribution should be ubuntu, linux distribution version should be 1404!"

sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev
sudo apt-get install libgoogle-glog-dev
sudo apt-get install libopenblas-dev
sudo apt-get install liblmdb-dev
sudo apt-get install libgflags-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install build-essential cmake libgtk2.0-dev pkg-config python-dev python-numpy libavcodec-dev libavformat-dev libswscale-dev

#install boost
echo "install boost"
wget --no-check-certificate https://dl.bintray.com/boostorg/release/1.68.0/source/boost_1_68_0.tar.bz2
tar -jxvf boost_1_68_0.tar.bz2
cd boost_1_68_0
./bootstrap.sh --with-libraries=system,thread,python --with-toolset=gcc
./b2 --with-python include=${ANACONDA3_HOME}"/include/python3.6m"  
sudo ./b2 install 
sudo ln -s /usr/local/lib/libboost_system.so.1.68.0 /usr/local/lib/libboost_system36.so
sudo ln -s /usr/local/lib/libboost_thread.so.1.68.0 /usr/local/lib/libboost_thread36.so
cd ..

echo "install protobuf"
wget --no-check-certificate https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-cpp-3.5.1.tar.gz
wget --no-check-certificate https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-python-3.5.1.tar.gz

tar -zxvf protobuf-cpp-3.5.1.tar.gz
mv protobuf-3.5.1 protobuf-cpp-3.5.1
tar -zxvf protobuf-python-3.5.1.tar.gz
mv protobuf-3.5.1 protobuf-python-3.5.1

cd protobuf-cpp-3.5.1
./configure
make -j4
#make check -j4  
sudo make install
sudo ldconfig

cd ..
cd protobuf-python-3.5.1
cd python
python setup.py build
python setup.py test
python setup.py install
cd ..
cd ..

echo "install caffe"

wget --no-check-certificate https://github.com/BVLC/caffe/archive/1.0.tar.gz
tar -zxvf 1.0.tar.gz
mv caffe-1.0 caffe

#make caffe
cd caffe
cp Makefile.config.example Makefile.config
sed -i 's/# CPU_ONLY := 1/CPU_ONLY := 1/' Makefile.config
sed -i 's/# USE_OPENCV := 0/USE_OPENCV := 0/' Makefile.config #这一步是否有必要
sed -i 's/# OPENCV_VERSION := 3/OPENCV_VERSION := 3/' Makefile.config
sed -i '68s/PYTHON_INCLUDE/#PYTHON_INCLUDE/' Makefile.config
sed -i '72s;# ANACONDA_HOME := $(HOME)/anaconda;ANACONDA_HOME:='$ANACONDA3_HOME';' Makefile.config
sed -i '72s/#/ /' Makefile.config
sed -i '73s/#/ /' Makefile.config
sed -i '74s/#/ /' Makefile.config
sed -i '75s/#/ /' Makefile.config
sed -i '74s/python2.7/python3.6m/' Makefile.config
sed -i '75s/python2.7/python3.6/' Makefile.config
sed -i '78s/# PYTHON_LIBRARIES := boost_python3 python3.5m/PYTHON_LIBRARIES := boost_python36 boost_thread36 boost_system36 python3.6m/' Makefile.config
sed -i '83s;PYTHON_LIB := /usr/lib;PYTHON_LIB := /usr/local/lib $(ANACONDA_HOME)/lib;' Makefile.config

sudo make all -j4
sudo make pycaffe -j4
sudo make test -j4
sudo make runtest -j4

echo "#added by caffe installer" >> $HOME/.bashrc
DIR="$( cd "$( dirname "$0"  )" && pwd  )"   # 脚本所在目录
echo $DIR
echo "export LD_LIBRARY_PATH=/usr/local/lib:$ANACONDA3_HOME/lib:\$LD_LIBRARY_PATH" >> $HOME/.bashrc
echo "export PYTHONPATH=\$env:\"$DIR/python\":\$PYTHONPATH" >> $HOME/.bashrc


cd $ANACONDA3_HOME/lib
wget --no-check-certificate http://mirrors.163.com/pypi/packages/50/f9/5c454f0f52788a913979877e6ed9b2454a9c7676581a0ee3a2d81db784a6/opencv_python-3.4.0.12-cp36-cp36m-manylinux1_x86_64.whl
pip install opencv_python-3.4.0.12-cp36-cp36m-manylinux1_x86_64.whl

sudo cp /usr/local/lib/libboost_python36.so.1.68.0 $ANACONDA3_HOME/lib
sudo cp /usr/local/lib/libboost_system.so.1.68.0 $ANACONDA3_HOME/lib
sudo cp /usr/local/lib/libboost_thread.so.1.68.0 $ANACONDA3_HOME/lib
sudo cp /usr/local/lib/libprotobuf.so.15.0.1 $ANACONDA3_HOME/lib

#pip install protobuf

echo "Please provide feedback in our support forum if you encountered difficulties."
