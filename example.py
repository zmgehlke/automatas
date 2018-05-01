import automata
import render

print("Automata building.")
x = automata.Automata((500,500,500)) # shape is (500 time, 500 height, 500 width)
xb = x.boundary()

xb[ x.shape[1] // 2] = 1 
# shape[1] corresponds to the height
# so this creates a horizontal line halfway through the grid.

x.run()

render.auto2bmp(x)
