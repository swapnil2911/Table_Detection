import xmltodict
import cv2
import os

image_folder_path = '/content/Table_Detection/images/'

for filename in os.listdir(image_folder_path):
  image_path = image_folder_path + filename
  xml_path = '/content/Table_Detection/xml/' + filename.split('.')[0] + '.xml'

  img = cv2.imread(image_path)

  with open(xml_path) as xml_file: 
    data_dict = xmltodict.parse(xml_file.read())
    if isinstance(data_dict['document']['table'], list):
      for i in range(len(data_dict['document']['table'])):
        download_path = '/content/Table_Detection/cropped_images/' + filename.split('.')[0] + '-' + str(i) + '-cropped.png'
        co_ord = data_dict['document']['table'][i]['Coords']['@points'].split(" ")
        X1,Y1 = co_ord[0].split(",")
        X2,Y2 = co_ord[2].split(",")
        cropped_image = img[int(Y1):int(Y2), int(X1):int(X2)]
        cv2.imwrite(download_path, cropped_image )
    else:
      download_path = '/content/Table_Detection/cropped_images/' + filename.split('.')[0] + '-cropped.png'
      co_ord = data_dict['document']['table']['Coords']['@points'].split(" ")
      X1,Y1 = co_ord[0].split(",")
      X2,Y2 = co_ord[2].split(",")
      cropped_image = img[int(Y1):int(Y2), int(X1):int(X2)]
      cv2.imwrite(download_path, cropped_image )