from pathlib import Path

from PIL import Image

data_dir= Path('data/')


for c in list(data_dir.glob('0/*')):
    img= Image.open(c)
    print(img.format)