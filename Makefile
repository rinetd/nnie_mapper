.PHONY: all
YOYO?=yolov3-drone
YOLOV3_WEIGHTS?=yolov3-voc.weights

all:
	# - sudo cp bin/* /usr/local/bin
	- export PYTHONPATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/python:$$(PYTHONPATH)"
	- export LD_LIBRARY_PATH="/home/ubuntu/caffe/models/twmht_caffe/distribute/lib:$$(LD_LIBRARY_PATH)"
	- python darknet2caffe/darknet2caffe.py ./data/detection/$(YOYO)/cfg/yolov3-voc.cfg ./data/detection/$(YOYO)/weights/yolov3-voc.weights ./data/caffemodel/yolov3-voc.prototxt ./data/caffemodel/yolov3-voc.caffemodel
	- ./nnie_mapper/bin/nnie_mapper_12 ./nnie_mapper/yolov3_inst.cfg

clean: