## bekk varma estimation ##

## load global data ##
global = 'https://raw.githubusercontent.com/joe-ascroft/phd/master/data/df_global_returns.csv'
df <- read.csv(global,header=T)
attach(df)
summary(df)
library(bmgarch)

## fit mgarch bekk model ## 

m1 <- bmgarch(df,parameterization="BEKK")
summary(m1)
m1.fc <- forecast(m1,ahead=10)
plot(m1.fc,type="mean")