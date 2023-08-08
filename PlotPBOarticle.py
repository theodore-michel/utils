import statistics
from tkinter import FALSE
import matplotlib.pyplot as plt
import numpy as np
import sys

# enter the reward file path:
REWARD = str(sys.argv[1])

### Extract reward
file         = open(f'myreward_pbo_{REWARD}.txt', 'r')
rewards_file = file.readlines()
file.close()
ENV          = 8        # number of env per episode
EPISODES     = 100
Eaxis        = []       # episodes/env axis
R            = []       # reward   
MR           = []       # moving avg reward  
A1           = []       # action 1
A2           = []       # action 2
A3           = []       # action 3
A4           = []       # action 4
A5           = []       # action 5
A6           = []       # action 6
MA1          = []       # moving avg action 1
MA2          = []       # moving avg action 2
MA3          = []       # moving avg action 3
MA4          = []       # moving avg action 4
MA5          = []       # moving avg action 5
MA6          = []       # moving avg action 6
for i in range(len(rewards_file)):
    # axis
    Eaxis.append( float(rewards_file[i].split() [0]) )
    # instantaneous
    R.append(   - float(rewards_file[i].split() [1]) ) 
    A1.append(    float(rewards_file[i].split() [2]) )  
    A2.append(    float(rewards_file[i].split() [3]) )
    A3.append(    float(rewards_file[i].split() [4]) )
    A4.append(    float(rewards_file[i].split() [5]) )
    A5.append(    float(rewards_file[i].split() [6]) )
    A6.append(    float(rewards_file[i].split() [7]) )
    # moving avg
    MR.append(  - float(rewards_file[i].split() [8] ) ) 
    MA1.append(   float(rewards_file[i].split() [9] ) )  
    MA2.append(   float(rewards_file[i].split() [10]) )
    MA3.append(   float(rewards_file[i].split() [11]) )
    MA4.append(   float(rewards_file[i].split() [12]) )
    MA5.append(   float(rewards_file[i].split() [13]) )
    MA6.append(   float(rewards_file[i].split() [14]) )

colors    = ['lightgray', 'black', 'darkred'] # instant reward, moving avg reward, markers
markersX  = [1.0, 15.0, 25.0, 43.375, 70.0, 98.875] 
markersY  = [R[int(markersX[0]*8)], R[int(markersX[1]*8)], R[int(markersX[2]*8)], R[int(markersX[3]*8)], R[int(markersX[4]*8)], R[int(markersX[5]*8)]]
markersA1 = [A1[int(markersX[0]*8)], A1[int(markersX[1]*8)], A1[int(markersX[2]*8)], A1[int(markersX[3]*8)], A1[int(markersX[4]*8)], A1[int(markersX[5]*8)]]
markersA2 = [A2[int(markersX[0]*8)], A2[int(markersX[1]*8)], A2[int(markersX[2]*8)], A2[int(markersX[3]*8)], A2[int(markersX[4]*8)], A2[int(markersX[5]*8)]]
markersA3 = [A3[int(markersX[0]*8)], A3[int(markersX[1]*8)], A3[int(markersX[2]*8)], A3[int(markersX[3]*8)], A3[int(markersX[4]*8)], A3[int(markersX[5]*8)]]
markersA4 = [A4[int(markersX[0]*8)], A4[int(markersX[1]*8)], A4[int(markersX[2]*8)], A4[int(markersX[3]*8)], A4[int(markersX[4]*8)], A4[int(markersX[5]*8)]]
markersA5 = [A5[int(markersX[0]*8)], A5[int(markersX[1]*8)], A5[int(markersX[2]*8)], A5[int(markersX[3]*8)], A5[int(markersX[4]*8)], A5[int(markersX[5]*8)]]
markersA6 = [A6[int(markersX[0]*8)], A6[int(markersX[1]*8)], A6[int(markersX[2]*8)], A6[int(markersX[3]*8)], A6[int(markersX[4]*8)], A6[int(markersX[5]*8)]]

