
import pandas as pd

url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

data = pd.DataFrame()

data = pd.read_csv(url)

data.to_csv("D:/Programming/Stockfolio/EQUITY_L.csv")
