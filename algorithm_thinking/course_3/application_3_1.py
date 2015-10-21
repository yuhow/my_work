"""
Application 3 of Algorithm thinking
2015/07/23

Question 3-1
Author: You-Hao Chang
"""

import helper
import AT_project_3 as pj3
import time
import matplotlib.pyplot as plt

running_time_scp = []
running_time_fcp = []

for num_clusters in range(2, 201):
    cluster_list = helper.gen_random_clusters(num_clusters)
    start_time = time.time()
    pj3.slow_closest_pair(cluster_list)
    running_time_scp.append(time.time() - start_time)
    start_time = time.time()
    pj3.fast_closest_pair(cluster_list)
    running_time_fcp.append(time.time() - start_time)

#making comparison plots
fig, ax = plt.subplots()
x_vals = [idx for idx in range(2, 201)]

ax.plot(x_vals, running_time_scp, '-b', label = 'slow closest pair')
ax.plot(x_vals, running_time_fcp, '-r', label = 'fast closest pair')

ax.legend(loc = 'upper left')
ax.set_title('Timing results (in desktop Python)')
ax.set_xlabel('number of initial clusters')
ax.set_ylabel('running time [second]')

plt.show()
