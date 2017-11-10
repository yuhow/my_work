
import numpy as np
import numpy.random as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def input_creator(input_x, fcn_name):
    """
    return normalized array
    """
    if fcn_name == "square":
        return normalize(np.square(input_x))
    elif fcn_name == "exp":
        return normalize(np.exp(input_x))
    elif fcn_name == "gauss":
        return normalize(np.exp(-np.power(input_x, 2.) / (2 * np.power(2, 2.))))
    elif fcn_name == "sin":
        return normalize(np.sin(input_x))
    elif fcn_name == "order1_poly":
        return normalize(np.random.randint(-5, 5)*input_x/np.random.randint(-5, 5) + np.random.randint(-5, 5))
    elif fcn_name == "None":
        return np.zeros(input_x.shape)


def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm


def softplus(x):
    return np.log(1 + np.exp(x))


def softplus_deriv(x):
    return 1 / (1 + np.exp(-x))


def setup_and_init_weights(nn_structure):
    W = {}
    b = {}
    for l in range(1, len(nn_structure)):
        W[l] = r.random_sample((nn_structure[l], nn_structure[l-1]))
        b[l] = r.random_sample((nn_structure[l],))
    return W, b


def init_tri_values(nn_structure):
    tri_W = {}
    tri_b = {}
    for l in range(1, len(nn_structure)):
        tri_W[l] = np.zeros((nn_structure[l], nn_structure[l-1]))
        tri_b[l] = np.zeros((nn_structure[l],))
    return tri_W, tri_b


def feed_forward(x, W, b):
    h = {1: x}
    z = {}
    for l in range(1, len(W) + 1):
        # if it is the first layer, then the input into the weights is x, otherwise,
        # it is the output from the last layer
        if l == 1:
            node_in = x
        else:
            node_in = h[l]
        z[l+1] = W[l].dot(node_in) + b[l] # z^(l+1) = W^(l)*h^(l) + b^(l)
        if l != len(W):
            h[l+1] = softplus(z[l+1]) # h^(l) = f(z^(l))
        else:
            h[l+1] = z[l+1] # h^(l) = f(z^(l))
    return h, z


def calculate_out_layer_delta(y, h_out, z_out):
    # delta^(nl) = -(y_i - h_i^(nl)) * f'(z_i^(nl))
    return -(y-h_out) 


def calculate_hidden_delta(delta_plus_1, w_l, z_l):
    # delta^(l) = (transpose(W^(l)) * delta^(l+1)) * f'(z^(l))
    return np.dot(np.transpose(w_l), delta_plus_1) * softplus_deriv(z_l)


def train_nn(nn_structure, X, y, iter_num=10000, alpha=0.25):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    frame_seq = []
    x_data = np.linspace(-1, 1, 100)[:, np.newaxis]  # np.newaxis adds a new dimension to x_data
    W, b = setup_and_init_weights(nn_structure)
    cnt = 0
    m = len(y)
    avg_cost_func = []
    print('Starting gradient descent for {} iterations'.format(iter_num))
    while cnt < iter_num:
        if cnt%1000 == 0:
            print('Iteration {} of {}'.format(cnt, iter_num))
        tri_W, tri_b = init_tri_values(nn_structure)
        avg_cost = 0
        for i in range(len(y)):
            delta = {}
            # perform the feed forward pass and return the stored h and z values, to be used in the
            # gradient descent step
            h, z = feed_forward(X[i, :], W, b)
            # loop from nl-1 to 1 backpropagating the errors
            for l in range(len(nn_structure), 0, -1):
                if l == len(nn_structure):
                    delta[l] = calculate_out_layer_delta(y[i,:], h[l], z[l])
                    avg_cost += np.linalg.norm((y[i,:]-h[l]))
                else:
                    if l > 1:
                        delta[l] = calculate_hidden_delta(delta[l+1], W[l], z[l])
                    # triW^(l) = triW^(l) + delta^(l+1) * transpose(h^(l))
                    tri_W[l] += np.dot(delta[l+1][:,np.newaxis], np.transpose(h[l][:,np.newaxis]))
                    # trib^(l) = trib^(l) + delta^(l+1)
                    tri_b[l] += delta[l+1]
        # perform the gradient descent step for the weights in each layer
        for l in range(len(nn_structure) - 1, 0, -1):
            #W[l] += -alpha * (1.0/m * tri_W[l])
            W[l] += -alpha * (1.0/m * tri_W[l] + 0.001 * W[l])
            b[l] += -alpha * (1.0/m * tri_b[l])
        # complete the average cost calculation
        avg_cost = 1.0/m * avg_cost
        avg_cost_func.append(avg_cost)
        cnt += 1
        if cnt%50 == 0:
            y_predict = predict_y(W, b, X, len(nn_structure))
            ax.set_xlim((np.amin(x_data)-abs(np.amin(x_data)*0.5), np.amax(x_data)+abs(np.amax(x_data)*0.5)))
            ax.set_ylim((np.amin(y)-abs(np.amin(y)*0.5), np.amax(y)+abs(np.amax(y)*0.5)))
            frame_seq.append(plt.plot(x_data, y_predict, 'r.'))
    #ani = animation.ArtistAnimation(fig, frame_seq, interval=100, blit=True, repeat=False)
    ani = animation.ArtistAnimation(fig, frame_seq, interval=100, blit=True, repeat=True)
    ax.scatter(x_data, y)
    plt.show()
    return W, b, avg_cost_func


