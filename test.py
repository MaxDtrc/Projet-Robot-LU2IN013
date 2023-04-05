import cv2
import numpy as np

cam = cv2.VideoCapture(0)
ret, im = cam.read()

div_x = 128
div_y = 128


size_cell_x = len(im)//div_x
size_cell_y = len(im[0])//div_y

for i in range(div_x):
    for j in range(div_y):
        #calcul de la valeur
        tab = []
        for x in range(size_cell_x):
            for y in range(size_cell_y):
                tab.append(im[x + i * size_cell_x][y  + j * (size_cell_y)])

        val = np.mean(np.array(tab), axis=(0))

        #On remplace
        for x in range(size_cell_x):
            for y in range(size_cell_y):
                im[x + i * size_cell_x][y + j * size_cell_y] = val

        val = np.mean(np.array(tab), axis=(0))
    


from PIL import Image
im = Image.fromarray(im)
im.save("test.jpeg")