from pickle import LIST
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from plot_styles import scientific_style 
import csv
import pandas as pd
import re

### INPUTS
n_args = len(sys.argv)
if n_args <4:
    print("Usage: python script.py data vitesse simutype... ")
    sys.exit(1)

DATA_FILE        = sys.argv[1]
VITESSE_SIMU     = int(sys.argv[2])
SIMU_TYPE        = sys.argv[3]    # IPEAMONT or IPEAVAL

LIST_OF_OBJECTS  = ['IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5']
               # = ['All','IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5']
               # = ['All', 'IPE', 'Table0', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5', 'Poutre0', 'Poutre1', 'Poutre2', 'Poutre3', 'Poutre4', 'Poutre5']
LIST_OBJECTS_EXT = ['IPE am', 'Table1', 'Table2', 'Table3', 'Table4', 'Table5', 'Table6', 'IPE av']
LIST_OF_ANGLES   = [-75, -60, -30, -5, 5, 30, 60, 75] # [-5]


### PREPROCESS
DATA_PLOT           = pd.read_csv(DATA_FILE, sep=',')
DATA_PLOT_50        = pd.read_csv('compare_efforts_V50_FULLTABLE.csv', sep=',')
DATA_PLOT_105       = pd.read_csv('compare_efforts_V105_FULLTABLE.csv', sep=',')
TSE_DATA_PLOT_50    = pd.read_csv('EFFORTS_VALUES_TSE_REFORMATTED_50.csv', sep=',')
TSE_DATA_PLOT_105   = pd.read_csv('EFFORTS_VALUES_TSE_REFORMATTED_105.csv', sep=',')
EUROCODE_DATA_PLOT  = pd.read_csv('eurocode_values.csv', sep=',')

SREF_FACTOR         = 1    # 2 if data from half-tables, 1 if data from full-tables

def AxLimits4All(DATA_PLOT, ListObjects=['All'], Incidences=[-5], SimuType='IPEAMONT', Function = 'Drag'):
    '''Read through DATA_PLOT data filtered by ListObjects, Incidences, SimuType, Function (Drag or Lift according to subplot) 
    and determine a common (y_min,y_max) for all plots that will use these data.'''
    SimuType = SimuType if isinstance(SimuType, list) else [SimuType] # make sure SimuType is list because pandas .isin() takes only lists as arg
    margin   = 1.05
    sub_data = DATA_PLOT[DATA_PLOT['simu'].isin(SimuType) & DATA_PLOT['incidence'].isin(Incidences) & DATA_PLOT['object'].isin(ListObjects)]
    min_data = sub_data[sub_data['function'] == f'Min {Function}']['value'].values * SREF_FACTOR
    max_data = sub_data[sub_data['function'] == f'Max {Function}']['value'].values * SREF_FACTOR
    y_min    = round(np.min(min_data) * margin, 2)
    y_max    = round(np.max(max_data) * margin, 2)
    return (y_min,y_max)

def rename_simutype(simutype):
    '''Rename IPEAMONT to am., IPEAVAL to av.'''
    if simutype == 'IPEAMONT':
        return 'am.'
    if simutype == 'IPEAVAL':
        return 'av.'
    return simutype

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


