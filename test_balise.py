from PIL import Image
import numpy as np
import time

def getPosBaliseV3(img):
    #Redimension de l'image
    img = Image.fromarray(img)
    width, height = int(img.width/8), int(img.height/8)
    img = img.resize((width, height), Image.NEAREST)
    img = img.convert('HSV')
    img = np.array(img)[:,:,0]

    #On cherche les carrés jaunes
    j = np.where((img > 30) & (img < 85))
    
    #Recherche des coins
    bs = 4

    hist = np.histogram(j[0], bins = [b * bs for b in range(int(width/bs))])[0]
    x = [e * bs + int(bs/2) for e in np.where(hist != 0)][0]
    hist = np.histogram(j[1], bins = [b * bs for b in range(int(height/bs))])[0]
    y = [e * bs + int(bs/2) for e in np.where(hist != 0)][0]

    t = img[x[0]:x[2], y[0]:y[3]]
    b = np.where((t > 150) & (t < 270))

    x_coord, y_coord = np.mean(b[0]), np.mean(b[1])

    droite = 1 if x_coord > 0.5 else 0
    haut = 1 if y_coord < 0.5 else 0

    return(droite, haut)



im = Image.open("test.png")

n = 100
t1 = time.time()
for i in range(n):
    getPosBaliseV3(np.array(im))
t2 = time.time()

print((t2 - t1)/n)