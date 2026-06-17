#Author: Atiye Buker. Purpose: Convert JSON file to COCO format
import json
import os
from PIL import Image

#file paths
via_json = 'cleaned_via_project.json'
image_dir = '/mnt/c/Users/buker/Downloads/SURP2026/Annotated/September 10th and Aug, 2021'
output_dir = './coco_output'
output_json_path = os.path.join(output_dir, 'annotations', 'instances_default.json')

#create directory
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

#define the categories
cats = {"Chili": 1, "Soil": 2, "Weed": 3, "Sky": 4, "Chili Background": 5}

#coco structure initalize
coco_dataset = {
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 1, "name": "Chili", "supercategory": "none"},
        {"id": 2, "name": "Soil", "supercategory": "none"},
        {"id": 3, "name": "Weed", "supercategory": "none"},
        {"id": 4, "name": "Sky", "supercategory": "none"},
        {"id": 5, "name": "Chili Background", "supercategory": "none"}
    ]
}

#load the clean JSON file
with open(via_json, 'r') as file:
    via_data = json.load(file)

ann_id = 1
img_id = 1

for img_key, img_data in via_data.items():
    filename = img_key.split('.png')[0] + '.png'
    img_path = os.path.join(image_folder if 'image_folder' in locals() else image_dir, filename)

    #get dimensions
    try:
       with Image.open(img_path) as img:
           width, height = img.size
    except Exception as e:
        #fail safe if image cant be opened
        width, height = 1920, 1080

    #insert img info to coco
    coco_dataset["images"].append({
        "id": img_id,
        "file_name": filename,
        "width": width,
        "height": height
    })    

    #annotations
    for region in img_data.get("regions", []):
        label = region["region_attributes"].get("names", "object")
        cat_id = cats.get(label, 4) #defailt to sky if unknown
        shape = region["shape_attributes"]
        if shape["name"] == "polygon":
            x_pts = shape["all_points_x"]
            y_pts = shape["all_points_y"]

            segmentation = []
            for x, y in zip(x_pts, y_pts):
                segmentation.extend([float(x), float(y)])

            # calculate bounding box
            min_x, max_x = min(x_pts), max(x_pts)
            min_y, max_y = min(y_pts), max(y_pts)
            bbox = [float(min_x), float(min_y), float(max_x - min_x), float(max_y - min_y)]
            area = float(bbox[2] * bbox[3]) #area

            coco_dataset["annotations"].append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": cat_id,
                "segmentation": [segmentation],
                "area": area,
                "bbox": bbox,
                "iscrowd": 0
            })
            ann_id += 1
            
    img_id += 1

# save
with open(output_json_path, 'w') as outfile:
    json.dump(coco_dataset, outfile, indent=4)