### PLOTS
def Plot_Effort_vs_Angles_by_Object(DATA_PLOT, ListObjects='All', Incidences=[-5], SimuType='IPEAMONT'):
    '''Plot effort vs incidence angle for each object in ListObjects, for each SimuType in SimuType, for each incidence angle in Incidences'''
    colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    linestl   = ['dotted','solid','dashed']
    y_min_drag,y_max_drag = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift,y_max_lift = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    # loop on objects
    for object in ListObjects:
        objectname = rename_object(object)
        color_it   = 0
        fig,ax     = plt.subplots(1,2,figsize=(12,6))
        x_incidences = []
        MeanLift     = []
        MaxLift      = []
        MinLift      = []
        MeanDrag     = []
        MaxDrag      = []
        MinDrag      = []
        # loop on incidence angles
        for angle in Incidences:
            # get data
            sub_data = DATA_PLOT[(DATA_PLOT['simu'] == SimuType) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]

            MeanLift.append(sub_data[sub_data['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLift.append(sub_data[sub_data['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLift.append(sub_data[sub_data['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)

            MeanDrag.append(sub_data[sub_data['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDrag.append(sub_data[sub_data['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDrag.append(sub_data[sub_data['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            x_incidences.append(int(angle))
        # plot
        ax[0].scatter(x_incidences, MeanDrag, color=colors[color_it],   label=f'$\overline{{F_x}}$')
        ax[0].plot(x_incidences,    MeanDrag, linestyle=linestl[0],     color=colors[color_it], linewidth=1.3)
        ax[0].scatter(x_incidences, MaxDrag,  color=colors[color_it+1], label=f'$\max{{F_x}}$')
        ax[0].plot(x_incidences,    MaxDrag,  linestyle=linestl[0],     color=colors[color_it+1], linewidth=1.3) 

        ax[1].scatter(x_incidences, MeanLift, color=colors[color_it],   label=f'$\overline{{F_z}}$')
        ax[1].plot(x_incidences,    MeanLift, linestyle=linestl[0],     color=colors[color_it], linewidth=1.3)
        ax[1].scatter(x_incidences, MaxLift,  color=colors[color_it+1], label=f'$\max{{F_z}}$')
        ax[1].plot(x_incidences,    MaxLift,  linestyle=linestl[0],     color=colors[color_it+1], linewidth=1.3)
        ax[1].scatter(x_incidences, MinLift,  color=colors[color_it+2], label=f'$\min{{F_z}}$')
        ax[1].plot(x_incidences,    MinLift,  linestyle=linestl[0],     color=colors[color_it+2], linewidth=1.3) 

        # handles, labels = ax.get_legend_handles_labels()
        # ax.grid(True, linewidth=0.5, linestyle='--', color='gray')
        ax[0].set(xlabel='Incidence ($^\circ$)', ylabel='$F_x$ (N)')
        ax[0].set_ylim(y_min_drag,y_max_drag)  # same for all Drag subplots
        ax[0].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[0].set_xticks(Incidences)
        ax[0].set_xticklabels([f'{val}' for val in Incidences])
        ax[0].legend(loc = 'lower right', fontsize='small')
        ax[1].set(xlabel='Incidence ($^\circ$)', ylabel='$F_z$ (N)')
        ax[1].set_ylim(y_min_lift,y_max_lift)  # same for all Lift subplots
        ax[1].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[1].set_xticks(Incidences)
        ax[1].set_xticklabels([f'{val}' for val in Incidences])
        ax[1].legend(loc = 'lower right', fontsize='small')
        fig.suptitle(f'{SimuType} -- {objectname} $F_x$ and $F_z$ vs incidence angle at $V={VITESSE_SIMU}km.h^{{-1}}$')
        fig.tight_layout()
        fig.savefig(f'{SimuType}_{objectname}_polaire_V{VITESSE_SIMU}.png')
    plt.close()

    return()

def Plot_Effort_vs_Objects_by_Angle(DATA_PLOT, ListObjects='IPE', Incidences=[-5], SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean'):
    '''Plot effort vs object for each incidence angle in Incidences, for each SimuType in SimuType, for each object in ListObjects'''
    colors    = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    linestl   = ['dotted','solid','dashed']
    markers   = ['o','s']
    y_min_drag,y_max_drag = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift,y_max_lift = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    # loop on incidence angles
    for angle in Incidences:
        color_it  = 0
        fig,ax  = plt.subplots(1,2,figsize=(12,6))
        # loop on objects
        MeanLiftAMONT     = []
        MaxLiftAMONT      = []
        MinLiftAMONT      = []
        MeanDragAMONT     = []
        MaxDragAMONT      = []
        MinDragAMONT      = []
        MeanLiftAVAL      = []
        MaxLiftAVAL       = []
        MinLiftAVAL       = []
        MeanDragAVAL      = []
        MaxDragAVAL       = []
        MinDragAVAL       = []
        for object in ListObjects:
            # get data
            sub_data_AM = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[0]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]
            sub_data_AV = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[1]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]

            MeanLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)

            MeanDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            MeanLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)

            MeanDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            # x_objects.append(object)

        # adapt objs for visu
        MeLAv_ipeAv = MeanLiftAVAL.pop(0)
        MeanLiftAVAL.append(MeLAv_ipeAv)
        MxLAv_ipeAv = MaxLiftAVAL.pop(0)
        MaxLiftAVAL.append(MxLAv_ipeAv)
        MiLAv_ipeAv = MinLiftAVAL.pop(0)
        MinLiftAVAL.append(MiLAv_ipeAv)
        MeDAv_ipeAv = MeanDragAVAL.pop(0)
        MeanDragAVAL.append(MeDAv_ipeAv)
        MxDAv_ipeAv = MaxDragAVAL.pop(0)
        MaxDragAVAL.append(MxDAv_ipeAv)
        MiDAv_ipeAv = MinDragAVAL.pop(0)
        MinDragAVAL.append(MiDAv_ipeAv)

        # plot
        if MaxOrMean=='Mean':
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MeanDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_x}}$ {SimuType[0]}')
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MeanDragAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_x}}$ {SimuType[1]}') 

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MeanLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_z}}$ {SimuType[0]}')
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MeanLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_z}}$ {SimuType[1]}')

        if MaxOrMean=='Max':
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_x)$ {SimuType[0]}')
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_x)$ {SimuType[1]}') 

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MaxLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_z)$ {SimuType[0]}')
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MaxLiftAMONT[:2], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MaxLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_z)$ {SimuType[1]}') 
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MaxLiftAVAL[-2:], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MinLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAMONT[1:], linestyle=linestl[2], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\min(F_z)$ {SimuType[0]}')
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MinLiftAMONT[:2], linestyle=linestl[2], color=colors[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MinLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAVAL[:-1], linestyle=linestl[2], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\min(F_z)$ {SimuType[1]}') 
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MinLiftAVAL[-2:], linestyle=linestl[2], color=colors[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAMONT[1:], MaxLiftAMONT[1:], color=colors[color_it],   alpha=0.1)
            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAVAL[:-1], MaxLiftAVAL[:-1], color=colors[color_it+1], alpha=0.1)

        ax[0].set(xlabel='Objects', ylabel='$F_x$ (N)')
        ax[0].set_ylim(y_min_drag, y_max_drag)
        ax[0].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[0].tick_params(axis='x',which='minor',bottom=False)
        ax[0].set_xticks(LIST_OBJECTS_EXT)
        ax[0].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
        ax[0].legend(loc = 'upper right', fontsize='small')

        ax[1].set(xlabel='Objects', ylabel='$F_z$ (N)')
        ax[1].set_ylim(y_min_lift, y_max_lift)
        ax[1].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[1].tick_params(axis='x', which='minor', bottom=False, top=False)
        ax[1].set_xticks(LIST_OBJECTS_EXT)
        ax[1].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
        if MaxOrMean=='Mean': ax[1].legend(loc = 'upper right', fontsize='small')
        if MaxOrMean=='Max':  ax[1].legend(loc = 'upper right', fontsize='small', ncol=2)

        fig.suptitle(f'Incidence {angle}$^\circ$ -- $F_x$ and $F_z$ vs Objects at $V={VITESSE_SIMU}km.h^{{-1}}$')
        fig.tight_layout()
        fig.savefig(f'Incidence{angle}_objects_V{VITESSE_SIMU}_{MaxOrMean}.png')
    plt.close()

    return()

def Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT, TSE_DATA_PLOT, ListObjects=['IPE','Table1'], SimuType=['IPEAMONT','IPEAVAL'], IncidenceType= 'appui', MaxOrMean = 'Mean'):
    '''Plot effort vs object for each incidence angle in Incidences, for each SimuType in SimuType, for each object in ListObjects, according to IncidenceType (appui or soulèvement)'''
    colors    = ['darkblue', 'saddlebrown', 'darkorange', 'darkgreen']
    linestl   = ['dotted','solid','dashed']
    markers   = ['o','s']

    figAV,axAV  = plt.subplots(1,2,figsize=(12,6))
    figAM,axAM  = plt.subplots(1,2,figsize=(12,6))

    if IncidenceType == 'appui': Incidences = [-75, -60, -30, -5] 
    else: Incidences = [75, 60, 30, 5]
    color_it  = 0

    y_min_drag_CIMLIB,y_max_drag_CIMLIB = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift_CIMLIB,y_max_lift_CIMLIB = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    y_min_drag_TSE,y_max_drag_TSE       = AxLimits4All(TSE_DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift_TSE,y_max_lift_TSE       = AxLimits4All(TSE_DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    y_min_drag,y_max_drag               = min(y_min_drag_CIMLIB,y_min_drag_TSE), max(y_max_drag_CIMLIB,y_max_drag_TSE)
    y_min_lift,y_max_lift               = min(y_min_lift_CIMLIB,y_min_lift_TSE), max(y_max_lift_CIMLIB,y_max_lift_TSE)

    # loop on incidence angles
    for angle in Incidences:
        # loop on objects
        MeanLiftAMONT     = []
        MaxLiftAMONT      = []
        MinLiftAMONT      = []
        MeanDragAMONT     = []
        MaxDragAMONT      = []
        MinDragAMONT      = []
        MeanLiftAVAL      = []
        MaxLiftAVAL       = []
        MinLiftAVAL       = []
        MeanDragAVAL      = []
        MaxDragAVAL       = []
        MinDragAVAL       = []
        TSEMeanLiftAMONT  = []
        TSEMaxLiftAMONT   = []
        TSEMinLiftAMONT   = []
        TSEMeanDragAMONT  = []
        TSEMaxDragAMONT   = []
        TSEMinDragAMONT   = []
        TSEMeanLiftAVAL   = []
        TSEMaxLiftAVAL    = []
        TSEMinLiftAVAL    = []
        TSEMeanDragAVAL   = []
        TSEMaxDragAVAL    = []
        TSEMinDragAVAL    = []
        for object in ListObjects:
            # get data
            sub_data_AM = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[0]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]
            MeanLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)
            MeanDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            sub_data_AV = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[1]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]
            MeanLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)
            MeanDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            tse_data_AM = TSE_DATA_PLOT[(TSE_DATA_PLOT['simu'] == SimuType[0]) & (TSE_DATA_PLOT['incidence'] == angle) & (TSE_DATA_PLOT['object'] == object)]
            TSEMeanLiftAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Mean Lift']['value'].values[0])
            TSEMaxLiftAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Max Lift']['value'].values[0])
            TSEMinLiftAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Min Lift']['value'].values[0])
            TSEMeanDragAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Mean Drag']['value'].values[0])
            TSEMaxDragAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Max Drag']['value'].values[0])
            TSEMinDragAMONT.append(tse_data_AM[tse_data_AM['function'] == 'Min Drag']['value'].values[0])

            tse_data_AV = TSE_DATA_PLOT[(TSE_DATA_PLOT['simu'] == SimuType[1]) & (TSE_DATA_PLOT['incidence'] == angle) & (TSE_DATA_PLOT['object'] == object)]
            TSEMeanLiftAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Mean Lift']['value'].values[0])
            TSEMaxLiftAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Max Lift']['value'].values[0])
            TSEMinLiftAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Min Lift']['value'].values[0])
            TSEMeanDragAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Mean Drag']['value'].values[0])
            TSEMaxDragAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Max Drag']['value'].values[0])
            TSEMinDragAVAL.append(tse_data_AV[tse_data_AV['function'] == 'Min Drag']['value'].values[0])

        # adapt objs for visu
        MeLAv_ipeAv = MeanLiftAVAL.pop(0)
        MeanLiftAVAL.append(MeLAv_ipeAv)
        MxLAv_ipeAv = MaxLiftAVAL.pop(0)
        MaxLiftAVAL.append(MxLAv_ipeAv)
        MiLAv_ipeAv = MinLiftAVAL.pop(0)
        MinLiftAVAL.append(MiLAv_ipeAv)
        MeDAv_ipeAv = MeanDragAVAL.pop(0)
        MeanDragAVAL.append(MeDAv_ipeAv)
        MxDAv_ipeAv = MaxDragAVAL.pop(0)
        MaxDragAVAL.append(MxDAv_ipeAv)
        MiDAv_ipeAv = MinDragAVAL.pop(0)
        MinDragAVAL.append(MiDAv_ipeAv)

        TSEMeLAv_ipeAv = TSEMeanLiftAVAL.pop(0)
        TSEMeanLiftAVAL.append(TSEMeLAv_ipeAv)
        TSEMxLAv_ipeAv = TSEMaxLiftAVAL.pop(0)
        TSEMaxLiftAVAL.append(TSEMxLAv_ipeAv)
        TSEMiLAv_ipeAv = TSEMinLiftAVAL.pop(0)
        TSEMinLiftAVAL.append(TSEMiLAv_ipeAv)
        TSEMeDAv_ipeAv = TSEMeanDragAVAL.pop(0)
        TSEMeanDragAVAL.append(TSEMeDAv_ipeAv)
        TSEMxDAv_ipeAv = TSEMaxDragAVAL.pop(0)
        TSEMaxDragAVAL.append(TSEMxDAv_ipeAv)
        TSEMiDAv_ipeAv = TSEMinDragAVAL.pop(0)
        TSEMinDragAVAL.append(TSEMiDAv_ipeAv)

        # plot
        if MaxOrMean == 'Mean':
            # CIMLIB amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   MeanDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (CimLib)")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   MeanLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (Cimlib)")
            # TSE amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   TSEMeanDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMeanDragAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (TSE)")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   TSEMeanLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMeanLiftAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (TSE)")

            # CIMLIB aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (CimLib)") 
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  MeanDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (CimLib)") 
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  MeanLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])
            # TSE aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMeanDragAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (TSE)") 
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  TSEMeanDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMeanLiftAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (TSE)") 
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  TSEMeanLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])

        if MaxOrMean == 'Max' and IncidenceType == 'appui':
            # CIMLIB amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   MaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max)")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   MinLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (min)")
            # TSE amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   TSEMaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxDragAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max) TSE")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   TSEMinLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMinLiftAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (min) TSE")

            # CIMLIB aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max)") 
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  MaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (min)") 
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  MinLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])
            # TSE aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxDragAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max) TSE")
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  TSEMaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMinLiftAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (min) TSE")
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  TSEMinLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])

        if MaxOrMean == 'Max' and IncidenceType == 'soulevement':
            # CIMLIB amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   MaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max)")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   MaxLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max)")
            # TSE amont
            axAM[0].scatter(LIST_OBJECTS_EXT[0],   TSEMaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxDragAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max) TSE")
            axAM[1].scatter(LIST_OBJECTS_EXT[0],   TSEMaxLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            axAM[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxLiftAMONT[1:], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[0], label=f"$\\alpha={angle}^\circ$ (max) TSE")

            # CIMLIB aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max)") 
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  MaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max)") 
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  MaxLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])
            # TSE aval
            axAV[0].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[0].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxDragAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max) TSE")
            axAV[0].scatter(LIST_OBJECTS_EXT[-1],  TSEMaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it])
            axAV[1].scatter(LIST_OBJECTS_EXT[0],   None)
            axAV[1].plot(LIST_OBJECTS_EXT[1:-1],   TSEMaxLiftAVAL[:-1], linestyle=linestl[0], color=colors[color_it], linewidth=1.5, marker=markers[1], label=f"$\\alpha={angle}^\circ$ (max) TSE")
            axAV[1].scatter(LIST_OBJECTS_EXT[-1],  TSEMaxLiftAVAL[-1],  marker=markers[1],    color=colors[color_it])

        color_it += 1
        
    #save
    axAM[0].set(xlabel='Objects', ylabel='$\overline{F_x}$ (N)')
    axAM[0].set_ylim(y_min_drag, y_max_drag)
    axAM[0].tick_params(labelright=False, labelleft=True, left=True, right=True)
    axAM[0].tick_params(axis='x',which='minor',bottom=False,top=False)
    axAM[0].set_xticks(LIST_OBJECTS_EXT)
    axAM[0].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
    axAM[0].legend(loc = 'upper right', fontsize='small', ncol=2)
    axAM[1].set(xlabel='Objects', ylabel='$\overline{F_z}$ (N)')
    axAM[1].set_ylim(y_min_lift, y_max_lift)
    axAM[1].tick_params(labelright=False, labelleft=True, left=True, right=True)
    axAM[1].tick_params(axis='x', which='minor', bottom=False, top=False)
    axAM[1].set_xticks(LIST_OBJECTS_EXT)
    axAM[1].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
    axAM[1].legend(loc = 'upper right', fontsize='small', ncol=2)
    figAM.suptitle(f'Configuration {SimuType[0]} {IncidenceType} -- $\overline{{F_x}}$ and $\overline{{F_z}}$ vs Objects at $V={VITESSE_SIMU}km.h^{{-1}}$')
    figAM.tight_layout()
    figAM.savefig(f'{IncidenceType}_{SimuType[0]}_all_V{VITESSE_SIMU}_{MaxOrMean}_CIMLIBvsTSE.png')
    
    axAV[0].set(xlabel='Objects', ylabel='$\overline{F_x}$ (N)')
    axAV[0].set_ylim(y_min_drag, y_max_drag)
    axAV[0].tick_params(labelright=False, labelleft=True, left=True, right=True)
    axAV[0].tick_params(axis='x',which='minor',bottom=False, top=False)
    axAV[0].set_xticks(LIST_OBJECTS_EXT)
    axAV[0].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
    axAV[0].legend(loc = 'upper right', fontsize='small',ncol=2)
    axAV[1].set(xlabel='Objects', ylabel='$\overline{F_z}$ (N)')
    axAV[1].set_ylim(y_min_lift, y_max_lift)
    axAV[1].tick_params(labelright=False, labelleft=True, left=True, right=True)
    axAV[1].tick_params(axis='x', which='minor', bottom=False, top=False)
    axAV[1].set_xticks(LIST_OBJECTS_EXT)
    axAV[1].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
    axAV[1].legend(loc = 'upper right', fontsize='small', ncol=2)
    figAV.suptitle(f'Configuration {SimuType[1]} {IncidenceType} -- $\overline{{F_x}}$ and $\overline{{F_z}}$ vs Objects at $V={VITESSE_SIMU}km.h^{{-1}}$')
    figAV.tight_layout()
    figAV.savefig(f'{IncidenceType}_{SimuType[1]}_all_V{VITESSE_SIMU}_{MaxOrMean}_CIMLIBvsTSE.png')
    plt.close()

    return()

