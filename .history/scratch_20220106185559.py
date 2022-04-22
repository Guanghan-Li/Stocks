import yfinance as yf
amr = yf.Ticker("AMR")
print(amr.info)
GetFacebookInformation = yf.Ticker("AAPL")
print("Price Earnings Ratio : ", GetFacebookInformation.info['trailingPE'])
# # Import yfinance module  
# import yfinance as yahooFin  
# # Using ticker for the Facebook in yfinance function  
# retrFBInfo = yahooFin.Ticker("AAPL")  
# # Initializing variable for retrieving market prices  
# maxHisMP = retrFBInfo.history(period="4y")  
# # Printing the historical market prices in the output  
# print("Historical Market Prices data from the Facebook page financial data of Yahoo: ")  
# print(maxHisMP)  