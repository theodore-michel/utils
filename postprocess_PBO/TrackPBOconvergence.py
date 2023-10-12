import statistics
import matplotlib.pyplot as plt
import numpy as np
import sys

# enter the reward file path:
if len(sys.argv) != 2:
    print("Usage: python script.py rewardfilepath")
    sys.exit(1)
REWARD = str(sys.argv[1])

### Extract reward
file         = open(f'{REWARD}', 'r')
rewards_file = file.readlines()
file.close()
ENV          = 8        # number of env per episode
index_0line  = next((index for index, line in enumerate(rewards_file) if all("0.000" in col.strip() for col in line.split())) , None) # crop to rewards already output in file
EPISODES     = (index_0line//ENV) if index_0line is not None else (len(rewards_file) // ENV)
rewards_file = rewards_file[:EPISODES*ENV]
R            = []       # reward     
A1           = []       # action 1
A2           = []       # action 2
A3           = []       # action 3
A4           = []       # action 4
A5           = []       # action 5
A6           = []       # action 6
for i in range(len(rewards_file)):
    R.append(- float(rewards_file[i].split() [2]))  # stocking all the rewards of each Environment
    A1.append( float(rewards_file[i].split() [3]))  # stocking all the angles of each environment
    A2.append( float(rewards_file[i].split() [4]))
    A3.append( float(rewards_file[i].split() [5]))
    A4.append( float(rewards_file[i].split() [6]))
    A5.append( float(rewards_file[i].split() [7]))
    A6.append( float(rewards_file[i].split() [8]))

############## REWARD CONVERGENCE #####################################
colors   = ['darkblue', 'blue','darkorange']
fig, ax = plt.subplots(figsize=(8,8))
### Reward plot
M         = []
St        = []
MR        = []
EpAxis    = np.arange(0, EPISODES, dtype=int)  # setting the x axis by number of episode
EpEnvAxis = np.arange(0,EPISODES*ENV, dtype=int)
maxr      = -1000000
for i in range(0, EPISODES * ENV, 8):  # evaluate reward deviation on each episode of 8 Environments
    Ri = [R[i], R[i+1], R[i+2], R[i+3], R[i+4], R[i+5], R[i+6], R[i+7]]

    st   = statistics.stdev(Ri)
    mean = statistics.mean(Ri)
    # maxr = max(Ri)
    maxr = max(maxr,max(Ri))

    MR.append(maxr)
    St.append(st)
    M.append(mean)
Up = [M[i] + St[i] for i in range(len(M))]
Dw = [M[i] - St[i] for i in range(len(M))]
#
ax.plot(EpAxis, M, color = colors[0], linewidth=1.5, label = REWARD)
ax.fill_between(EpAxis, Up, Dw, color = colors[1], label = f'{REWARD} var', alpha = 0.15)
ax.plot(EpAxis, MR, color = colors[2], label = f'{REWARD} best', linewidth = 1, linestyle='--')
#
ax.legend(loc="lower right", fontsize="large")  # Set the font size to "small"
ax.grid(True, linewidth=0.5, linestyle='--', color='gray')
ax.set_title('Reward Convergence')
ax.set_xlabel('Episode')
ax.set_ylabel('Reward')
ax.set_xlim((0,EPISODES))
ax.set_xticks(np.arange(0, EPISODES+1, 5))
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
ax.set_ylim((1.1*min(M),0))
ax.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
fig.tight_layout()
fig.savefig(f'{REWARD}_reward.png')


################ ACTIONS CONVERGENCE ###################################################
figs, axs = plt.subplots(3,2, figsize=(8,8))
axs[0, 0].plot(EpEnvAxis, A1, color = colors[0], linewidth=0.4) #, label='Theta 1')
axs[0, 0].set_title('Theta 1')
axs[0, 1].plot(EpEnvAxis, A2, color = colors[0], linewidth=0.4) #, label='Theta 2')
axs[0, 1].set_title('Theta 2')
axs[1, 0].plot(EpEnvAxis, A3, color = colors[0], linewidth=0.4) #, label='Theta 3')
axs[1, 0].set_title('Theta 3')
axs[1, 1].plot(EpEnvAxis, A4, color = colors[0], linewidth=0.4) #, label='Theta 4')
axs[1, 1].set_title('Theta 4')
axs[2, 0].plot(EpEnvAxis, A5, color = colors[0], linewidth=0.4) #, label='Theta 5')
axs[2, 0].set_title('Theta 5')
axs[2, 1].plot(EpEnvAxis, A6, color = colors[0], linewidth=0.4) #, label='Theta 6')
axs[2, 1].set_title('Theta 6')
x_ticks        = np.arange(0,EPISODES*ENV+8,160)       # ,80)
x_ticks_labels = [str(int(x//8)) for x in x_ticks]   
for axss in axs.flat:
    # axss.legend(loc = 'lower right', framealpha=0.5, fontsize="large")
    axss.grid(True, linewidth=0.5, linestyle='--', color='gray')
    axss.set(xlabel='Episodes', ylabel='Angles (30°)', ylim=(-1.05,1.05))
    axss.set_xticks(x_ticks)
    axss.set_xticklabels(x_ticks_labels)
    axss.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    axss.set_yticks([-1, -0.5, 0, 0.5, 1])
    axss.tick_params(labelright=True, labelleft=True, labeltop=True, left=True, right=True, top=True)
    axss.label_outer()
figs.suptitle('Action Convergence')
figs.tight_layout()
figs.savefig(f'{REWARD}_actions.png')