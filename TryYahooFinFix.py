from pandas_datareader import data as pdr
import datetime
import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

# download dataframe
today = datetime.date.today()
tlist = ["XLF", "XLK", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB"]
for t in tlist:
    file  = t + ".csv"
    data = pdr.get_data_yahoo(t, start="2017-01-01", end= today)
# download Panel
#data = pdr.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")
    data.to_csv(file, sep='\t')