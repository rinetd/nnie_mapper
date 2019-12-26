.PHONY: caffe



caffe:
	- cd caffe;git checkout upsample;cp Makefile.config.example Makefile.config
		sed -i -e 's/# CPU_ONLY := 1/CPU_ONLY := 1/' \
		-e 's/# USE_OPENCV := 0/USE_OPENCV := 0/' \
		-e 's/# OPENCV_VERSION := 3/OPENCV_VERSION := 3/'  caffe/Makefile.config
caffe-clone:
	- git clone https://github.com/twmht/caffe


clean: