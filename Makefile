.PHONY 
YOLOV3_WEIGHTS?=yolov3-voc.weights
all:
	# - sudo cp bin/* /usr/local/bin
	- python darknet2caffe/darknet2caffe.py ./data/detection/yolov3/cfg/yolov3-voc.cfg ./data/detection/yolov3/weights/yolov3-voc.weights ./data/caffemodel/yolov3-voc.prototxt ./data/caffemodel/yolov3-voc.caffemodel
	- ./nnie_mapper/bin/nnie_mapper_12 ./nnie_mapper/yolov3_inst.cfg

clean: