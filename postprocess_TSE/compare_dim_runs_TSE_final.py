from ast import List
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from plot_styles import scientific_style 
import csv
import re
import pandas as pd

### INPUTS
n_args = len(sys.argv)
if n_args <3:
    print("Usage: python script.py plotstart name1 name2 name3 ... ")
    sys.exit(1)

PLOT_START          = float(sys.argv[1])
LIST_OF_OBJECTS     = ['IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5']
                  # = ['','IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5', 'Poutre0', 'Poutre1', 'Poutre2', 'Poutre3', 'Poutre4', 'Poutre5']
                  # = ['','IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5']
OUTPUT_CSV          = 'compare_efforts.csv'
VITESSE_SIMU        = 50
SREF_FACTOR         = 2    # 2 if data from half-tables, 1 if data from full-tables
DT_SIMU             = 0.002 # for cropping increments in adapted axes function
ADAPTED_AXES        = True

LIST_FOR_COMPARISON = []
for i in range(2,n_args):
    LIST_FOR_COMPARISON.append(str(sys.argv[i]))



### PREPROCESS
def retrieve_lift(path, suffix=''):
    L = [ ]
    with open(f'{os.getcwd()}/{path}Efforts{suffix}.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            L.append(float(line.split()[3]) * SREF_FACTOR) # select Lift column value
    L = np.array(L)
    return(L)

def retrieve_drag(path, suffix=''):
    D = [ ]
    with open(f'{os.getcwd()}/{path}Efforts{suffix}.txt', 'r') as f:
        next(f) # Skip header
        for line in f:
            D.append(float(line.split()[1]) * SREF_FACTOR) # select Lift column value
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

def crop_data(data, start=5, dt=0.1):
    return(data[ int(start//dt) : ])

def compute_mean(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    Mean     = np.mean( LCropped )
    return(Mean)

def compute_std(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    STD      = np.std( LCropped )
    return(STD)

def compute_max(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    Mean     = np.max( LCropped )
    return(Mean)

def compute_min(L, window=[50,100], dt=0.1):
    LCropped = L[ int(window[0]//dt) : int(window[1]//dt) ]
    Mean     = np.min( LCropped )
    return(Mean)

def AxLimits4AllForces(ListToCompare, plot_start=5, ListObjects='', Function = 'Drag'):
    '''Read through capteurs data cropped starting at plot_start, filtered by ListObjects, Function (Drag or Lift according to subplot) 
    and determine a common (y_min,y_max) for all plots that will use this data.'''
    y_min  =  10000000
    y_max  = -10000000
    margin = 1.05
    for object in ListObjects:
        for data in ListToCompare:
            if Function=='Drag': 
                drag_data = crop_data(retrieve_drag(f'simu_{data}/resultats/capteurs/', suffix=object), start=plot_start, dt=DT_SIMU)
                y_min     = min(y_min,np.min(drag_data))
                y_max     = max(y_max,np.max(drag_data))
            if Function=='Lift':
                lift_data = crop_data(retrieve_lift(f'simu_{data}/resultats/capteurs/', suffix=object), start=plot_start, dt=DT_SIMU)
                y_min = min(y_min,np.min(lift_data))
                y_max = max(y_max,np.max(lift_data))
    y_min    = round(y_min * margin, 2)
    y_max    = round(y_max * margin, 2)
    return (y_min,y_max)

def rename_object(object):
    '''Rename Table0 to Table1, Table1 to Table2, ...'''
    if object.startswith(' IP'):
        return 'IPE'
    match = re.search(r'\d$', object)
    if match:
        object_name = re.sub(r'\d$', str(int(match.group()) + 1), object)
    else:
        object_name = object
    return object_name

def inverse_rename_object(object):
    '''Inverse of rename_object'''
    if object.startswith(' IP'):
        return 'IPE'
    match = re.search(r'\d$', object)
    if match:
        object_name = re.sub(r'\d$', str(int(match.group()) - 1), object)
    else:
        object_name = object
    return(object_name)

def reformat_TSE_csv(input_csv, output_csv):
    '''Reformat TSE csv file to be able to use it in the same way as my CIMLIB csv files'''
    df                  = pd.read_csv(input_csv+'.csv',sep=',')
    reformatted_df_50   = pd.DataFrame(columns=['simu', 'incidence', 'object', 'function', 'value'])
    reformatted_df_105  = pd.DataFrame(columns=['simu', 'incidence', 'object', 'function', 'value'])
    # rename 
    df['Configuration'] = df['Configuration'].replace({'Front': 'IPEAMONT', 'Rear': 'IPEAVAL'})
    df['Component']     = df['Component'].apply(inverse_rename_object)
    column_mapping      = {
                        'Alpha': 'incidence',
                        'Configuration': 'simu', 
                        'Component': 'object',
                        'Avg(Fx)': 'Mean Drag',
                        'Std(Fx)': 'STD Drag',
                        'Min(Fx)': 'Min Drag',
                        'Max(Fx)': 'Max Drag',
                        'Avg(Fz)': 'Mean Lift',
                        'Std(Fz)': 'STD Lift',
                        'Min(Fz)': 'Min Lift',
                        'Max(Fz)': 'Max Lift'
                        }
    df                  = df.rename(columns=column_mapping)
    # melt dataframe
    df                  = pd.melt(df, id_vars=['simu', 'object', 'Vinf', 'incidence'], var_name='function', value_name='value')
    # filter according to Vinf (50km/h or 105km/h)
    df_filtered_50      = df[df['Vinf']==13.8889]
    df_filtered_105     = df[df['Vinf']==29.1667]
    reformatted_df_50   = df_filtered_50[['simu', 'incidence', 'object', 'function', 'value']]
    reformatted_df_105  = df_filtered_105[['simu', 'incidence', 'object', 'function', 'value']]
    # save
    reformatted_df_50.to_csv(output_csv+"_50"+'.csv', index=False)
    reformatted_df_105.to_csv(output_csv+"_105"+'.csv', index=False)
    print(reformatted_df_50)
    print(reformatted_df_105)
    return()

def inverse_reformat_TSE_csv(input_csv, output_csv):
    '''Inverse of reformat_TSE_csv'''
    # read
    df_50               = pd.read_csv(input_csv+"_V50_FULLTABLE"+'.csv',sep=',')
    df_105              = pd.read_csv(input_csv+"_V105_FULLTABLE"+'.csv',sep=',')
    df_50['Vinf']       = 13.8889
    df_105['Vinf']      = 29.1667
    df                  = pd.concat([df_50, df_105])
    # rename
    column_mapping      = {
                        'incidence': 'Alpha',
                        'simu': 'Configuration', 
                        'object': 'Component',
                        'Mean Drag': 'Avg(Fx)',
                        'STD Drag': 'Std(Fx)',
                        'Min Drag': 'Min(Fx)',
                        'Max Drag': 'Max(Fx)',
                        'Mean Lift': 'Avg(Fz)',
                        'STD Lift': 'Std(Fz)',
                        'Min Lift': 'Min(Fz)',
                        'Max Lift': 'Max(Fz)'
                        }
    df                  = pd.pivot_table(df, index=['incidence', 'simu','object','Vinf'], columns='function', values='value').reset_index()
    df                  = df.rename(columns=column_mapping)
    df['Configuration'] = df['Configuration'].replace({'IPEAMONT': 'Front', 'IPEAVAL': 'Rear'})
    df['Component']     = df['Component'].apply(rename_object)
    # df['Component']     = df['Component'].replace({'IPE': 'IPN0'})
    # save
    # df                  = df['Configuration','Component','Vinf','Alpha','Avg(Fx)','Std(Fx)','Min(Fx)','Max(Fx)','Avg(Fz)','Std(Fz)','Min(Fz)','Max(Fz)']
    df.to_csv(output_csv+'.csv', index=False)
    print(df)
    return()


### MESH COMPARISON
def CompareRuns(ListToCompare, plot_start=5, comparisontype='mesh', ListObjects='', AdaptedAxes=True):
    '''Plot Lift and Drag for different mesh resolutions (ListToCompare) and different objects (ListObjects)'''
    colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    linestl   = ['dotted','solid','dashed']
    if AdaptedAxes: 
        y_min_D, y_max_D = AxLimits4AllForces(ListToCompare, plot_start, ListObjects, Function='Drag')
        y_min_L, y_max_L = AxLimits4AllForces(ListToCompare, plot_start, ListObjects, Function='Lift')
    # loop on simulations
    for object in ListObjects:
        color_it  = 0
        figl,axl  = plt.subplots(1,1,figsize=(11,6.5))
        figd,axd  = plt.subplots(1,1,figsize=(11,6.5))
        # loop on objects (ipe, table, poutre, ...)
        for data in ListToCompare:
            # get data
            Lift          = retrieve_lift(f'simu_{data}/resultats/capteurs/', suffix=object) # setups+'/Resultats/'
            Drag          = retrieve_drag(f'simu_{data}/resultats/capteurs/', suffix=object)
            SimuTime      = retrieve_time(f'simu_{data}/resultats/capteurs/', suffix=object)  # setups+'/Resultats/'
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
        if AdaptedAxes: axl.set(xlabel='Time (s)', ylabel='$F_z$ (N)', xlim=(plot_start,SimuTime[-1]), ylim=(y_min_L,y_max_L))
        else: axl.set(xlabel='Time (s)', ylabel='$F_z$ (N)', xlim=(plot_start,SimuTime[-1]))
        axl.tick_params(labelright=True, labelleft=True, left=True, right=True)
        axl.legend(handles, labels, loc = 'lower center', ncol=3+(n_args-2)%3, fontsize='small')
        figl.suptitle(f'{object} $F_z$ for different {comparisontype} resolutions - H3 IPE amont $\Theta=-5^{{\circ}}$ $V=50km.h^{{-1}}$')
        figl.tight_layout()
        figl.savefig(f'{comparisontype}_{object}_LIFT_COMP_PLOT.png')

        handles, labels = axd.get_legend_handles_labels()
        axd.grid(True, linewidth=0.5, linestyle='--', color='gray')
        if AdaptedAxes: axd.set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1]), ylim=(y_min_D,y_max_D))
        else: axd.set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1]))
        axd.tick_params(labelright=True, labelleft=True, left=True, right=True)
        axd.legend(handles, labels, loc = 'lower center', ncol=3+(n_args-2)%3, fontsize='small')
        figd.suptitle(f'{object} $F_x$ for different {comparisontype} resolutions - H3 IPE amont $\Theta=-5^{{\circ}}$ $V=50km.h^{{-1}}$')
        figd.tight_layout()
        figd.savefig(f'{comparisontype}_{object}_DRAG_COMP_PLOT.png')
    
    return()

def PlotForces(ListToPlot, plot_start=5, ListObjects='', Vitesse= 50, AdaptedAxes=True):
    '''Plot Lift and Drag isntantaneous and mean values for given simulations (ListToPlot), and different objects (ListObjects), starting cumulated avg at plot_start'''
    colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    linestl   = ['dotted','solid','dashed']
    color_it  = 0
    if AdaptedAxes:
        y_min_D, y_max_D = AxLimits4AllForces(ListToPlot, plot_start, ListObjects, Function='Drag')
        y_min_L, y_max_L = AxLimits4AllForces(ListToPlot, plot_start, ListObjects, Function='Lift')
    # loop on simulations
    for data in ListToPlot:
        # loop on objects (ipe, table, poutre, ...)
        for object in ListObjects:
            # create plot
            fig,ax  = plt.subplots(1,2,figsize=(12,6))

            # get data
            Lift          = retrieve_lift(f'simu_{data}/resultats/capteurs/', suffix=object) # setups+'/Resultats/'
            Drag          = retrieve_drag(f'simu_{data}/resultats/capteurs/', suffix=object)
            SimuTime      = retrieve_time(f'simu_{data}/resultats/capteurs/', suffix=object)  # setups+'/Resultats/'
            DT            = SimuTime[0]
            incr_start    = int(plot_start/DT)
            MeanLift      = []
            MeanDrag      = []
            for t in SimuTime[incr_start:]: # plot_start is when to start plotting and computing cumul avg (in s)
                MeanLift.append(compute_mean(Lift, window=[plot_start,t], dt=DT))
                MeanDrag.append(compute_mean(Drag, window=[plot_start,t], dt=DT))
            MeanLift = np.array(MeanLift)
            MeanDrag = np.array(MeanDrag)
            
            labelname  = f"{data.split('_')[0]} $\\theta={data.split('_')[1]}^\circ$ $V={Vitesse} km.h^{{-1}}$"
            objectname = rename_object(object)

            ax[1].plot(SimuTime[incr_start:], MeanLift, linestyle=linestl[1], color=colors[color_it+2], label=f'$\overline{{F_z}}$ {labelname}', linewidth=0.9)    
            ax[1].plot(SimuTime[incr_start:], Lift[incr_start:],  linestyle=linestl[1], color=colors[color_it], label=f'$F_z$ {labelname}', linewidth=0.5, alpha=0.7) 

            ax[0].plot(SimuTime[incr_start:], MeanDrag, linestyle=linestl[1], color=colors[color_it+2], label=f'$\overline{{F_x}}$ {labelname}', linewidth=0.9)    
            ax[0].plot(SimuTime[incr_start:], Drag[incr_start:], linestyle=linestl[1], color=colors[color_it], label=f'$F_x$ {labelname}', linewidth=0.5, alpha=0.7) 


            ax[0].set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1])) 
            if AdaptedAxes: ax[0].set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1]), ylim=(y_min_D,y_max_D))
            else: ax[0].set(xlabel='Time (s)', ylabel='$F_x$ (N)', xlim=(plot_start,SimuTime[-1]))
            ax[0].tick_params(labelright=True, labelleft=True, left=True, right=True)
            ax[0].legend(loc = 'lower center', fontsize='small')

            if AdaptedAxes: ax[1].set(xlabel='Time (s)', ylabel='$F_z$ (N)', xlim=(plot_start,SimuTime[-1]), ylim=(y_min_L,y_max_L))
            else: ax[1].set(xlabel='Time (s)', ylabel='$F_z$ (N)', xlim=(plot_start,SimuTime[-1]))
            ax[1].tick_params(labelright=True, labelleft=True, left=True, right=True)
            ax[1].legend(loc = 'lower center', fontsize='small')

            fig.suptitle(f'{objectname} Drag Lift for {labelname}')
            fig.tight_layout()
            fig.savefig(f'{data}_{objectname}_FORCES.png')
            plt.close()

    return()