def train_nn_SGD(nn_structure, X, y, iter_num=3000, alpha=0.25, lamb=0.000):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    frame_seq = []
    x_data = np.linspace(-1, 1, 100)[:, np.newaxis]  # np.newaxis adds a new dimension to x_data
    W, b = setup_and_init_weights(nn_structure)
    cnt = 0
    m = len(y)
    avg_cost_func = []
    print('Starting gradient descent for {} iterations'.format(iter_num))
    while cnt < iter_num:
        if cnt%50 == 0:
            print('Iteration {} of {}'.format(cnt, iter_num))
        tri_W, tri_b = init_tri_values(nn_structure)
        avg_cost = 0
        for i in range(len(y)):
            delta = {}
            # perform the feed forward pass and return the stored h and z values, 
            # to be used in the gradient descent step
            h, z = feed_forward(X[i, :], W, b)
            # loop from nl-1 to 1 backpropagating the errors
            for l in range(len(nn_structure), 0, -1):
                if l == len(nn_structure):
                    delta[l] = calculate_out_layer_delta(y[i,:], h[l], z[l])
                    avg_cost += np.linalg.norm((y[i,:]-h[l]))
                else:
                    if l > 1:
                        delta[l] = calculate_hidden_delta(delta[l+1], W[l], z[l])
                    # triW^(l) = triW^(l) + delta^(l+1) * transpose(h^(l))
                    tri_W[l] = np.dot(delta[l+1][:,np.newaxis], np.transpose(h[l][:,np.newaxis])) 
                    # trib^(l) = trib^(l) + delta^(l+1)
                    tri_b[l] = delta[l+1]
            # perform the gradient descent step for the weights in each layer
            for l in range(len(nn_structure) - 1, 0, -1):
                W[l] += -alpha * (tri_W[l] + lamb * W[l])
                b[l] += -alpha * (tri_b[l])
        # complete the average cost calculation
        avg_cost = 1.0/m * avg_cost
        avg_cost_func.append(avg_cost)
        cnt += 1
        if cnt%50 == 0:
            y_predict = predict_y(W, b, X, len(nn_structure))
            ax.set_xlim((np.amin(x_data)-abs(np.amin(x_data)*0.5), np.amax(x_data)+abs(np.amax(x_data)*0.5)))
            ax.set_ylim((np.amin(y)-abs(np.amin(y)*0.5), np.amax(y)+abs(np.amax(y)*0.5)))
            frame_seq.append(plt.plot(x_data, y_predict, 'r.'))
    #ani = animation.ArtistAnimation(fig, frame_seq, interval=100, blit=True, repeat=False)
    ani = animation.ArtistAnimation(fig, frame_seq, interval=100, blit=True, repeat=True)
    ax.scatter(x_data, y)
    plt.show()
    return W, b, avg_cost_func


