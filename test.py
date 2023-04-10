import cv2
import numpy as np

for i in range(50):
    im = cv2.imread("test" + i + ".jpeg")
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    im = cv2.resize(im, (160, 120))

    div_x = 20
    div_y = 20

    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    yellow = [255, 255, 0]


    size_cell_x = len(im)//div_x
    size_cell_y = len(im[0])//div_y

    for i in range(div_x):
        for j in range(div_y):
            #calcul de la valeur
            tab = []
            for x in range(size_cell_x):
                for y in range(size_cell_y):
                    #Detection rouge
                    clr = im[x + i * size_cell_x][y + j * size_cell_y]
                    if clr[0] > 85 and clr[0] > clr[1] * 2 and clr[0] > clr[2] * 2:
                        tab.append(1)
                    elif clr[1] > 100 and clr[1] > clr[0] * 1.5 and clr[1] > clr[2] * 1.5:
                        tab.append(2)
                    elif clr[2] > 100 and clr[2] > clr[1] * 1.5 and clr[2] > clr[0] * 1.5:
                        tab.append(3)
                    elif clr[0] > 80 and clr[1] > 80 and clr[1] > 1.5 * clr[2] and clr[0] > 1.5 * clr[2]:
                        tab.append(4)
                    else:
                        tab.append(0)


            val = np.bincount(np.array(tab)).argmax()

            if(val == 1):
                clr = red
            elif(val == 2):
                clr = green
            elif(val == 3):
                clr = blue
            elif(val == 4):
                clr = yellow
            else:
                clr = [0, 0, 0]

            #On remplace
            for x in range(size_cell_x):
                for y in range(size_cell_y):
                    im[x + i * size_cell_x][y + j * size_cell_y] = clr

    from PIL import Image
    im = Image.fromarray(im)
    im.save("test.jpeg")