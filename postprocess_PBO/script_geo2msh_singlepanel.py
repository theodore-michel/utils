import math as m
import sys, os
import time
import gmsh

# script python permettant de créer une simulation de 6 rangées de PV panels automatiquement

# entrée des paramètres fixes de la simulation
# cotes paneau Abiola2017 experimental study thesis
x_init = 9.325  # = 8.25 + (2.25-0.1)/2 (bottom left corner x coord of stand)
B = 2.49        # breadth of panel
L = 0.1         # streamwise width of stands
H = 1.11825     # height of panel stand = 1.15-0.03175
e = 0.03175     # thickness of panel
delta = 0       # distance between each row   

# entrée par l'utilisateur des valeurs d'angle souhaitées
k = 1   # facteur normalisation si angles entre -1 et 1 pour DRL

# calcul des angles en radians
theta1      = m.pi/180 * int(float(sys.argv[1])*k)  

# calcul des grandeurs utiles
Lp = L/m.cos(theta1)

# calcul des coordonnées des 8 points pour chaque rangée

## 1ERE RANGEE

x_1_1 = x_init
y_1_1 = 0
x_1_2 = x_1_1
y_1_2 = H - (Lp/2) * m.sin(theta1)
x_1_3 = x_1_1 - (B-Lp)/2 * m.cos(theta1)
y_1_3 = H - (B-Lp)/2 * m.sin(theta1)
x_1_4 = x_1_3 - e * m.sin(theta1)
y_1_4 = y_1_3 + e * m.cos(theta1)
x_1_5 = x_1_4 + B * m.cos(theta1)
y_1_5 = y_1_4 + B * m.sin(theta1)
x_1_6 = x_1_5 + e * m.sin(theta1)
y_1_6 = y_1_5 - e * m.cos(theta1)
x_1_7 = x_1_1 + L
y_1_7 = H + (Lp/2) * m.sin(theta1)
x_1_8 = x_1_7
y_1_8 = 0


# import du fichier GEO

geo = open("meshing/3D_config.geo", "r")
X = geo.readlines()
geo.close()

X[59] = f'x13 = {x_1_3}; y13 = {y_1_3};\n'
X[60] = f'x14 = {x_1_4}; y14 = {y_1_4};\n'
X[61] = f'x15 = {x_1_5}; y15 = {y_1_5};\n'
X[62] = f'x16 = {x_1_6}; y16 = {y_1_6};\n'

X[104] = f'x11 = {x_1_1}; y11 = {y_1_1};\n'
X[105] = f'x12 = {x_1_2}; y12 = {y_1_2};\n'
X[106] = f'x17 = {x_1_7}; y17 = {y_1_7};\n'
X[107] = f'x18 = {x_1_8}; y18 = {y_1_8};\n'

# Création d'un nouveau fichier .geo

f = open("maillage.geo", "w")
f.writelines(X)
f.close()

gmsh.initialize()
gmsh.option.setNumber("General.Verbosity", 1) # don't print gmsh's log except for errors

# # Maillage de gmsh et création du fichier .msh

gmsh.open("maillage.geo")


########### Création des fichiers de panneaux 3d indépendants with stand

theta = [theta1]

