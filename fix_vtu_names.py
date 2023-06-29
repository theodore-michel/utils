### RENAME VTU FILES

import os
from tqdm import tqdm

path     = os.getcwd()

for filename in tqdm(os.listdir(path)):
    if filename.endswith('.vtu'):
        file_path = os.path.join(path, filename)
        new_filename = 'panels_'+filename.split('_')[-1][-9:]
        new_file_path = os.path.join(path, new_filename)
        os.rename(file_path, new_file_path)
    
print('done')

