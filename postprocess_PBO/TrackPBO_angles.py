import statistics
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 4:
    print("Usage: python script.py episodes environments rewardfilepath")
    sys.exit(1)
# enter the number of episodes
ep = int(sys.argv[1])
# enter the number of environments per episode
env = int(sys.argv[2])
# enter the path of reward file // ex : pbo_blm100\results\panels_09-47-46
rwd_path = sys.argv[3]

### Extract reward
f = open(f'{rwd_path}', 'r')
f1 = f.readlines()
f.close()
R1 = []
R2 = []
R3 = []
R4 = []
R5 = []
R6 = []

for i in range(ep*env):

    R1.append(float(f1[i].split() [3]))  # stocking all the angles of each environment
    R2.append(float(f1[i].split() [4]))
    R3.append(float(f1[i].split() [5]))
    R4.append(float(f1[i].split() [6]))
    R5.append(float(f1[i].split() [7]))
    R6.append(float(f1[i].split() [8]))

### angle plot
EE = np.arange(0,ep*env)

# subplots
fig, axs = plt.subplots(3,2, figsize=(10,10))

axs[0, 0].plot(EE, R1, color = 'darkblue', linewidth=0.5)
axs[0, 0].set_title('Theta_1')

axs[0, 1].plot(EE, R2, color = 'darkblue', linewidth=0.5)
axs[0, 1].set_title('Theta_2')

axs[1, 0].plot(EE, R3, color = 'darkblue', linewidth=0.5)
axs[1, 0].set_title('Theta_3')

axs[1, 1].plot(EE, R4, color = 'darkblue', linewidth=0.5)
axs[1, 1].set_title('Theta_4')

axs[2, 0].plot(EE, R5, color = 'darkblue', linewidth=0.5)
axs[2, 0].set_title('Theta_5')

axs[2, 1].plot(EE, R6, color = 'darkblue', linewidth=0.5)
axs[2, 1].set_title('Theta_6')

for ax in axs.flat:
    ax.grid()
    ax.set(xlabel='environments', ylabel='angles (30°)', ylim=(-1,1))
    ax.tick_params(labelright=True, labelleft=True, left=True, right=True)

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
fig.suptitle(f'{rwd_path} angles')
fig.tight_layout()
# plt.plot(EE, R, color = 'darkblue', linewidth=1.3, label = 'angles')
# plt.plot(G, MR, color = 'orange', label = 'min', linewidth = 1, linestyle='-')
# plt.plot(G, Up, 'g:', color = 'blue')
# plt.plot(G, Dw, 'g:', color = 'blue')
# plt.fill_between(G, Up, Dw, color = 'blue', label = 'std_dev', alpha = 0.15)
# plt.legend(loc="lower right")
# plt.grid()
# plt.title(f'{rwd_path} angles')
# plt.xlabel('Environments')
# plt.ylabel('angle')
# plt.tick_params(labelright=True, labelleft=True, left=True, right=True)
plt.savefig(f'{rwd_path}_ANGLE_PLOT.png')