### REORGANIZING VTU FILES

import sys, os

# Enter the path of the pbo results // ex : pbo_blm\results\panels_15-41-42\0
path = sys.argv[1]
res_path = path.split('\\') [0]
print(res_path)
# Enter the number of episodes and environments
ep = int(sys.argv[2])
env = int(sys.argv[3])
print(path)
print(res_path)

os.mkdir(f'{res_path}/vtu_video')

for i in range(ep * env):
    j = i*10
    os.system(f'cp -r {path}/{i}/vtu/*.vtu {res_path}/vtu_video/.')
    os.system(f'rm {res_path}\\vtu_video\panels_00000.vtu')  
    filenum = '0000'+str(j+0)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00100.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+1)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00200.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+2)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00300.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+3)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00400.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+4)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00500.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+5)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00600.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+6)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00700.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+7)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00800.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+8)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_00900.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')
    
    filenum = '0000'+str(j+9)
    filenum = filenum[-6:]
    os.system(f'mv {res_path}\\vtu_video\panels_01000.vtu {res_path}\\vtu_video\panels_{filenum}.vtu')

    # # os.system(f'del {path}\{i}\\vtu\panels_00000.vtu')  # keeping vtu files only after timestep 400
    # # os.system(f'del {path}\{i}\\vtu\panels_00100.vtu')
    # # os.system(f'del {path}\{i}\\vtu\panels_00200.vtu')
    # # os.system(f'del {path}\{i}\\vtu\panels_00300.vtu')
    # os.system(f'copy {path}\{i}\\vtu\*.vtu {res_path}\\vtu_video')

    # j = i * 7  # avoid identical numerotation
    # os.system(f'ren {res_path}\\vtu_video\panels_00400.vtu panels{j}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_00500.vtu panels{j+1}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_00600.vtu panels{j+2}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_00700.vtu panels{j+3}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_00800.vtu panels{j+4}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_00900.vtu panels{j+5}.vtu')
    # os.system(f'ren {res_path}\\vtu_video\panels_01000.vtu panels{j+6}.vtu')

