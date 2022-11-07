from nsepy import get_history as gh
from datetime import datetime, timedelta

tickers = 'TCS'

start = datetime.today() - timedelta(days=10)
end = datetime.today() - timedelta(days=2)

data = gh(symbol=tickers,start=start,end=end)

print(data)