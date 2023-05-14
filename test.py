from PIL import Image
import numpy as np


f = np.array(Image.open("driftator/driftator/affichage/models/balise/balise1.png").convert('HSV'))


x = len(f)
y = len(f[0])


print(f[int(x * 0.75)][int(y * 0.25)][0])