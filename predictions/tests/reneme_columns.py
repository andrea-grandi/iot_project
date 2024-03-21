import pandas as pd  

df = pd.read_csv("dataset.csv")

df.rename(columns={'Date': 'ds'}, inplace=True)
df.rename(columns={'Volume': 'y'}, inplace=True)

df.to_csv("dataset.csv", index=False)
