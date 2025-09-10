# import numpy as np
# import math
# Inspired by QuantPy

def binomial_options_pricing_model(K,T,S0,r,N,u,d,opttype='P'):

    dt = T/N
    q = (np.exp(r*dt) - d)/(u-d)
    disc = np.exp(-r*dt)

    # initialise stock prices at maturity
    S = S0 * d**(np.arange(N,-1,-1)) * u**(np.arange(0,N+1,1))

    # option payoff
    if opttype == 'P':
        C = np.maximum(0, K - S)
    else:
        C = np.maximum(0, S - K)

    # backward recursion through the tree
    for i in np.arange(N-1,-1,-1):
        S = S0 * d**(np.arange(i,-1,-1)) * u**(np.arange(0,i+1,1))
        C[:i+1] = disc * ( q*C[1:i+2] + (1-q)*C[0:i+1] )
        C = C[:-1]
        if opttype == 'P':
            C = np.maximum(C, K - S)
        else:
            C = np.maximum(C, S - K)

    return C[0]


# print(binomial_options_pricing_model(100,1,100,0.05,3,1.122,0.892,opttype='C'))


# def Bjerksund_Stensland_model(call_put,stock_price,strike_price,risk_free_intrest_rate,time_to_expiry,Volatility,cost_to_carry):
#     if cost_to_carry>= risk_free_intrest_rate:
#         return black_scholes_model(call_put,stock_price,strike_price,risk_free_intrest_rate,time_to_expiry,Volatility,cost_to_carry)    
#     if call_put == "c":
#        Beta = (1/2-cost_to_carry/Volatility**2)+ math.sqrt((cost_to_carry/Volatility**2-1/2)**2 +2 * risk_free_intrest_rate/Volatility**2)
#        Binfinity = Beta/(Beta-1)*strike_price
#        B0 = max(strike_price,risk_free_intrest_rate/(risk_free_intrest_rate-cost_to_carry)*strike_price)
#        ht = -(cost_to_carry*time_to_expiry+2*Volatility*math.sqrt(time_to_expiry)*B0/(Binfinity-B0))
#        I = B0 + (Binfinity-B0)*(1- math.exp(ht))
#        Alpha = (I-strike_price)*I**(-Beta)
#        if stock_price >= I:
#                 call_apporximation = stock_price-strike_price
#                 return call_apporximation
#        else:
#            American_call_app = Alpha* stock_price**Beta - Alpha * phi(stock_price,time_to_expiry,0,strike_price,I,risk_free_intrest_rate,cost_to_carry,Volatility)+ phi(stock_price,time_to_expiry,0,strike_price,I,risk_free_intrest_rate,cost_to_carry,Volatility) - phi(stock_price,time_to_expiry,0,strike_price,I,risk_free_intrest_rate,cost_to_carry,Volatility) - strike_price * phi(stock_price,time_to_expiry,0,strike_price,I,risk_free_intrest_rate,cost_to_carry,Volatility) + strike_price* phi(stock_price,time_to_expiry,0,strike_price,I,risk_free_intrest_rate,cost_to_carry,Volatility)
#            return American_call_app
#     elif call_put == "p":
#         American_put_app = Bjerksund_Stensland_model(call_put, strike_price, stock_price, (risk_free_intrest_rate - cost_to_carry),time_to_expiry,Volatility,-cost_to_carry,)
#         return American_put_app

       
#     else:
#         return print("error input c for call or p for put")
        


# def phi(S,T,gamma,H,I,r,b,v):
#     lam= (-r+gamma*b+0.5*gamma*(gamma-1)*v**2)*T
#     d = -(math.log(S/H)+(b+(gamma-0.5)*v**2)*T)/(v*math.sqrt(T))
#     kappa = 2*b/(v**2)+(2*gamma-1)
#     phight = math.exp(lam)*S**gamma*(cumulative_normal_distribution(d)-(I/S)**kappa* 
#     cumulative_normal_distribution(d-2* math.log(I/S)/(v*math.sqrt(T))))

#     return phight
    
# ## General Black Scholes model because the incorperation of cost of carry

# def Black_Scholes_model(call_put,stock_price,strike_price,risk_free_intrest_rate,time_to_expiry,Volatility,cost_to_carry):
#     d1 = math.log(stock_price/strike_price)+((cost_to_carry+Volatility**2/2)*time_to_expiry)/(Volatility*math.sqrt(time_to_expiry))
#     d2 = d1 - Volatility*math.sqrt(time_to_expiry)

#     if call_put == "c":
#         Black_Scholes = stock_price*math.exp((cost_to_carry-risk_free_intrest_rate)*time_to_expiry)*cumulative_normal_distribution_function(d1)- strike_price*math.exp(-risk_free_intrest_rate*time_to_expiry)*cumulative_normal_distribution_function(d2)
#     elif call_put == "p":
#         Black_Scholes = strike_price*math.exp(-risk_free_intrest_rate*time_to_expiry)*cumulative_normal_distribution_function(-d2)- strike_price * math.exp((cost_to_carry-risk_free_intrest_rate)*time_to_expiry) *cumulative_normal_distribution_function(-d1)

#     else:
#         return print("error")
    
#     return Black_Scholes


# def cumulative_normal_distribution_function(x):
#     a1=0.31938153
#     a2 = -0.356563782
#     a3=1.781477937
#     a4=-1.821255978
#     a5=1.330274429
#     L=abs(x)
#     k= 1/(1+0.2316419*L)
    
