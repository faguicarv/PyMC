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
dir_0 = np.random.randn(nro_part, 3)
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
sphere_r = 10.0 # With this vector we will define a sphere of radius 100.0

# Once the beam is ready, the transport occur in the incoming lines
sigma_vac = 1e-14
sigma_mat = 1e-1

beam_final = np.zeros(nro_part, dtype=particle_layout)
for i in range(nro_part):
    beam_final[i] = beam[i]
    initial_dist = -np.log(np.random.rand(1)) / sigma_mat
    beam_final[i]['pos'] = beam_final[i]['pos'] + (initial_dist * beam_final[i]['dir'])
    while np.any(beam_final[i]['alive']):
        dist_step = -np.log(np.random.rand(1)) / sigma_mat
        dist_bound = np.sum(beam_final[i]['pos'] * beam_final[i]['dir'])
        dist = np.minimum(dist_step, dist_bound)
        beam_final[i]['pos'] = beam_final[i]['pos'] + (dist * beam_final[i]['dir'])
        norm = np.linalg.norm(beam_final[i]['pos'])
        if (norm > sphere_r):
            pichintun = sphere_r - norm
            beam_final[i]['alive'] = False
            beam_final[i]['pos'] = beam_final[i]['pos'] + (pichintun * beam_final[i]['dir'])
            norm = np.linalg.norm(beam_final[i]['pos'])

            # beam_final[i]['pos'] = [0.0, 0.0, sphere_r]
            break;
#
        print(beam_final[i])
        print(norm)
#
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
