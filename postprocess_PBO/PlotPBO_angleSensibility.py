from argparse import REMAINDER
import statistics
from tkinter import FALSE
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.colorbar import Colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable


# enter the reward file path:
if len(sys.argv) != 2:
    print("Usage: python script.py rewardfile")
    sys.exit(1)
REWARD = str(sys.argv[1])

### Extract reward
file         = open(f'{REWARD}', 'r')
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
colors       = []       # color for each action arrays

for i in range(len(rewards_file)):
    # axis
    Eaxis.append( int(float((rewards_file[i].split() [1]))) )
    # instantaneous
    R.append(   - float(rewards_file[i].split() [2]) ) 
    A1.append(    30*float(rewards_file[i].split() [3]) )  
    A2.append(    30*float(rewards_file[i].split() [4]) )
    A3.append(    30*float(rewards_file[i].split() [5]) )
    A4.append(    30*float(rewards_file[i].split() [6]) )
    A5.append(    30*float(rewards_file[i].split() [7]) )
    A6.append(    30*float(rewards_file[i].split() [8]) )
    colors.append(i/(ENV))

# colors    = ['lightgray', 'black', 'darkred'] # instant reward, moving avg reward, markers
indexBest   = R.index(max(R))
markerBest  = [ R[indexBest], A1[indexBest], A2[indexBest], A3[indexBest], A4[indexBest], A5[indexBest], A6[indexBest] ] 
# markersY  = [R[int(markersX[0]*8)], R[int(markersX[1]*8)], R[int(markersX[2]*8)], R[int(markersX[3]*8)], R[int(markersX[4]*8)], R[int(markersX[5]*8)]]
# markersA1 = [A1[int(markersX[0]*8)], A1[int(markersX[1]*8)], A1[int(markersX[2]*8)], A1[int(markersX[3]*8)], A1[int(markersX[4]*8)], A1[int(markersX[5]*8)]]
# markersA2 = [A2[int(markersX[0]*8)], A2[int(markersX[1]*8)], A2[int(markersX[2]*8)], A2[int(markersX[3]*8)], A2[int(markersX[4]*8)], A2[int(markersX[5]*8)]]
# markersA3 = [A3[int(markersX[0]*8)], A3[int(markersX[1]*8)], A3[int(markersX[2]*8)], A3[int(markersX[3]*8)], A3[int(markersX[4]*8)], A3[int(markersX[5]*8)]]
# markersA4 = [A4[int(markersX[0]*8)], A4[int(markersX[1]*8)], A4[int(markersX[2]*8)], A4[int(markersX[3]*8)], A4[int(markersX[4]*8)], A4[int(markersX[5]*8)]]
# markersA5 = [A5[int(markersX[0]*8)], A5[int(markersX[1]*8)], A5[int(markersX[2]*8)], A5[int(markersX[3]*8)], A5[int(markersX[4]*8)], A5[int(markersX[5]*8)]]
# markersA6 = [A6[int(markersX[0]*8)], A6[int(markersX[1]*8)], A6[int(markersX[2]*8)], A6[int(markersX[3]*8)], A6[int(markersX[4]*8)], A6[int(markersX[5]*8)]]

############## REWARD CONVERGENCE #####################################
# fig, ax  = plt.subplots(figsize=(6,4))
# #
# ax.plot(Eaxis,  R, color = colors[0], linewidth = 1, label = 'Instant',         linestyle='-')
# ax.plot(Eaxis, MR, color = colors[1], linewidth = 2, label = 'Moving Average',  linestyle='-')
# ax.scatter(markersX, markersY, s=30, facecolors='none', edgecolors=colors[2])
# #
# ax.legend(loc="lower right", fontsize="large")  # Set the font size to "small"
# ax.grid(True, linewidth=0.5, linestyle='--', color='gray')
# ax.set_title('Reward Convergence')
# ax.set_xlabel('Episode')
# ax.set_ylabel('Reward')
# ax.set_xlim((0,EPISODES))
# ax.set_xticks(np.arange(0, EPISODES+1, 10))
# ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
# ax.set_ylim((1.1*min(R),0))
# ax.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
# fig.tight_layout()
# fig.savefig(f'{REWARD}_reward_article.png')


################ REWARD SENSIBILITY TO ACTIONS ###################################################
figs, axs = plt.subplots(3,2, figsize=(8,8))
# action 1
axs[0, 0].scatter(A1, R,  s=2, c= colors, alpha=0.6, cmap='copper')
axs[0, 0].scatter(markerBest[1], markerBest[0], marker='+', s=30, linewidths=1, color='red', label='best')
axs[0, 0].set_title(r"$\theta_1$")
axs[0, 0].legend(fontsize='small')
# action 2
axs[0, 1].scatter(A2, R,  s=2, c= colors, alpha=0.6, cmap='copper')
axs[0, 1].scatter(markerBest[2], markerBest[0], marker='+', s=30, linewidths=1, color='red')
axs[0, 1].set_title(r"$\theta_2$")
# action 3
axs[1, 0].scatter(A3, R,  s=2, c= colors, alpha=0.6, cmap='copper')
axs[1, 0].scatter(markerBest[3], markerBest[0], marker='+', s=30, linewidths=1, color='red')
axs[1, 0].set_title(r"$\theta_3$")
# action 4
axs[1, 1].scatter(A4, R,  s=2, c = colors, alpha=0.6, cmap='copper')
axs[1, 1].scatter(markerBest[4], markerBest[0], marker='+', s=30, linewidths=1, color='red')
axs[1, 1].set_title(r"$\theta_4$")
# action 5
axs[2, 0].scatter(A5, R,  s=2, c= colors, alpha=0.6, cmap='copper')
axs[2, 0].scatter(markerBest[5], markerBest[0], marker='+', s=30, linewidths=1, color='red')
axs[2, 0].set_title(r"$\theta_5$")
# action 6
axs[2, 1].scatter(A6, R,  s=2, c= colors, alpha=0.6, cmap='copper')
axs[2, 1].scatter(markerBest[6], markerBest[0], marker='+', s=30, linewidths=1, color='red')
axs[2, 1].set_title(r"$\theta_6$")

for axss in axs.flat:
    axss.grid(True, linewidth=0.5, linestyle='--', color='gray')
    axss.set(xlabel='Actions (°)', ylabel='Reward', xlim= (-30.1,30.1), ylim=(min(R),0))
    axss.set_xticks([-30, -15, 0, 15, 30])
    # axss.set(xlabel='Actions (°)', ylabel='Reward', xlim= (0.9,2.1), ylim=(-13.5,-12.5))
    # axss.set_xticks([1, 1.25, 1.5, 1.75, 2])
    axss.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
    axss.label_outer()

# Create a common colorbar for all subplots
cax  = figs.add_axes([0.125, 0.05, 0.775, 0.02])
cbar = figs.colorbar(axs[0, 0].scatter(A1, R, s=2, c=colors, alpha=0.8, cmap='copper'), cax=cax, orientation='horizontal')
axs[0, 0].scatter(markerBest[1], markerBest[0], marker='+', s=30, linewidths=1, color='red', label='best')
cbar.set_label('Episodes')
cbar.set_ticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
plt.subplots_adjust(bottom=0.13)  # Adjust the bottom margin to accommodate the colorbar

#save
figs.suptitle(f'{REWARD} reward sensibility to actions')
# figs.tight_layout()
plt.show()
figs.savefig(f'{REWARD}_reward_sensibility.png')