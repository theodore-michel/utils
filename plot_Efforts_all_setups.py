import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plc
import os, sys

### INPUTS
WINDOW          = [ float(sys.argv[1]) , float(sys.argv[2]) ]
DT              = float(sys.argv[3])

### PREPROCESS
def retrieve_lifts(path):
    L = [ [], [], [], [], [], []]
    for i in range (6):
        with open(os.getcwd() + '/' + path + 'Efforts' + str(i) + '.txt', 'r') as f:
            next(f) # Skip header
            for line in f:
                L[i].append(float(line.split()[3])) # select Lift column value
    L = np.array(L)
    return(L)

### FUNCTION
def compute_mlift(L, window=[50,100], dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg      = np.mean( LCropped , axis=0 )
    return(Avg)

### SUBPLOTS
fig, axs = plt.subplots(3,2, figsize=(10,10))
colors   = [1,2,3]
cmap     = plt.cm.jet
norm     = plc.Normalize(vmin=1, vmax=3)
color_it = 1

for setups in ['setup0','setup1','setup2']:
    Lifts = retrieve_lifts(setups+'/Resultats/')
    TimeExtended = np.arange(1, WINDOW[1], DT)

    axs[0, 0].plot(TimeExtended, Lifts[0][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[0, 0].set_title('Efforts0')
    axs[0, 0].legend()
    axs[0, 1].plot(TimeExtended, Lifts[1][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[0, 1].set_title('Efforts1')
    axs[0, 1].legend()
    axs[1, 0].plot(TimeExtended, Lifts[2][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[1, 0].set_title('Efforts2')
    axs[1, 0].legend()
    axs[1, 1].plot(TimeExtended, Lifts[3][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[1, 1].set_title('Efforts3')
    axs[1, 1].legend()
    axs[2, 0].plot(TimeExtended, Lifts[4][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[2, 0].set_title('Efforts4')
    axs[2, 0].legend()
    axs[2, 1].plot(TimeExtended, Lifts[5][10:], color = cmap(norm(color_it)), label=setups, linewidth=0.7)
    axs[2, 1].set_title('Efforts5')
    axs[2, 1].legend()

    color_it+=1

for ax in axs.flat:
    ax.grid()
    ax.set(xlabel='time (s)', ylabel='Lift')
    ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
    
fig.suptitle(f'Lift Efforts Plot')
fig.tight_layout()
plt.show()
plt.savefig('COMPARE_EFFORTS_PLOT.png')