def Plot_Effort_vs_Objects_by_Angle_with_TSE_data(DATA_PLOT, TSE_DATA_PLOT, ListObjects=['IPE','Table1'], Incidences=[-5],SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean', VitesseSimu=50, CompEurocode=True):
    '''Plot effort vs object for each incidence angle in Incidences, for each SimuType in SimuType, for each object in ListObjects, with both CIMLIB and TSE data on same plot'''
    colors       = ['darkblue', 'darkgreen', 'darkred', 'darkorange', 'darkorchid','darksalmon','darkmagenta','darkcyan','darkgray','saddlebrown']
    colors_TSE   = ['blue', 'green', 'red', 'orange', 'orchid','salmon','magenta','cyan','gray','saddlebrown']
    linestl      = ['dotted','solid','dashed']
    markers      = ['o','s']
    SimuType_rnm = [rename_simutype(SimuType[0]),rename_simutype(SimuType[1])]
    EurocodeData = EUROCODE_DATA_PLOT[EUROCODE_DATA_PLOT['velocity'] == VitesseSimu]
    y_min_drag_CIMLIB,y_max_drag_CIMLIB = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift_CIMLIB,y_max_lift_CIMLIB = AxLimits4All(DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    y_min_drag_TSE,y_max_drag_TSE       = AxLimits4All(TSE_DATA_PLOT, ListObjects, Incidences, SimuType, 'Drag')
    y_min_lift_TSE,y_max_lift_TSE       = AxLimits4All(TSE_DATA_PLOT, ListObjects, Incidences, SimuType, 'Lift')
    y_min_drag,y_max_drag               = min(y_min_drag_CIMLIB,y_min_drag_TSE), max(y_max_drag_CIMLIB,y_max_drag_TSE)
    y_min_lift,y_max_lift               = min(y_min_lift_CIMLIB,y_min_lift_TSE), max(y_max_lift_CIMLIB,y_max_lift_TSE)
    # loop on incidence angles
    for angle in Incidences:
        color_it  = 0
        fig,ax  = plt.subplots(1,2,figsize=(12,6))
        # loop on objects
        MeanLiftAMONT     = []
        MaxLiftAMONT      = []
        MinLiftAMONT      = []
        MeanDragAMONT     = []
        MaxDragAMONT      = []
        MinDragAMONT      = []
        MeanLiftAVAL      = []
        MaxLiftAVAL       = []
        MinLiftAVAL       = []
        MeanDragAVAL      = []
        MaxDragAVAL       = []
        MinDragAVAL       = []
        MeanLiftAMONT_TSE = []
        MaxLiftAMONT_TSE  = []
        MinLiftAMONT_TSE  = []
        MeanDragAMONT_TSE = []
        MaxDragAMONT_TSE  = []
        MinDragAMONT_TSE  = []
        MeanLiftAVAL_TSE  = []
        MaxLiftAVAL_TSE   = []
        MinLiftAVAL_TSE   = []
        MeanDragAVAL_TSE  = []
        MaxDragAVAL_TSE   = []
        MinDragAVAL_TSE   = []

        for object in ListObjects:
            # get data CIMLIB
            sub_data_AM = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[0]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]
            sub_data_AV = DATA_PLOT[(DATA_PLOT['simu'] == SimuType[1]) & (DATA_PLOT['incidence'] == angle) & (DATA_PLOT['object'] == object)]
            MeanLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)
            MeanDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAMONT.append(sub_data_AM[sub_data_AM['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)
            MeanLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Lift']['value'].values[0]*SREF_FACTOR)
            MaxLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Lift']['value'].values[0]*SREF_FACTOR)
            MinLiftAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Lift']['value'].values[0]*SREF_FACTOR)
            MeanDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Mean Drag']['value'].values[0]*SREF_FACTOR)
            MaxDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Max Drag']['value'].values[0]*SREF_FACTOR)
            MinDragAVAL.append(sub_data_AV[sub_data_AV['function'] == 'Min Drag']['value'].values[0]*SREF_FACTOR)

            # get data TSE
            sub_data_AM_TSE = TSE_DATA_PLOT[(TSE_DATA_PLOT['simu'] == SimuType[0]) & (TSE_DATA_PLOT['incidence'] == angle) & (TSE_DATA_PLOT['object'] == object)]
            sub_data_AV_TSE = TSE_DATA_PLOT[(TSE_DATA_PLOT['simu'] == SimuType[1]) & (TSE_DATA_PLOT['incidence'] == angle) & (TSE_DATA_PLOT['object'] == object)]
            MeanLiftAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Mean Lift']['value'].values[0])
            MaxLiftAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Max Lift']['value'].values[0])
            MinLiftAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Min Lift']['value'].values[0])
            MeanDragAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Mean Drag']['value'].values[0])
            MaxDragAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Max Drag']['value'].values[0])
            MinDragAMONT_TSE.append(sub_data_AM_TSE[sub_data_AM_TSE['function'] == 'Min Drag']['value'].values[0])
            MeanLiftAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Mean Lift']['value'].values[0])
            MaxLiftAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Max Lift']['value'].values[0])
            MinLiftAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Min Lift']['value'].values[0])
            MeanDragAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Mean Drag']['value'].values[0])
            MaxDragAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Max Drag']['value'].values[0])
            MinDragAVAL_TSE.append(sub_data_AV_TSE[sub_data_AV_TSE['function'] == 'Min Drag']['value'].values[0])

            # x_objects.append(object)

        # adapt objs for visu CIMLIB
        MeLAv_ipeAv = MeanLiftAVAL.pop(0)
        MeanLiftAVAL.append(MeLAv_ipeAv)
        MxLAv_ipeAv = MaxLiftAVAL.pop(0)
        MaxLiftAVAL.append(MxLAv_ipeAv)
        MiLAv_ipeAv = MinLiftAVAL.pop(0)
        MinLiftAVAL.append(MiLAv_ipeAv)
        MeDAv_ipeAv = MeanDragAVAL.pop(0)
        MeanDragAVAL.append(MeDAv_ipeAv)
        MxDAv_ipeAv = MaxDragAVAL.pop(0)
        MaxDragAVAL.append(MxDAv_ipeAv)
        MiDAv_ipeAv = MinDragAVAL.pop(0)
        MinDragAVAL.append(MiDAv_ipeAv)
        # adapt objs for visu TSE
        MeLAv_ipeAv_TSE = MeanLiftAVAL_TSE.pop(0)
        MeanLiftAVAL_TSE.append(MeLAv_ipeAv_TSE)
        MxLAv_ipeAv_TSE = MaxLiftAVAL_TSE.pop(0)    
        MaxLiftAVAL_TSE.append(MxLAv_ipeAv_TSE)
        MiLAv_ipeAv_TSE = MinLiftAVAL_TSE.pop(0)
        MinLiftAVAL_TSE.append(MiLAv_ipeAv_TSE)
        MeDAv_ipeAv_TSE = MeanDragAVAL_TSE.pop(0)
        MeanDragAVAL_TSE.append(MeDAv_ipeAv_TSE)
        MxDAv_ipeAv_TSE = MaxDragAVAL_TSE.pop(0)
        MaxDragAVAL_TSE.append(MxDAv_ipeAv_TSE)
        MiDAv_ipeAv_TSE = MinDragAVAL_TSE.pop(0)
        MinDragAVAL_TSE.append(MiDAv_ipeAv_TSE)


        # plot
        if MaxOrMean=='Mean':
            # CIMLIB
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MeanDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_x}}$ {SimuType_rnm[0]} CimLib')
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MeanDragAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_x}}$ {SimuType_rnm[1]} CimLib') 

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MeanLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_z}}$ {SimuType_rnm[0]} CimLib')
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MeanLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_z}}$ {SimuType_rnm[1]} CimLib')
            
            # TSE
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MeanDragAMONT_TSE[0],  marker=markers[0],    color=colors_TSE[color_it],   alpha=0.75)
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAMONT_TSE[1:], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_x}}$ {SimuType_rnm[0]} TSE', alpha=0.75)
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MeanDragAVAL_TSE[-1],  marker=markers[1],    color=colors_TSE[color_it+1], alpha=0.75)
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MeanDragAVAL_TSE[:-1], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_x}}$ {SimuType_rnm[1]} TSE', alpha=0.75)

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MeanLiftAMONT_TSE[0],  marker=markers[0],    color=colors_TSE[color_it],   alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAMONT_TSE[1:], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], label=f'$\overline{{F_z}}$ {SimuType_rnm[0]} TSE', alpha=0.75)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MeanLiftAVAL_TSE[-1],  marker=markers[1],    color=colors_TSE[color_it+1], alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MeanLiftAVAL_TSE[:-1], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\overline{{F_z}}$ {SimuType_rnm[1]} TSE', alpha=0.75)

        if MaxOrMean=='Max':
            # CIMLIB
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MaxDragAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_x)$ {SimuType_rnm[0]} CimLib')
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MaxDragAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_x)$ {SimuType_rnm[1]} CimLib')

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MaxLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_z)$ {SimuType_rnm[0]} CimLib')
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MaxLiftAMONT[:2], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MaxLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_z)$ {SimuType_rnm[1]} CimLib')
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MaxLiftAVAL[-2:], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MinLiftAMONT[0],  marker=markers[0],    color=colors[color_it])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAMONT[1:], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], label=f'$\min(F_z)$ {SimuType_rnm[0]} CimLib')
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MinLiftAMONT[:2], linestyle=linestl[1], color=colors[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MinLiftAVAL[-1],  marker=markers[1],    color=colors[color_it+1])
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAVAL[:-1], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\min(F_z)$ {SimuType_rnm[1]} CimLib')
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MinLiftAVAL[-2:], linestyle=linestl[1], color=colors[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAMONT[1:], MaxLiftAMONT[1:], color=colors[color_it],   alpha=0.1)
            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAVAL[:-1], MaxLiftAVAL[:-1], color=colors[color_it+1], alpha=0.1)

            # TSE
            ax[0].scatter(LIST_OBJECTS_EXT[0],   MaxDragAMONT_TSE[0],  marker=markers[0],    color=colors_TSE[color_it],   alpha=0.75)
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAMONT_TSE[1:], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_x)$ {SimuType_rnm[0]} TSE', alpha=0.75)
            ax[0].scatter(LIST_OBJECTS_EXT[-1],  MaxDragAVAL_TSE[-1],  marker=markers[1],    color=colors_TSE[color_it+1], alpha=0.75)
            ax[0].plot(LIST_OBJECTS_EXT[1:-1],   MaxDragAVAL_TSE[:-1], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_x)$ {SimuType_rnm[1]} TSE', alpha=0.75)

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MaxLiftAMONT_TSE[0],  marker=markers[0],    color=colors_TSE[color_it],   alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAMONT_TSE[1:], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], label=f'$\max(F_z)$ {SimuType_rnm[0]} TSE', alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MaxLiftAMONT_TSE[:2], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MaxLiftAVAL_TSE[-1],  marker=markers[1],    color=colors_TSE[color_it+1], alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MaxLiftAVAL_TSE[:-1], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\max(F_z)$ {SimuType_rnm[1]} TSE', alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MaxLiftAVAL_TSE[-2:], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].scatter(LIST_OBJECTS_EXT[0],   MinLiftAMONT_TSE[0],  marker=markers[0],    color=colors_TSE[color_it],   alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAMONT_TSE[1:], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], label=f'$\min(F_z)$ {SimuType_rnm[0]} TSE', alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[:2],     MinLiftAMONT_TSE[:2], linestyle=linestl[0], color=colors_TSE[color_it],   linewidth=1.5, marker=markers[0], alpha=0.15)
            ax[1].scatter(LIST_OBJECTS_EXT[-1],  MinLiftAVAL_TSE[-1],  marker=markers[1],    color=colors_TSE[color_it+1], alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[1:-1],   MinLiftAVAL_TSE[:-1], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], label=f'$\min(F_z)$ {SimuType_rnm[1]} TSE', alpha=0.75)
            ax[1].plot(LIST_OBJECTS_EXT[-2:],    MinLiftAVAL_TSE[-2:], linestyle=linestl[0], color=colors_TSE[color_it+1], linewidth=1.5, marker=markers[1], alpha=0.15)

            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAMONT_TSE[1:], MaxLiftAMONT_TSE[1:], color=colors_TSE[color_it],   alpha=0.1)
            ax[1].fill_between(LIST_OBJECTS_EXT[1:-1], MinLiftAVAL_TSE[:-1], MaxLiftAVAL_TSE[:-1], color=colors_TSE[color_it+1], alpha=0.1)
        
        # Eurocode
        if CompEurocode & (angle in EurocodeData['incidence'].values) :
            ax[0].hlines(EurocodeData[(EurocodeData['incidence']==angle)&(EurocodeData['function']=='Drag')]['value'].values[0], xmin=LIST_OBJECTS_EXT[0], xmax=LIST_OBJECTS_EXT[-1], linestyle=linestl[2], color='black', linewidth=1.5, label=f'$F_x$ Eurocode')
            ax[1].hlines(EurocodeData[(EurocodeData['incidence']==angle)&(EurocodeData['function']=='Lift')]['value'].values[0], xmin=LIST_OBJECTS_EXT[0], xmax=LIST_OBJECTS_EXT[-1], linestyle=linestl[2], color='black', linewidth=1.5, label=f'$F_z$ Eurocode')

        # params plot
        ax[0].set(xlabel='Objects', ylabel='$F_x$ (N)')
        ax[0].set_ylim(y_min_drag, y_max_drag)
        ax[0].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[0].tick_params(axis='x',which='minor',bottom=False)
        ax[0].set_xticks(LIST_OBJECTS_EXT)
        ax[0].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
        ax[0].legend(loc = 'upper right', fontsize='x-small', ncol=2)

        ax[1].set(xlabel='Objects', ylabel='$F_z$ (N)')
        ax[1].set_ylim(y_min_lift, y_max_lift)
        ax[1].tick_params(labelright=False, labelleft=True, left=True, right=True)
        ax[1].tick_params(axis='x', which='minor', bottom=False, top=False)
        ax[1].set_xticks(LIST_OBJECTS_EXT)
        ax[1].set_xticklabels([f'{val}' for val in LIST_OBJECTS_EXT])
        if MaxOrMean=='Mean': ax[1].legend(loc = 'upper right', fontsize='x-small', ncol=2)
        if MaxOrMean=='Max':  ax[1].legend(loc = 'upper right', fontsize='x-small', ncol=2)

        fig.suptitle(f'Incidence {angle}$^\circ$ -- $F_x$ and $F_z$ vs Objects at $V={VitesseSimu}km.h^{{-1}}$ (CIMLIB vs TSE)')
        fig.tight_layout()
        fig.savefig(f'CIMLIB_vs_TSE_Incidence{angle}_objects_V{VitesseSimu}_{MaxOrMean}.png')
    plt.close()

    return()

