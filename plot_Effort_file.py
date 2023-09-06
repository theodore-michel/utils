import numpy as np
import matplotlib.pyplot as plt
import os, sys

### INPUTS
NAME   = str(sys.argv[1])
WINDOW = [ float(sys.argv[2]) , float(sys.argv[3]) ]

INCR = []
TIME = []
CX   = []
CY   = []

with open(os.getcwd() + '/' + NAME + '.txt', 'r') as f:
    next(f) # Skip header
    for line in f:
        INCR.append(int(line.split()[0]))
        TIME.append(float(line.split()[1]))
        CX.append(float(line.split()[2]))
        CY.append(float(line.split()[3]))
INCR = np.array(INCR)
TIME = np.array(TIME)
CX   = np.array(CX)
CY   = np.array(CY)

DT        = TIME[1]-TIME[0]
WINDOW[1] = min(WINDOW[1],TIME[-1])
Indexes   = (int(WINDOW[0]/DT),int(WINDOW[1]/DT))

### FUNCTION
def moving_avg(List, window=50):
    MAList   = []
    for i in range(len(List)):
        MAList.append(np.mean(List[max(0,i-window):i+1]))
    return(MAList)
CX_ma = moving_avg(CX,50)
CY_ma = moving_avg(CY,50)

### PLOTS
CX_limits = (min(CX[Indexes[0]:Indexes[1]]), max(CX[Indexes[0]:Indexes[1]]))
CY_limits = (min(CY[Indexes[0]:Indexes[1]]), max(CY[Indexes[0]:Indexes[1]]))
# CX
fig1, ax1  = plt.subplots(figsize=(10,8))
ax1.plot(TIME[Indexes[0]:Indexes[1]],  CX[Indexes[0]:Indexes[1]],    color = 'lightgray', linewidth = 0.6, label = 'Instant', linestyle='-')
ax1.plot(TIME[Indexes[0]:Indexes[1]],  CX_ma[Indexes[0]:Indexes[1]], color = 'black',     linewidth = 1, label = 'Moving Average',  linestyle='-')
ax1.legend(loc="lower right", fontsize="large")  # Set the font size to "small"
ax1.grid(False)# (True, linewidth=0.5, linestyle='--', color='gray')
ax1.set_title(f'{NAME} Cx')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Cx')
ax1.set_xlim((WINDOW[0],WINDOW[1]))
ax1.set_ylim((CX_limits[0],CX_limits[1]))
ax1.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
fig1.tight_layout()
fig1.savefig(f'{NAME}_CX.png')

# CY
fig2, ax2  = plt.subplots(figsize=(10,8))
ax2.plot(TIME[Indexes[0]:Indexes[1]],  CY[Indexes[0]:Indexes[1]],    color = 'lightgray', linewidth = 0.6, label = 'Instant', linestyle='-')
ax2.plot(TIME[Indexes[0]:Indexes[1]],  CY_ma[Indexes[0]:Indexes[1]], color = 'black',     linewidth = 1, label = 'Moving Average',  linestyle='-')
ax2.legend(loc="lower right", fontsize="large")  # Set the font size to "small"
ax2.grid(False)# (True, linewidth=0.5, linestyle='--', color='gray')
ax2.set_title(f'{NAME} Cy')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Cy')
ax2.set_xlim((WINDOW[0],WINDOW[1]))
ax2.set_ylim((CY_limits[0],CY_limits[1]))
ax2.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
fig2.tight_layout()
fig2.savefig(f'{NAME}_CY.png')

