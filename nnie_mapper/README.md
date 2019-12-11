# nnie_mapper
海思hi3516dv300 nnie_mapper 工具 for ubuntu18.04


## 第一部分： Ubuntu18.04 nnie_mapper_12 环境安装
参考文档 《HiSVP 开发指南》3.4节 Linux 版 NNIE mapper 安装
    linux 版本的 NNIE mapper 编译环境：ubuntu 14.04, gcc 4.8.5, protobufall-3.5.1, OpenCV 3.4.2.1 
 
查看 nnie_mapper_12 运行依赖项
    `ldd nnie_mapper_12`
        linux-vdso.so.1 (0x00007fff0cd2f000)
        libprotobuf.so => /usr/local/lib/libprotobuf.so (0x00007f033dd44000)
        libopencv_core.so.3.4 => /usr/local/lib/libopencv_core.so.3.4 (0x00007f033d737000)

注意 ：
1. 你的gcc的版本最好是4.8，我的是4.8.5，而且你的protobuf需要是在这个版本下编译的，否则会报错 undefined symbol: _ZN6google8protobuf8internal26fixed_address_empty_stringE
2. nnie mapper的源代码不开放，只有可执行文件。而根据<Hisvp开发指南>，它们是在ubuntu14.04， protobuf3.5.1，opencv3.4.0以及gcc4.8.5上编译出来的。
所以直接来运行nnie mapper可执行文件，肯定会遇到一些问题。我们这里只考虑cpu版本，因为gpu版本依赖库更多，更复杂。

用命令：`nm -s libprotobuf.so|grep _ZN6google8protobuf8internal26fixed_address_empty_stringE `会发现有这个符号，但是多了B5cxx11，这个是和编译程序的gcc程序有关系，由于protobuf的源码中含有c++程序，所以需要使用gcc4.8.5和g++4.8.5来编译protobuf才行。


### 3.4.1 mapper 依赖库 Protobuf 安装与配置

请至 https://github.com/google/protobuf/releases/tag/v3.5.1 ，进入下载页面点击 protobufall-3.5.1.tar.gz：

```sh
cd  protobuf-3.5.1

./autogen.sh
./configure  --prefix=/usr/local/protobuf  # 默认--prefix=/usr/local/lib/libprotobuf.so 为了与protobuf-2.5.0分开来，设定配置目录
make
make check
sudo make install
# sudo make unisntall # 卸载
```

export PATH=/home/test/protobuflib/protobuf-3.5.1/bin:$PATH
export LD_LIBRARY_PATH=/home/test/protobuflib/protobuf-3.5.1/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=/home/test/protobuflib/protobuf-3.5.1/lib/pkgconfig

### 3.4.2 mapper 依赖库 OpenCV 安装与配置 3.4.2.1 OpenCV 安装包下载
请到 OpenCV 的官方网站:http://opencv.org/releases.html 下载 Opencv3.4.2

 wget https://github.com/Itseez/opencv/archive/3.4.2.zip
```sh 
mkdir build && cd build 
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local/opencv \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=ON .. 
    
make -j $(nproc)
        sudo make install
		sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
		sudo ldconfig
```
## 第二部分： 使用 nnie_mapper_12 将 caffe 模型转换 wk 模型

注意：marked_prototxt 是选择自己的caffe model后自动生成的并更新的，无法自己填写。理论上是每次选择caffe文件后都会自动生成一个并更新过去，有时软件问题会生成文件但无法自动更新，此时需要将.cfg文件 open with -  text， 在文件的第一行自己填写在mark_prototxt下最新生成的结构文件

文件准备：


模型转换命令：

`nnie_mapper_12 yolov3_inst.cfg`

