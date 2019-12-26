import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

def convertimageBGRtoHSV(imgBGR):
    imgHSV = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2HSV)  # avec plt.imshow, il faut reconvertir l'image
    return imgHSV

def convertimageBGRtoRGB(imgBGR):
    # IMAGE BRG -> cv2.imread
    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)  # avec plt.imshow, il faut reconvertir l'image
    return imgRGB

def convertimageRGBtoBGR(imgRGB):
    # IMAGE BRG -> cv2.imread
    imgBGR = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)  # avec plt.imshow, il faut reconvertir l'image
    return imgBGR

def convertimageRGBtoHSV(imgRGB):
    imgHSV = cv2.cvtColor(imgRGB,cv2.COLOR_RGB2HSV)
    return imgHSV

def convertimageHSVtoRGB(imgHSV):
    imgRGB= cv2.cvtColor(imgHSV,cv2.COLOR_HSV2RGB)
    return imgRGB

def colorpickerHSVgenerator(color):
    value = cv2.cvtColor(tableColorRGB(color), cv2.COLOR_RGB2HSV)
    min = value[0][0][0] / 2 - 5
    max = value[0][0][0] / 2 + 15
    return np.array([min, 0, 0]), np.array([max, 255, 255])

def tableColorRGB(name):
    if name == 'jaune':
        return np.uint8([[[255,255,0 ]]])
    pass

def binariseHSV(imgHSV, lower, upper):
    mask = cv2.inRange(imgHSV, lower, upper)
    return mask

def seuillageCouleur(binarise):
    res = cv2.bitwise_and(imgBGR, imgBGR, mask=binarise)
    return res

    # 保存图片
def saveImage(img, name):
    cv2.imwrite(name + '.jpg', img)

def filtregaussien(img, nb=5):
    img = cv2.GaussianBlur(img, (nb, nb), 0)
    return img

def filtremedian(img, nb=5):
    img = cv2.medianBlur(img, nb)
    return img

def openingclosing(img):
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    return closing

def reductionbruit(img, filtre="null"):
    if filtre == "gaussien":
        img = filtregaussien(img)
    elif filtre == "median":
        img = filtremedian(img)
    elif filtre == "ouverture/fermeture":
        openingclosing(img)
    else:
        img = cv2.bilateralFilter(img, 9, 75, 75)
    return img

def denombrementetiquageconnexes(img):
    _, comp_conn = cv2.connectedComponents(img)
    return comp_conn

# imgsize = 416
# def JPG2BGR(path,out,size=416):
#     img = cv2.imread(path)
#     img = cv2.resize(img,(size,size))
#     bgr=convertimageRGBtoBGR(img)
#     saveImage(bgr,out)

# import cv2
 
# imgpath = "./BGR_img/917.jpg"
# saveimg = r"./BGR_img/917_608x608.bgr"
 


def JPG2BGR(imgpath,saveimg,save_img_size = 416):
    img = cv2.imread(imgpath)
    if img is None:
        print("img is none")
    else:
        img = cv2.resize(img,(save_img_size,save_img_size),interpolation=cv2.INTER_CUBIC)
        (B, G, R) = cv2.split(img)
        # print(B[1, 1])
        with open(saveimg,'wb')as fp:
            for i in range(save_img_size):
                for j in range(save_img_size):
                    fp.write(B[i, j])
            for i in range(save_img_size):
                for j in range(save_img_size):
                    fp.write(G[i, j])
            for i in range(save_img_size):
                for j in range(save_img_size):
                    fp.write(R[i, j])


def showreact(imgpath):
    if imgpath is None:
        # imgpath='img/niaochao_416_416.jpg'
        imgpath='img/dog_bike_car_416x416.jpg'
    save_img_size=416
    img = cv2.imread(imgpath)
    img = cv2.resize(img,(save_img_size,save_img_size))
    (B, G, R) = cv2.split(img)
    print("B:",B[1, 1])
    print("G:",G[1, 1])
    print("R:",R[1, 1])


    # cv2.imwrite("niaochao_416_416.jpg",img)
    # w=(380, 0) 
    # h=(385, 148)
    # w382 0 385 148
    # 

    # 196.36  126.46  209.52  153.52
