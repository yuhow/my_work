"""
YH's NN

fixed input fitting template(s)

2017.10.25
"""

#from __future__ import print_function
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def input_creator(input_x, fcn_name):
    if fcn_name == "square":
        #return tf.Variable(np.square(input_x))
        return np.square(input_x)
    elif fcn_name == "exp":
        #return tf.Variable(np.exp(input_x))
        return np.exp(input_x)
    elif fcn_name == "gauss":
        #return tf.Variable(np.exp(-np.power(input_x, 2.) / (2 * np.power(2, 2.))))
        return np.exp(-np.power(input_x, 2.) / (2 * np.power(2, 2.)))

def add_layer(inputs, in_size, out_size, activation_function=None):
    # add one more layer and return the output of this layer
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

# global setting
H1_NEURON = 5

# Make up some real data and input fitting template(s)
x_data = np.linspace(-1, 1, 50)[:, np.newaxis]  # np.newaxis adds a new dimension to x_data
fcn_1 = input_creator(x_data, 'square')
fcn_2 = input_creator(x_data, 'exp')
fcn_3 = input_creator(x_data, 'gauss')

input_template = np.concatenate((fcn_1, fcn_2, fcn_3), axis=1)
#print input_template.shape

noise = np.random.normal(0, 0.05, x_data.shape)  # noise has the same shape as x
#y_data = np.square(x_data) + np.exp(x_data) - 0.5 + noise  # y = x*x - 0.5 + noise
y_data = np.square(x_data) + 0.5 + noise  # y = x*x + 0.5 + noise
#y_data = np.square(x_data) - 0.5  # y = x*x - 0.5

#y_data = np.repeat(y_data.reshape(1,y_data.shape[0]), 2, axis=0)

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 3])
ys = tf.placeholder(tf.float32, [None, 1])

# Input -> hidden1 -> output
#   3   ->   5     ->   1
# add hidden layer (3 in and 5 out)
l1 = add_layer(xs, 3, H1_NEURON, activation_function=tf.nn.softplus)
#l1 = add_layer(xs, 3, H1_NEURON,, activation_function=tf.nn.relu)

# add output layer (10 in and 1 out)
prediction = add_layer(l1, H1_NEURON, 1, activation_function=None)

# the error between prediciton and real data
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                      reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# plot the real data
fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('bisque')

#ax_bg = fig.add_subplot(1, 1, 1)
ax_in = []
for k_idx in range(3):
    ax_in.append(fig.add_subplot(5, 3, k_idx*3+4))
ax_h1 = []
for k_idx in range(H1_NEURON):
    ax_h1.append(fig.add_subplot(5, 3, k_idx*3+2))
ax = fig.add_subplot(1, 3, 3)
frame_seq = []

# background
#ax_bg.plot()

# input fitting templates
ax_in[0].plot(x_data, fcn_1, c='blue')
ax_in[1].plot(x_data, fcn_2, c='blue')
ax_in[2].plot(x_data, fcn_3, c='blue')

# start training NN
for i in range(10000):
    # training
    sess.run(train_step, feed_dict={xs: input_template, ys: y_data})
    if i % 50 == 0:
        # to visualize the result and improvement
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass

        h1_kernels = sess.run(l1, feed_dict={xs: input_template})
        prediction_value = sess.run(prediction, feed_dict={xs: input_template})

        # h1 output
        all_output = []
        for k_idx in range(h1_kernels.shape[1]):
            if i == 0:
                plot_tmp, = ax_h1[k_idx].plot(x_data, h1_kernels[:, k_idx], c='blue', label='kernel_h1-'+str(k_idx+1))
            else:
                plot_tmp, = ax_h1[k_idx].plot(x_data, h1_kernels[:, k_idx], c='blue')
            ax_h1[k_idx].legend(loc="upper right", prop={'size': 10})
            all_output.append(plot_tmp)
        
        # plot the prediction
        #plt.pause(0.1)
        #frame_seq.append(plt.plot(x_data, prediction_value, 'r-', lw=5))
        ax.set_xlim((np.amin(x_data)-abs(np.amin(x_data)*0.1), np.amax(x_data)+abs(np.amax(x_data)*0.1)))
        ax.set_ylim((np.amin(y_data)-abs(np.amin(y_data)*0.1), np.amax(y_data)+abs(np.amax(y_data)*0.1)))
        plot_output, = ax.plot(x_data, prediction_value, 'r.')
        all_output.append(plot_output)
        frame_seq.append(tuple(all_output))
#        frame_seq.append(ax.plot(x_data, prediction_value, 'r.'))

ani = animation.ArtistAnimation(fig, frame_seq, interval=250, blit=True, repeat=False)
ax.scatter(x_data, y_data)

plt.tight_layout()

# subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
plt.subplots_adjust(wspace = 1)

plt.show()
