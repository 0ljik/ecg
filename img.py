import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

FILE = "./img/1.jpeg"

bgr_img_array = cv2.imread(FILE)

b,g,r = cv2.split(bgr_img_array)       # get b,g,r
rgb_img = cv2.merge([r,g,b])     # switch it to rgb

#print(r)
#print(g)
#print(b)

lower = np.array([0,0,0], dtype = "uint8")
upper = np.array([150,150,150], dtype = "uint8")
image = bgr_img_array

# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask = mask)

#""" fill white
output[mask==0] = (255,255,255)
#"""
# show the images
cv2.imshow("images", np.hstack([image, output]))


""" Noise Removal
img_bw = 255*(cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) > 5).astype('uint8')

se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

mask = np.dstack([mask, mask, mask]) / 255
out = output * mask

cv2.imshow('Output', out)

# write result to disk
cv2.imwrite("output.png", output)
"""

"""
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(rgb_img, low_threshold, high_threshold)
plt.imshow(edges)
plt.xticks([]), plt.yticks([])   # to hide tick values on X and Y axis
plt.show()"""

out_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

out_gray_reverse = np.swapaxes(out_gray, 0, 1)
ecg_points_all_blacks = []

for i in range(0, len(out_gray_reverse)):
    vertical_line_founds = []
    for j in range(0, len(out_gray_reverse[i])):
        if(int(out_gray_reverse[i][j]) < 150):
            vertical_line_founds.append(j)
    ecg_points_all_blacks.append(vertical_line_founds)

ecg_points_blacks_maximums = []
for i in range(0, len(ecg_points_all_blacks)):
    if(len(ecg_points_all_blacks[i]) == 0):
        continue
    last_point = 0
    max_points = []
    for j in range(0, len(ecg_points_all_blacks[i])):
        if(j == 0):
            last_point = ecg_points_all_blacks[i][j]
            max_points.append(last_point)
        elif(j != 0 and last_point != (ecg_points_all_blacks[i][j] - 1)):
            last_point = ecg_points_all_blacks[i][j]
            max_points.append(last_point)
        else:
            last_point = ecg_points_all_blacks[i][j]
            continue
    if(len(max_points) == 1):
        max_points = max_points[0]
    ecg_points_blacks_maximums.append(max_points)

print(ecg_points_blacks_maximums)


plt.imshow(out_gray, cmap="gray", vmin=0, vmax=255)
plt.xticks([]), plt.yticks([])   # to hide tick values on X and Y axis

plt.show()
