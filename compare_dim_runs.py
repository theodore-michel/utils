import numpy as np
import matplotlib.pyplot as plt
import os

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
    Avg      = np.mean( LCropped , axis=1 )
    AbsAvg   = np.abs(Avg)
    MeanLift = np.mean(AbsAvg, axis=0)
    return(MeanLift)


### SUBPLOTS

### MESH COMPARISON
colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
color_it  = 0
linestl   = ['dotted','solid','dashed']
line_it   = 0
figm,axm  = plt.subplots(1,1,figsize=(8,6))
for conf in ['1','2','3']:
    line_it = 0
    for mesh in ['C','M','F']:
        strDT         = '005'
        Lifts         = retrieve_lifts(conf+mesh+strDT+'/Resultats/') # setups+'/Resultats/'
        SimuTime      = retrieve_time(conf+mesh+strDT+'/Resultats/')  # setups+'/Resultats/'
        F_of_T        = []
        for t in SimuTime[5:]:
            if t<1.1: F_of_T.append(compute_mlift(Lifts, window=[0.1,t], dt=0.05))
            else: F_of_T.append(compute_mlift(Lifts, window=[0.5,t], dt=0.05))
        F_of_T = np.array(F_of_T)

        axm.plot(SimuTime[5:], F_of_T, linestyle=linestl[line_it], color = colors[color_it], label=f'conf {conf} mesh {mesh}', linewidth=0.7)    
        
        line_it += 1
    color_it += 1

handles, labels = axm.get_legend_handles_labels()
axm.grid()
axm.set(xlabel='Time (s)', ylabel='Mean Abs Lift')
axm.tick_params(labelright=True, labelleft=True, left=True, right=True)
axm.legend(handles, labels, loc = 'upper center', ncol=3)
figm.suptitle('Mesh comparison for dt=0.05')
figm.tight_layout()
figm.savefig('MESH_COMP_PLOT.png')

### DT COMPARISON
colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
color_it  = 0
linestl   = ['dotted','solid','dashed']
line_it   = 0
figd,axd  = plt.subplots(1,1,figsize=(8,6))
for conf in ['1','2','3']:
    line_it = 0
    for DT in [0.1, 0.05, 0.025]:
        strDT         = '0'+str(DT)[2:]
        mesh          = 'M'
        Lifts         = retrieve_lifts(conf+mesh+strDT+'/Resultats/') # setups+'/Resultats/'
        SimuTime      = retrieve_time(conf+mesh+strDT+'/Resultats/')  # setups+'/Resultats/'
        F_of_T        = []
        for t in SimuTime[5:]:
            if t<1.1: F_of_T.append(compute_mlift(Lifts, window=[0.1,t], dt=DT))
            else: F_of_T.append(compute_mlift(Lifts, window=[0.5,t], dt=DT))
        F_of_T = np.array(F_of_T)

        axd.plot(SimuTime[5:], F_of_T, linestyle=linestl[line_it], color = colors[color_it], label=f'conf {conf} dt {DT}', linewidth=0.7)    
        
        line_it += 1
    color_it += 1

handles, labels = axd.get_legend_handles_labels()
axd.grid()
axd.set(xlabel='Time (s)', ylabel='Mean Abs Lift')
axd.tick_params(labelright=True, labelleft=True, left=True, right=True)
axd.legend(handles, labels, loc = 'upper center', ncol=3)
figd.suptitle('DT comparison for mesh M')
figd.tight_layout()
figd.savefig('DT_COMP_PLOT.png')


### WINDOW COMPARISON
colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
color_it  = 0
linestl   = ['solid','dashed','dotted']
line_it   = 0
figw,axw  = plt.subplots(1,1,figsize=(8,6))
for conf in ['1','2','3']:
    line_it = 0
    for wndw in [200, 300, 400]:
        strDT         = '005'
        mesh          = 'M'
        Lifts         = retrieve_lifts(conf+mesh+strDT+'/Resultats/')
        SimuTime      = retrieve_time(conf+mesh+strDT+'/Resultats/')  
        F_of_T        = []
        for t in SimuTime[int(100/0.05):]:
            if t<=wndw: F_of_T.append(compute_mlift(Lifts, window=[100,t], dt=0.05))
            else: F_of_T.append(compute_mlift(Lifts, window=[100,wndw], dt=0.05))
        F_of_T = np.array(F_of_T)

        axw.plot(SimuTime[int(100/0.05):], F_of_T, linestyle=linestl[line_it], color = colors[color_it], label=f'conf {conf} window 100-{wndw}', linewidth=0.8)    
        
        line_it += 1
    color_it += 1

handles, labels = axw.get_legend_handles_labels()
axw.grid()
axw.set(xlabel='Time (s)', ylabel='Mean Abs Lift')
axw.tick_params(labelright=True, labelleft=True, left=True, right=True)
axw.legend(handles, labels, loc = 'upper center', ncol=3)
figw.suptitle('Window comparison for mesh M, dt=0.05')
figw.tight_layout()
figw.savefig('WINDOW_COMP_PLOT.png')
