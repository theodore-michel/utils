import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plc
import os, sys

### INPUTS
if len(sys.argv) != 4:
    print("Usage: python script.py start end dt")
    sys.exit(1)
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

def retrieve_time(path):
    T = [ ]
    with open(os.getcwd() + '/' + path + 'Efforts0.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            T.append(float(line.split()[1])) # select time column value
    T = np.array(T)
    return(T)

### FUNCTION
def compute_mlift(L, window=[50,100], dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg      = np.mean( LCropped , axis=0 )
    return(Avg)

### SUBPLOTS
fig, axs = plt.subplots(3,2, figsize=(10,8))
colors   = [1,2,3,4,5,6,7,8,9,10]
colors   =['darkblue', 'darkgreen', 'darkred']
cmap     = plt.cm.tab10
norm     = plc.Normalize(vmin=1, vmax=10)
color_it = 0
start    = int(1/DT)

figm,axm = plt.subplots(1,1,figsize=(5,5))

# for setups in ['0','25','50','80','799']:
#     Lifts        = retrieve_lifts(PATH+setups+'/LiftSensor/')
#     SimuTime     = retrieve_time(PATH+setups+'/LiftSensor/')
#     Time         = SimuTime[int(WINDOW[0]//DT) : int(WINDOW[1]//DT) ] # np.arange(WINDOW[0], WINDOW[1], DT)
#     TimeExtended = SimuTime[start:] # np.arange(1, WINDOW[1], DT)
#     Mean         = compute_mlift(Lifts, WINDOW, DT)
Lifts_min = 0
Lifts_max = 0
for setups in ['conf1','conf2','conf3']:
    Lifts         = retrieve_lifts(setups+'/') # setups+'/Resultats/'
    SimuTime      = retrieve_time(setups+'/')  # setups+'/Resultats/'
    Mean          = compute_mlift(Lifts, WINDOW, DT)
    start         = int(1/DT)
    Mean          = compute_mlift(Lifts, WINDOW, DT)
    Time          = SimuTime[int(WINDOW[0]//DT) : int(WINDOW[1]//DT) ] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtended  = SimuTime[start:] # np.arange(1, WINDOW[1], DT)
    Flat_Lifts    = [item for sublist in Lifts for item in sublist[start:]]
    Lifts_min     = min(Lifts_min, min(Flat_Lifts))
    Lifts_max     = max(Lifts_max, max(Flat_Lifts))


    axs[0, 0].plot(TimeExtended, Lifts[0][start:], color = colors[color_it], label=setups, linewidth=0.5)    # color = cmap(norm(color_it))
    axs[0, 0].set_title('Panel 1')
    axs[0, 0].legend(loc='upper right')
    axs[0, 1].plot(TimeExtended, Lifts[1][start:], color = colors[color_it], label=setups, linewidth=0.5)
    axs[0, 1].set_title('Panel 2')
    axs[0, 1].legend(loc='upper right')
    axs[1, 0].plot(TimeExtended, Lifts[2][start:], color = colors[color_it], label=setups, linewidth=0.5)
    axs[1, 0].set_title('Panel 3')
    axs[1, 0].legend(loc='upper right')
    axs[1, 1].plot(TimeExtended, Lifts[3][start:], color = colors[color_it], label=setups, linewidth=0.5)
    axs[1, 1].set_title('Panel 4')
    axs[1, 1].legend(loc='upper right')
    axs[2, 0].plot(TimeExtended, Lifts[4][start:], color = colors[color_it], label=setups, linewidth=0.5)
    axs[2, 0].set_title('Panel 5')
    axs[2, 0].legend(loc='upper right')
    axs[2, 1].plot(TimeExtended, Lifts[5][start:], color = colors[color_it], label=setups, linewidth=0.5)
    axs[2, 1].set_title('Panel 6')
    axs[2, 1].legend(loc='upper right')

    axm.plot(Time, Mean, linestyle='solid', color = colors[color_it], label=setups, linewidth=1)            # color = cmap(norm(color_it))
    axm.legend()
    axm.grid()
    axm.set(xlabel='time (s)', ylabel='mean lift')
    axm.tick_params(labelright=True, labelleft=True, left=True, right=True)

    color_it+=1

for ax in axs.flat:
    ax.grid()
    ax.set(xlabel='time (s)', ylabel='Lift', ylim=(min(Lifts_min,-1.05), max(Lifts_max,1.05)))
    ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.label_outer()

fig.suptitle(f'Lift Efforts Plot')
fig.tight_layout()
fig.savefig('COMPARE_EFFORTS_PLOT.png')

figm.suptitle('Mean Lift over Time')
figm.tight_layout()
figm.savefig('MEAN_LIFT_PLOT_COMPARISON.png')

plt.show()