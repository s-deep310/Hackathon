import numpy as np
import pandas as pd
rng = np.random.default_rng(42)

# ----- basics: numeric + categorical -----
n = 2000
ages = rng.integers(18, 70, size=n)                      # uniform ints
income = rng.lognormal(mean=10.5, sigma=0.5, size=n)     # right-skewed
country = rng.choice(["US","IN","GB","DE"], size=n, p=[0.4,0.3,0.2,0.1])

# ----- relationships: make variables depend on others -----
# price depends on income (richer → higher spend) + noise
spend = (income * 0.015) + rng.normal(0, 20, size=n)
spend = np.clip(spend, 0, None)

# binary label with a probabilistic rule (logistic)
logit = -6 + 0.04*(ages) + 0.00006*(income) + 0.02*(spend) + 0.4*(country == "IN")
p_buy = 1 / (1 + np.exp(-logit))
bought = rng.binomial(1, p_buy)

# ----- sprinkle realism: missingness / outliers -----
mask_missing = rng.random(n) < 0.02
country = country.astype(object)
country[mask_missing] = None

spend[rng.random(n) < 0.01] *= 5  # 1% outliers

df = pd.DataFrame({
    "age": ages,
    "income": income.round(2),
    "country": country,
    "spend": spend.round(2),
    "bought": bought.astype(bool)
})
print(df.head())
