import numpy as np

# --------- BEAM INPUT INTO A LAYOUT DEFINITION ---------
def beam_definition(**kwargs):

    # Layout with all information of the particle
    particle_layout = np.dtype([
        ("type", "i4"), # Particle type
        ("pos", 'f8', (3,)), # Position
        ('energy', 'f8'), # Energy
        ('dir', 'f8', (3,)), # Direction
        ('region', 'f8'), # Region
        ('alive', 'b1') # Border condition
        ])

    number_part = kwargs['number_particles']
    if (kwargs['particle'] == 'neutron'):
        kwargs['particle'] = 21

    source = np.zeros(number_part, dtype=particle_layout) # Create an auxiliar layout with the same shape to re-write the initial values of the beam
    source['type'], source['pos'], source['energy'], source['alive'], source['region'] = kwargs['particle'], kwargs['position'], kwargs['energy'], True, 0 # Fill the beam layout with the data of the beam definition

    if isinstance(kwargs['direction'], str) and kwargs['direction'].lower() == 'isotropic':
        rng = np.random.default_rng()
        cos_theta = rng.uniform(-1.0, 1.0, number_part)
        sin_theta = np.sqrt(1.0 - cos_theta**2)
        phi = rng.uniform(0.0, 2*np.pi, number_part)
        x = sin_theta * np.cos(phi)
        y = sin_theta * np.sin(phi)
        z = cos_theta
        source['dir'] = np.column_stack((x, y, z))

    return source

def geometry_body(body_type, **kwargs):
    if (body_type == 'sphere'):
        sphere_layout = np.dtype([
            ("radius", "f8"),
            ("origin", "f8", (3,))
            ])
        sphere = np.zeros(1, dtype=sphere_layout)
        # sphere['radius'], sphere['center'] = kwargs['radius'], kwargs['origin']
        sphere['radius'] = kwargs['radius']
        return sphere

    elif (body_type == 'box'):
        box_layout = np.dtype([
            ("xdims", 'f8', (2,)),
            ("ydims", 'f8', (2,)),
            ("zdims", 'f8', (2,)),
            ])
        box = np.zeros(1, dtype=box_layout)
        box['xdims'], box['ydims'], box['zdims'] = kwargs['xdims'], kwargs['ydims'], kwargs['zdims']
        return box
