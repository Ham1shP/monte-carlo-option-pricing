import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
# Here I am pricing a European call, and then checking it against Black-Scholes

# S0: The initial price of the stock
# r: The risk-free rate
# sigma: The volatility of the stock
# T: The time to expiry/maturity
# Z: Standard normal random variable

def euro_call(S0, K, r, sigma, T, N):
    Z = np.random.normal(0, 1, N) #Generates N standard normal random variables
    S_t = S0*np.exp((r - 0.5*sigma**2)*T + sigma*Z*np.sqrt(T)) #Calculates the price on expiry of all N simulations
    payoff = np.maximum(S_t - K, 0) #Calculates the payoff for each simulation
    return np.exp(-r*T)*np.mean(payoff) #Discounts the mean payoff
# Uses the geometric Brownian motion model to find the price of a European call option via Monte Carlo simulation.
    

# Uses the Black-Scholes formula to verify the Monte Carlo numerical method used above
def black_scholes_euro_call(S0, K, r, sigma, T):
    d1 = (np.log(S0/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    N = norm.cdf
    return S0*N(d1) - K*np.exp(-r*T)*N(d2)

x = np.linspace(50, 150, 10)
y = np.array([euro_call(100, k, 0.05, 0.2, 1, 100000) for k in x])
plt.plot(x, y, label = 'Monte Carlo Simulation')
plt.xlabel('Strike Price')
plt.ylabel('Option Price')
plt.legend()
plt.savefig('option_price_vs_strike_price.png', dpi = 150, bbox_inches = 'tight')
plt.show()
#This all plots the option price against the strike price using the Monte Carlo method.

#Now to create a 95% confidence interval. 
def confidence_interval(S0, K, r, sigma, T, N):
    Z = np.random.normal(0, 1, N) #Generates N standard normal variables. 
    S_t = S0*np.exp((r - 0.5*sigma**2)*T + sigma*Z*np.sqrt(T)) #Calculates the price on expiry.
    payoff = np.exp(-r*T)*np.maximum(S_t - K, 0) #Calculates discounted payoff.
    price = np.mean(payoff) #Calculates the option price as mean payoff.
    se = np.std(payoff, ddof=1)/np.sqrt(N) #Calculates sample standard error of the payoff.
    low, high = price - 1.96*se, price + 1.96*se #Calculates the limits for a 95% confidence interval. 
    return price, se, (low, high)

#Now we want to plot the error against N.
N_values = [10**k for k in range(2,7)]
ses = [confidence_interval(100, 100, 0.05, 0.2, 1, N)[1] for N in N_values]
plt.plot(N_values, ses, label = 'Standard Error')
plt.xlabel('Number of simulations')
plt.ylabel('Standard error')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.savefig('standard_error_vs_simulations.png', dpi = 150, bbox_inches = 'tight')
plt.show()

#Now to check if our confidence interval is right.
blackscholesprice = black_scholes_euro_call(100, 100, 0.05, 0.2, 1)
a = 0
b = 500
for i in range(b):
    price, se, (low, high) = confidence_interval(100, 100, 0.05, 0.2, 1, 10000)
    if low <= blackscholesprice <= high: #Tests if the Black-Scholes answer is in our confidence interval.
        a += 1
print(a/b) #We would expect this to be around 0.95.