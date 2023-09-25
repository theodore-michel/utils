import numpy as np
import matplotlib.pyplot as plt
import os, sys

### INPUTS
if len(sys.argv) != 6:
    print("Usage: python script.py path2abl path2dirty start end dt")
    sys.exit(1)
PATH_TO_EFFORTS     = str(sys.argv[1])
PATH_TO_EFFORTS_BIS = str(sys.argv[2])
WINDOW              = [ float(sys.argv[3]) , float(sys.argv[4]) ]
DT                  = float(sys.argv[5])
NUM_OF_PANELS       = 6
AVG_WINDOW          = [ 100 , float(sys.argv[4]) ]

if NUM_OF_PANELS==6 :   # CFL
    ### PREPROCESS
    def retrieve_lifts(path):
        L = [ [], [], [], [], [], [] ]
        for i in range (6):
            with open(os.getcwd() + '/' + path + 'Efforts' + str(i) + '.txt', 'r') as f:
                next(f) # Skip header
                for line in f:
                    L[i].append(float(line.split()[3])) # select Lift column value
        L = np.array(L)
        return(L)
    
    def retrieve_torques(path):
        Tq = [ [], [], [], [], [], [] ]
        for i in range (6):
            with open(os.getcwd() + '/' + path + 'Torque' + str(i) + '.txt', 'r') as f:
                next(f) # Skip header
                for line in f:
                    Tq[i].append(float(line.split()[2])) # select Lift column value
        Tq = np.array(Tq)
        return(Tq)

    def retrieve_time(path):
        T = [ ]
        with open(os.getcwd() + '/' + path + 'Efforts0.txt', 'r') as f:
            next(f) # Skip header
            for line in f:
                T.append(float(line.split()[1])) # select time column value
        # T = np.array(T)
        return(T)

    ### FUNCTION
    def compute_mlift(L, window=[50,100], dt=0.1):
        # L is an array of shape (6,timesteps)
        LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
        Avg      = np.mean( LCropped , axis=0 )
        return(Avg)
    
    def compute_avglift(L, window=[50,100], dt=0.1):
        # L is an array of shape (6,timesteps)
        LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
        Avg      = np.mean( LCropped , axis=1 )
        return(Avg)
    
    def compute_mtorque(Tq, window=[50,100], dt=0.1, start_t=100):
        # L is an array of shape (8,timesteps)
        TqCropped = Tq[ : , int((window[0]-start_t)//dt) : int((window[1]-start_t)//dt) ]
        Avg      = np.mean( TqCropped , axis=0 )
        return(Avg)

    ### DATA
    start_time_plot = 45
    # Initial path
    Lifts           = retrieve_lifts(PATH_TO_EFFORTS)
    Mean            = compute_mlift(Lifts, WINDOW, DT)
    AvgLift         = compute_avglift(Lifts, AVG_WINDOW, DT)
    SimuTime        = retrieve_time(PATH_TO_EFFORTS)

    window_start    = SimuTime.index(float(WINDOW[0]))
    window_end      = SimuTime.index(float(WINDOW[1]))
    start           = SimuTime.index(float(start_time_plot))
    end             = min(window_end, len(SimuTime))

    Time            = SimuTime[window_start : window_end] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtended    = SimuTime[start:end] # np.arange(1, WINDOW[1], DT)
    Flat_Lifts      = [item for sublist in Lifts for item in sublist[start:]]
    Lift_limits     = (min(Flat_Lifts), max(Flat_Lifts))

    # Bis path
    LiftsBis        = retrieve_lifts(PATH_TO_EFFORTS_BIS)
    MeanBis         = compute_mlift(LiftsBis, WINDOW, DT)
    AvgLiftBis      = compute_avglift(LiftsBis, AVG_WINDOW, DT)
    SimuTimeBis     = retrieve_time(PATH_TO_EFFORTS_BIS)

    window_startBis = SimuTimeBis.index(float(WINDOW[0]))
    window_endBis   = SimuTimeBis.index(float(WINDOW[1]))
    startBis        = SimuTimeBis.index(float(start_time_plot))
    endBis          = min(window_endBis, len(SimuTimeBis))

    TimeBis         = SimuTimeBis[window_startBis : window_endBis] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtendedBis = SimuTimeBis[startBis:endBis] # np.arange(1, WINDOW[1], DT)
    Flat_LiftsBis   = [item for sublist in LiftsBis for item in sublist[startBis:]]
    Lift_limitsBis  = ( min(min(Flat_LiftsBis),Lift_limits[0]), max(max(Flat_LiftsBis),Lift_limits[1]) )

    ### SUBPLOTS
    fig, axs = plt.subplots(3,2, figsize=(10,10))
    # Table 0
    axs[0, 0].plot(TimeExtended,     Lifts[0][start:end],          color = 'darkblue',  linewidth=0.8, label="$C_z$ inst. ABL")
    axs[0, 0].axhline(AvgLift[0],    color = 'blue',               linestyle = '--',    linewidth=1.0, label="$C_z$ avg. ABL")
    axs[0, 0].plot(TimeExtendedBis,  LiftsBis[0][startBis:endBis], color = 'darkred',   linewidth=0.8, label="$C_z$ inst. Dirty")
    axs[0, 0].axhline(AvgLiftBis[0], color = 'red',                linestyle = '--',    linewidth=1.0, label="$C_z$ avg. Dirty")
    axs[0, 0].set_title('Table 0')
    # Table 1
    axs[0, 1].plot(TimeExtended,     Lifts[1][start:end],          color = 'darkblue',  linewidth=0.8)
    axs[0, 1].axhline(AvgLift[1],    color = 'blue',               linestyle = '--',    linewidth=1.0)
    axs[0, 1].plot(TimeExtendedBis,  LiftsBis[1][startBis:endBis], color = 'darkred',   linewidth=0.8)
    axs[0, 1].axhline(AvgLiftBis[1], color = 'red',                linestyle = '--',    linewidth=1.0)
    axs[0, 1].set_title('Table 1')
    # Table 2
    axs[1, 0].plot(TimeExtended,     Lifts[2][start:end],          color = 'darkblue',  linewidth=0.8)
    axs[1, 0].axhline(AvgLift[2],    color = 'blue',               linestyle = '--',    linewidth=1.0)
    axs[1, 0].plot(TimeExtendedBis,  LiftsBis[2][startBis:endBis], color = 'darkred',   linewidth=0.8)
    axs[1, 0].axhline(AvgLiftBis[2], color = 'red',                linestyle = '--',    linewidth=1.0)
    axs[1, 0].set_title('Table 2')
    # Table 3
    axs[1, 1].plot(TimeExtended,     Lifts[3][start:end],          color = 'darkblue',  linewidth=0.8)
    axs[1, 1].axhline(AvgLift[3],    color = 'blue',               linestyle = '--',    linewidth=1.0)
    axs[1, 1].plot(TimeExtendedBis,  LiftsBis[3][startBis:endBis], color = 'darkred',   linewidth=0.8)
    axs[1, 1].axhline(AvgLiftBis[3], color = 'red',                linestyle = '--',    linewidth=1.0)
    axs[1, 1].set_title('Table 3')
    # Table 4
    axs[2, 0].plot(TimeExtended,     Lifts[4][start:end],          color = 'darkblue',  linewidth=0.8)
    axs[2, 0].axhline(AvgLift[4],    color = 'blue',               linestyle = '--',    linewidth=1.0)
    axs[2, 0].plot(TimeExtendedBis,  LiftsBis[4][startBis:endBis], color = 'darkred',   linewidth=0.8)
    axs[2, 0].axhline(AvgLiftBis[4], color = 'red',                linestyle = '--',    linewidth=1.0)
    axs[2, 0].set_title('Table 4')
    # Table 5
    axs[2, 1].plot(TimeExtended,     Lifts[5][start:end],          color = 'darkblue',  linewidth=0.8)
    axs[2, 1].axhline(AvgLift[5],    color = 'blue',               linestyle = '--',    linewidth=1.0)
    axs[2, 1].plot(TimeExtendedBis,  LiftsBis[5][startBis:endBis], color = 'darkred',   linewidth=0.8)
    axs[2, 1].axhline(AvgLiftBis[5], color = 'red',                linestyle = '--',    linewidth=1.0)
    axs[2, 1].set_title('Table 5')
    # Legends
    for ax in axs.flat:
        ax.grid(True, linewidth=0.3, linestyle='--', color='gray') # False
        ax.set(xlabel='time (s)', ylabel='$C_z$', ylim=Lift_limits)
        ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
    handles, labels = axs[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc = 'lower center', ncol=2)
    fig.suptitle(f'Dirty Inlet $C_z$ Comparison Plot')
    fig.tight_layout()
    plt.savefig('COMPARISON_EFFORTS_PLOT.png')
    plt.show()