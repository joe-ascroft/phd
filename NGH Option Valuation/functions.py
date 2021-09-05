## pi_tax => corporate rate, c_tax => carbon tax ##

def profit_t(E,Pt,vc,fc,pi_tax,c_tax):
    pi = ((E*(Pt-vc-c_tax))-fc)*(1-pi_tax)
    return pi

## T => days of extraction remaining, r => effective daily interest rate ##

def value_simple(T,r,pi):
    v = pi*(math.exp(-r*T))*(1/r)
    return v