### RUN
plt.style.use(scientific_style)

# ### V50 SIMULATIONS
# Plot_Effort_vs_Angles_by_Object(DATA_PLOT, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType='IPEAMONT')
# Plot_Effort_vs_Angles_by_Object(DATA_PLOT, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType='IPEAVAL')
# Plot_Effort_vs_Objects_by_Angle(DATA_PLOT, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean')
# Plot_Effort_vs_Objects_by_Angle(DATA_PLOT, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Max')
# Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='soulevement', MaxOrMean='Max')
# Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='appui', MaxOrMean='Max')
# Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='soulevement', MaxOrMean='Mean')
# Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='appui', MaxOrMean='Mean')

### V105 SIMULATIONS
# Plot_Effort_vs_Angles_by_Object(DATA_PLOT, LIST_OF_OBJECTS, Incidences=[-5], SimuType='IPEAMONT')
# Plot_Effort_vs_Angles_by_Object(DATA_PLOT, LIST_OF_OBJECTS, Incidences=[-5], SimuType='IPEAVAL')
# Plot_Effort_vs_Objects_by_Angle(DATA_PLOT, LIST_OF_OBJECTS, Incidences=[-5], SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean')
# Plot_Effort_vs_Objects_by_Angle(DATA_PLOT, LIST_OF_OBJECTS, Incidences=[-5], SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Max')

