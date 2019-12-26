


git clone https://github.com/ChenYingpeng/darknet2caffe

### darknet2caffe 依赖caffe-yolov3库

1.  安装caffe支持upsample的环境

    `git clone https://github.com/twmht/caffe`

2.  切换到 upsample 分支 支持yolov3
    `git checkout upsample`

3. 配置环境caffe编译环境
    `cp Makefile.config.example Makefile.config`
```makefile

#Uncomment if you're using OpenCV 3
OPENCV_VERSION := 3

# Whatever else you find you need goes here.
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib

# 添加以下3行支持hdf5
INCLUDE_DIRS += /usr/include/hdf5/serial/
LIBRARY_DIRS += /usr/lib/x86_64-linux-gnu/hdf5/serial
LIBRARIES += glog gflags protobuf boost_system boost_filesystem m hdf5_serial_hl hdf5_serial
```
4. 编译
    `make pycaffe`      ## 生成pycaffe库
    `make distribute`   ## 生成发布的caffe程序
5. 导出python使用的caffe库

export PYTHONPATH="`pwd`/distribute/python:$PYTHONPATH"
export LD_LIBRARY_PATH="`pwd`/distribute/lib:$LD_LIBRARY_PATH"


### 转换步骤
  First,you should install this repo https://github.com/marvis/pytorch-caffe-darknet-convert;

  Note:this repo need install pytorch and caffe.

  Second,you should install upsample_layer into caffe,please check this link https://github.com/BVLC/caffe/pull/6384/commits/4d2400e7ae692b25f034f02ff8e8cd3621725f5c.

  Finally,download yolov3.weights and run yolov3_darknet2caffe.py this file.

  	1) download yolov3.weights 

	$ wget https://pjreddie.com/media/files/yolov3.weights

	2) run yolov3_darknet2caffe.py this file in this folder (/home/xx/pytorch-caffe-darknet-convert/).

	$ python yolov3_darknet2caffe.py yolov3.cfg yolov3.weights yolov3.prototxt yolov3.caffemodel 


1. https://github.com/BVLC/caffe.git

#### Yolov3转化Caffe框架
git clone https://github.com/ChenYingpeng/darknet2caffe

Python2.7
Pytorch >= 0.40

`pip install torch==0.4.0`
Demo
$ darknet2caffe cfg[in] weights[in] prototxt[out] caffemodel[out]

Example

darknet2caffe cfg/yolov3.cfg weights/yolov3.weights prototxt/yolov3.prototxt caffemodel/yolov3.caffemodel




os.environ['PYTHONPATH']=' caffe/python:'
os.environ['LD_LIBRARY_PATH']='caffe/.build_release/lib:$LD_LIBRARY_PATH:'



### caffe 运行环境

pip install scikit-image==0.10 scipy


