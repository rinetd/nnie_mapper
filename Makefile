.PHONY: all darknet2caffe mapper
# YOYO?=yolov3-caffe
YOYO?=yolov3_behavior
YOLOV3_WEIGHTS?=yolov3-voc

mapper:
	- ./nnie_mapper/bin/nnie_mapper_12 ./nnie_mapper/yolov3_inst.cfg

darknet2caffe:
	- export PYTHONPATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/python:$(PYTHONPATH)" 
	  export LD_LIBRARY_PATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/lib:$(LD_LIBRARY_PATH)"
	  python darknet2caffe/darknet2caffe.py ./data/detection/$(YOYO)/yolov3-voc.cfg ./data/detection/$(YOYO)/yolov3-voc.weights ./data/detection/$(YOYO)/model/yolov3-voc.prototxt ./data/detection/$(YOYO)/model/yolov3-voc.caffemodel
	#   python darknet2caffe/darknet2caffe.py ./data/detection/yolov3-caffe/cfg/yolov3-voc.cfg ./data/detection/yolov3-caffe/weights/yolov3-voc.weights ./data/detection/yolov3-caffe/model/yolov3-voc.prototxt ./data/detection/yolov3-caffe/model/yolov3-voc.caffemodel
	#   python darknet2caffe/darknet2caffe.py ./data/detection/$(YOYO)/cfg/yolov3-voc.cfg ./data/detection/$(YOYO)/weights/yolov3-voc.weights ./data/detection/$(YOYO)/model/yolov3-voc.prototxt ./data/detection/$(YOYO)/model/yolov3-voc.caffemodel


all: darknet2caffe mapper
	# - sudo cp bin/* /usr/local/bin

bgr:
	- python convert.py data/images/jueyuanzi.jpg jueyuanzi.bgr
clean: