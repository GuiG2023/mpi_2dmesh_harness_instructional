import sys
import numpy as np
import matplotlib.pyplot as plt

files = [
    'tile_25procs.raw',  # 5×5
    'tile_36procs.raw',  # 6×6
    'tile_64procs.raw',  # 8×8
]

fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()

for i, filename in enumerate(files):
    try:
        img = np.fromfile(filename, dtype='uint8').reshape([5146, 7112])
        axes[i].imshow(img, cmap="gray")
        axes[i].set_title(f'{filename} - {int(np.sqrt(int(filename.split("_")[1].replace("procs.raw", ""))))}×{int(np.sqrt(int(filename.split("_")[1].replace("procs.raw", ""))))} tiles')
        axes[i].axis('off')
    except:
        axes[i].text(0.5, 0.5, f'err:\n{filename}', ha='center', va='center')
        axes[i].set_title(filename)

plt.tight_layout()
plt.savefig('seams_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
