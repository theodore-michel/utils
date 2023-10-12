import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

# Check command-line arguments
if len(sys.argv) != 3:
    print("Usage: python name_of_script.py input.t profile.csv")
    sys.exit(1)
mesh_file = sys.argv[1]
csv_file  = sys.argv[2]

# Load the CSV file with Z coordinates and Velocity
PROFILE   = pd.read_csv(csv_file, sep=";")

# Load the .t mesh file
with open(mesh_file, 'r') as MESH:
    MESH_LINES = MESH.readlines()

# Get the number of mesh points
num_points = int(MESH_LINES[0].strip().split()[0])

# Extract the Z coordinates from mesh
z_coordinates = np.array([float(line.split()[2]) for line in MESH_LINES[1:num_points + 1]])

# Create an array for velocity vectors
velocity_vectors = np.zeros((num_points, 3))

# Calculate the velocity vectors
for i in range(num_points):
    z = z_coordinates[i]
    matching_rows = PROFILE[(PROFILE['Z'] <= z) & (PROFILE['Z'].shift(-1) >= z)]

    if not matching_rows.empty:
        velocity_vectors[i, 0] = matching_rows['Vx'].values[0]

# Save the result to a .mtc file
mtc_file = 'VitesseInlet.mtc'
champ    = 'VitesseIn'
with open(mtc_file, 'w') as mtc:
    # Write mtc file header for Champ VitesseIn
    mtc.write("{ Type= P1_Vecteur_Par }\n")
    mtc.write(f"{{ Nom= {champ} }}\n")
    mtc.write(f"{{ Data= {num_points} 3\n")

    # Write Data
    for vector in tqdm(velocity_vectors):
        mtc.write(f'{vector[0]} {vector[1]} {vector[2]}\n')

    # Write footer to close Champ VitesseIn
    mtc.write("}")

print(f'Generated {mtc_file} successfully.')