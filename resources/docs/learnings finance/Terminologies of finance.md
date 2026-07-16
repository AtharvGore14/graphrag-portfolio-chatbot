### What is Normal and Log Returns ?
>Normal returns represent simple percentage price change, while log returns measure continuously compounded returns and are preferred for statistical and financial modeling.>
---
### Formula for Daily Normal Return
>Daily Normal Return = (Today Close-Yesterday Close)/Yesterday close
### Formula for Daily Log Return
>Daily Log Return = Log(Today's Close/Yesterday's Close)
---
### Formula for Annualised Return
There are approximately **252 trading days in a year**.

Log returns are additive.
So:
Daily average × number of days = yearly return
### formula
>=AVERAGE(F3:F1000)*252

That gives the **annualized log return**.

---
### Annualised Volatility
Volatility is just **standard deviation of daily returns**

---
## What is Alpha in the Stock Market?
The extra return that a stock earns over its expected return after accounting for random variations and volatility associated with the market is represented by alpha, a standard calculating metric. Put more simply, it's a measurement of the stock's performance in relation to its benchmark index. Alpha measures how much a specific stock has done better or worse than its predicted performance, given its risk in the stock market.

For a stock, the alpha figure is marked as a single number, such as 5 or -7. This number, however, represents the percentage above or below the market index achieved by the stock or fund price. A positive alpha suggests that a stock has outperformed its expected return. A negative alpha, on the other hand, indicates underperformance. For example, if the alpha is 1.0, it means that the stock or investment has outdone its benchmark by 1%. And if the alpha is -1.0, it indicates that by 1%, the investment had fallen short of its benchmark index.

---
# **Alpha**, **Beta**, and **R² (R-squared)**.

## 🔵 Beta (β) — Market Sensitivity

Beta measures **how much a stock moves compared to the market**.

Think of the market as the ocean. 🌊  
Beta tells you how wild your boat behaves when waves rise.

- **Beta = 1** → Moves exactly like the market
    
- **Beta > 1** → More volatile than the market
    
- **Beta < 1** → Less volatile than the market
    
- **Beta < 0** → Moves opposite to the market
    

### Example:

If NIFTY goes up 1%:

- Beta 1.5 stock → goes up ~1.5%
    
- Beta 0.5 stock → goes up ~0.5%
    

So beta = **risk relative to the market**.

If you're analyzing Indian stocks like TCS or HDFCBANK against NIFTY, beta tells you who’s the drama king and who’s the calm monk.

---
# Doubt
##### Since NIFTY is composed of individual stocks, and each stock contributes to the index value, doesn’t a stock’s volatility influence NIFTY rather than NIFTY influencing the stock?
##### If that is true, why do we model Beta as the stock responding to the market, instead of the market responding to the stock?
### Answer 


---

## 🟢 Alpha (α) — Extra Return

Alpha is the **extra return beyond what beta predicts**.

If beta explains how much return you _should_ get given the risk,  
alpha tells you whether you **beat expectations**.

Formula idea:

Expected Return = Risk-Free Rate + Beta × (Market Return − Risk-Free Rate)

Alpha = Actual Return − Expected Return

- **Positive alpha** → Outperformed
    
- **Negative alpha** → Underperformed
    
- **Zero alpha** → Performed exactly as predicted
    

If beta is the script, alpha is the improvisation. 🎭

---

## 🟡 R-squared (R²) — Reliability Score

R² tells you **how well beta explains the stock’s movement**.

It ranges from 0 to 1 (or 0% to 100%).

- **R² = 0.90 (90%)** → 90% of stock movement is explained by market movement
    
- **R² = 0.30 (30%)** → Market explains very little; stock moves independently
    

High R² = Beta is meaningful  
Low R² = Beta is shaky, like predicting Mumbai rain in April ☁️

---

## 📊 Quick Summary Table

|Metric|Meaning|What It Tells You|
|---|---|---|
|Beta|Market sensitivity|How risky vs market|
|Alpha|Excess return|Skill or underperformance|
|R²|Explanation power|How reliable beta is|

---

## 🧠 In One Line Each

- **Beta** = How much you shake when the market shakes
    
- **Alpha** = How much you outperform after accounting for risk
    
- **R²** = How trustworthy that relationship is
    

---

Since you’re working with yfinance and portfolio optimization, next step would be:  
👉 Compute beta of BEL, M&M, ITC vs NIFTY  
👉 Then check alpha  
👉 Then verify R² before trusting beta

If you want, I can give you a clean Python script to calculate all three using regression.