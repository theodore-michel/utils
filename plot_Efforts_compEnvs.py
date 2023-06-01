import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as plc
import os, sys

### INPUTS
WINDOW          = [ float(sys.argv[1]) , float(sys.argv[2]) ]
DT              = float(sys.argv[3])
PATH            = sys.argv[4]

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
    # L is an array of shape (8,timesteps)
    LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg      = np.mean( LCropped , axis=0 )
    return(Avg)

### SUBPLOTS
fig, axs = plt.subplots(3,2, figsize=(10,10))
colors   = [1,2,3,4,5]
cmap     = plt.cm.winter  # jet, gnuplot, gnuplot2, hot
norm     = plc.Normalize(vmin=colors[0], vmax=colors[-1])
color_it = 1
start    = int(1/DT)

figm,axm = plt.subplots(1,1,figsize=(10,10))

for setups in ['0','25','50','80','799']:
    Lifts        = retrieve_lifts(PATH+setups+'/LiftSensor/')
    SimuTime     = retrieve_time(PATH+setups+'/LiftSensor/')
    Time         = SimuTime[int(WINDOW[0]//DT) : int(WINDOW[1]//DT) ] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtended = SimuTime[start:] # np.arange(1, WINDOW[1], DT)
    Mean         = compute_mlift(Lifts, WINDOW, DT)


    axm.plot(Time, Mean, linestyle='solid', color = cmap(norm(color_it)), label='env'+setups, linewidth=1)
    axm.legend()
    axm.grid()
    axm.set(xlabel='time (s)', ylabel='mean lift')
    axm.tick_params(labelright=True, labelleft=True, left=True, right=True)


    axs[0, 0].plot(TimeExtended, Lifts[0][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[0, 0].set_title('Efforts0')
    axs[0, 0].legend()
    axs[0, 1].plot(TimeExtended, Lifts[1][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[0, 1].set_title('Efforts1')
    axs[0, 1].legend()
    axs[1, 0].plot(TimeExtended, Lifts[2][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[1, 0].set_title('Efforts2')
    axs[1, 0].legend()
    axs[1, 1].plot(TimeExtended, Lifts[3][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[1, 1].set_title('Efforts3')
    axs[1, 1].legend()
    axs[2, 0].plot(TimeExtended, Lifts[4][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[2, 0].set_title('Efforts4')
    axs[2, 0].legend()
    axs[2, 1].plot(TimeExtended, Lifts[5][start:], color = cmap(norm(color_it)), label='env'+setups, linewidth=0.5)
    axs[2, 1].set_title('Efforts5')
    axs[2, 1].legend()

    color_it+=1

for ax in axs.flat:
    ax.grid()
    ax.set(xlabel='time (s)', ylabel='Lift')
    ax.tick_params(labelright=True, labelleft=True, left=True, right=True)

fig.suptitle('Lift Efforts Plot')
fig.tight_layout()
fig.savefig('EFFORTS_PLOT_COMPARISON.png')
figm.suptitle('Mean Lift over Time')
figm.tight_layout()
figm.savefig('MEAN_LIFT_PLOT_COMPARISON.png')

plt.show()