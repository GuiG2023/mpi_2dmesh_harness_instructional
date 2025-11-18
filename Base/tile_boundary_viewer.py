import matplotlib.pyplot as plt
import numpy as np


img1 = np.fromfile('verify_tile_4procs_final.raw', dtype='uint8').reshape([5146, 7112])
img2 = np.fromfile('verify_tile_16procs_final.raw', dtype='uint8').reshape([5146, 7112])

diff = np.abs(img1.astype(float) - img2.astype(float))
plt.imshow(diff, cmap='hot')
plt.title("difference between configurations")
plt.show()