# >>>>>>> HI_MPI_SVP_NNIE_Forward(Seg-0) FINISH <<<<<<<
# n:1, c:21, h:13, w:13
# n:1, c:21, h:26, w:26
# n:1, c:21, h:52, w:52
# u32BoxResultNum: 1
# ==============================================================================
# 416  416
# dog_bike_car_416x416     0  0.82002997  196.36  126.46  209.52  153.52
# ==============================================================================
# 128 230 230 359
# 134 231 229 362  interpolation=cv2.INTER_AREA
# 128 229 230 360

# 216 133 307 234 0.951904
# 1 118 226 246 304 0.856201 niaochao
    # w,h=((128,229),(230,360))  ## niaochao
    # w,h=((128,229),(230,360))  ## niaochao
    # w,h=((216,133),(307,234))  ## niaochao

    # (123,87),(416,265)
    w,h=((123,87),(416,265))  ## niaochao
    img = cv2.rectangle(img, w,h, (255, 0, 0), 2)
    
# ==============================================================================
# 416  416
# imgName	class	confidence	xmin	ymin	xmax	ymax
# dog_bike_car_416x416    16  0.99853194  64.87  166.71  174.98  383.54
# dog_bike_car_416x416     1  0.99768275  60.40  92.48  311.95  311.59
# dog_bike_car_416x416     7  0.87849325  255.03  59.72  376.12  121.87

    # w,h=((60, 92),(311, 311))  ## bike
    # img = cv2.rectangle(img, w,h, (255, 0, 0), 2)

    # w,h=((257 ,59 ),(373 ,121))  ## car
    # img = cv2.rectangle(img, w,h, (255, 0, 0), 2)

    # w,h=((64 ,165 ),(175,387))  ## car
    # img = cv2.rectangle(img, w,h, (255, 0, 0), 2)

