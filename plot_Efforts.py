import numpy as np
import matplotlib.pyplot as plt
import os, sys

### INPUTS
PATH_TO_EFFORTS = str(sys.argv[1])
WINDOW          = [ float(sys.argv[2]) , float(sys.argv[3]) ]
DT              = float(sys.argv[4])

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

### PLOTS
Lifts = retrieve_lifts(PATH_TO_EFFORTS)
Mean  = compute_mlift(Lifts, WINDOW, DT)
Time  = np.arange(WINDOW[0], WINDOW[1], DT)
TimeExtended = np.arange(1, WINDOW[1], DT)

plt.plot(Time, Mean, label='Mean Lift', linestyle='solid', linewidth=0.5)
plt.legend()
plt.xlabel('time (s)')
plt.ylabel('mean lift')
plt.title(f'Mean Lift over Time')
plt.savefig('MEAN_LIFT_PLOT.png')
plt.show()

### SUBPLOTS
fig, axs = plt.subplots(3,2, figsize=(10,10))
axs[0, 0].plot(TimeExtended, Lifts[0][10:], color = 'darkblue', linewidth=0.5)
axs[0, 0].set_title('Efforts0')
axs[0, 1].plot(TimeExtended, Lifts[1][10:], color = 'darkblue', linewidth=0.5)
axs[0, 1].set_title('Efforts1')
axs[1, 0].plot(TimeExtended, Lifts[2][10:], color = 'darkblue', linewidth=0.5)
axs[1, 0].set_title('Efforts2')
axs[1, 1].plot(TimeExtended, Lifts[3][10:], color = 'darkblue', linewidth=0.5)
axs[1, 1].set_title('Efforts3')
axs[2, 0].plot(TimeExtended, Lifts[4][10:], color = 'darkblue', linewidth=0.5)
axs[2, 0].set_title('Efforts4')
axs[2, 1].plot(TimeExtended, Lifts[5][10:], color = 'darkblue', linewidth=0.5)
axs[2, 1].set_title('Efforts5')
for ax in axs.flat:
    ax.grid()
    ax.set(xlabel='time (s)', ylabel='Lift')
    ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
# for ax in axs.flat:
#     ax.label_outer()
fig.suptitle(f'Lift Efforts Plot')
fig.tight_layout()
plt.show()
plt.savefig('EFFORTS_PLOT.png')