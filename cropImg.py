import cv2
def cropAndSave(str, cropedDst):
    image = cv2.imread(str)
    #print(image)
    cropImg = image[1000:1300,2700:3000]
    #cropedName = "C:/ca_project/Demo/cropedImage/image_croped.jpg"
    cv2.imwrite(cropedDst,cropImg)
    return cropedDst
if __name__ == '__main__':
    cropAndSave("C:/ca_project/Demo/front/abb730d0gy1fp13awhymej23vc2kw7wi.jpg", "C:/ca_project/Demo/cropedImageFwd/image_croped.jpg")
