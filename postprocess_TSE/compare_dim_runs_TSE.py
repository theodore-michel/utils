from ast import List
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from plot_styles import scientific_style 
import csv

### INPUTS
n_args = len(sys.argv)
if n_args <3:
    print("Usage: python script.py plotstart name1 name2 name3 ... ")
    sys.exit(1)

PLOT_START          = float(sys.argv[1])
LIST_OF_OBJECTS     = ['','IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5']
OUTPUT_CSV          = 'compare_efforts.csv'
LIST_FOR_COMPARISON = []
for i in range(2,n_args):
    LIST_FOR_COMPARISON.append(str(sys.argv[i]))

### PREPROCESS
def retrieve_lift(path, suffix=''):
    L = [ ]
    with open(f'{os.getcwd()}/{path}Efforts{suffix}.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            L.append(float(line.split()[3])) # select Lift column value
    L = np.array(L)
    return(L)

def retrieve_drag(path, suffix=''):
    D = [ ]
    with open(f'{os.getcwd()}/{path}Efforts{suffix}.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            D.append(float(line.split()[1])) # select Lift column value
    D = np.array(D)
    return(D)

def retrieve_time(path, suffix=''):
    T = [ ]
    with open(f'{os.getcwd()}/{path}Efforts{suffix}.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            T.append(round(float(line.split()[0]),3)) # select time column value
    T = np.array(T)
    return(T)

def compute_mean(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    Mean     = np.mean( LCropped )
    return(Mean)

def compute_std(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    STD      = np.std( LCropped )
    return(STD)


### MESH COMPARISON
def CompareRuns(ListToCompare, plot_start=5, comparisontype='mesh'):
    colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    color_it  = 0
    linestl   = ['dotted','solid','dashed']
    line_it   = 0
    figl,axl  = plt.subplots(1,1,figsize=(11,6.5))
    figd,axd  = plt.subplots(1,1,figsize=(11,6.5))
    for data in ListToCompare:
        Lift          = retrieve_lift(f'simu_{data}/resultats/capteurs/') # setups+'/Resultats/'
        Drag          = retrieve_drag(f'simu_{data}/resultats/capteurs/')
        SimuTime      = retrieve_time(f'simu_{data}/resultats/capteurs/')  # setups+'/Resultats/'
        DT            = SimuTime[0]
        incr_start    = int(plot_start/DT)
        MeanLift      = []
        MeanDrag      = []
        for t in SimuTime[incr_start:]: # plot_start is when to start plotting and computing cumul avg (in s)
            MeanLift.append(compute_mean(Lift, window=[plot_start,t], dt=DT))
            MeanDrag.append(compute_mean(Drag, window=[plot_start,t], dt=DT))
        MeanLift = np.array(MeanLift)
        MeanDrag = np.array(MeanDrag)

        if comparisontype=='mesh': labelname = f'{data} mesh'
        if comparisontype=='dt': labelname = f'$\Delta t = {DT}$'

        axl.plot(SimuTime[incr_start:], MeanLift, linestyle=linestl[0], color=colors[color_it], label=f'$\overline{{F_z}}$ {labelname}', linewidth=1.3)    
        axl.plot(SimuTime[incr_start:], Lift[incr_start:],  linestyle=linestl[1], color=colors[color_it], label=f'$F_z$ {labelname}', linewidth=0.5, alpha=0.7) 

        axd.plot(SimuTime[incr_start:], MeanDrag, linestyle=linestl[0], color=colors[color_it], label=f'$\overline{{F_x}}$ {labelname}', linewidth=1.3)    
        axd.plot(SimuTime[incr_start:], Drag[incr_start:], linestyle=linestl[1], color=colors[color_it], label=f'$F_x$ {labelname}', linewidth=0.5, alpha=0.7) 

        color_it += 1

    handles, labels = axl.get_legend_handles_labels()
    axl.grid(True, linewidth=0.5, linestyle='--', color='gray')
    axl.set(xlabel='Time (s)', ylabel='$F_z$ (N)', xlim=(plot_start,SimuTime[-1])) # xlim=(plot_start,SimuTime[-1])
    axl.tick_params(labelright=True, labelleft=True, left=True, right=True)
    axl.legend(handles, labels, loc = 'lower center', ncol=3+(n_args-2)%3, fontsize='small')
    figl.suptitle(f'$F_z$ for different {comparisontype} resolutions - H3 IPE amont $\Theta=-5^{{\circ}}$ $V=50km.h^{{-1}}$')
    figl.tight_layout()
    figl.savefig(f'{comparisontype}_LIFT_COMP_PLOT.png')

    handles, labels = axd.get_legend_handles_labels()
    axd.grid(True, linewidth=0.5, linestyle='--', color='gray')
    axd.set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1])) # xlim=(plot_start,SimuTime[-1])
    axd.tick_params(labelright=True, labelleft=True, left=True, right=True)
    axd.legend(handles, labels, loc = 'lower center', ncol=3+(n_args-2)%3, fontsize='small')
    figd.suptitle(f'$F_x$ for different {comparisontype} resolutions - H3 IPE amont $\Theta=-5^{{\circ}}$ $V=50km.h^{{-1}}$')
    figd.tight_layout()
    figd.savefig(f'{comparisontype}_DRAG_COMP_PLOT.png')
    
    return()


### Data Evaluation
def PrintEvaluation(ListToCompare, OutputCSV='output.csv', plot_start=5, comparisontype='mesh', ListObjects=['']):
    # generate csv file
    with open(OutputCSV, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([comparisontype, 'object', 'function', 'value'])
        # compute values needed
        for data in ListToCompare:
            for object in ListObjects:
                # get data
                Lift          = retrieve_lift(f'simu_{data}/resultats/capteurs/', suffix=object) # setups+'/Resultats/'
                Drag          = retrieve_drag(f'simu_{data}/resultats/capteurs/', suffix=object)
                SimuTime      = retrieve_time(f'simu_{data}/resultats/capteurs/', suffix=object)  # setups+'/Resultats/'
                DT            = SimuTime[0]
                # compute values
                MeanLift      = compute_mean(Lift, window=[plot_start,SimuTime[-1]], dt=DT)
                MeanDrag      = compute_mean(Drag, window=[plot_start,SimuTime[-1]], dt=DT)
                STDLift       = compute_std(Lift, window=[plot_start,SimuTime[-1]], dt=DT)
                STDDrag       = compute_std(Drag, window=[plot_start,SimuTime[-1]], dt=DT)
                # names
                if comparisontype=='mesh': labelname = data
                if comparisontype=='dt':   labelname = f'dt{DT}'
                # write in csv
                csv_writer.writerow([labelname, object, 'Mean Lift', MeanLift])
                csv_writer.writerow([labelname, object, 'Mean Drag', MeanDrag])
                csv_writer.writerow([labelname, object, 'STD Lift',  STDLift])
                csv_writer.writerow([labelname, object, 'STD Drag',  STDDrag])
                # print to terminal
                print(f'\n {object} : \n')
                print(f'Mean Lift {labelname} : {MeanLift}')
                print(f'Mean Drag {labelname} : {MeanDrag}')
                print(f'STD Lift  {labelname} : {STDLift}')
                print(f'STD Drag  {labelname} : {STDDrag}')
                print()


### RUN
plt.style.use(scientific_style)
# CompareRuns(LIST_FOR_COMPARISON, PLOT_START, comparisontype='dt')
# CompareRuns(LIST_FOR_COMPARISON, PLOT_START, comparisontype='dt', ListObjects=LIST_OF_OBJECTS)
# CompareRuns(LIST_FOR_COMPARISON, PLOT_START, comparisontype='mesh')
# CompareRuns(LIST_FOR_COMPARISON, PLOT_START, comparisontype='mesh', ListObjects=LIST_OF_OBJECTS)
PrintEvaluation(LIST_FOR_COMPARISON, OUTPUT_CSV, PLOT_START, comparisontype='mesh', ListObjects=LIST_OF_OBJECTS)
