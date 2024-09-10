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

