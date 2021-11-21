import numpy as np
import pandas as pd
import math

# finite difference parameter definition ##

# parameter defn for P_i in i = 2,...,i_max-1 #

def difference(P, p_low, p_high, sigma, eta, mean):
    difference = np.zeros(2)
    a_i_central = (sigma**2)*(P**2)/((P - p_low)*(p_high - p_low)) - (eta*(mean - P))/(p_high - p_low)
    b_i_central = (sigma**2)*(P**2)/((p_high - P)*(p_high - p_low)) + (eta*(mean - P))/(p_high - p_low)
    a_i_forward = (sigma**2)*(P**2)/((P - p_low)*(p_high - p_low))
    b_i_forward = (sigma**2)*(P**2)/(p_high - P)*(p_high - p_low) + (eta*(mean - P))/(p_high - p_low)
    a_i_backward = (sigma**2)*(P**2)/((P - p_low)*(p_high - p_low)) - (eta*(mean - P))/(p_high - p_low)
    b_i_backward = (sigma**2)*(P**2)/((p_high - P)*(p_high - p_low))
    if a_i_central > 0:
        difference[0] = a_i_central
    else:
        difference[0] = a_i_forward
    if b_i_central > 0:
        difference[1] = b_i_central
    else:
        difference[1] = b_i_backward
    return (difference)


# parameter defn for P_i in i = 1 ##

def difference_min(P, p_step, eta, mean):
    a_i = 0
    b_i = eta * (mean - P) / (p_step)
    return [a_i, b_i]


# parameter defn for P_i in i = i_max ##

def difference_max(P, p_step, eta, mean):
    a_i = abs(eta * (mean - P) / (p_step))
    b_i = 0
    return [a_i, b_i]

class State:
    def __init__(self, mean, eta, lambda_switch, sigma):
        self.m = mean
        self.e = eta
        self.l = lambda_switch
        self.s = sigma
        
def Profit(E, P, vc, fc, pi_tax, c_tax):
    pi = ((E * (P - vc - c_tax)) - fc) * (1 - pi_tax)
    return pi