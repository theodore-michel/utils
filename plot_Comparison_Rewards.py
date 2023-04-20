import numpy as np
import matplotlib.pyplot as plt


def compute_rms(L, window=[50,100],dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped      = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg           = np.mean( L , axis=1 )
    LMinusAvg     = LCropped - Avg[:,None]
    LMASquared    = LMinusAvg**2
    RMSIndividual = np.sqrt( np.mean(LMASquared, axis=1) )
    RMS           = np.mean(RMSIndividual)
    return(RMS)

def compute_mlift(L,window=[50,100],dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    LAbs     = np.abs(LCropped)
    Avg      = np.mean( LAbs , axis=1 )
    MeanLift = np.mean(Avg, axis=0)
    return(MeanLift)






def plot_EffortsAll(folder, dt = 0.05, cut=(0,300), numComp=2):
    A = [ [[],[],[]] , [[],[],[]] , [[],[],[]] , [[],[],[]] ]
    for eff in range(numComp):
        with open(folder + '/Data' + str(eff) + '/EffortsAll.txt', 'r') as f:
            next(f) # Skip header
            for line in f:
                A[eff][1].append(float(line.split()[3])) # select Lift column value
                A[eff][0].append(float(line.split()[1]))
        M = np.array(A[eff][1])
        M = np.mean(M[int(cut[0]//dt) : int(cut[1]//dt)])
        A[eff][2] = [M]*len(A[eff][0])

    ## Plot
    plt.plot(A[0][0], A[0][1], color='red',  label='coarse dt='+str(dt), linestyle='solid',  linewidth=0.5)
    plt.plot(A[0][0], A[0][2], color='red',  label='coarse dt='+str(dt)+' mean',  linestyle='dashed', linewidth=0.5)

    plt.plot(A[1][0], A[1][1], color='blue',  label='fine dt='+str(dt),  linestyle='solid', linewidth=0.5)
    plt.plot(A[1][0], A[1][2], color='blue',  label='fine dt='+str(dt)+' mean',  linestyle='dashed', linewidth=0.5)

    # Adding a legend
    plt.legend()

    # Set the bounds of the axes
    y_min, y_max = (-5, 3)
    x_min, x_max = (0, 325)
    plt.ylim(y_min, y_max)
    plt.xlim(x_min, x_max)

    # Adding axis labels and title
    plt.xlabel('time (s)')
    plt.ylabel('mean lift')
    plt.title(f'dt={dt} (avg {cut[0]}s-{cut[1]}s)')

    # Displaying the plot
    name = 'mesh_comparison_dt'
    plt.savefig(name)
    plt.show()

# plot_EffortsAll(folder='compare_dt005', dt=0.05, cut=(50,180))
# plot_EffortsAll(folder='compare_dt01',  dt=0.1,  cut=(50,180))


def plot_AllDT(folder, DT = [0.05,0.1], cut=[0,300], meshes=['coarse','fine']):

    it=0

    print('REWARD')
    print(f'{cut[0]}s - {cut[1]}s averages:')
    print()

    for dt in DT:
        A = [ [[],[],[]] , [[],[],[]] ]
        meshnum = 0
        for mesh in meshes:
            L = [[],[],[],[],[],[]]
            for i in range (6):
                with open(folder + '/Data_'+str(it)+'_'+mesh+'/Efforts'+str(i)+'.txt', 'r') as f:
                    next(f) # Skip header
                    for line in f:
                        L[i].append(float(line.split()[3])) # select Lift column value
                        if i==0: A[meshnum][0].append(float(line.split()[1]))

            L             = np.array(L)
            A[meshnum][1] = np.mean(L, axis=0).tolist()
            A[meshnum][2] = [np.mean(L)]*len(A[meshnum][0])

            RMS      = compute_rms(L,   window=cut, dt=dt)
            MeanLift = compute_mlift(L, window=cut, dt=dt)

            meshnum +=1

            print(f'moy {mesh} mesh, dt {dt} : {MeanLift} ')
            print(f'rms {mesh} mesh, dt {dt} : {RMS} ')
            print()

        ## Plot
        plt.plot(A[0][0], A[0][1], color=plt.cm.tab20(it),     label='coarse dt='+str(dt),         linestyle='solid',  linewidth=0.65)
        plt.plot(A[0][0], A[0][2], color=plt.cm.tab20(it),     label='coarse dt='+str(dt)+' mean', linestyle='dashed', linewidth=0.65)

        plt.plot(A[1][0], A[1][1], color=plt.cm.tab20((it+1)), label='fine dt='+str(dt),           linestyle='solid',  linewidth=0.65)
        plt.plot(A[1][0], A[1][2], color=plt.cm.tab20((it+1)), label='fine dt='+str(dt)+' mean',   linestyle='dashed', linewidth=0.65)

        it += meshnum

    # Adding a legend
    plt.legend()

    # Set the bounds of the axes
    y_min, y_max = (-1, 1)
    x_min, x_max = ( 0, 325)
    plt.ylim(y_min, y_max)
    plt.xlim(x_min, x_max)

    # Adding axis labels and title
    plt.xlabel('time (s)')
    plt.ylabel('mean lift')
    plt.title(f'dt={DT} (avg {cut[0]}s-{cut[1]}s)')

    # Displaying the plot
    name = 'comp_mesh_dt_reward'
    plt.savefig(name)
    plt.show()




######### EXECUTE ####################

plot_AllDT(folder='compare_dt', DT=[0.05,0.1], cut=[50,300])





