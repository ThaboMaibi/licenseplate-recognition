import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\thabo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Read image file
image = cv2.imread("licensePlate1.jpg")

# Resize the image
image = imutils.resize(image,width=500)

#Display the original image////
cv2.imshow("original image",image)
cv2.waitKey(0)

#RBG to gray scale conversion
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("gray img",gray)
cv2.waitKey(0)

#remove noise
gray=cv2.bilateralFilter(gray,11,17,17)
cv2.imshow("filtered img",gray)
cv2.waitKey(0)

#Find edges of the grayscale image
edged = cv2.Canny(gray,170,200)
cv2.imshow("canny edges",edged)
cv2.waitKey(0)

#Find contours  based on edges
cnts,new = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

# create copy of original image
img1 = image.copy()
cv2.drawContours(img1,cnts,-1,(0,255,0),3)
cv2.imshow("All contours",img1)
cv2.waitKey(0)

# set contours based on their area keeping minimum required area of as 30
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberplateCnt = None #no number plate currently

# Top 30 contours
img2 =image.copy()
cv2.drawContours(img2,cnts,-1,(0,255,0),3)
cv2.imshow('top 30 contours',img2)
cv2.waitKey(0)

#loop over the contours to find the best possible approximate contours of the plate
count = 0
idx = 7
for c in cnts:
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*peri,True)
    # print ("approx = ",approx)
    if len(approx)== 4:
        NumberplateCnt = approx #This will find out co-ord for plate

        #crop those contours and store it in Cropped Image folder
        x,y,w,h = cv2.boundingRect(c) #This will find  co-ord for the plate
        new_image = image[y:y + h,x:x + w] #create new image
        cv2.imwrite(str(idx)+'.png',new_image)#store new image
        idx+=1

        break
#Drawing the selected contour on the original image
cv2.drawContours(image, [NumberplateCnt], -1,(0,255,0),3)
cv2.imshow('final image with number plate detected', image)
cv2.waitKey(0)

Cropped_img_loc = '7.png'
cropedIMG = cv2.imread(Cropped_img_loc)
gray2 = cv2.cvtColor(cropedIMG,cv2.COLOR_BGR2GRAY)

cv2.imshow('Cropped image', gray2)
cv2.waitKey(0)

# use tesseract to convert image into string
text = pytesseract.image_to_string(image,lang='eng')

print("number plate is : ",text)