for i in range(len(theta)):

    # import du fichier GEO
    geo = open("meshing/3dpanelbottom_config.geo", "r")
    X = geo.readlines()
    geo.close()

    x1 = x_init + i * delta
    y1 = 0
    x2 = x1 
    y2 = H - (Lp/2) * m.sin(theta1)
    x3 = x1 - (B-Lp)/2 * m.cos(theta1)
    y3 = H - (B-Lp)/2 * m.sin(theta1)
    x4 = x3 - e * m.sin(theta1)
    y4 = y3 + e * m.cos(theta1)
    x5 = x4 + B * m.cos(theta1)
    y5 = y4 + B * m.sin(theta1)
    x6 = x5 + e * m.sin(theta1)
    y6 = y5 - e * m.cos(theta1)
    x7 = x1 + L
    y7 = H + (Lp/2) * m.sin(theta1)
    x8 = x7
    y8 = 0

    
    X[20] = f'x13 = {x3}; y13 = {y3};\n'
    X[21] = f'x14 = {x4}; y14 = {y4};\n'
    X[22] = f'x15 = {x5}; y15 = {y5};\n'
    X[23] = f'x16 = {x6}; y16 = {y6};\n'

    X[63] = f'x11 = {x1}; y11 = {y1};\n'
    X[64] = f'x12 = {x2}; y12 = {y2};\n'
    X[65] = f'x17 = {x7}; y17 = {y7};\n'
    X[66] = f'x18 = {x8}; y18 = {y8};\n'

# Modification du nom de fichier .msh

    X[186] = f'Save "3dpanelbottom{i}.msh";'

# Création d'un nouveau fichier .geo

    f = open(f"3dpanelbottom{i}.geo", "w")
    f.writelines(X)
    f.close()

# Ouverture et maillage de gmsh

    gmsh.open(f"3dpanelbottom{i}.geo")
    
########### Création des fichiers de panneaux 3d indépendants no stand

for i in range(len(theta)):

# import du fichier GEO

    geo = open("meshing/3dpanel_config.geo", "r")
    X = geo.readlines()
    geo.close()

    x1 = x_init + i * delta
    y1 = 0
    x2 = x1 
    y2 = H - (Lp/2) * m.sin(theta1)
    x3 = x1 - (B-Lp)/2 * m.cos(theta1)
    y3 = H - (B-Lp)/2 * m.sin(theta1)
    x4 = x3 - e * m.sin(theta1)
    y4 = y3 + e * m.cos(theta1)
    x5 = x4 + B * m.cos(theta1)
    y5 = y4 + B * m.sin(theta1)
    x6 = x5 + e * m.sin(theta1)
    y6 = y5 - e * m.cos(theta1)
    x7 = x1 + L
    y7 = H + (Lp/2) * m.sin(theta1)
    x8 = x7
    y8 = 0

    
    X[20] = f'x13 = {x3}; y13 = {y3};\n'
    X[21] = f'x14 = {x4}; y14 = {y4};\n'
    X[22] = f'x15 = {x5}; y15 = {y5};\n'
    X[23] = f'x16 = {x6}; y16 = {y6};\n'

# Modification du nom de fichier .msh

    X[71] = f'Save "3dpanel{i}.msh";'

# Création d'un nouveau fichier .geo

    f = open(f"3dpanel{i}.geo", "w")
    f.writelines(X)
    f.close()

# Ouverture et maillage de gmsh

    gmsh.open(f"3dpanel{i}.geo")    

########### Création du fichier allpanelmesh.t pour l'adaptation de maillage BLM

# import du fichier GEO

geo = open("meshing/allpanelmesh_config.geo", "r")
X = geo.readlines()
geo.close()


X[20] = f'x13 = {x_1_3}; y13 = {y_1_3};\n'
X[21] = f'x14 = {x_1_4}; y14 = {y_1_4};\n'
X[22] = f'x15 = {x_1_5}; y15 = {y_1_5};\n'
X[23] = f'x16 = {x_1_6}; y16 = {y_1_6};\n'


X[63] = f'x11 = {x_1_1}; y11 = {y_1_1};\n'
X[64] = f'x12 = {x_1_2}; y12 = {y_1_2};\n'
X[65] = f'x17 = {x_1_7}; y17 = {y_1_7};\n'
X[66] = f'x18 = {x_1_8}; y18 = {y_1_8};\n'

# Création d'un nouveau fichier .geo

f = open("allpanelmesh.geo", "w")
f.writelines(X)
f.close()

# Maillage de gmsh et création du fichier .msh

gmsh.open("allpanelmesh.geo")


gmsh.finalize()