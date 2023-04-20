import statistics
import matplotlib.pyplot as plt
import numpy as np
import sys

# enter the number of episodes
ep = int(sys.argv[1])

# enter the number of environments per episode
env = int(sys.argv[2])

# enter the path of reward file // ex : pbo_blm100\results\panels_09-47-46
rwd_path = sys.argv[3]

### Extract reward
f = open(f'{rwd_path}\pbo_0', 'r')
f1 = f.readlines()
f.close()
R = []

for i in range(len(f1)):

    R.append(- float(f1[i].split() [2]))  # stocking all the rewards of each environment

# max and min reward
max_r = np.max(R)
min_r = np.min(R)

### Reward plot
M = []
St = []
MR = []
G = np.arange(0, ep)  # setting the x axis by number of episode

for i in range(0, ep * env, 8):  # evaluate reward deviation on each episode of 8 environments

    Ri = [R[i], R[i+1], R[i+2], R[i+3], R[i+4], R[i+5], R[i+6], R[i+7]]

    st = statistics.stdev(Ri)
    mean = statistics.mean(Ri)
    maxr = max(Ri)

    MR.append(maxr)
    St.append(st)
    M.append(mean)

Up = [M[i] + St[i] for i in range(len(M))]
Dw = [M[i] - St[i] for i in range(len(M))]


plt.plot(G, M, color = 'darkblue', label = 'mean_reward')
plt.plot(G, MR, color = 'orange', label = 'min_reward', linewidth = 2)
plt.plot(G, Up, 'g:', color = 'blue')
plt.plot(G, Dw, 'g:', color = 'blue')
plt.fill_between(G, Up, Dw, color = 'blue', label = 'std_deviation', alpha = 0.2)
plt.legend(loc="lower right")
plt.grid()
plt.title('Reward : mean_lift')
plt.xlabel('Episode')
plt.ylabel('REWARD')
plt.savefig(f'{rwd_path}\plot_reward.png')