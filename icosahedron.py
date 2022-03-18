# Generates triangle code for icosahedron

ϕ = 1.618

point = ["[0.0, +1.0, +ϕ]","[0.0, +1.0, -ϕ]","[0.0, -1.0, +ϕ]","[0.0, -1.0, -ϕ]","[+1.0, +ϕ, 0.0]","[+1.0, -ϕ, 0.0]","[-1.0, +ϕ, 0.0]","[-1.0, -ϕ, 0.0]","[+ϕ, 0.0, +1.0]","[+ϕ, 0.0, -1.0]","[-ϕ, 0.0, +1.0]","[-ϕ, 0.0, -1.0]"]

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']


s = ["akg","ack","aeg","aie","aci","kgl","lhk","kch","chf","cfi","ifj","iej","ejb","egb","glb","dfj","djb","dbl","dlh","dfh"] # triangles of icosahedron as defined on GeoGebra

for order in s:
    one = point[letters.index(order[0])]
    two = point[letters.index(order[1])]
    three = point[letters.index(order[2])]
    print(f"start.addShape(Shape([np.array({one}), np.array({two}), np.array({three})]))")