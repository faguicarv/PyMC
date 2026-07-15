import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from functions import *
import csv

# --------- DEFINE SOURCE WITH NUMPY ---------
## --------- SOURCE PARTICLE ---------
part_type = str('neutron') # Beam type
## --------- NUMBER OF PRIMARY PARTICLES ---------
nro_part = 20
## --------- INITIAL ENERGY - MONOENERGETIC ---------
energy_0 = 2.44e1 # Monoenergetic beam
## --------- POSITION OF SOURCE ---------
pos_0 = np.array([0.0, 0.0, 0.0])
## --------- DIRECTION OF SOURCE - ISOTROPIC ---------
dir_0 = np.random.randn(nro_part, 3)
## --------- DIRECTION OF SOURCE - MONODIRECTIONAL ---------
# dir_0 = np.array([0.0, 0.0, 3.4])
dir_0 = dir_0 / np.linalg.norm(dir_0) # Normalization of the direction
## ---------
# --------- END DEFINITION OF SOURCE ---------

beam, beam_final = beam_definition(part_type, nro_part, pos_0, dir_0, energy_0)

# --------- GEOMETRY DEFINITION ---------
## --------- UNIVERSE ---------
sphere_r = 30.0 # With this vector we will define a sphere of radius 30.0
## --------- BOX ---------
xlim, ylim, zlim = [-4.0, 4.0], [-4.0, 4.0], [5.0, 15.0]
box = box_def(xlim, ylim, zlim)
## ---------

sigma_sph = 3
# Once the beam is ready, the transport occur in the incoming lines
sigma_box = 10

