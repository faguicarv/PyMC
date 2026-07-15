import numpy as np

# --------- BEAM INPUT INTO A LAYOUT DEFINITION ---------
def beam_definition(part, number_part, pos, dirc, energy):
    if (part == 'neutron'):
        part = 21

    # Layout with all information of the particle
    particle_layout = np.dtype([
        ("type", "i4"), # Particle type
        ("pos", 'f8', (3,)), # Position
        ('energy', 'f8'), # Energy
        ('dir', 'f8', (3,)), # Direction
        ('region', 'f8'), # Region
        ('alive', 'b1') # Border condition
        ])

    source = np.zeros(number_part, dtype=particle_layout) # Create an auxiliar layout with the same shape to re-write the initial values of the beam
    particles = np.zeros(number_part, dtype=particle_layout) # Create an auxiliar layout with the same shape to re-write the initial values of the beam
    source['type'], source['pos'], source['energy'], source['dir'], source['alive'], source['region'] = part, pos, energy, dirc, True, 0 # Fill the beam layout with the data of the beam definition
    return source, particles

def box_def(xlim, ylim, zlim):
    box_layout = np.dtype([
    ("xdims", 'f8', (2,)),
    ("ydims", 'f8', (2,)),
    ("zdims", 'f8', (2,)),
    ])

    box = np.zeros(1, dtype=box_layout)
    box['xdims'], box['ydims'], box['zdims'] = np.array(xlim), np.array(ylim), np.array(zlim)
    return box