# ### V50 SIMULATIONS WITH TSE DATA
# Plot_Effort_vs_Objects_by_Angle_with_TSE_data(DATA_PLOT_50, TSE_DATA_PLOT_50, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean', VitesseSimu=50, CompEurocode=True)
# Plot_Effort_vs_Objects_by_Angle_with_TSE_data(DATA_PLOT_50, TSE_DATA_PLOT_50, LIST_OF_OBJECTS, LIST_OF_ANGLES, SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Max', VitesseSimu=50, CompEurocode=True)

### V105 SIMULATIONS WITH TSE DATA
# Plot_Effort_vs_Objects_by_Angle_with_TSE_data(DATA_PLOT_105, TSE_DATA_PLOT_105, LIST_OF_OBJECTS, Incidences=[-5], SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Mean', VitesseSimu=105, CompEurocode=True)
# Plot_Effort_vs_Objects_by_Angle_with_TSE_data(DATA_PLOT_105, TSE_DATA_PLOT_105, LIST_OF_OBJECTS, Incidences=[-5], SimuType=['IPEAMONT','IPEAVAL'], MaxOrMean='Max', VitesseSimu=105, CompEurocode=True)
Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT_50, TSE_DATA_PLOT_50, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='appui', MaxOrMean='Mean')
Plot_Effort_vs_Objects_by_IncidenceType(DATA_PLOT_50, TSE_DATA_PLOT_50, LIST_OF_OBJECTS, SimuType=['IPEAMONT','IPEAVAL'], IncidenceType='soulevement', MaxOrMean='Mean')
