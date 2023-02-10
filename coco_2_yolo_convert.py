import json
import cv2
import os
import matplotlib.pyplot as plt
import shutil

'''
input_path ____ coco_image_foldername
        |______ coco_json_filename


output_path ___ yolo_image_foldername
        |______ yolo_label_foldername

'''

input_path = "/home/haoxuan362709/object_detection_data/conversion_testing_data/coco_dataset"
coco_image_foldername = 'images'
coco_json_filename = 'result.json'

output_path = "/home/haoxuan362709/object_detection_data/conversion_testing_data/yolo_dataset"
yolo_image_foldername = 'images'
yolo_label_foldername = 'labels'

# open json file of coco dataset
f = open(input_path + '/' + coco_json_filename)
json_data = json.load(f)
f.close()



def load_images_from_folder(folder):
    count = 0
    for filename in os.listdir(folder):
        source = os.path.join(folder,filename)
        destination = f"{output_path}/{yolo_image_foldername}/img{count}.jpg"

        try:
            shutil.copy(source, destination)
            print("File copied successfully.")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        file_names.append(filename)
        count += 1


#list of filenames : only the image name in coco
file_names = []
load_images_from_folder(input_path + '/' + coco_image_foldername + '/')

# return image dict
def get_img(filename):
  for img in data['images']:
    # img is a dict     {
    #   "width": 1920,
    #   "height": 1200,
    #   "id": 0,
    #   "file_name": "images/1/5986065b-Frame_158.jpg"
    # }
    if filename in img['file_name']:
      return img

# return annotation dict
def get_img_ann(image_id):
    img_ann = []
    isFound = False
    for ann in data['annotations']:
        if ann['image_id'] == image_id:
            img_ann.append(ann)
            isFound = True
    if isFound:
        return img_ann
    else:
        return Non

count = 0

# for every image in coco 
for filename in file_names:

  # Extracting image 
  img = get_img(filename)
  img_id = img['id']
  img_w = img['width']
  img_h = img['height']

  # Get Annotations for this image
  img_ann = get_img_ann(img_id)

  if img_ann:
    # Opening file for current image
    file_object = open(f"{output_path}/{yolo_label_foldername}/img{count}.txt", "a")

    # ann is each polygon
    for ann in img_ann:
        current_category = ann['category_id'] # seems coco also start form 0 , As yolo format labels start from 0 
        current_segmentation = ann['segmentation']

        input_string = ""
        input_string += f"{current_category} "

        # not sure if this is necessary for multiple polygon in 1 image
        for each_polygon in len(current_segmentation):

            current_polygon = current_segmentation[each_polygon]

            for each_pair_coor in len(current_polygon)/2:
                x_coor = current_polygon[each_pair_coor * 2]
                y_coor = current_polygon[each_pair_coor *2 +1]
                x_coor = x_coor / img_w
                y_coor = y_coor / img_h
                # Limiting upto fix number of decimal places
                # x_coor = format(x_centre, '.6f')
                # y_coor = format(y_centre, '.6f')

                input_string = input_string + "f{x_coor} " + "f{y_coor} "


          
      # Writing current object 
      file_object.write(input_string)

    file_object.close()
    count += 1  # This should be outside the if img_ann block.