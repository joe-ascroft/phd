## pi_tax => corporate rate, c_tax => carbon tax ##

def profit_t(E,P,vc,fc,pi_tax,c_tax):
    pi = ((E*(P-vc-c_tax))-fc)*(1-pi_tax)
    return pi

## T => days of extraction remaining, r => effective daily interest rate ##

def value_simple(T,r,pi):
    v = pi*(math.exp(-r*T))*(1/r)
    return v


## differencing defns ##

a_i_central = (sigma**2)*(P**2)/((p_step*2)*p_step) - eta*(mean-P)/(p_step*2)
b_i_central = (sigma**2)*(P**2)/((p_step*2)*p_step) - eta*(mean-P)/(p_step*2)

## forward differencing ##

a_i_forward = (sigma**2)*(P**2)/((p_step*2)*p_step)
b_i_forward = (sigma**2)*(P**2)/((p_step*2)*p_step) - eta*(mean-P)/(p_step*2)

## backward differencing ##

a_i_backward = (sigma**2)*(P**2)/((p_step*2)*p_step) - eta*(mean-P)/(p_step*2)
b_i_backward = (sigma**2)*(P**2)/((p_step*2)*p_step)

