import numpy as np
import matplotlib.pyplot as plt

np.random.seed(3)

H = 120
W = 160
C = 3
image = np.random.randint(0, 256, size=(H, W, C), dtype=np.uint8)

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
ax1.set_title('Random image')
ax1.imshow(image)

image = np.where(
    image <= 85, 
    0, 
    image
)
image = np.where(
    (image > 58) & (image <= 170), 
    100, 
    image
)
image = np.where(
    image > 170, 
    255, 
    image
)
ax2.set_title('Treated image')
ax2.imshow(image)
fig.tight_layout()
plt.show()
