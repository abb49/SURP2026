#Author: Atiye Buker. Purpose: clean up JSON file
import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


json_file_path = 'myenv/segmentation/via_project_24Apr2025_15h0m_json (5) (1).json'
image_folder = '/mnt/c/Users/buker/Downloads/SURP2026/Annotated/September 10th and Aug, 2021'

with open(json_file_path, 'r') as file:
    segmentation = json.load(file)

#the files we actually have
actual_files = os.listdir(image_folder)

cleaned_segmentation = {}
match_count = 0

for img_key, img_data in segmentation.items():
    base_name = img_key.split('.png')[0] + '.png' #file contains some random numbers, so just get the base 
    
    #ssee if this exists in the dataset
    if base_name in actual_files:
        cleaned_segmentation[img_key] = img_data
        match_count += 1

#make new JSON file with the existing entries
with open('cleaned_via_project.json', 'w') as outfile:
    json.dump(cleaned_segmentation, outfile, indent=4)

#print how many there are
print(f"Found {match_count}")


