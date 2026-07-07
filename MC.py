import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import csv

# --------- DEFINE SOURCE WITH NUMPY ---------
## --------- SOURCE PARTICLE ---------
part_type = str('neutron') # Beam type
if (part_type == 'neutron'):
    part_type = 21
## --------- NUMBER OF PRIMARY PARTICLES ---------
nro_part = 20
## --------- INITIAL ENERGY - MONOENERGETIC ---------
energy_0 = 2.44e1 # Monoenergetic beam
## --------- POSITION OF SOURCE ---------
pos_0 = np.array([0.0, 0.0, 0.0])
## --------- DIRECTION OF SOURCE - ISOTROPIC ---------
# dir_0 = np.random.randn(nro_part, 3)
## --------- DIRECTION OF SOURCE - MONODIRECTIONAL ---------
dir_0 = np.array([0.0, 0.0, 3.4])
dir_0 = dir_0 / np.linalg.norm(dir_0) # Normalization of the direction
## ---------
# --------- END DEFINITION OF SOURCE ---------

# --------- BEAM INPUT INTO A LAYOUT DEFINITION ---------
# Layout with all information of the particle
particle_layout = np.dtype([
    ("type", "i4"), # Particle type
    ("pos", 'f8', (3,)), # Position
    ('energy', 'f8'), # Energy
    ('dir', 'f8', (3,)), # Direction
    ('alive', 'b1') # Border condition
    ])

beam = np.zeros(nro_part, dtype=particle_layout) # Create an auxiliar layout with the same shape to re-write the initial values of the beam

beam['type'], beam['pos'], beam['energy'], beam['dir'], beam['alive'] = part_type, pos_0, energy_0, dir_0, True # Fill the beam layout with the data of the beam definition


# --------- GEOMETRY DEFINITION ---------
## --------- UNIVERSE ---------
sphere_r = 10.0 # With this vector we will define a sphere of radius 10.0
box_
# Once the beam is ready, the transport occur in the incoming lines
sigma_vac = 1e-14
sigma_mat = 1e-1

beam_final = np.zeros(nro_part, dtype=particle_layout)
for i in range(nro_part):

    print(f"Transporte de la partícula {i+1}")
    beam_final[i] = beam[i] # Copy beam information in a new layout
    cont = 0

    # Verify if the particle is inside the sphere
    if (beam_final[i]['pos'].dot(beam_final[i]['pos']) > sphere_r**2):
        beam_final[i]['alive'] = False

    while (beam_final[i]['alive']):
        cont += 1
        dist_sigma = -np.log(np.random.rand(1)) / sigma_mat # Calculate sigma distance
        dist_bound =

        # dist_bound = sphere_r - np.linalg.norm(beam_final[i]['pos']) # Calculate boundary distance
        distance = min(dist_sigma, dist_bound) # Choose the minimum distance between the two
        # If the particle is at the boundary, then distance is zero and the loop will be infinite.
        # if (distance > 1e-7):
        if (distance <= 0.0):
            beam_final[i]['alive'] = False
        else:
            beam_final[i]['pos'] = beam_final[i]['pos'] + (distance * beam_final[i]['dir']) # Add minimum distance to initial position

        print(f"Paso {cont}")
        print(beam_final[i])

print(beam_final)
#         dist_step = -np.log(np.random.rand(1)) / sigma_mat
#         dist_bound = np.sum(beam_final[i]['pos'] * beam_final[i]['dir'])
#         dist = np.minimum(dist_step, dist_bound)
#         beam_final[i]['pos'] = beam_final[i]['pos'] + (dist * beam_final[i]['dir'])
#         norm = np.linalg.norm(beam_final[i]['pos'])
#         if (norm > sphere_r):
#             pichintun = sphere_r - norm
#             beam_final[i]['alive'] = False
#             beam_final[i]['pos'] = beam_final[i]['pos'] + (pichintun * beam_final[i]['dir'])
#             norm = np.linalg.norm(beam_final[i]['pos'])
#
#             # beam_final[i]['pos'] = [0.0, 0.0, sphere_r]
#             break;
# #
#         # print(beam_final[i])
#         print(norm)
#
    # print(beam_final)



#
#
#
# print(beam[0]['energy'])
# # # Verify if the particles are inside the defined geometry
# # initial_r = np.linalg.norm(beam['pos'], axis=1)
# # beam['alive'] = initial_r <= sphere_r
#
# # Transport the particles with the following function
# def trans_part(beam_array, sigma):
#     lengths = -np.log(np.random.rand(len(beam_array))) / sigma
#     lengths_reshaped = lengths[:, np.newaxis]
#
#     beam_array['pos'] = beam_array['pos'] + (lengths_reshaped * beam_array['dir'])
#     return beam_array
#
#
#
# print("Antes del transporte: ")
# print(beam)
#
# cont = 1
# #
# # for i in range(len(beam)):
# #     beam_final =
# while (beam['alive']):
#
#     mask = beam['alive']
#     beam[mask] = trans_part(beam[mask], sigma_mat)
#     new_r = np.linalg.norm(beam['pos'][mask], axis=1)
#     beam['alive'][mask] = new_r <= sphere_r
#     print(f"Transporte en el material paso {cont}: ")
#     print(beam)
#     cont += 1
#
#
#
#
#