#     cnd = 1-(1/math.sqrt(2*math.pi)*math.exp(-L**2)/2)*(a1*k+a2*k**2+a3*k**3+a4*k**4+a5*k**5)
#     if x < 0:
#         cnd = 1- cnd
    
#     return cnd




# print(Black_Scholes_model("p",75,70,0.1,0.5,0.35,0.05))
# # def Black_Scholes_model(call_put,stock_price,strike_price,risk_free_intrest_rate,time_to_expiry,Volatility,cost_to_carry):




# import math

# def black_scholes_model(option_type, stock_price, strike_price, risk_free_interest_rate, time_to_expiry, volatility, cost_to_carry):
#     d1 = (math.log(stock_price / strike_price) + (cost_to_carry + volatility**2 / 2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
#     d2 = d1 - volatility * math.sqrt(time_to_expiry)

#     if option_type.lower() == "c":
#         price = (stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) * cumulative_normal_distribution(d1) 
#                  - strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) * cumulative_normal_distribution(d2))
#     elif option_type.lower() == "p":
#         price = (strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) * cumulative_normal_distribution(-d2) 
#                  - stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) * cumulative_normal_distribution(-d1))
#     else:
#         raise ValueError("Invalid option type. Use 'c' for call or 'p' for put.")
    
#     return price

# def cumulative_normal_distribution(x):
#     a1, a2, a3, a4, a5 = 0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429
#     L = abs(x)
#     k = 1 / (1 + 0.2316419 * L)
    
#     cnd = 1 - (1 / math.sqrt(2 * math.pi)) * math.exp(-L**2 / 2) * (a1*k + a2*k**2 + a3*k**3 + a4*k**4 + a5*k**5)
    
#     return cnd if x >= 0 else 1 - cnd

# # Example usage
# try:
#     result = black_scholes_model("c",75,70,0.1,0.5,0.35,0.05)

#     print(f"Option price: {result:.4f}")
# except ValueError as e:
#     print(f"Error: {e}")




# print(Bjerksund_Stensland_model("c",42,40,0.04,0.75,0.35,-0.04))





import math
from scipy.stats import norm

def cumulative_normal_distribution(x):
    return norm.cdf(x)

def black_scholes_model(call_put, stock_price, strike_price, risk_free_interest_rate, time_to_expiry, volatility, cost_to_carry):
    d1 = (math.log(stock_price / strike_price) + (cost_to_carry + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - volatility * math.sqrt(time_to_expiry)
    
    if call_put == "c":
        price = stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) * cumulative_normal_distribution(d1) - strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) * cumulative_normal_distribution(d2)
    elif call_put == "p":
        price = strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) * cumulative_normal_distribution(-d2) - stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) * cumulative_normal_distribution(-d1)
    
    return price

def phi(S, T, gamma, H, I, r, b, v):
    lam = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * v**2) * T
    d = -(math.log(S / H) + (b + (gamma - 0.5) * v**2) * T) / (v * math.sqrt(T))
    kappa = 2 * b / (v**2) + (2 * gamma - 1)
    return math.exp(lam) * S**gamma * (cumulative_normal_distribution(d) - (I / S)**kappa * cumulative_normal_distribution(d - 2 * math.log(I / S) / (v * math.sqrt(T))))

def Bjerksund_Stensland_model(call_put, stock_price, strike_price, risk_free_interest_rate, time_to_expiry, volatility, cost_to_carry):
    if cost_to_carry >= risk_free_interest_rate:
        return black_scholes_model(call_put, stock_price, strike_price, risk_free_interest_rate, time_to_expiry, volatility, cost_to_carry)
    
    if call_put == "c":
        Beta = (1/2 - cost_to_carry / volatility**2) + math.sqrt((cost_to_carry / volatility**2 - 1/2)**2 + 2 * risk_free_interest_rate / volatility**2)
        Binfinity = Beta / (Beta - 1) * strike_price
        B0 = max(strike_price, risk_free_interest_rate / (risk_free_interest_rate - cost_to_carry) * strike_price)
        ht = -(cost_to_carry * time_to_expiry + 2 * volatility * math.sqrt(time_to_expiry)) * B0 / (Binfinity - B0)
        I = B0 + (Binfinity - B0) * (1 - math.exp(ht))
        Alpha = (I - strike_price) * I**(-Beta)
        
        if stock_price >= I:
            return stock_price - strike_price
        else:
            return (Alpha * stock_price**Beta 
                    - Alpha * phi(stock_price, time_to_expiry, Beta, I, I, risk_free_interest_rate, cost_to_carry, volatility)
                    + phi(stock_price, time_to_expiry, 1, I, I, risk_free_interest_rate, cost_to_carry, volatility)
                    - phi(stock_price, time_to_expiry, 1, strike_price, I, risk_free_interest_rate, cost_to_carry, volatility)
                    - strike_price * phi(stock_price, time_to_expiry, 0, I, I, risk_free_interest_rate, cost_to_carry, volatility)
                    + strike_price * phi(stock_price, time_to_expiry, 0, strike_price, I, risk_free_interest_rate, cost_to_carry, volatility))
    
    elif call_put == "p":
        return Bjerksund_Stensland_model("c", strike_price, stock_price, risk_free_interest_rate - cost_to_carry, time_to_expiry, volatility, -cost_to_carry)
    
    else:
        raise ValueError("Invalid input: use 'c' for call or 'p' for put")

result = Bjerksund_Stensland_model("c", 42, 40, 0.04, 0.75, 0.35, -0.04)

print(f"Option price: {result}")
