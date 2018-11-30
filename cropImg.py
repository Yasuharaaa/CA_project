import cv2
def cropAndSave(str):
    image = cv2.imread(str)
    #print(image)
    cropImg = image[600:1200,750:1500]
    cropedName = "C:/ca_project/Demo/cropedImage/image_croped.jpg"
    cv2.imwrite(cropedName,cropImg)
    return cropedName
if __name__ == '__main__':
    cropAndSave("C:\ca_project\Demo/back/abb730d0gy1fp13awhymej23vc2kw7wi.jpg")