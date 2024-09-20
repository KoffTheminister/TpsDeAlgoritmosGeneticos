<<<<<<< HEAD
from pathlib import Path

from PIL import Image

data_dir= Path('data/')


for c in list(data_dir.glob('0/*')):
    img= Image.open(c)
    print(img.format)
=======
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import load_model

new_iteration = load_model("mejormodelo")
print(new_iteration)

>>>>>>> 1170c6c34af4a97dea17e489d8a6f206d3b557d4
