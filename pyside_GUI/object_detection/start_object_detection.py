#######################################################
# Tensorflow object detection with inference graph 
# Author: You-Hao Chang, 2017/09/22
#
# required input file(s):
#
# 1) graph.pb             -> sys.argv[1]
# 2) label_map.pbtxt      -> sys.argv[2]
# 3) number of classes    -> sys.argv[3]
# 4) input list of images -> sys.argv[4]
# 5) show image or not    -> sys.argv[5]
# 6) gray scale or not    -> sys.argv[6]
#######################################################

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time

from collections import defaultdict
#from io import StringIO

from matplotlib import pyplot as plt
from PIL import Image

from object_detection.utils import label_map_util
import visualization_utils_yhc as vis_util

# path to frozen detection graph. 
# This is the actual model that is used for the object detection.
PATH_TO_CKPT = sys.argv[1]

# list of the strings that is used to add correct label for each box.
PATH_TO_LABELS = sys.argv[2]

# number of object categories exist in this model
# which will be extracted from label_map.pbtxt
NUM_CLASSES = sys.argv[3]

# initialize a TF graph
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    if not int(sys.argv[6]):
        return np.array(image.getdata()).reshape(
              (im_height, im_width, 3)).astype(np.uint8)
    else: # gray scale
        return np.repeat(np.array(image.getdata()).reshape(
            (im_height, im_width, 1)), 3, 2).astype(np.uint8) 

# list of input image data
FILE_LIST_OF_IMAGE = open(sys.argv[4], 'r')
TEST_IMAGE_PATHS = []
for line in FILE_LIST_OF_IMAGE.readlines():
    TEST_IMAGE_PATHS.append(line.strip())
FILE_LIST_OF_IMAGE.close()

# create output directory (image and text information)
output_directory = 'output_'+time.strftime("%Y%m%d%H%M%S", time.localtime())
os.system('mkdir '+output_directory)
sys.stdout.write('output files will be stored in '+os.getcwd()+'/'+output_directory)
sys.stdout.flush()

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

# output text check
if os.path.isfile(output_directory+'/objection_detection_results.txt'):
    os.system('rm -f'+output_directory+'/objection_detection_results.txt')
    
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        for num, image_path in enumerate(TEST_IMAGE_PATHS):

            image = Image.open(image_path)

            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = load_image_into_numpy_array(image)

            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run([boxes, scores, classes, num_detections],
                                                                 feed_dict={image_tensor: image_np_expanded})

            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(image_np,
                                                               np.squeeze(boxes),
                                                               np.squeeze(classes).astype(np.int32),
                                                               np.squeeze(scores),
                                                               category_index,
                                                               use_normalized_coordinates=True,
                                                               line_thickness=2,
                                                               image_name=image_path.strip().split('/')[-1],
                                                               output_text=output_directory+'/objection_detection_results.txt')

            #plt.figure(figsize=IMAGE_SIZE)
            fig = plt.figure(frameon=False, figsize=(image_np.shape[0]/100., image_np.shape[1]/100.))
            ax = plt.Axes(fig, [0., 0., 1., 1.])
            
            ax.set_axis_off()
            fig.add_axes(ax)
    
            ax.imshow(image_np, aspect='auto')
            fig.savefig(output_directory+'/'+image_path.strip().split('/')[-1])

            if int(sys.argv[5]):
                plt.show()
