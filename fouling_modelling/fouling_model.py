import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import math

from utils import double_data


class BiofoulingGrowth():


    def __init__(self, data, fouling_type, solution="analytic"):
        """
        `data` come in the form of a Nx2 numpy array. Each element is a tuple (t, y(t))
        """
        self.data_gr, _ = data
        self.data = np.concatenate(data, axis=0)

        self.bf_type_to_rate = {"A": 100, "B": 50, "C": 20}
        self.a_max = self.bf_type_to_rate[fouling_type]

        if solution == "analytic":   
            self.analytic_solution()
        else:
            self.optimization_solution()

    
    def biofouling_growth(self, batch, t_0, sigma):

        mask, exp_fun = (batch <= t_0), np.exp(-((batch-t_0)/sigma)**2)
        bf_growth = self.a_max * exp_fun * mask + self.a_max * (1 - mask)
        
        return bf_growth


    def analytic_solution(self, plot=True):

        data = double_data(self.data, self.data_gr, self.a_max)
        mean_val = np.mean(data[:, 0])

        frac_up = np.sum((data[:, 0] - mean_val)**4)
        frac_down = np.sum(np.log(data[:, 1])*((data[:, 0] - mean_val)**2))
        std = np.sqrt(frac_up / frac_down)

        if plot:
            self.plot(mean_val, std)
        else:
            print(f"The mean value of the left-normal distribution is: {mean_val}")
            print(f"The standard deviation of the left-normal distribution is: {std}")
    

    def optimization_solution(self, plot=True):

        mean, std = self.optimize_parameters()

        if plot:
            self.plot(mean, std)
        else:
            print(f"The mean value of the left-normal distribution is: {mean}")
            print(f"The standard deviation of the left-normal distribution is: {std}")
    

    def loss(self, t_0, sigma):

        res = self.data[:, 1] - self.biofouling_growth(self.data[:, 0], t_0, sigma)
        return np.sum(res**2)
    

    def optimize_parameters(self):
        
        init_t_0 = np.mean(self.data[:, 0])
        init_sigma = 1

        initial_params = [init_t_0, init_sigma]
        opt = minimize(self.loss, initial_params, args=(self.data[:, 0], self.data[:, 1]))

        return opt.x
    
        
    def plot(self, mean, sigma):

        x = np.arange(0, math.ceil(self.data[-1, 0]/100)*100, 10)

        plt.scatter(self.data[:, 0], self.data[:, 1], label="data")
        plt.plot(x, self.biofouling_growth(x, mean, sigma), label="normal")
        
        plt.legend()
        plt.show()


if __name__ == "__main__":

    equatorial_type_A_gr = np.array([[5, 0.1], [113, 30], [166, 30], [172, 30], [223, 30], [230, 75], [280, 75], [335, 75], [390, 100], [445, 100]])
    equatorial_type_A_st = np.array([[505, 100], [565, 100], [615, 100], [665, 100]])
    equatorial_type_A = [equatorial_type_A_gr, equatorial_type_A_st]

    eq_type_a = BiofoulingGrowth(equatorial_type_A, "A")




