import numpy as np
import matplotlib.pyplot as plt
import os, sys

### INPUTS
PATH_TO_EFFORTS = str(sys.argv[1])
WINDOW          = [ float(sys.argv[2]) , float(sys.argv[3]) ]
DT              = float(sys.argv[4])
NUM_OF_PANELS   = 8


if NUM_OF_PANELS==8 :   # TSE
    ### PREPROCESS
    def retrieve_lifts(path):
        L = [ [], [], [], [], [], [], [], []]
        for i in range (8):
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

    ### PLOTS
    start        = int(1/DT)
    Lifts        = retrieve_lifts(PATH_TO_EFFORTS)
    Mean         = compute_mlift(Lifts, WINDOW, DT)
    SimuTime     = retrieve_time(PATH_TO_EFFORTS)
    Time         = SimuTime[int(WINDOW[0]//DT) : int(WINDOW[1]//DT) ] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtended = SimuTime[start:] # np.arange(1, WINDOW[1], DT)

    plt.plot(Time, Mean, label='Mean Lift', linestyle='solid', linewidth=0.5)
    plt.legend()
    plt.xlabel('time (s)')
    plt.ylabel('mean lift')
    plt.title(f'Mean Lift over Time')
    plt.savefig('MEAN_LIFT_PLOT.png')
    plt.show()

    ### SUBPLOTS
    fig, axs = plt.subplots(4,2, figsize=(10,10))
    axs[0, 0].plot(TimeExtended, Lifts[0][start:], color = 'darkblue', linewidth=0.5)
    axs[0, 0].set_title('Table0')
    axs[0, 1].plot(TimeExtended, Lifts[1][start:], color = 'darkblue', linewidth=0.5)
    axs[0, 1].set_title('Table1')
    axs[1, 0].plot(TimeExtended, Lifts[2][start:], color = 'darkblue', linewidth=0.5)
    axs[1, 0].set_title('Table2')
    axs[1, 1].plot(TimeExtended, Lifts[3][start:], color = 'darkblue', linewidth=0.5)
    axs[1, 1].set_title('Table3')
    axs[2, 0].plot(TimeExtended, Lifts[4][start:], color = 'darkblue', linewidth=0.5)
    axs[2, 0].set_title('Table4')
    axs[2, 1].plot(TimeExtended, Lifts[5][start:], color = 'darkblue', linewidth=0.5)
    axs[2, 1].set_title('Table5')
    axs[3, 0].plot(TimeExtended, Lifts[6][start:], color = 'darkblue', linewidth=0.5)
    axs[3, 0].set_title('Table6')
    axs[3, 1].plot(TimeExtended, Lifts[7][start:], color = 'darkblue', linewidth=0.5)
    axs[3, 1].set_title('Table7')
    for ax in axs.flat:
        ax.grid()
        ax.set(xlabel='time (s)', ylabel='Lift')
        ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
    # for ax in axs.flat:
    #     ax.label_outer()
    fig.suptitle(f'Lift Efforts Plot')
    fig.tight_layout()
    plt.savefig('EFFORTS_PLOT.png')
    plt.show()


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

    ### PLOTS
    start        = int(1/DT)
    Lifts        = retrieve_lifts(PATH_TO_EFFORTS)
    Mean         = compute_mlift(Lifts, WINDOW, DT)
    SimuTime     = retrieve_time(PATH_TO_EFFORTS)
    Time         = SimuTime[int(WINDOW[0]//DT) : int(WINDOW[1]//DT) ] # np.arange(WINDOW[0], WINDOW[1], DT)
    TimeExtended = SimuTime[start:] # np.arange(1, WINDOW[1], DT)

    plt.plot(Time, Mean, label='Mean Lift', linestyle='solid', linewidth=0.5)
    plt.legend()
    plt.xlabel('time (s)')
    plt.ylabel('mean lift')
    plt.title(f'Mean Lift over Time')
    plt.savefig('MEAN_LIFT_PLOT.png')
    plt.show()

    ### SUBPLOTS
    fig, axs = plt.subplots(3,2, figsize=(10,10))
    axs[0, 0].plot(TimeExtended, Lifts[0][start:], color = 'darkblue', linewidth=0.5)
    axs[0, 0].set_title('Table0')
    axs[0, 1].plot(TimeExtended, Lifts[1][start:], color = 'darkblue', linewidth=0.5)
    axs[0, 1].set_title('Table1')
    axs[1, 0].plot(TimeExtended, Lifts[2][start:], color = 'darkblue', linewidth=0.5)
    axs[1, 0].set_title('Table2')
    axs[1, 1].plot(TimeExtended, Lifts[3][start:], color = 'darkblue', linewidth=0.5)
    axs[1, 1].set_title('Table3')
    axs[2, 0].plot(TimeExtended, Lifts[4][start:], color = 'darkblue', linewidth=0.5)
    axs[2, 0].set_title('Table4')
    axs[2, 1].plot(TimeExtended, Lifts[5][start:], color = 'darkblue', linewidth=0.5)
    axs[2, 1].set_title('Table5')
    for ax in axs.flat:
        ax.grid()
        ax.set(xlabel='time (s)', ylabel='Lift')
        ax.tick_params(labelright=True, labelleft=True, left=True, right=True)
    # for ax in axs.flat:
    #     ax.label_outer()
    fig.suptitle(f'Lift Efforts Plot')
    fig.tight_layout()
    plt.savefig('EFFORTS_PLOT.png')
    plt.show()