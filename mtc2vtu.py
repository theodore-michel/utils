import sys
import numpy as np
import pandas as pd
from tqdm import tqdm

# Check if the user provided the input.t file and VitesseIn.mtc file as command-line arguments
if len(sys.argv) != 3:
    print("Usage: python script.py input.t input.mtc")
    sys.exit(1)

# Get the input.t and VitesseIn.mtc file names from the command-line arguments
MESH_FILE = sys.argv[1]
MTC_FILE  = sys.argv[2]

# Load the .t mesh file
with open(MESH_FILE, 'r') as MESH:
    MESH_LINES = MESH.readlines()

# Extract the number of points and cells from the header of the .t mesh file
num_points = int(MESH_LINES[0].strip().split()[0])
tot_cells  = int(MESH_LINES[0].strip().split()[2])
num_cells  = 0
for line in MESH_LINES[num_points + 2:num_points + 2 + tot_cells]:
    # Assuming that the cell_line contains 4 integers separated by spaces
    if line.strip().split()[3] != '0':
        num_cells += 1

# Extract the Z coordinates from the mesh file
z_coordinates = [float(line.strip().split()[2]) for line in MESH_LINES[1:num_points + 1]]

# Load the .mtc file to retrieve velocity vectors
with open(MTC_FILE, 'r') as MTC:
    MTC_LINES = MTC.readlines()

# Extract velocity vectors from the .mtc file (skip the first 3 lines)
velocity_vectors = []
header_lines = 3  # Number of header lines to skip

for line in MTC_LINES[header_lines:]:
    if line.strip() == '}':
        break
    parts = line.strip().split()
    velocity_vectors.append([float(parts[0]), float(parts[1]), float(parts[2])])

# Create a VTU file manually
vtu_file = 'output.vtu'
with open(vtu_file, 'w') as vtu:
    vtu.write('<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
    vtu.write('<UnstructuredGrid>\n')
    vtu.write(f'<Piece NumberOfPoints="{num_points}" NumberOfCells="{num_cells}">\n')
    vtu.write('<Points>\n')
    vtu.write('<DataArray type="Float64" NumberOfComponents="3" format="ascii">\n')

    # Write mesh points
    print("Writing Points")
    for point_line in tqdm(MESH_LINES[1:num_points + 1]):
        x, y, z = map(float, point_line.strip().split()[:3])
        vtu.write(f'{x} {y} {z}\n')

    vtu.write('</DataArray>\n')
    vtu.write('</Points>\n')
    
    # Write cell connectivities
    vtu.write('<Cells>\n')
    vtu.write('<DataArray type="Int32" Name="connectivity" format="ascii">\n')

    print("Writing Connectivites")
    for cell_line in tqdm(MESH_LINES[num_points + 2:num_points + 2 + num_cells]):          
        connectivities = list(map(int, cell_line.strip().split()[:4]))
        # Subtract 1 from each value in the connectivities
        adjusted_connectivities = [str(val - 1) for val in connectivities]
        vtu.write(' '.join(adjusted_connectivities) + '\n')

    vtu.write('</DataArray>\n')

    # Write cell offsets
    vtu.write('<DataArray type="Int32" Name="offsets" format="ascii">\n')

    print("Writing Offsets")
    offset = 0
    for cell_line in tqdm(MESH_LINES[num_points + 2:num_points + 2 + num_cells]):
        connectivities = list(map(int, cell_line.strip().split()[:4]))
        offset += len(connectivities)
        vtu.write(f'{offset}\n')

    vtu.write('</DataArray>\n')

    # Write cell types
    vtu.write('<DataArray type="UInt8" Name="types" format="ascii">\n')

    print("Writing Types")
    for cell_line in tqdm(MESH_LINES[num_points + 2:num_points + 2 + num_cells]):
        # Assuming cell type 10 (Tetrahedron) for all cells
        vtu.write('10\n')
    vtu.write('</DataArray>\n')

    vtu.write('</Cells>\n')

    vtu.write('<PointData Scalars="Velocity">\n')
    vtu.write('<DataArray type="Float64" Name="Vitesse" NumberOfComponents="3" format="ascii">\n')

    # Write velocity vectors
    print("Writing Vitesse")
    for vector in tqdm(velocity_vectors):
        vtu.write(f'{vector[0]} {vector[1]} {vector[2]}\n')

    vtu.write('</DataArray>\n')
    vtu.write('</PointData>\n')
    vtu.write('</Piece>\n')
    vtu.write('</UnstructuredGrid>\n')
    vtu.write('</VTKFile>\n')

print(f'Generated {vtu_file} successfully.')