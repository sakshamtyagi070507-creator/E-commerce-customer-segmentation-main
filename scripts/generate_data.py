"""Generate a SYNTHETIC e-commerce customer dataset for learning purposes.
No real customer data is used. Run: python scripts/generate_data.py"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
n = 500
# Hidden customer types (used only to generate realistic data; the analysis must discover them)
kind = rng.choice(['loyal','big','new','sleeping','casual'], n, p=[.18,.10,.20,.22,.30])
P = {  # recency mean/sd, orders mean/sd, avg order value mean/sd
 'loyal':   (15, 10, 22, 6, 1100, 250),
 'big':     (25, 15, 12, 4, 3500, 700),
 'new':     (12, 8,  2, 1,  900, 300),
 'sleeping':(200,60, 6, 3, 1000, 300),
 'casual':  (70, 30, 5, 2,  850, 250)}
rec, orders, aov = [], [], []
for k in kind:
    r, ro, o, oo, a, ao = P[k]
    rec.append(max(1, rng.normal(r, ro))); orders.append(max(1, round(rng.normal(o, oo)))); aov.append(max(150, rng.normal(a, ao)))
rec = np.round(rec); orders = np.array(orders); aov = np.array(aov)
spend = (orders * aov).round(0)
df = pd.DataFrame({
 'Customer_ID': [f'C{10001+i}' for i in range(n)],
 'Gender': rng.choice(['Male','Female'], n, p=[.48,.52]),
 'Age': np.clip(rng.normal(32, 9, n), 18, 65).round(0),
 'City_Tier': rng.choice(['Tier 1','Tier 2','Tier 3'], n, p=[.45,.35,.20]),
 'Preferred_Device': rng.choice(['Mobile','Desktop','Tablet'], n, p=[.68,.27,.05]),
 'Acquisition_Channel': rng.choice(['Organic','Paid Ads','Social Media','Referral','Email'], n, p=[.30,.25,.20,.15,.10]),
 'Last_Purchase_Days_Ago': rec,
 'Total_Orders': orders,
 'Total_Spend': spend,
 'Discount_Orders_Pct': np.clip(rng.normal(35, 18, n), 0, 100).round(1),
 'Return_Rate_Pct': np.clip(rng.normal(8, 6, n), 0, 60).round(1),
 'Avg_Rating_Given': np.clip(rng.normal(4.0, 0.6, n), 1, 5).round(1)})
# Realistic data-quality problems for the cleaning exercise
for col, k in [('Age',8),('Last_Purchase_Days_Ago',5),('Discount_Orders_Pct',6),('Avg_Rating_Given',10)]:
    df.loc[rng.choice(n, k, replace=False), col] = np.nan
df.loc[11,'Total_Spend'] = -2500.0            # impossible value
df.loc[40,'Age'] = 150.0                       # impossible value
df.loc[[30,90],'Gender'] = ['male','FEMALE']   # inconsistent text
df.loc[[55,120],'City_Tier'] = ['tier 1',' Tier 2 ']
df = pd.concat([df, df.sample(8, random_state=1)], ignore_index=True)   # 8 duplicate rows
df.to_csv('data/raw/ecommerce_customers.csv', index=False)
print(df.shape)