#     60 92 311 311 0.996582
# [Level]:Info,[Func]:SAMPLE_SVP_NNIE_Detection_PrintResult [Line]:1086 [Info]:==== The index 8 and bias 1  and scorce 3922  and roinum 1 class box info====
# [Level]:Info,[Func]:SAMPLE_SVP_NNIE_Detection_PrintResult [Line]:1104 [Info]:257 59 373 121 0.957520
# [Level]:Info,[Func]:SAMPLE_SVP_NNIE_Detection_PrintResult [Line]:1086 [Info]:==== The index 17 and bias 2  and scorce 4093  and roinum 1 class box info====
# [Level]:Info,[Func]:SAMPLE_SVP_NNIE_Detection_PrintResult [Line]:1104 [Info]:64 165 175 387 0.999268

    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    
    showreact("img/dog_bike_car_416x416.jpg")
    # JPG2BGR("data/images/niaochao.jpg","img/dog_bike_car_416x416.bgr")
    # if len(sys.argv) < 3:
    #     print("python convert.py data/images/jueyuanzi.jpg jueyuanzi.bgr")
    # src=sys.argv[1]
    # dst=sys.argv[2]
    # # size=sys.argv[3]
    # JPG2BGR(src,dst)

    # cv2.colorpickerHSVgenerator
    # img = cv2.imread("output/--dog_bike_car_416x416.bgr")
    # print(img.shape)
    # cv2.imshow("img1",img)
    # img = cv2.imread("output/-dog_bike_car_416x416.bgr")
    # cv2.imshow("img2",img)
    # img = cv2.imread("output/dog_bike_car_416x416.bgr")
    # cv2.imshow("img3",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    '''
    # PARTIE 1
    plt.subplot(4, 4, 1)
    imgBGR = cv2.imread('pollen.jpg')
    plt.imshow(convertimageBGRtoRGB(imgBGR), cmap='gray')
    plt.title('imgBGR')

    # imgBGR=convertImageRGBtoBGR(imgRGB)
    # plt.title('imgBGR')
    # plt.subplot(4, 4, 1)

    plt.subplot(4, 4, 2)
    imgHSV = convertimageBGRtoHSV(imgBGR)
    plt.imshow(convertimageHSVtoRGB(imgHSV), cmap='gray')
    plt.title('imgHSV')

    plt.subplot(4, 4, 3)
    lower, upper = colorpickerHSVgenerator('jaune')
    img_binarise = binariseHSV(imgHSV, lower, upper)
    saveImage(img_binarise, name='image_binaire')
    plt.imshow(img_binarise, cmap='gray')
    plt.title('image_binaire')

    plt.subplot(4, 4, 4)
    img_seuillage = seuillageCouleur(img_binarise)
    saveImage(img_seuillage, name='image_couleur_seuillee')
    plt.imshow(convertimageHSVtoRGB(img_seuillage), cmap='gray')
    plt.title('image_couleur_seuillee')

    #PARTIE 2 : GAUSSIEN

    plt.subplot(4, 4, 5)
    imggaussien = reductionbruit(imgBGR, filtre="gaussien")
    plt.imshow(convertimageBGRtoRGB(imggaussien), cmap='gray')
    plt.title('Filtre Gaussien')

    plt.subplot(4, 4, 6)
    imgHSV = convertimageBGRtoHSV(imggaussien)
    plt.imshow(convertimageHSVtoRGB(imgHSV), cmap='gray')
    plt.title('imgHSV')

    plt.subplot(4, 4, 7)
    lower, upper = colorpickerHSVgenerator('jaune')
    img_binarise = binariseHSV(imgHSV, lower, upper)
    saveImage(img_binarise, name='image_binaire_gaussien')
    plt.imshow(img_binarise, cmap='gray')
    plt.title('image_binaire')

    plt.subplot(4, 4, 8)
    img_seuillage = seuillageCouleur(img_binarise)
    saveImage(img_seuillage, name='image_couleur_seuillee_gaussien')
    plt.imshow(convertimageHSVtoRGB(img_seuillage), cmap='gray')
    plt.title('image_couleur_seuillee')

    #PARTIE 3: MEDIAN
    plt.subplot(4, 4, 9)
    img = reductionbruit(imgBGR, filtre="ouverture/fermeture")
    plt.imshow(convertimageBGRtoRGB(img), cmap='gray')
    plt.title('Ouverture/Fermeture')

    plt.subplot(4, 4, 10)
    imgHSV = convertimageBGRtoHSV(img)
    plt.imshow(convertimageHSVtoRGB(imgHSV), cmap='gray')
    plt.title('imgHSV')

    plt.subplot(4, 4, 11)
    lower, upper = colorpickerHSVgenerator('jaune')
    img_binarise = binariseHSV(imgHSV, lower, upper)
    saveImage(img_binarise, name='image_binaire_post')
    plt.imshow(img_binarise, cmap='gray')
    plt.title('image_binaire')

    plt.subplot(4, 4, 12)
    img_seuillage = seuillageCouleur(img_binarise)
    saveImage(img_seuillage, name='image_couleur_seuillee_post')
    plt.imshow(convertimageHSVtoRGB(img_seuillage), cmap='gray')
    plt.title('image_couleur_seuillee')

    #PARTIE 4 : DENOMBREMENT
    plt.subplot(4, 4, 13)
    img_denom = denombrementetiquageconnexes(img_binarise)
    saveImage(img_denom, name='image_binaire_post_denombre')
    plt.imshow(img_denom)
    plt.colorbar()
    plt.title('image_denombre')

    #PARTIE 5 :
    # plt.subplot(4, 4, 14)
    # img_contours=contourFinder(img_denom)
    # plt.imshow(img_contours)
    # plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''