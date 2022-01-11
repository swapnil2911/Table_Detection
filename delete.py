import os
 
dir = '/content/Table_Detection/cropped_images'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))