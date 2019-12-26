import cv2 as cv
import sys
import os
import argparse
import numpy as np

confThreshold = 0.5
nmsThreshold = 0.4
inpWidth = 416
inpHeight = 416

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3-voc.cfg"
modelWeights = "yolov3-voc_last.weights"
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# Load names of classes
classesFile = "voc.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# Draw the predicted bounding box
def drawPred(frame,classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0),2)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 2, 2)
    top = max(top, labelSize[1])
    cv.putText(frame, label, (left, top-20), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
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
        # for fighting
        tmp_id = []
        # tmp_boxes = []
        tmp_left=[]
        tmp_top=[]
        tmp_confidence = []
        tmp_centerx = []
        tmp_width = []
        tmp_centery=[]
        tmp_height=[]
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                print('detection:', detection)
                print('classId:',classId)
                print('confidence:', confidence)
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                #figting or not
                if int(classId)==1:
                    tmp_id.append(classId)
                    tmp_confidence.append(confidence)
                    # tmp_boxes.append([left, top, width, height])
                    tmp_left.append(left)
                    tmp_top.append(top)
                    tmp_centerx.append(center_x)
                    tmp_centery.append(center_y)
                    tmp_width.append(width)
                    tmp_height.append(height)
                    if len(tmp_id)==2:
                        center_distancex=tmp_centerx[1]-tmp_centerx[0]
                        if abs(center_distancex)>(tmp_width[0]+tmp_width[1])*0.5:
                            continue
                        else:
                            center_distancey=tmp_centery[1]-tmp_centery[0]
                            left_x=min(tmp_left[0],tmp_left[1])
                            top_p=min(tmp_top[0],tmp_top[1])
                            width_x=int((tmp_width[0]+tmp_width[1])*0.5+abs(center_distancex))
                            height_y=int((tmp_height[0]+tmp_height[1])*0.5+abs(center_distancey))
                            avg_confidence=float((tmp_confidence[0]+tmp_confidence[1])*0.5)
                            classIds.append(tmp_id[0])
                            confidences.append(avg_confidence)
                            boxes.append([left_x,top_p,width_x,height_y])
                if int(classId)!=1:
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

    img_dir='/input/folder'   #图片文件夹
    img_out_dir='/output/folder'  #图片输出文件夹
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
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(img, label, (5, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        #save img
        cv.imwrite(out_path, img.astype(np.uint8))






