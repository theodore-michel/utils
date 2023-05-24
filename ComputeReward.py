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

### OUTPUT
MEAN_LIFT = reward_meanlift(PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)
RMS_LIFT  = reward_rmslift( PATH_TO_EFFORTS, WINDOW, DT, rescale=1000)

print(f'Mean Lift Reward : {MEAN_LIFT} ')
print(f'RMS  Lift Reward : {RMS_LIFT} ')