def train_nn_MBGD(nn_structure, X, y, bs=100, iter_num=3000, alpha=0.25, lamb=0.000):
    W, b = setup_and_init_weights(nn_structure)
    cnt = 0
    m = len(y)
    avg_cost_func = []
    print('Starting gradient descent for {} iterations'.format(iter_num))
    while cnt < iter_num:
        if cnt%1000 == 0:
            print('Iteration {} of {}'.format(cnt, iter_num))
        tri_W, tri_b = init_tri_values(nn_structure)
        avg_cost = 0
        mini_batches = get_mini_batches(X, y, bs)
        for mb in mini_batches:
            X_mb = mb[0]
            y_mb = mb[1]
            # pdb.set_trace()
            for i in range(len(y_mb)):
                delta = {}
                # perform the feed forward pass and return the stored h and z values, 
                # to be used in the gradient descent step
                h, z = feed_forward(X_mb[i, :], W, b)
                # loop from nl-1 to 1 backpropagating the errors
                for l in range(len(nn_structure), 0, -1):
                    if l == len(nn_structure):
                        delta[l] = calculate_out_layer_delta(y_mb[i,:], h[l], z[l])
                        avg_cost += np.linalg.norm((y_mb[i,:]-h[l]))
                    else:
                        if l > 1:
                            delta[l] = calculate_hidden_delta(delta[l+1], W[l], z[l])
                        # triW^(l) = triW^(l) + delta^(l+1) * transpose(h^(l))
                        tri_W[l] += np.dot(delta[l+1][:,np.newaxis], 
                                          np.transpose(h[l][:,np.newaxis])) 
                        # trib^(l) = trib^(l) + delta^(l+1)
                        tri_b[l] += delta[l+1]
            # perform the gradient descent step for the weights in each layer
            for l in range(len(nn_structure) - 1, 0, -1):
                W[l] += -alpha * (1.0/bs * tri_W[l] + lamb * W[l])
                b[l] += -alpha * (1.0/bs * tri_b[l])
        # complete the average cost calculation
        avg_cost = 1.0/m * avg_cost
        avg_cost_func.append(avg_cost)
        cnt += 1
    return W, b, avg_cost_func


def predict_y(W, b, X, n_layers):
    m = X.shape[0]
    y = np.zeros((m,))
    for i in range(m):
        h, z = feed_forward(X[i, :], W, b)
        y[i] = h[n_layers]
    return y


if __name__ == "__main__":
    # global setting
    
    # Make up some real data and input fitting template(s)
    x_data = np.linspace(-1, 1, 100)[:, np.newaxis]  # np.newaxis adds a new dimension to x_data
    fcn_1 = input_creator(x_data, 'square')
    fcn_2 = input_creator(x_data, 'exp')
    fcn_3 = input_creator(x_data, 'gauss')
    #fcn_1 = input_creator(x_data, 'order1_poly')
    #fcn_2 = input_creator(x_data, 'order1_poly')
    #fcn_3 = input_creator(x_data, 'order1_poly')
    
    input_template = np.concatenate((fcn_1, fcn_2, fcn_3), axis=1)
    #print input_template.shape
    num_templates = input_template.shape[1]
    
    noise = np.random.normal(0, 0.005, x_data.shape)  # noise has the same shape as x
    y_data = np.square(x_data) + 0.5 + noise  # y = x*x + 0.5 + noise
    #y_data = np.square(x_data)*np.sin(x_data) + 0.5 + noise  # y = x*x + 0.5 + noise
    #y_data = np.square(x_data)*x_data + 0.5 + noise  # y = x*x + 0.5 + noise

    # setup the NN structure
    nn_structure = [3, 10, 5, 1]
    #nn_structure = [3, 10, 5, 1]
    #nn_structure = [3, 5, 1]

    # train the NN
    W, b, avg_cost_func = train_nn(nn_structure, input_template, y_data, iter_num=10000, alpha=0.1)
    #W, b, avg_cost_func = train_nn_SGD(nn_structure, input_template, y_data, iter_num=10000, alpha=0.1, lamb=0.001)

    # prediction
    #plt.plot(x_data, y_data, 'b.')
    #plt.plot(x_data, predict_y(W, b, input_template, 3), 'r')
    print avg_cost_func[-1]
    plt.plot(avg_cost_func)
    plt.show()
