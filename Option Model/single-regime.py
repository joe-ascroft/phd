import numpy as np
import pandas as pd
import math
import datetime as dt
import datapackage
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import multinomial
from typing import List
import seaborn as sns


# system characterisation

class State:
    def __init__(self, mean, eta, lambda_switch, sigma):
        self.m = mean
        self.e = eta
        self.l = lambda_switch
        self.s = sigma


M = 2
N = 2

state_1 = State(4, 0.1, 0.1, 0.05)


def Profit(E, P, vc, fc, pi_tax, c_tax):
    pi = ((E * (P - vc - c_tax)) - fc) * (1 - pi_tax)
    return pi


T = 2
E = 2000
r = 0.0125
vc = 1
fc = 200
pi_tax = 0.2
c_tax = 0.4

switch = (0.2, 0.6)

# finite difference parameter definition ##

# parameter defn for P_i in i = 2,...,i_max-1 #

def difference(P, p_step, sigma, eta, mean):
    difference = np.zeros(2)
    a_i_central = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step) - eta * (mean - P) / (p_step * 2)
    b_i_central = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step) - eta * (mean - P) / (p_step * 2)
    a_i_forward = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step)
    b_i_forward = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step) - eta * (mean - P) / (p_step * 2)
    a_i_backward = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step) - eta * (mean - P) / (p_step * 2)
    b_i_backward = (sigma ** 2) * (P ** 2) / ((p_step * 2) * p_step)
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
    a_i = eta * (mean - P) / (p_step)
    b_i = 0
    return [a_i, b_i]


# lattice parameters ##

p_step = 1
s0_step = 100000

p_1 = 0.5
p_max = 8
p_steps = int((p_max - p_1) / p_step)

s0_1 = 100000
s0_max = 500000

# lattice construction ##

P_grid_lower = list(range(5, 40, p_steps))
P_grid_middle = list(range(41, 66, 1))
P_grid_upper = list(range(68, 80, 2))
P_grid_high = list(range(85, 110, 5))
P_grid_vhigh = list(range(120, 160, 10))

P_grid = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 11]

s0_grid = list(range(s0_1, s0_max, s0_step))

temp_node = np.full((len(P_grid), len(s0_grid), M, N), 0)
node_value = np.full((len(P_grid), len(s0_grid), M, N), 0)
Lv = np.full((len(P_grid), len(s0_grid), M, N), 0)

# here we store the optimal state n in N conditional on prior state m in M ##

temp_path = np.full((len(P_grid), len(s0_grid), M), 0)
opt_path = []

cost = np.zeros((2, 2))
temp_compare = np.zeros((2))

cost[0, 0] = 0
cost[1, 0] = 2000
cost[1, 1] = 0
cost[0, 1] = 2000

for t in range(20):
    for q in range(4):

## M refers to adjacent state, N refers to current state ##

## Quarterly profit at each node ##

        for i in range(len(P_grid)):
            for k in range(len(s0_grid)):
                for m in range(M):
                    for n in range(N):
                        if n == 1:
                            if (120 - (t*4 + q))*E < s0_grid[k]:
                                temp_node[i,k,m,n] = temp_node[i,k,m,n] + Profit(E,P_grid[i],vc,fc,pi_tax,c_tax)
                            else:
                                temp_node[i,k,m,n] = temp_node[i,k,m,n] - fc
                        else:
                            temp_node[i,k,m,n] = temp_node[i,k,m,n] - fc

## Lagrange Differential at each node ##

## then we loop over lagrange differential for nodes inside the boundary ##

        for i in range(1,len(P_grid) - 1):
            for k in range(len(s0_grid)):
                for m in range(M):
                    for n in range(N):
                        diff = difference(P_grid[i],p_step,state_1.s,state_1.e,state_1.m)
                        Lv[i,k,m,n] = diff[0]*temp_node[i - 1,k,m,n] + diff[1]*temp_node[i + 1,k,m,n] - (diff[0]+diff[1]+r)*temp_node[i,k,m,n]

## we loop over Lagrange differential for boundary nodes ##

        for k in range(len(s0_grid)):
            for m in range(M):
                for n in range(N):
                    diff = difference_min(P_grid[0],(P_grid[1]-P_grid[0]),state_1.e,state_1.m)
                    Lv[0,k,m,n] = diff[1]*temp_node[1,k,m,n] - (diff[1]+r)*temp_node[0,k,m,n]

        for k in range(len(s0_grid)):
            for m in range(M):
                for n in range(N):
                    diff = difference_max(P_grid[len(P_grid)-1],(P_grid[len(P_grid)-1]-P_grid[len(P_grid)-2]),state_1.e,state_1.m)
                    Lv[len(P_grid) - 1,k,m,n] = diff[0]*temp_node[len(P_grid)-2,k,m,n] - (diff[0]+r)*temp_node[len(P_grid)-1,k,m,n]

## then we apply Lv to temporary node values ##
        for i in range(len(P_grid)):
            for k in range(len(s0_grid)):
                for m in range(M):
                    for n in range(N):
                        temp_node[i,k,m,n] = temp_node[i,k,m,n] + Lv[i,k,m,n]


## we apply conditional costs on each state ##

    for i in range(len(P_grid)):
        for k in range(len(s0_grid)):
            for m in range(M):
                for n in range(N):
                    temp_node[i,k,m,n] = temp_node[i,k,m,n] - cost[m,n]

## we identify the optimal conditional state n in N for every adjacent state m in M ##

    for i in range(len(P_grid)):
        for k in range(len(s0_grid)):
            for m in range(M):
                for n in range(N):
                    temp_compare[n] = temp_node[i,k,m,n]
                temp_path[i,k,m] = np.argmax(temp_compare)

## we for the next cycle, we adjust option value ##

    for i in range(len(P_grid)):
        for k in range(len(s0_grid)):
            for m in range(M):
                for n in range(N):
                    node_value[i,k,m,n] = temp_node[i,k,m,(temp_path[i,k,m])]
                    temp_node[i,k,m,n] = node_value[i,k,m,n]



