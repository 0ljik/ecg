from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

import wfdb


def calc_img(imgpath):
    FILE = imgpath

    bgr_img_array = cv2.imread(FILE)

    height = 100
    width = bgr_img_array.shape[1] / bgr_img_array.shape[0] * height

    resized_bgr_img_array = cv2.resize(bgr_img_array, (int(width), height))

    b, g, r = cv2.split(resized_bgr_img_array)  # get b,g,r
    rgb_img = cv2.merge([r, g, b])  # switch it to rgb

    lower = np.array([0, 0, 0], dtype="uint8")
    upper = np.array([150, 150, 150], dtype="uint8")
    image = resized_bgr_img_array

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)

    # """ fill white
    output[mask == 0] = (255, 255, 255)
    # """
    # show the images
    # cv2.imshow("images", np.hstack([image, output]))

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

    # TODO 1 filter pass

    ecg_points_all_blacks = []

    for i in range(0, len(out_gray_reverse)):
        vertical_line_founds = []
        for j in range(0, len(out_gray_reverse[i])):
            if (int(out_gray_reverse[i][j]) < 150):
                vertical_line_founds.append(j)
        ecg_points_all_blacks.append(vertical_line_founds)

    ecg_points_blacks_maximums = []
    for i in range(0, len(ecg_points_all_blacks)):
        if (len(ecg_points_all_blacks[i]) == 0):
            continue
        last_point = 0
        max_points = []
        for j in range(0, len(ecg_points_all_blacks[i])):
            if (j == 0):
                last_point = ecg_points_all_blacks[i][j]
                max_points.append(last_point)
            elif (j != 0 and last_point != (ecg_points_all_blacks[i][j] - 1)):
                last_point = ecg_points_all_blacks[i][j]
                max_points.append(last_point)
            else:
                last_point = ecg_points_all_blacks[i][j]
                continue
        if (len(max_points) == 1):
            max_points = max_points[0]
        ecg_points_blacks_maximums.append(max_points)

    print(ecg_points_blacks_maximums)
    print(len(ecg_points_blacks_maximums))

    plt.imshow(out_gray, cmap="gray", vmin=0, vmax=255)
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis

    plt.show()


def calc_aami(filepath):
    record = wfdb.rdsamp(
        './zapisi/x34')  # В папке "zapisi" лежат 2 файла "aami3a.dat" и "aami3a.hea". Если одного нет, выполнение метода даст ошибку.
    points = record[0]  # Точки сигнала
    properties = record[1]  # Информация о сигнале (частота дискредитизации, длина сигнала, единица измерения)

    print(points.tolist())

imgfilepath = ""
datfilepath = ""
heafilepath = ""

window = Tk()
window.title("Tkinter crash course")
# window.configure(background="black")

# s = ttk.Style()
# s.configure('Kim.TButton', foreground='maroon')


def openImg():
    filepath = filedialog.askopenfilename(title="Выберите скан",
                                          filetypes=[('Выберите файл форматом jpg, png или ..', "*.jpeg")]
                                          )
    global imgfilepath
    imgfilepath = filepath
    print(filepath)


def openDat():
    filepath = filedialog.askopenfilename(title="Выберите скан",
                                          filetypes=[('Выберите файл Dat', "*.dat")]
                                          )
    global datfilepath
    datfilepath = filepath[:-4]
    print(datfilepath)


# def openHea():
#     filepath = filedialog.askopenfilename(title="Выберите скан",
#                                           filetypes=[('Выберите файл Dat', "*.dat")]
#                                           )
#     global heafilepath
#     heafilepath = filepath
#     print(filepath)

def calc():
    if inputchoosen.current() == 0:
        calc_img(imgfilepath)
    elif inputchoosen.current() == 1:
        calc_aami(datfilepath)
imgLabel = Label(window, text="Выберите сканированный файл:", fg="white", font="none 12")
imgLabel.grid(row=2, column=0, sticky=W)
imgButton = Button(window, text="Выбрать", width=8, command=openImg)
imgButton.grid(row=2, column=1, sticky=W)

datLabel = Label(window, text="Выберите файл dat:", fg="white", font="none 12")
datLabel.grid(row=2, column=0, sticky=W)
datButton = Button(window, text="Выбрать", width=8, command=openDat)
datButton.grid(row=2, column=1, sticky=W)

# heaLabel = Label(window, text="Выберите файл hea:", fg="white", font="none 12")
# heaLabel.grid(row=3, column=0, sticky=W)
# heaButton = Button(window, text="Выбрать", width=8, command=openHea)
# heaButton.grid(row=3, column=1, sticky=W)

Button(window, text="Расчитать", width=14, command=calc).grid(row=4, column=1, sticky=W)

def type_selected(event):
    print(inputchoosen.current(), inputchoosen.get())
    if inputchoosen.current() == 0:
        imgButton.grid()
        imgLabel.grid()
        datButton.grid_remove()
        # heaButton.grid_remove()
        datLabel.grid_remove()
        # heaLabel.grid_remove()
    elif inputchoosen.current() == 1:
        imgButton.grid_remove()
        imgLabel.grid_remove()
        datButton.grid()
        # heaButton.grid()
        datLabel.grid()
        # heaLabel.grid()


Label(window, text="Выберите тип данных:", fg="white", font="none 12").grid(row=1, column=0, sticky=W)
# Combobox creation
n = StringVar()
inputchoosen = ttk.Combobox(window, width = 27, textvariable = n, exportselection=0,
                            state = "readonly"
                            )
inputchoosen['values'] = ('scan', 'aami')
inputchoosen.grid(row = 1, column =1, sticky=W)
inputchoosen.current(0)
inputchoosen.bind("<<ComboboxSelected>>", type_selected)


#exit func
def close_window():
    window.destroy()
    exit()
# exit block
# Label(window, text="Нажмите чтобы выйти:", fg="white", font="none 12").grid(row=7, column=0, sticky=W)
Button(window, text="Закрыть", width=14, command=close_window).grid(row=7, column=1, sticky=W)


if __name__ == '__main__':
    datButton.grid_remove()
    datLabel.grid_remove()
    window.mainloop()