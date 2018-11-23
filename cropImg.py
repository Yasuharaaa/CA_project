import cv2
def cropAndSave(str):

    image = cv2.imread(str)
    #print(image)
    cropImg = image[600:650,600:650]
    cropedName = "C:/ca_project/Demo/cropedImage/"+"image_croped.bmp"
    cv2.imwrite(cropedName,cropImg)
    return cropedName
if __name__ == '__main__':
    cropAndSave("C:\PyTorch\hymenoptera_data/train/ants\VietnameseAntMimicSpider.jpg")