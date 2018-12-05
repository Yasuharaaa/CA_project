import cv2
def cropAndSave(str, cropedDst):
    image = cv2.imread(str)
    #print(image)
    cropImg = image[100:150,100:150]
    #cropedName = "C:/ca_project/Demo/cropedImage/image_croped.jpg"
    cv2.imwrite(cropedDst,cropImg)
    return cropedDst
if __name__ == '__main__':
    cropAndSave("C:\ca_project\Demo/back/abb730d0gy1fp13awhymej23vc2kw7wi.jpg")