### Data Evaluation
def PrintEvaluation(ListToCompare, OutputCSV='output.csv', plot_start=5, comparisontype='mesh', ListObjects=['']):
    '''Print Lift and Drag mean, std, max, min values for given simulations (ListToPlot), and different objects (ListObjects), starting avg calculation at plot_start'''
    # generate csv file
    with open(OutputCSV, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([comparisontype, 'incidence', 'object', 'function', 'value'])
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
                MaxLift       = compute_max(Lift, window=[plot_start,SimuTime[-1]], dt=DT)
                MinLift       = compute_min(Lift, window=[plot_start,SimuTime[-1]], dt=DT)
                MaxDrag       = compute_max(Drag, window=[plot_start,SimuTime[-1]], dt=DT)
                MinDrag       = compute_min(Drag, window=[plot_start,SimuTime[-1]], dt=DT)
                STDLift       = compute_std(Lift, window=[plot_start,SimuTime[-1]], dt=DT)
                STDDrag       = compute_std(Drag, window=[plot_start,SimuTime[-1]], dt=DT)
                # names
                if comparisontype=='mesh': labelname, angle = data,''
                if comparisontype=='dt':   labelname, angle = f'dt{DT}',''
                if comparisontype=='simu': labelname, angle = data.split('_')[0], data.split('_')[1]
                # write in csv
                csv_writer.writerow([labelname, angle, object, 'Mean Lift', MeanLift])
                csv_writer.writerow([labelname, angle, object, 'Mean Drag', MeanDrag])
                csv_writer.writerow([labelname, angle, object, 'Max Lift',  MaxLift])
                csv_writer.writerow([labelname, angle, object, 'Min Lift',  MinLift])
                csv_writer.writerow([labelname, angle, object, 'Max Drag',  MaxDrag])
                csv_writer.writerow([labelname, angle, object, 'Min Drag',  MinDrag])
                csv_writer.writerow([labelname, angle, object, 'STD Lift',  STDLift])
                csv_writer.writerow([labelname, angle, object, 'STD Drag',  STDDrag])
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
# PrintEvaluation(LIST_FOR_COMPARISON, OUTPUT_CSV, PLOT_START, comparisontype='simu', ListObjects=LIST_OF_OBJECTS)
# PlotForces(LIST_FOR_COMPARISON, plot_start=PLOT_START, ListObjects=LIST_OF_OBJECTS, Vitesse= VITESSE_SIMU)
# PlotForces(['IPEAMONT_-30'], plot_start=PLOT_START, ListObjects=['IPE','Table0','Table4'], Vitesse= 50)
# for tilt in ['-75','-60','-30','-5','5','30','60','75']:
#     PlotForces([f'IPEAMONT_{tilt}',f'IPEAVAL_{tilt}'], plot_start=PLOT_START, ListObjects=LIST_OF_OBJECTS, Vitesse=VITESSE_SIMU, AdaptedAxes=ADAPTED_AXES)
# for angle in ['-5_V105']:
#     PlotForces([f'IPEAMONT_{angle}',f'IPEAVAL_{angle}'], plot_start=8, ListObjects=LIST_OF_OBJECTS, Vitesse=105, AdaptedAxes=ADAPTED_AXES)

# reformat_TSE_csv('EFFORTS_VALUES_DAMIEN_TSE', 'EFFORTS_VALUES_TSE_REFORMATTED')
inverse_reformat_TSE_csv('compare_efforts','EFFORTS_VALUES_CIMLIB_REFORMATTED')

