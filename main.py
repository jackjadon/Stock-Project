import yfinance as yf
import time
import smtplib

#Global constant variables
EMAIL = "bobmar123789@gmail.com"
PASSWORD = "ngvd mryb zsbt hjwg"
PHONE_NUMBER = "3104903655"
CARRIER = "@vtext.com"
STOCK_CODES = ["TSLA", "AAPL", "AMZN", "GOOGL", "NVDA", "NFLX", "DIS", "MSFT", "CCL", "AAL", "BAC", "F", "LCID", "CMG", "DAL","UNH", "EMR", "UBER", "SMCI", "INTC"]
TIME_ELAPSED = 10
DATA_RANGE = 60

#Initializes stock_data to be a 2D array
stock_data = []
for i in range(0, len(STOCK_CODES)):
    stock_data.append([])

def send_message(message):
    recipient = PHONE_NUMBER + CARRIER
    auth = (EMAIL, PASSWORD)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)

#Recursively finds the sum of the rates of change between 5 minutes intervals
def sumRateOfChange(arr, index):
    #if the index goes back further than 60 minutes ago, we stop
  if index <= len(arr) - DATA_RANGE:
        return (arr[index] - arr[index - TIME_ELAPSED])/arr[index-TIME_ELAPSED]

  return sumRateOfChange(arr, index - 1) + (arr[index] - arr[index - TIME_ELAPSED])/arr[index-TIME_ELAPSED]

#Checks the rate of change over the past 5 minutes against the average rate of change for today
def checkRateofChange(arr):
    avgRateofChange = sumRateOfChange(arr, len(arr) - 1)/DATA_RANGE
    currRateofChange = (arr[-1] - arr[-1 - TIME_ELAPSED])/arr[-1 - TIME_ELAPSED]

    if avgRateofChange != 0:  
      percentDiff = (currRateofChange-avgRateofChange)/avgRateofChange
      percentDiff *= 100

    if percentDiff > 1000 or percentDiff < -1000:
        print("PING")

    return avgRateofChange

#Checks the current stock for relevant data
def checkStock(code, arr):
    if(len(arr) > DATA_RANGE + TIME_ELAPSED):
        print(code + " has an average rate of change of " + str(checkRateofChange(arr) * 100) + "%")

while True:

    start = time.time()
    
    for i in range(0,len(STOCK_CODES)):
        ticker = yf.Ticker(STOCK_CODES[i])
        stock_data[i].append(ticker.info["currentPrice"])
        checkStock(STOCK_CODES[i], stock_data[i])

    end = time.time()
    process_time = end - start
    print(process_time)
    time.sleep(60 - process_time)