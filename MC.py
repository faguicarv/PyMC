import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import csv

# Geometry definition
sphere_r = 30.0 # With this vector we will define a sphere of radius 100.0

# Layout with all information of the particle
particle_layout = np.dtype([
    ("type", "i4"),
    ("pos", 'f8', (3,)),
    ('energy', 'f8'),
    ('dir', 'f8', (3,)),
    ('alive', 'b1')
    ])

# Beam definition
nro_part = 20
part_type = str('neutron') # Beam type
if (part_type == 'neutron'):
    part_type = 21
pos_0 = np.array([0.0, 0.0, 0.0]) # Initial position
energy_0 = 2.44e1 # Initial energy
dir_0 = np.array([0.0, 0.0, 2.0]) # Initial direction of the beam
dir_0 = dir_0 / np.linalg.norm(dir_0) # Normalization of the direction

beam = np.zeros(nro_part, dtype=particle_layout) # Create an arrange with the same shape as the layout to then put the values without a for cicle

beam['type'], beam['pos'], beam['energy'], beam['dir'], beam['alive'] = part_type, pos_0, energy_0, dir_0, True # Put values in the beam array


# Once the beam is ready, the transport occur in the incoming lines
sigma_vac = 1e-14
sigma_mat = 1e-1

beam_final = np.zeros(nro_part, dtype=particle_layout)
for i in range(nro_part):
    beam_final[i] = beam[i]
    while np.any(beam_final[i]['alive']):
        length = -np.log(np.random.rand(1)) / sigma_mat
        beam_final[i]['pos'] = beam_final[i]['pos'] + (length * beam_final[i]['dir'])
        norm = np.linalg.norm(beam_final[i]['pos'])
        if (norm > sphere_r):
            beam_final[i]['alive'] = False
            beam_final[i]['pos'] = [0.0, 0.0, sphere_r]

        print(beam_final[i])

print(beam_final)



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
