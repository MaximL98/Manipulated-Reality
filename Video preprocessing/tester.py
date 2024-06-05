from PIL import Image
import numpy as np
import os
'''data = np.load("Video preprocessing\\extracted_frames_real\\processed_video0_frames.npy")
print(data.size)
img = Image.fromarray(data[110], 'RGB')
img.save('my.png')
img.show()
'''
print(os.path.exists("Video preprocessing\Processed_data\Celeb-DF-v2\Celeb-real\id0_0000.mp4_frames.npy"))