with open('pos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(nro_part):
        print(f"Transporte de la partícula {i+1}")
        beam_final[i] = beam[i] # Copy beam information in a new layout
        cont = 0
        while (beam_final[i]['alive']):
            cont += 1
            pos = beam_final[i]['pos']
            dirc = beam_final[i]['dir']
            region = beam_final[i]['region']

            # Verify where the particle is
            if (box[0]['xdims'][0] <= pos[0] <= box[0]['xdims'][1] and
                box[0]['ydims'][0] <= pos[1] <= box[0]['ydims'][1] and
                box[0]['zdims'][0] <= pos[2] <= box[0]['zdims'][1]):
                region = 2

                # IF enters into the box, kill the particle
                beam_final[i]['alive'] = False


            elif (np.dot(pos, pos) > sphere_r**2):
                region = 3
                beam_final[i]['alive'] = False
                continue
            else:
                region = 1

            if (region == 1):
                sigma = sigma_sph
            elif (region == 2):
                sigma = sigma_box

            beam_final[i]['region'] = region

            # Calculate distance of next step
            ## Calculate sigma distance
            dist_sigma = -np.log(np.random.rand(1)) / sigma

            ## Calculate distance to box
            ### Boundaries of the box in each axes
            x_min, x_max = box[0]['xdims'][0], box[0]['xdims'][1]
            y_min, y_max = box[0]['ydims'][0], box[0]['ydims'][1]
            z_min, z_max = box[0]['zdims'][0], box[0]['zdims'][1]

            ### Distance to get into the box boundaries
            ### Auxiliar epsilon for not divide by zero
            for k in range(3):
                if dirc[k] < 1e-10:
                    dirc[k] = 1e-14


            tmin_x, tmax_x = (x_min - pos[0]) / dirc[0], (x_max - pos[0]) / dirc[0]
            tmin_y, tmax_y = (y_min - pos[1]) / dirc[1], (y_max - pos[1]) / dirc[1]
            tmin_z, tmax_z = (z_min - pos[2]) / dirc[2], (z_max - pos[2]) / dirc[2]

            ### When the particle goes in and out of each boundary
            t_in_x, t_out_x = min(tmin_x, tmax_x), max(tmin_x, tmax_x)
            t_in_y, t_out_y = min(tmin_y, tmax_y), max(tmin_y, tmax_y)
            t_in_z, t_out_z = min(tmin_z, tmax_z), max(tmin_z, tmax_z)

            ### If the particle enters the box, should be inside the three boundaries
            t_in_box = max(t_in_x, t_in_y, t_in_z)

            ### If the particle goes out, then abandone one of the boundaries
            t_out_box = min(t_out_x, t_out_y, t_out_z)

            ### If the particle crash with the box,
            if t_in_box <= t_out_box and t_out_box > 0:
                if region == 2:
                    # If is inside the box, the distance is the one of exit
                    dist_geo = t_out_box
                    # print("Usando la distancia de salida de la caja")
                else:
                    # If it is out the box, the distance is the one of entrance
                    dist_geo = t_in_box if t_in_box > 0 else np.inf
                    # print("Usando la distancia de entrada a la caja")
            else: # In this case we already pass the box and the trayectory is to the boundary. So, we need to solve the sphere distance equation
                A_sph = np.dot(dirc, dirc)
                B_sph = 2.0 * np.dot(pos, dirc)
                C_sph = np.dot(pos, pos) - sphere_r**2
                disc = B_sph**2 - 4.0 * A_sph * C_sph
                dist_geo = (-B_sph + np.sqrt(disc)) / (2.0 * A_sph)
                # print("Usando distancia a esfera")


            ### Choose the minimum distance of the step
            step = min(dist_geo, dist_sigma)

            epsilon = 1e-8 if step == dist_geo else 0.0

            # Now the position change with this step
            pos = beam_final[i]['pos'] + ((step + epsilon) * beam_final[i]['dir'])
            for k in range(3):
                if pos[k] < 1e-10:
                    pos[k] = 0.0
                if dirc[k] < 1e-10:
                    dirc[k] = 0.0

            beam_final[i]['pos'] = pos
            if (beam_final[i]['alive'] == False):
                writer.writerow(beam_final[i]['pos'])
            # if (np.sqrt(np.dot(pos, pos)) == dist_sigma):

            beam_final[i]['region'] = region

            print(beam_final[i])

    # print(beam_final)


























# # --------- GEOMETRY DEFINITION ---------
# # # --------- UNIVERSE ---------
# body = 'sphere'
# sphere_r = 30.0 # With this vector we will define a sphere of radius 10.0
# sphere_o = np.array([0.0, 0.0, 0.0])
#
# def geometry_body(body_type):
#     if (body_type == 'sphere'):
#         sphere_layout = np.dtype([
#             ("type", "i4"),
#             ("radius", "f8"),
#             ("origin", "f8", (3,))
#             ])
#         sphere = np.zeros(1, dtype=sphere_layout)
#         sphere['type'], sphere['radius'], sphere['origin'] = body, sphere_r, sphere_o
#







#
# if (body == 'sphere'):
#     body = int(1)
#
# box_layout = np.dtype([
#     ("type", "i4"), # Geometric body
#     ("xdims", 'f8', (2,)),
#     ("ydims", 'f8', (2,)),
#     ("zdims", 'f8', (2,)),
#     ])
#
# box = np.zeros(1, dtype=box_layout)
#
# body = 'box'
# if body == 'box':
#     body = int(2)
#
# box['type'], box['xdims'], box['ydims'], box['zdims'] = body, np.array([-4.0, 4.0]), np.array([-4.0, 4.0]), np.array([5.0, 15.0])
#
# # Once the beam is ready, the transport occur in the incoming lines
# sigma_sph = 1e1
# sigma_box = 5e1

# beam_final = np.zeros(nro_part, dtype=particle_layout)
# for i in range(nro_part):
#     print(f"Transporte de la partícula {i+1}")
#     beam_final[i] = beam[i] # Copy beam information in a new layout
#     cont = 0
#     while (beam_final[i]['alive']):
#         cont += 1
#         pos = beam_final[i]['pos']
#         dirc = beam_final[i]['dir']
#         region = beam_final[i]['region']
#
#         # Verify where the particle is
#         if (box[0]['xdims'][0] <= pos[0] <= box[0]['xdims'][1] and
#             box[0]['ydims'][0] <= pos[1] <= box[0]['ydims'][1] and
#             box[0]['zdims'][0] <= pos[2] <= box[0]['zdims'][1]):
#             region = 2
#         elif (np.dot(pos, pos) > sphere_r**2):
#             region = 3
#             beam_final[i]['alive'] = False
#             continue
#         else:
#             region = 1
#
#         if (region == 1):
#             sigma = sigma_sph
#         elif (region == 2):
#             sigma = sigma_box
#
#         beam_final[i]['region'] = region
#
#         # Calculate distance of next step
#         ## Calculate sigma distance
#         dist_sigma = -np.log(np.random.rand(1)) / sigma
#
#         ## Calculate distance to box
#         ### Boundaries of the box in each axes
#         x_min, x_max = box[0]['xdims'][0], box[0]['xdims'][1]
#         y_min, y_max = box[0]['ydims'][0], box[0]['ydims'][1]
#         z_min, z_max = box[0]['zdims'][0], box[0]['zdims'][1]
#
#         ### Distance to get into the box boundaries
#         ### Auxiliar epsilon for not divide by zero
#         for k in range(3):
#             if dirc[k] < 1e-10:
#                 dirc[k] = 1e-14
#
#         tmin_x, tmax_x = (x_min - pos[0]) / dirc[0], (x_max - pos[0]) / dirc[0]
#         tmin_y, tmax_y = (y_min - pos[1]) / dirc[1], (y_max - pos[1]) / dirc[1]
#         tmin_z, tmax_z = (z_min - pos[2]) / dirc[2], (z_max - pos[2]) / dirc[2]
#
#         ### When the particle goes in and out of each boundary
#         t_in_x, t_out_x = min(tmin_x, tmax_x), max(tmin_x, tmax_x)
#         t_in_y, t_out_y = min(tmin_y, tmax_y), max(tmin_y, tmax_y)
#         t_in_z, t_out_z = min(tmin_z, tmax_z), max(tmin_z, tmax_z)
#
#         ### If the particle enters the box, should be inside the three boundaries
#         t_in_box = max(t_in_x, t_in_y, t_in_z)
#
#         ### If the particle goes out, then abandone one of the boundaries
#         t_out_box = min(t_out_x, t_out_y, t_out_z)
#
#         ### If the particle crash with the box,
#         if t_in_box <= t_out_box and t_out_box > 0:
#             if region == 2:
#                 # If is inside the box, the distance is the one of exit
#                 dist_geo = t_out_box
#                 # print("Usando la distancia de salida de la caja")
#             else:
#                 # If it is out the box, the distance is the one of entrance
#                 dist_geo = t_in_box if t_in_box > 0 else np.inf
#                 # print("Usando la distancia de entrada a la caja")
#         else: # In this case we already pass the box and the trayectory is to the boundary. So, we need to solve the sphere distance equation
#             A_sph = np.dot(dirc, dirc)
#             B_sph = 2.0 * np.dot(pos, dirc)
#             C_sph = np.dot(pos, pos) - sphere_r**2
#             disc = B_sph**2 - 4.0 * A_sph * C_sph
#             dist_geo = (-B_sph + np.sqrt(disc)) / (2.0 * A_sph)
#             # print("Usando distancia a esfera")
#
#
#         ### Choose the minimum distance of the step
#         step = min(dist_geo, dist_sigma)
#
#         epsilon = 1e-8 if step == dist_geo else 0.0
#
#         # Now the position change with this step
#         pos = beam_final[i]['pos'] + ((step + epsilon) * beam_final[i]['dir'])
#         for k in range(3):
#             if pos[k] < 1e-10:
#                 pos[k] = 0.0
#             if dirc[k] < 1e-10:
#                 dirc[k] = 0.0
#
#         beam_final[i]['pos'] = pos
#         beam_final[i]['region'] = region
#
#         print(beam_final[i])
#
# print(beam_final)
