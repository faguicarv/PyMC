import matplotlib.pyplot as plt
import numpy as np
import csv

lists = []
with open("pos.csv", 'r') as cfile:
    raw_data = cfile.read().strip()

string_blocks = raw_data.split(',')

parsed_points = []
for block in string_blocks:
    # Eliminamos los corchetes de cada bloque
    clean_block = block.replace('[', '').replace(']', '')

    # split() sin argumentos separa automáticamente por cualquier cantidad de espacios
    coords = [float(val) for val in clean_block.split()]
    parsed_points.append(coords)

points = np.array(parsed_points)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Definimos el origen
origin = np.array([0.0, 0.0, 0.0])

# 3. Graficar
for pt in points:
    # Dibujar la línea desde el origen (0,0,0) hasta el punto (x,y,z)
    ax.plot([origin[0], pt[0]],
            [origin[1], pt[1]],
            [origin[2], pt[2]],
            color='blue', alpha=0.6, linewidth=1.5)

    # Dibujar el punto final de la trayectoria
    ax.scatter(pt[0], pt[1], pt[2], color='red', s=40)

# Resaltar el origen
ax.scatter(origin[0], origin[1], origin[2], color='black', s=80, label='Origen')

# Configuraciones visuales
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')
ax.set_title('Vectores de posición desde el origen')
ax.legend()

plt.show()
