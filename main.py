import automata
import render



rounds = 100
time = 50000
dt = time // rounds
width = 2522
height = 2522
shape = (dt, height, width)



print("Automata building.")
x = automata.Automata(shape)
xb = x.boundary()
xb[ x.shape[1] // 2] = 1 
# shape[1] corresponds to the height
# so this creates a horizontal line halfway through the grid.

for j in range(rounds):
    offset = shape[0] * j - j # Because the rounds share a boundary.
    
    x.run()
    for index in range(shape[0]):
        render.layer2bmp(x, index, offset=offset)
    
    y = automata.Automata(shape)    
    y._data[0] = x._data[-1]
    x=y
    
    #Uh.... Yeah.
    render.bmp2mp4(shape, j)
