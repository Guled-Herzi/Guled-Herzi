import math

def cumulative_normal_distribution_function(x: float) -> float:
    a1 = 0.31938153
    a2 = -0.356563782
    a3 = 1.781477937
    a4 = -1.821255978
    a5 = 1.330274429

    L = abs(x)
    k = 1 / (1 + 0.2316419 * L)

    cnd = 1 - (1 / math.sqrt(2 * math.pi) * math.exp(-L ** 2 / 2)) * (
        a1 * k + a2 * k ** 2 + a3 * k ** 3 + a4 * k ** 4 + a5 * k ** 5
    )

    if x < 0:
        cnd = 1 - cnd

    return cnd


def black_scholes_model(call_put: str, stock_price: float, strike_price: float,
                        risk_free_interest_rate: float, time_to_expiry: float,
                        volatility: float, cost_to_carry: float) -> float:
    d1 = (math.log(stock_price / strike_price) +
          (cost_to_carry + volatility ** 2 / 2) * time_to_expiry) / \
         (volatility * math.sqrt(time_to_expiry))

    d2 = d1 - volatility * math.sqrt(time_to_expiry)

    if call_put.lower() == "c":
        return (stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) *
                cumulative_normal_distribution_function(d1) -
                strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) *
                cumulative_normal_distribution_function(d2))
    elif call_put.lower() == "p":
        return (strike_price * math.exp(-risk_free_interest_rate * time_to_expiry) *
                cumulative_normal_distribution_function(-d2) -
                stock_price * math.exp((cost_to_carry - risk_free_interest_rate) * time_to_expiry) *
                cumulative_normal_distribution_function(-d1))
    else:
        print("Error: call_put must be 'c' or 'p'")
        return 0.0


if __name__ == "__main__":
    # Test the Black-Scholes model with example values
    call_put = "c"   # "c" for call option, "p" for put option
    stock_price = 100
    strike_price = 95
    risk_free_interest_rate = 0.05
    time_to_expiry = 1
    volatility = 0.2
    cost_to_carry = 0.05

    result = black_scholes_model(call_put, stock_price, strike_price,
                                  risk_free_interest_rate, time_to_expiry,
                                  volatility, cost_to_carry)

    print("Black-Scholes result:", result)
