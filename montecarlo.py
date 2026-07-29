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
