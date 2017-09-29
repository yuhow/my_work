##############################################
# Tensorflow record/sample generator
# Author: You-Hao Chang (yuhow), 2017/09/13
#
# required input file(s):
#
# 1) annotation.txt     -> sys.argv[1]
# 2) label_map.pbtxt    -> sys.argv[2]
# 3) directory of image -> sys.argv[3]
##############################################

import sys
import hashlib
import io
import logging
import os
import random
import re

from lxml import etree
import PIL.Image
import tensorflow as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util

flags = tf.app.flags
flags.DEFINE_string('data_dir', '', 'Root directory to user-provided dataset.')
flags.DEFINE_string('output_dir', '', 'Path to directory of output TFRecords.')
FLAGS = flags.FLAGS

# setting of logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='TFRecord_logging.txt')
logging.info('Start to generating Tensorflow record/sample(s)')

def dict_to_tf_example(data,
                       label_map_dict,
                       image_subdirectory,
                       ignore_difficult_instances=False):
    """
    Convert user-defined dict to tf.Example proto.
    
    Notice that this function normalizes the bounding box coordinates provided
    by the raw data.
    
    Args:
        data: dict holding fields for a single image 
        label_map_dict: A map from string label names to integers ids.
        image_subdirectory: String specifying subdirectory within the
            Pascal dataset directory holding the actual image data.
        ignore_difficult_instances: Whether to skip difficult instances in the
            dataset (default: False).
    
    Returns:
        example: The converted tf.Example.
    
    Raises:
        ValueError: if the image pointed to by data['filename'] is not a valid JPEG
    """
    
    data = data.strip().split()
    
    img_path = os.path.join(image_subdirectory, data[0])
    
    with tf.gfile.GFile(img_path, 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = PIL.Image.open(encoded_jpg_io)

    if image.format != 'JPEG':
        raise ValueError('Image format not JPEG')

    key = hashlib.sha256(encoded_jpg).hexdigest()
    
    width, height = image.size
    
    num_boxes = len(data[1:])/5
    
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []
    truncated = []
    poses = []
    difficult_obj = []
    
    for i in xrange(num_boxes):
        xmin.append(int(data[1 + 5 * i]))
        ymin.append(int(data[2 + 5 * i]))
        
        xmax.append(int(data[3 + 5 * i]))
        ymax.append(int(data[4 + 5 * i]))
        
        xmin[-1] = float(xmin[-1]) / width
        ymin[-1] = float(ymin[-1]) / height
        xmax[-1] = float(xmax[-1]) / width
        ymax[-1] = float(ymax[-1]) / height
        
        classes.append(int(data[5 + 5 * i]))
        
        classes_text.append(label_map_dict[classes[-1]].encode('utf8'))
        truncated.append(0)
        poses.append('Frontal'.encode('utf8'))
        difficult_obj.append(0)
    
    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(
            data[0].encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(
            data[0].encode('utf8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
        'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
        'image/object/truncated': dataset_util.int64_list_feature(truncated),
        'image/object/view': dataset_util.bytes_list_feature(poses),
    }))
    return example


def create_tf_record(output_filename,
                     label_map_dict,
                     annotations_dir,
                     annotation_file,
                     image_dir,
                     examples):
    """
    Creates a TFRecord file from examples.
    
    Args:
        output_filename: Path to where output file is saved.
        label_map_dict: The label map dictionary.
        annotations_dir: Directory where annotation files are stored.
        image_dir: Directory where image files are stored.
        examples: Examples to parse and save to tf record.
    """
    with tf.gfile.GFile(os.path.join(annotations_dir, annotation_file)) as fid:
        lines = fid.readlines()

        writer = tf.python_io.TFRecordWriter(output_filename)

        for idx, example in enumerate(examples):
            if idx % 100 == 0:
                logging.info('On image %d of %d', idx, len(examples))
                print ' On image {0} of {1}'.format(idx, len(examples))

            pos = 0
            while pos < len(lines):
                line = lines[pos]
                line = line.strip().split()

                if len(line) != 0:
                    if line[0] == example:
                        break
                pos += 1

            if pos >= len(lines):
                logging.info('filename not found in '+annotation_file)

            tf_example = dict_to_tf_example(lines[pos], label_map_dict, image_dir)
            writer.write(tf_example.SerializeToString())
        
        writer.close()

def main(_):

    data_dir = FLAGS.data_dir
    
    label_map_dict = label_map_util.get_label_map_dict(sys.argv[2])
    
    tmp_dict = {}
    for key in label_map_dict:
        tmp_dict[label_map_dict[key]] = key
    
    label_map_dict = tmp_dict
    
    logging.info('Reading from user-provided dataset.')
    
    image_dir = os.path.join(data_dir, sys.argv[3])
    annotations_dir = os.path.join(data_dir, '')
    
    with tf.gfile.GFile(os.path.join(annotations_dir, sys.argv[1])) as fid:
        lines = fid.readlines()
    
    examples_list = [line.strip().split()[0] for line in lines if line.rstrip() != '']
    #examples_list = [line.strip().split()[0] for line in lines]
    print examples_list
    
    # random seed is not necessary. user can switch it off.
    #random.seed(42)
    #random.shuffle(examples_list)
    num_examples = len(examples_list)
    num_train = int(1 * num_examples)
    
    train_examples = examples_list[:num_train]
    val_examples = examples_list[num_train:]
    
    #logging.info('%d training and %d validation examples.', len(train_examples), len(val_examples))
    logging.info('%d training examples.', len(train_examples))
    
    train_output_path = os.path.join(FLAGS.output_dir, 'train.record')
    val_output_path   = os.path.join(FLAGS.output_dir, 'val.record')
    
    print 
    print " _________________________________________________________________________ "
    print "|_________________________________________________________________________|"
    print "|oooooooo_ooooooo_______ooooooo________________________________________oo_|"
    print "|___oo____oo____________oo____oo___ooooo___ooooo___ooooo__oo_ooo___oooooo_|"
    print "|___oo____oooo__________oo____oo__oo____o_oo___oo_oo___oo_ooo___o_oo___oo_|"
    print "|___oo____oo______ooooo_ooooooo___ooooooo_oo______oo___oo_oo______oo___oo_|"
    print "|___oo____oo____________oo____oo__oo______oo______oo___oo_oo______oo___oo_|"
    print "|___oo____oo____________oo_____oo__ooooo___ooooo___ooooo__oo_______oooooo_|"
    print "|_________________________________________________________________________|"
    print "|___oooo____________________________________________oo____________________|"
    print "|_oo____oo__ooooo__oo_ooo___ooooo__oo_ooo___ooooo___oo_____ooooo__oo_ooo__|"
    print "|oo________oo____o_ooo___o_oo____o_ooo___o_oo___oo_oooo___oo___oo_ooo___o_|"
    print "|oo____ooo_ooooooo_oo____o_ooooooo_oo______oo___oo__oo____oo___oo_oo______|"
    print "|_oo____oo_oo______oo____o_oo______oo______oo___oo__oo__o_oo___oo_oo______|"
    print "|___oooo____ooooo__oo____o__ooooo__oo_______oooo_o___ooo___ooooo__oo______|"
    print "|_________________________________________________________________________|"
    print "|_________________________________________________________________________|"
    print
    print "|| -- Object Detection --"
    print "|| Tensorflow Record/Sample Generator-v0.5"
    print "|| Copyright (c) yuhow-git. All rights reserved."
    print
    print " generating training data set, train.record"
    create_tf_record(train_output_path, label_map_dict, annotations_dir, sys.argv[1], image_dir, train_examples)
    #print " generating verification data set, val.record"
    #create_tf_record(val_output_path,   label_map_dict, annotations_dir, sys.argv[1], image_dir, val_examples)
    print " All done!"
    print
    print " More information is recored in log file 'TFRecord_logging.txt'."
    print
    

if __name__ == '__main__':
    tf.app.run()
