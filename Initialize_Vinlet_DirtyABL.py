import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

# Check if the user provided the input.t file as a command-line argument
if len(sys.argv) != 3:
    print("Usage: python name_of_script.py input.t profile.csv")
    sys.exit(1)
mesh_file = sys.argv[1]
csv_file  = sys.argv[2]

# Load the CSV file with Z coordinates and Velocity
PROFILE = pd.read_csv(csv_file, sep=";")

# Load the .t mesh file
with open(mesh_file, 'r') as MESH:
    MESH_LINES = MESH.readlines()

# Parse the header of the .t mesh file to get the number of mesh points
num_points = int(MESH_LINES[0].strip().split()[0])

# Extract the Z coordinates from the mesh file
z_coordinates = [float(line.strip().split()[2]) for line in MESH_LINES[1:num_points + 1]]
velocity_vectors = []

# Associate velocities from the CSV file based on Z coordinates
for z in tqdm(z_coordinates):
    # Find the corresponding row in the CSV file based on the Z coordinate
    matching_row = PROFILE[(PROFILE['Z'] <= z) & (PROFILE['Z'].shift(-1) >= z)]

    # Extract the Velocity value or set it to 0 if there is no match
    if not matching_row.empty:
        velocity = matching_row['Vx'].values[0]
    else:
        velocity = 0

    # Append the velocity vector to the list
    velocity_vectors.append([velocity, 0, 0])

# Save the result to a .mtc file
mtc_file = 'VitesseInlet.mtc'
with open(mtc_file, 'w') as mtc:
    # Write mtc file header for Champ VitesseIn
    mtc.write("{ Type= P1_Vecteur_Par }\n")
    mtc.write("{ Nom= VitesseIn }\n")
    mtc.write("{ Data=  " + str(num_points) + " 3\n")

    # Write Data
    for vector in velocity_vectors:
        mtc.write(f'{vector[0]} {vector[1]} {vector[2]}\n')

    # Write footer to close Champ VitesseIn
    mtc.write("}")

print(f'Generated {mtc_file} successfully.')