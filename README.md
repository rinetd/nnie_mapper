# nnie_mapper
海思hi3516dv300 nnie_mapper 工具 for ubuntu18.04

1. 通过 darknet-yolov3训练自己的数据集生成
`./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg darknet53.conv.74`
    yolov3-voc.cfg
    yolov3-voc.weights

2. 通过 darknet2caffe 将 yolov3-voc.weights 转换为caffemodel
YOYO=yolov3_behavior
export PYTHONPATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/python:$PYTHONPATH" 
export LD_LIBRARY_PATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/lib:$LD_LIBRARY_PATH"
python darknet2caffe/darknet2caffe.py ./data/detection/yolov3_behavior/yolov3-voc.cfg ./data/detection/yolov3_behavior/yolov3-voc.weights ./data/detection/yolov3_behavior/model/yolov3-voc.prototxt ./data/detection/yolov3_behavior/model/yolov3-voc.caffemodel
	
`python ../data/detection/yolov3/cfg/yolov3-voc.cfg ../data/detection/yolov3/weights/yolov3-voc.weights ../data/caffemodel/yolov3-voc.prototxt ../data/caffemodel/yolov3-voc.caffemodel`

    yolov3.prototxt 
    yolov3.caffemodel

3. 通过 nnie_mapper_12 转换为 wk

`nnie_mapper_12 yolov3_inst.cfg`

