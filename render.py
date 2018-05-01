import skimage.io as io
import numpy as np

def layer2bmp(automata, index):
    image = np.copy(automata._data[index])
    image = image * 255

    io.imsave("renders/automata_{:0>5d}.bmp".format(index), image)
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
