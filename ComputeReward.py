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

def retrieve_torques(path):
    T = [ [], [], [], [], [], []]
    for i in range (6):
        with open(os.getcwd() + '/' + path + 'Torque' + str(i) + '.txt', 'r') as f:
            next(f) # Skip header
            for line in f:
                T[i].append(float(line.split()[2])) # select Lift column value
    T = np.array(T)
    return(T)

def retrieve_energy(path):
    Vx = [ [], [], [], [], [], []]
    Vy = [ [], [], [], [], [], []]
    for i in range (6):
        with open(os.getcwd() + '/' + path + 'Sensor' + str(i+1) + '.txt', 'r') as f:
            next(f) # Skip header
            for line in f:
                Vx[i].append(float(line.split()[2])) # select Vx column value
                Vy[i].append(float(line.split()[3])) # select Vy column value
    Vx = np.array(Vx)
    Vy = np.array(Vy)
    return(Vx,Vy)

### FUNCTIONS
def compute_rms(L, window=[50,100], dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped      = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg           = np.mean( LCropped , axis=1 )
    LMinusAvg     = LCropped - Avg[:,None]
    LMASquared    = LMinusAvg**2
    RMSIndividual = np.sqrt( np.mean(LMASquared, axis=1) )
    RMS           = np.mean(RMSIndividual)
    return(RMS)

def compute_mlift(L, window=[50,100], dt=0.1):
    # L is an array of shape (6,timesteps)
    LCropped = L[ : , int(window[0]//dt) : int(window[1]//dt) ]
    Avg      = np.mean( LCropped , axis=1 )
    AbsAvg   = np.abs(Avg)
    MeanLift = np.mean(AbsAvg, axis=0)
    return(MeanLift)

def compute_mtorque(T, window=[50,100], dt=0.1, start_t=100):
    # T is an array of shape (6,timesteps)
    # Torque computation starts at timestep start_t = 100
    TCropped = T[ : , int((window[0]-start_t)//dt) : int((window[1]-start_t)//dt) ]
    Avg      = np.mean( TCropped , axis=1 )
    AbsAvg   = np.abs(Avg)
    MeanLift = np.mean(AbsAvg, axis=0)
    return(MeanLift)

def compute_energy(Vx, Vy, window=[50,100], dt=0.1):
    # Vx/Vy is an array of shape (6,timesteps)
    VxCropped   = Vx[ : , int(window[0]//dt) : int(window[1]//dt) ]
    VyCropped   = Vy[ : , int(window[0]//dt) : int(window[1]//dt) ]
    AvgVx       = np.mean( VxCropped , axis=1 )
    AvgVy       = np.mean( VyCropped , axis=1 )
    VxMinusAvg  = VxCropped - AvgVx[:,None]
    VyMinusAvg  = VyCropped - AvgVy[:,None]
    VxMASquared = VxMinusAvg**2
    VyMASquared = VyMinusAvg**2
    E           = VxMASquared+VyMASquared
    Efluct      = np.sqrt( np.mean(E, axis=1) )
    Efluct      = np.mean(Efluct)
    return(Efluct)

### REWARDS 
def reward_meanlift(path, window=[100,300], dt=0.05, rescale=1000):
    '''computes mean of the time-averaged lift on each panel
    rescaled by a multiplication factor. time-average is performed 
    on the time window specified'''
    L      = retrieve_lifts(path)
    mean   = compute_mlift(L, window=window, dt=dt)
    reward = mean*rescale
    return reward

def reward_rmslift(path, window=[100,300], dt=0.05, rescale=1000):
    '''compute RMS lift on each panel and average on six panels'''
    L      = retrieve_lifts(path)
    rms    = compute_rms(L, window=window, dt=dt)
    reward = rms*rescale
    return reward

def reward_meantorque(path, window=[100,300], dt=0.05, rescale=1000):
    '''compute Torque on each panel and average on six panels'''
    T      = retrieve_torques(path)
    mean   = compute_mtorque(T, window=window, dt=dt)
    reward = mean*rescale
    return reward

def reward_energy(path, window=[100,300], dt=0.05, rescale=1000):
    '''compute energy on each capteur and average on six capteur or take rms'''
    Vx,Vy  = retrieve_energy(path)
    Efluct = compute_energy(Vx, Vy, window=window, dt=dt)
    reward = Efluct*rescale
    return reward   


### OUTPUT
MEAN_LIFT   = reward_meanlift(PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)
RMS_LIFT    = reward_rmslift( PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)
MEAN_TORQUE = reward_meantorque(PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)
FLUC_ENERGY = reward_energy(PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)

print(f'Mean Lift   Reward : {MEAN_LIFT} ')
print(f'RMS  Lift   Reward : {RMS_LIFT} ')
print(f'Mean Torque Reward : {MEAN_TORQUE} ')
print(f'Fluc Energy Reward : {FLUC_ENERGY} ')