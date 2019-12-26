import cv2 as cv
import sys
import os
import argparse
import numpy as np


# parser = argparse.ArgumentParser(description='Args')
# # parser.add_argument('--image',default='img/1531383732422-ganta.JPG')
# # parser.add_argument('--video',default=None)
# # args=parser.parse_args()
# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "data/detection/yolov3-drone/cfg/yolov3-voc-drone.cfg"
modelWeights = "data/detection/yolov3-drone/weights/yolov3-voc.weights"
classesFile = "data/detection/yolov3-drone/voc.names"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Load names of classes
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#5.画出边框
# Draw the predicted bounding box
def drawPred(frame,classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),5)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 4, 1)
    top = max(top, labelSize[1])
    cv.putText(frame, label, (left, top-20), cv.FONT_HERSHEY_SIMPLEX, 4, (0,0,255),2)
    cv.imshow("",frame)
    cv.waitKey(0)
# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame,classIds[i], confidences[i], left, top, left + width, top + height)

if __name__ == '__main__':

    img_dir='img'   #图片文件夹
    img_out_dir='img_out'  #图片输出文件夹
    if not os.path.exists(img_out_dir):
        os.makedirs(img_out_dir)

    img_list=os.listdir(img_dir)
    for item in img_list:
        img_path=os.path.join(img_dir,item)
        out_path=os.path.join(img_out_dir,item)
        img=cv.imread(img_path)
        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(img, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))

        # Remove the bounding boxes with low confidence
        postprocess(img, outs)
        # Put efficiency information. The function getPerfProfile returns the
        # overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(img, label, (5, 100), cv.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 6)
        #save img
        # cv.imwrite(out_path, img.astype(np.uint8))
        # cv.imshow("",img)