yolov3_inst.cfg 文件介绍：
```s
[prototxt_file]  ./yolov3.prototxt        # caffe 的prototxt  
[caffemodel_file] ./yolov3.caffemodel     # caffe 的model文件
[batch_num] 1                            # [单张模式/多张模式]
[net_type] 0                             
[sparse_rate] 0                          # 0 - 不稀疏处理 0.5 - 0.5稀疏
[compile_mode] 1                         # 0 - 高速模式损失精度 1 - 高精度模式
[is_simulation] 0                        # 【0 - inst芯片模式,芯片中运行必须为0】, 1 - func 仿真模式用于pc端 
[log_level] 2
[instruction_name] ./data/yolov3_inst            # 【生成NNIE模型*.wk文件名】
[image_list] ./file_list.txt             # 用于存储数据的决定路径，30张左右的样例数据用于量化模型
[image_type] 1                           # 1 - 表示网络数据输入为 SVP_BLOB_TYPE_U8(普通的灰度图和RGB图)类型; 此时要求 image_list 配置是 RGB 图或者灰度图片的 list 文件;
[RGB_order] BGR 
[internal_stride] 16                     # align_byte 数据的维度必须是16的倍数，否则按16的倍数补全，默认为16，修改无效

[norm_type] 3                            # 0 - 不做预处理 5 - 减通道均值后再乘以 data_scale
[data_scale] 0.0039062                           # 0.00390625 = 1/ 256；1 就是不缩放
[mean_file] ./mean.txt                   # 均值文件，用于数据的标准化，每行代表一个通道要减去的值

```
```s
[prototxt_file] ./mark_prototxt/yolov3_mark_nnie_20191210173440.prototxt
[caffemodel_file] ./../data/detection/yolov3/model/yolov3.caffemodel
[batch_num] 1
[net_type] 0
[sparse_rate] 0
[compile_mode] 0
[is_simulation] 1          # func 功能仿真
[log_level] 2
[instruction_name] ./../data/detection/yolov3/inst/inst_yolov3_func
[RGB_order] BGR
[data_scale] 0.0039062
[internal_stride] 16
[image_list] ./../data/detection/yolov3/image_ref_list.txt
[image_type] 1
[mean_file] null
[norm_type] 3

```



大家知道，深度学习算法模型在推理前，都会对图像数据进行预处理，即RGB三个通道上的数据(0~255) normalize成0~1以内的值。值得注意的是，normalize方式有好几种，而且不同的算法模型所采用的预处理方式还不太一样。这就要求在nnie开发中，将caffe算法模型转换成wk文件时，必须选择合适的预处理方式。否则可能会导致识别结果不正常。

norm_type:  normalize方式的解释

在使用Ruyistudio进行模型文件转换时，支持下面5中方式，如下所示

下面对这5种方式分别进行解释：

1） mean file：

如果选择这种norm type， 就要选择一个后缀名为binaryproto的文件。 它是caffe框架中常用的一种均值数据格式。常见的做法就是统计train lmdb里面图像数据的均值（每个像素的每个channel累加和再除以image size）。其对应预处理方式是将待识别的图像每个像素值减去binaryproto里面对应的像素值。

2）channel mean value

该方式对应的均值文件就是里面含3个channel均值的txt文件，如mobilenet ssd的就是 127.5 127.5 127.5。 其预处理过程就是将图像上每个像素的三个通道数据分别减去127.5。注意，经过该预处理后，图像数据并没有normalize成0~1范围内。

3）data scale

顾名思义就是直接对图像数据除以255缩小到0~1内。1/255=0.0039216，但其缺省的scale值为1/256=0.0039062。

4）mean file with data scale

上面提到，光减去mean值，并不能使得图像数据落入到绝对值0~1范围内，所以，一般地，需要在这个基础上再做一个scale。

5）channel mean value with data scale

同上，每个像素的各个通道减去mean value后还得再除以mean value。  还是以mobilenet ssd为例子，减去127.5后还得再乘以scale值0.007843（约等于1/127.5)。



本博文则是讲解如何在linux环境中来运行nnie mapper。在海思sdk里面已经提供了nnie mapper的可执行文件，其父目录为mapper，如下红框所示。



在mapper里面有两个版本，分别为cpu和gpu版本。注意一下，for 3519av100， 其nnie mapper版本为1.2。



另外一个需要注意的地方就是，nnie mapper的源代码不开放，只有可执行文件。而根据<Hisvp开发指南>，它们是在ubuntu14， protobuf3.5.1，opencv3.4.0以及gcc4.8.5上编译出来的。所以直接来运行nnie mapper可执行文件，肯定会遇到一些问题。我们这里只考虑cpu版本，因为gpu版本依赖库更多，更复杂。

问题
下面就我遇到的问题进行逐一分析。

1）找不到opencv相关库。 先运行命令： readelf -d nnie_mapper_12 看看该可执行文件都依赖什么opencv库。



下载opencv3.4.x版本的代码，去掉opencv_world勾项，重新编译即可生成包括上面红框所示的库，然后将这三个库拷到/usr/lib/下面即可。

2）第二个问题则比较麻烦。如上图所示，该可执行文件还需要libprotobuf.so，所以按照开发指南，先下载对应版本的protobuf源代码，然后进行编译。



解压缩后，在其根目录下创建build子目录，然后进入build，输入下面命令：

sudo cmake -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_BUILD_SHARED_LIBS=ON DCMAKE_INSTALL_PREFIX=/home/test/protobuflib/protobuf-3.5.1 ../cmake
最后输入命令进行编译：sudo make -j8。 编译完后，将build目录中生成的libprotobuf.so拷贝到/usr/lib下面。

重点来了，这时遇到另外一个错误：



通`·nm -s libprotobuf.so | grep google8protobuf8internal26fixed_address_empty` 可以发现实际上libprotobuf.so里面是有下面这个符号的：_ZN6google8protobuf8internal26fixed_address_empty_stringEB5cxx11，即多了字符串：B5cxx11。后来查明是和gcc版本有关系。需要使用gcc4.8.5来编译protobuf源代码重新生成libprotobuf.so才能解决这个问题。

安装gcc-4.8.5，并切换gcc version到4.8.5的命令如下：

sudo apt-get install gcc-4.8
 
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 100
这时输入命令： gcc --version 发现打印出来的gcc版本号变成4.8了。 但是重新编译protobuf代码，却发现问题依旧在。

后来才知道， 因为protobuf里面有cpp文件，所以g++也要切换成4.8

sudo apt-get install g++-4.8
 
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/g++-4.8 100
将生成的新libprotobuf.so拷贝到/usr/lib/，重新输入如下类似的命令，就能够运行成功。当然要保证参数xxxfunc.cfg里面的路径是正确的。

nnie_mapper_12 ./data/classification/alexnet/alexnet_no_group_func.cfg 


 NNIE 板端运行、仿真，必须按上表的芯片型号和 mapper 版本匹配，否则可能出现
意想不到的错误。
 GPU 版本的 nnie_mapper 都需要安装 CUDA8.0。
 GPU 版本 mapper 和 CPU 版本的 mapper 编译出来的 wk 会有不同的地方，原因是
cuda 版本和 CPU 版本浮点的表示引起，caffe 的 CPU 和 GPU 版本也会有些许差
异。
### 3.5.2 配置文件说明
nnie_mapper 配置选项说明如表 3-6 所示。
表3-6 nnie_mapper 配置选项说明
配置选项 取值范围 描述
prototxt_file - 网络描述文件，详细要求见 3.2 “Prototxt 要求”，描
述外支持情况与 caffe 相同。
net_type {0, 1, 2} 网络的类型。
0：CNN（不包含
LSTM/RNN/ROIPooling/PSROIPooling 的任意网
络）；
1：ROI/PSROI（包含 ROI Pooling 和 PSROI Pooling
的网络）；
2：Recurrent（包含 LSTM、RNN 的网络）；
caffemodel_file - 网络模型数据文件。
image_list - NNIE mapper 用于数据量化的参考图像 list 文件或
feature map 文件。该配置跟 image_type 相关。
NNIE mapper 量化时需要的图片是典型场景图片，建
议从网络模型的测试场景随机选择 20~50 张作为参考
图片进行量化，选择的图像要尽量覆盖模型的各个场
景（图像要包含分类或检测的目标，如分类网的目标
是苹果、梨、桃子，则参考图像至少要包含苹果、
梨、桃子。比如检测人、车的模型，参考图像中必须
由人、车，不能仅使用人或者无人无车的图像进行量
化）。图片影响量化系数，选择典型场景的图片计算
出来的量化系数对典型场景的量化误差越小。所以请
不要选择偏僻场景、过度曝光、纯黑、纯白的图片，
请选择识别率高，色彩均匀的典型场景图片。
网络中如果存在多个输入层，则需要配置多个
image_list 顶，顺序、个数与 prototxt 完全对应。
如果网络的数据输入是灰度或者 RGB 图像输入，即
image_type 配置不为 0，image_list 配置为所有参考图

配置选项 取值范围 描述
片的 list，内容示意如下图图示，图片的格式支持以下
几种：
".bmp", ".dib", ".jpeg", ".jpg", ".jpe", ".jp2", ".png", 
".webp", ".pbm", ".pgm", ".ppm", ".sr", ".ras", ".tiff", 
".tif", ".BMP", ".DIB", ".JPEG", ".JPG", ".JPE", ".JP2", 
".PNG", ".WEBP", ".PBM", ".PGM", ".PPM", ".SR", 
".RAS", ".TIFF", ".TIF"
如果网络的输入是 feature map 或者 FC 向量输入，即
image_type 配置为 0，将 c*h*w 个点（即一个完整的
张量）以浮点文本的形式输出在一行内，点与点之间
以空格或逗号分隔。如果是多帧输入，则每一行输出
一个完整的张量。图示如下：
Recurrent 输入时，格式等同于 feature map 输入，每行
一个向量，一句话写成连续的多行，多句量化时需要
将每一句的帧数都补齐为最大帧数。
image_type {0,1,3,5} 表示网络实际执行时输入给网络的数据类型，该配置
跟 image_list 相关。
0：表示网络数据输入为 SVP_BLOB_TYPE_S32（参
考《HiSVP API 参考》）或者向量的类型（VEC_S32
和 SEQ_S32）；此时要求 image_list 配置为 feature
map 文件；
1：表示网络数据输入为 SVP_BLOB_TYPE_U8（普通
的灰度图和 RGB 图）类型； 此时要求 image_list 配
置是 RGB 图或者灰度图片的 list 文件；
3：网络数据输入为 SVP_BLOB_TYPE_YUV420SP 类
型；
5：网络数据输入为 SVP_BLOB_TYPE_YUV422SP 类
型；
当配置为 3 或者 5 时，image_list 配置为 RGB 图片的
list 文件。
norm_type {0, 1, 2, 3, 表示对网络数据输入的预处理方法。注意 image_type 

配置选项 取值范围 描述
4, 5} 配置为 0 时，norm_type 只能配置为 0；image_type 配
置为 3 或者 5 时，网络输入数据为 YUV 图像，但是
NNIE 硬件会根据 RGB_order 配置项自动转为 RGB 或
者 BGR 图像，此时 norm_type 配置方法跟 image_type
为 1 时一致。
0：不做任何预处理；
1：mean file，减图像均值；
2：channel mean_value，减通道均值；
3：data_scale，对图像像素值乘以 data_scale；
4：mean filewith data_scale，减图像均值后再乘以
data_scale；
5：channel mean_value with data_scale，减通道均值后
再乘以 data_scale。
data_scale (1/4096, 
FLT_MA
X)
default: 
0.0039062
5
数据预处理缩放比例，配置为浮点数，配合
norm_type 使用
本参数可省略，默认为 0.00390625=1/256。FLT_MAX
等于 3.402823466e+38。
mean_file - norm_type 为 1、4 时，表示均值文件
xxx.binaryproto；
norm_type 为 2、5 时，表示通道均值文件；
norm_type 为 0、3 时，用户也需要配置 mean_file
项，但具体内容可以是一个无效路径，比如 null；通
道均值文件 mean.txt 中每一行的浮点数表示对应的通
道均值，如单通道只有一个值。
batch_num [0, 256]
default: 
256
0/1：single（单张）模式；
>1：batch（多张）模式。
采用 single 模式 mapper 一个任务只能处理一张图片，
内部存储全部为一张图片分配，减少数据调度次数。
采用 batch 模式，在计算 FC 时 batch_num 张图片同时
计算，计算资源利用率高。
sparse_rate [0, 1]
default: 0
NNIE 引擎采用了参数压缩技术以减少带宽占用，为
了提高压缩率，可通对 FC 参数进稀疏处理。
用户通过 sparse_rate 数值指定多少比例的 FC 参数稀
疏为 0，例如配 0.5，则 FC 参数有 50%将被稀疏为
0，由于数据变的稀疏，压缩模块会获得更好的压缩
率。稀疏值越高，计算 FC 时所需参数带宽越低，但
精度会有所下降。
compile_mode {0, 1, 2} 0：Low-bandwidth(低带宽模式，默认)：通过量化算
法使参数与数据位宽最少，使系统所需带宽达到最


配置选项 取值范围 描述
default: 0 小，但会有精度损失；
1：High-precision(高精度模式): 结果精度最好，但是
性能会下降；；
2：User-specify(用户配置模式): 需要用户在 prototxt
中标明所有使用高精度计算的层，标注规则请见
prototxt_file 说明；
compress_mode {0, 1}
default: 0
配置压缩模式。
0：Normal 模式（包含 Normal、Ternary、Binary、
Sparse 四种压缩模式的自动切换）；
1：Bypass 模式，关闭压缩功能。
要求：
可不填，默认为 Normal 模式；用户提供的参数只有
三种值且正负对称时，nnie_mapper 会自动进入
Ternary 模式；用户提供的参数只有两种值且包含 0
时，nnie_mapper 会自动进入 Binary 模式；
max_roi_frame_
cnt
[1, 5000]
default: 
300
包含 ROI/PSROI 网络的 RPN 阶段输出的候选框最大
数目。
默认值：300。
roi_coordinate_f
ile
- Mapper 在网络模型转化过程中输入给 ROI Pooling 或
PSROI Pooling 层的配置参数，用于指定 ROI 框的坐
标信息，每一行五个值，分别代表 batch_index(int)、
left_x（float）、top_y（float）、right_x（float）、
bottom_y（float），不同的框以换行符分隔。
框坐标是在 caffe 中使用输入给 mapper 的 image_list
的相同图片运行到 RPN 层的输出结果，如 Faster
RCNN 网络中 Proposal 层的 top 为 rois，在 caffe 
forward 结束后，通过 np.savetxt('rois.txt', 
net.blobs['rois'].data[...], fmt="%.6f") 保存框坐标为文
件。需要保证两者图片输入顺序相同，同时要保证
caffe 运行时输入给网络的分辨率跟配置给 mapper 的
prototxt 中的分辨率相同。
For example:
0 734.01 147.02 806.03 294.04
0 723.05 157.06 818.07 306.08
1 749.09 170.10 817.11 310.12
1 678.13 220.14 855.15 374.16
如果一个网络中有多个 ROI Pooling 或 PSROI Pooling
层，则需要配置多行坐标文件，个数与 ROI Pooling
或 PSROI Pooling 层个数对应，配置的顺序也需要与
prototxt 内对应层顺序相同；
is_simulation {0, 1} 网络模型转化类型


配置选项 取值范围 描述
default: 0 0：Chip，芯片模式，网络模型转化成在芯片上加载的
wk 文件，指令仿真也使用此模式；
1：Simulation，仿真模式，网络模型转化成在 PC 端
仿真上加载的 wk 文件，功能仿真使用此模式；
instructions_na
me
string 
length <
120
default: 
inst
nnie_mapper 生成的知识库文件名称。
默认生成如下格式的知识库名：inst.wk；用户也可以
自行修改生成的知识库名字。
internal_stride {16, 32}
default: 16
用户根据 DDR 颗粒对应的最佳读写效率配置中间结
果的对齐方式。
要求：
DDR3 对应 16，DDR4 对应 32，可不填，默认为 16；
is_check_protot
xt
{0, 1}
default: 0
检查网络描述文件标志。
0：mapper 模式，对 prototxt、caffemodel 等进行转
化。
1：网络过滤器模式，对 prototxt 文件是否符合支持规
格进行检查。
log_level {0, 1, 2, 3}
default: 0
设置是否开启日志文件，以及配置打印的等级，本参
数可省略，当省略时，为不打印日志文件。
0：打印 main 函数流程，cfg 文件等信息；
1：打印 nnie_mapper 解析到的文件信息，包含
image_list、prototxt、内存分配过程；
2：打印中间表示信息；
3：打印详细信息，有大量文件输出，转化耗时较
长，请谨慎使用；
recurrent_tmax [1, 1024]
default: 
1024
Recurrent 网络（包含 LSTM/RNN 层）每一句话的最
大桢数，支持[1, 1024]范围内的配置，减小配置值可
以减小临时缓存大小。
RGB_order {RGB, 
BGR}
default: 
BGR
image_type 设置为 0 时，该参数无效；
image_type 设置为 1 时，表示输入给网络的 RGB 图像
的 RGB 三通道的顺序；
image_type 设置为 3、5 时，表示 YUV 图像数据转成
RGB Planar 或者 BGR Planar 图像输入给网络。
本参数可省略


