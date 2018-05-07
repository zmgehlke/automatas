import subprocess

import skimage.io as io
import numpy as np

def layer2bmp(automata, index, offset=0):
    image = np.copy(automata._data[index])
    image = image * 255

    filenum = index + offset
    io.imsave("renders/stills/automata_{:0>5d}.bmp".format(filenum), image)
    return
    
def auto2bmp(automata):
    for i in range(automata.shape[0]):
        layer2bmp(automata, i)
    return
    
# WARING:
#   This runs into memory issues when called on large automata via Python.
#   However, the shell command works fine even on large automata when called directly from the terminal.
def auto2mp4(automata):
    dump(automata)
    
    steps, height, width = automata.shape
    
    print("RENDERING SEQUENCE VIDEO")
    subprocess.run(
        "ffmpeg -pattern_type glob -r 24 -i 'renders/*.bmp' -vf scale={vwidth}:{vheight} -c:v libx264 -preset slow -crf 21 renders/automata.mp4".format(**{
            "vwidth":   width,
            "vheight":  height,
        }),
        shell=True, check=True
    )
    print("G'DAY MATE!\n")
    
def bmp2mp4(shape, index):
    subprocess.run(
        "ffmpeg -pattern_type glob -r 24 -i 'renders/stills/*.bmp' -vf scale={vwidth}:{vheight} -c:v libx264 -preset slow -crf 21 renders/clips/automata_{index:0>5d}.mp4".format(**{
            "vwidth":   shape[2],
            "vheight":  shape[1],
            "index": index,
        }),
        shell=True, check=True
    )
    
    subprocess.run(
        "rm renders/stills/*.bmp",
        shell=True, check=True
    )
    
    return
    
