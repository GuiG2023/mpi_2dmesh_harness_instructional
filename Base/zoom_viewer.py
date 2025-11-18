import sys
import numpy as np
import matplotlib.pyplot as plt


srcImg = np.fromfile(sys.argv[1], dtype='uint8')
cols = int(sys.argv[2])
rows = int(sys.argv[3])
srcImg = srcImg.reshape([rows, cols])


plt.figure(figsize=(15, 10))
plt.imshow(srcImg, cmap="gist_ncar")
plt.colorbar()
plt.title("zoom viewer image")


plt.tight_layout()
plt.show()
