#!/usr/bin/env python
import numpy as np
import pandas as pd


def guess(x, y, n_points):

    '''accepts x and y (array-like) and returns a grid 
    for the linear parameter space based on a crude guess'''


    slope0 = (max(y) - min(y)) / (max(x) - min(x))
    intercept0 = ((max(y)) + (min(y))) / 2.

    
    return slope0, intercept0


def grid_generator(slope, intercept, n_points, n_iteration):

    min_slope = (1 - (0.5**n_iteration) * slope)
    max_slope = (1 + (0.5**n_iteration) * slope)

    min_intercept = (1 - (0.5**n_iteration)) * intercept 
    max_intercept = (1 + (0.5**n_iteration)) * intercept

    slopespace = np.linspace(min_slope, max_slope, n_points)
    interspace = np.linspace(min_intercept, max_intercept, n_points)

    return slopespace, interspace

def lin_model(x, slope, intercept):

    '''accepts array-like x and numbers slope and intercept and returns array-like y
    using a linear model'''

    return slope * x + intercept

def one_d_chisq(y, y_predict, y_error):

    '''accepts three array-like arguments of data, model, and error data
    and computes chi squared'''

    return sum(((y - y_predict)/y_error)**2)

def chi_sq_generator(x, y, y_error, slopes, intercepts):

    chisq = float('inf')
    slope = 0
    intercept = 0

    for i in slopes:
        for j in intercepts:
            test_chisq = one_d_chisq(y,lin_model(x, i, j), y_error)
            if test_chisq < chisq:
                chisq = test_chisq
                slope = i
                intercept = j

    return chisq, i, j


def adaptive_generator(x, y, y_error, slope, intercept, chisq_array, tolerance, n_points, n_iteration):

    '''uses adaptive mesh refinement to obtain the 
    parameters to a user specificed tolerance in chisq'''

    grid = grid_generator(slope, intercept, n_points, n_iteration)

    state = chi_sq_generator(x,y,y_error,grid[0],grid[1])

    n_iteration += 1

    chisq_array[1] = chisq_array[0]

    chisq_array[0] = state[0]

    slope = state[1]

    intercept  = state[2]



    if abs(chisq_array[0] - chisq_array[1]) < tolerance:
        return state

    else:
        adaptive_generator(x,y,y_error,slope,intercept,chisq_array,tolerance,n_points,n_iteration)


if __name__ == '__main__':

    df = pd.read_csv('../../data/01_heights_weights_genders_errors.csv')

    heights = df['Height']
    weights = df['Weight']
    weight_err = df['Weight errors']

    state0 = guess(heights, weights, 1000)
    chisq_array = np.zeros(2)
    adaptive_generator(heights, weights, weight_err, state0[0], state0[1], chisq_array, 1e-4, 1000, 1)



