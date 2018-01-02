import numpy
import cv2
import time
import Tkinter
import Image, ImageTk

x = 100
y = 100
lv_width = 0
lv_hight = 0
lv_blurring = 0
blurring_cycles = 1

#vid_cap = cv2.VideoCapture("rtsp://192.168.178.201:554")

#_, frame = vid_cap.read()
#frame = cv2.flip(frame, 1)
#cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#cv2.imshow("test", cv2img)
#image = cv2img

image = cv2.imread("snooker_2.jpg")  # Load Image from File
#image = cv2img
image_width = numpy.size(image, 1)  # Get image width via matrix size
image_hight = numpy.size(image, 0)  # Get image hight via matrix size
greyscale_image = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
blurring_image = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
blurring_image_temp = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
blurring_filter = numpy.uint8(0)
edge_image_x = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
edge_image_y = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
edge_image = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
edge_filter = numpy.uint8(0)
binary_image = numpy.zeros((image_hight, image_width, 1), numpy.uint8)
binary_black = numpy.uint8(0)
binary_white = numpy.uint8(255)

# original image ==> greyscale image
while lv_hight < image_hight:   # loop to run through y-coordinates
    lv_width = 0   
    while lv_width < image_width:   # loop to run through x-coordinates
        r = 0
        g = 0
        b = 0
        greyscale = 0
        (b,g,r) = image[lv_hight, lv_width] # get colour values for each pixel
        greyscale = int((0.3*r + 0.59*g + 0.11*b) / 3)  # calculate gray shade for each pixel
        greyscale_image[lv_hight, lv_width] = greyscale # write gray shade to greyscale_image
        lv_width = lv_width + 1 # increment x-value
    lv_hight = lv_hight + 1 # increment y-value

# greyscale image ==> blurring image
lv_width = 1    # Pixel offset
lv_hight = 1    # Pixel offset
blurring_image_temp = greyscale_image   # temp image you need if you want to run more then one time
while lv_blurring < blurring_cycles:    # loop if you want to run more then one times
    while lv_hight < image_hight -1:    # loop to run through y-coordinates
        lv_width = 1   
        while lv_width < image_width -1:    # loop to run through x-coordinates
            blurring_filter = 0 # blurring temp value
            blurring_filter = blurring_filter + 0.075 * blurring_image_temp[lv_hight -1, lv_width -1]   # filter matrix
            blurring_filter = blurring_filter + 0.125 * blurring_image_temp[lv_hight -1, lv_width +0]
            blurring_filter = blurring_filter + 0.075 * blurring_image_temp[lv_hight -1, lv_width +1]
            blurring_filter = blurring_filter + 0.125 * blurring_image_temp[lv_hight +0, lv_width -1]
            blurring_filter = blurring_filter + 0.200 * blurring_image_temp[lv_hight +0, lv_width +0]
            blurring_filter = blurring_filter + 0.125 * blurring_image_temp[lv_hight +0, lv_width +1]
            blurring_filter = blurring_filter + 0.075 * blurring_image_temp[lv_hight +1, lv_width -1]
            blurring_filter = blurring_filter + 0.125 * blurring_image_temp[lv_hight +1, lv_width +0]
            blurring_filter = blurring_filter + 0.075 * blurring_image_temp[lv_hight +1, lv_width +1]
            blurring_image[lv_hight, lv_width] = blurring_filter    # write blurring value to blurring_image
            lv_width = lv_width + 1 # increment x-value
        lv_hight = lv_hight + 1 # increment y-value
    blurring_image_temp = blurring_image    # save finished image to temp for next loop
    lv_blurring = lv_blurring + 1   # increment loop counter