############## REWARD CONVERGENCE #####################################
fig, ax  = plt.subplots(figsize=(6,4))
#
ax.plot(Eaxis,  R, color = colors[0], linewidth = 1, label = 'Instant',         linestyle='-')
ax.plot(Eaxis, MR, color = colors[1], linewidth = 2, label = 'Moving Average',  linestyle='-')
ax.scatter(markersX, markersY, s=30, facecolors='none', edgecolors=colors[2])
#
ax.legend(loc="lower right", fontsize="large")  # Set the font size to "small"
ax.grid(True, linewidth=0.5, linestyle='--', color='gray')
ax.set_title('Reward Convergence')
ax.set_xlabel('Episode')
ax.set_ylabel('Reward')
ax.set_xlim((0,EPISODES))
ax.set_xticks(np.arange(0, EPISODES+1, 10))
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.set_ylim((1.1*min(R),0))
ax.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
fig.tight_layout()
fig.savefig(f'{REWARD}_reward_article.png')


################ ACTIONS CONVERGENCE ###################################################
figs, axs = plt.subplots(3,2, figsize=(8,8))
# action 1
axs[0, 0].plot(Eaxis, A1,  color = colors[0], linewidth=0.7)
axs[0, 0].plot(Eaxis, MA1, color = colors[1], linewidth=1)
axs[0, 0].scatter(markersX, markersA1, s=30, facecolors='none', edgecolors=colors[2])
axs[0, 0].set_title(r"$\theta_1$")
# action 2
axs[0, 1].plot(Eaxis, A2,  color = colors[0], linewidth=0.7)
axs[0, 1].plot(Eaxis, MA2, color = colors[1], linewidth=1)
axs[0, 1].scatter(markersX, markersA2, s=30, facecolors='none', edgecolors=colors[2])
axs[0, 1].set_title(r"$\theta_2$")
# action 3
axs[1, 0].plot(Eaxis, A3,  color = colors[0], linewidth=0.7)
axs[1, 0].plot(Eaxis, MA3, color = colors[1], linewidth=1)
axs[1, 0].scatter(markersX, markersA3, s=30, facecolors='none', edgecolors=colors[2])
axs[1, 0].set_title(r"$\theta_3$")
# action 4
axs[1, 1].plot(Eaxis, A4,  color = colors[0], linewidth=0.7)
axs[1, 1].plot(Eaxis, MA4, color = colors[1], linewidth=1)
axs[1, 1].scatter(markersX, markersA4, s=30, facecolors='none', edgecolors=colors[2])
axs[1, 1].set_title(r"$\theta_4$")
# action 5
axs[2, 0].plot(Eaxis, A5,  color = colors[0], linewidth=0.7)
axs[2, 0].plot(Eaxis, MA5, color = colors[1], linewidth=1)
axs[2, 0].scatter(markersX, markersA5, s=30, facecolors='none', edgecolors=colors[2])
axs[2, 0].set_title(r"$\theta_5$")
# action 6
axs[2, 1].plot(Eaxis, A6,  color = colors[0], linewidth=0.7)
axs[2, 1].plot(Eaxis, MA6, color = colors[1], linewidth=1)
axs[2, 1].scatter(markersX, markersA6, s=30, facecolors='none', edgecolors=colors[2])
axs[2, 1].set_title(r"$\theta_6$")
#

for axss in axs.flat:
    # axss.legend(loc = 'lower right', framealpha=0.5, fontsize="large")
    axss.grid(True, linewidth=0.5, linestyle='--', color='gray')
    axss.set(xlabel='Episodes', ylabel='Angles (°)', ylim=(-30.1,30.1))
    axss.set_xticks(np.arange(0, EPISODES+1, 10))
    axss.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    axss.set_yticks([-30, -15, 0, 15, 30])
    axss.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
    axss.label_outer()
figs.suptitle('Action Convergence')
figs.tight_layout()
figs.savefig(f'{REWARD}_actions_article.png')