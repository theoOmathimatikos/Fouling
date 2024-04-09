import numpy as np


def double_data(data, data_gr, a_max):

    max_t, max_y = data_gr[-1, :]
    
    if max_y < a_max:
        rand_noize = np.abs(np.random.normal(0, 1))*(100-max_y)
        rand_noize *= (data[0, 0] + data[-1, 0])/data.shape[0]
        max_t += rand_noize

    double_data = np.copy(data_gr)
    double_data[:, 0] = 2*max_t - data_gr[:, 0]

    return np.concatenate((data_gr, double_data[::-1]), axis=0)