# edge detection
lv_width = 1
lv_hight = 1
# x direction
while lv_hight < image_hight -1:    # loop to run through y-coordinates
    lv_width = 1   
    while lv_width < image_width -1:    # loop to run through x-coordinates
        edge_filter = 0
        edge_filter = edge_filter + (-1) * blurring_image[lv_hight -1, lv_width -1] # filter matrix
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight -1, lv_width +0]
        edge_filter = edge_filter + (+1) * blurring_image[lv_hight -1, lv_width +1]
        edge_filter = edge_filter + (-2) * blurring_image[lv_hight +0, lv_width -1]
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight +0, lv_width +0]
        edge_filter = edge_filter + (+2) * blurring_image[lv_hight +0, lv_width +1]
        edge_filter = edge_filter + (-1) * blurring_image[lv_hight +1, lv_width -1]
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight +1, lv_width +0]
        edge_filter = edge_filter + (+1) * blurring_image[lv_hight +1, lv_width +1]
        edge_image_x[lv_hight, lv_width] = edge_filter  # write value to matrix
        lv_width = lv_width + 1 # increment x-value
    lv_hight = lv_hight + 1 # increment y-value
lv_width = 1
lv_hight = 1
# y direction
while lv_hight < image_hight -1:    # loop to run through y-coordinates
    lv_width = 1   
    while lv_width < image_width -1:    # loop to run through x-coordinates
        edge_filter = 0
        edge_filter = edge_filter + (-1) * blurring_image[lv_hight -1, lv_width -1] # filter matrix
        edge_filter = edge_filter + (-2) * blurring_image[lv_hight -1, lv_width +0]
        edge_filter = edge_filter + (-1) * blurring_image[lv_hight -1, lv_width +1]
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight +0, lv_width -1]
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight +0, lv_width +0]
        edge_filter = edge_filter + (+0) * blurring_image[lv_hight +0, lv_width +1]
        edge_filter = edge_filter + (+1) * blurring_image[lv_hight +1, lv_width -1]
        edge_filter = edge_filter + (+2) * blurring_image[lv_hight +1, lv_width +0]
        edge_filter = edge_filter + (+1) * blurring_image[lv_hight +1, lv_width +1]
        edge_image_y[lv_hight, lv_width] = edge_filter  # write value to matrix
        lv_width = lv_width + 1 # increment x-value
    lv_hight = lv_hight + 1 # increment y-value
lv_width = 1
lv_hight = 1
#  combining x and y image
while lv_hight < image_hight -1:    # loop to run through y-coordinates
    lv_width = 1   
    while lv_width < image_width -1:    # loop to run through x-coordinates
        edge_filter = 0
        edge_filter = numpy.sqrt(numpy.square(edge_image_x[lv_hight, lv_width]) + numpy.square(edge_image_y[lv_hight, lv_width]))
        edge_image[lv_hight, lv_width] = edge_filter    # write value to matrix in
        lv_width = lv_width + 1 # increment x-value
    lv_hight = lv_hight + 1 # increment y-value

lv_width = 1
lv_hight = 1
# edge image ==> binary image
while lv_hight < image_hight -1:    # loop to run through y-coordinates
    lv_width = 1   
    while lv_width < image_width -1:    # loop to run through x-coordinates
        if edge_image[lv_hight, lv_width] < 10: # threshold
            binary_image[lv_hight, lv_width] = binary_black
        else:
            binary_image[lv_hight, lv_width] = binary_white
        lv_width = lv_width + 1 # increment x-value
    lv_hight = lv_hight + 1 # increment y-value

# hough cirlce transformation
circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, 1, 40, param1=50, param2=25, minRadius=25, maxRadius=55) # 25, 55
circles = numpy.uint16(numpy.around(circles))

for i in circles[0,:]:
        cv2.circle(image, (i[0], i[1]), i[2], (0,255,0), 2) # outer circle, green
        cv2.circle(image, (i[0], i[1]), 2, (0,0,255), 3)    # center point, red


cv2.imshow("original_image", image)
cv2.imshow("greyscale_image", greyscale_image)
cv2.imshow("blurring_image", blurring_image)
cv2.imshow("edge_image", edge_image)
cv2.imshow("binary_image", binary_image)
cv2.waitKey(0)

