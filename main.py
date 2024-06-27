    import yfinance as yf
    import smtplib
    import time

    #Global constant variables
    EMAIL = "bobmar123789@gmail.com"
    PASSWORD = "ngvd mryb zsbt hjwg"
    PHONE_NUMBER = "3104903655"
    CARRIER = "@mms.att.net"
    STOCK_CODES = ["TSLA", "AAPL", "AMZN", "GOOGL", "NVDA", "NFLX", "DIS", 
                   "RIVN", "CCL", "AAL", "BAC", "F", "LCID", "CMG", "DAL", 
                   "UNH", "EMR", "UBER","SMCI", "INTC"]
    KEYS = ("price_history", "stable_stock")

    #Number of minutes between collecting the current price
    COLLECTION_INTERVAL = 5

    #Number of minutes between points of comparison for rates of change
    TIME_ELAPSED = int(10 / COLLECTION_INTERVAL)

    #Number of minutes for the range data that we compare when looking back
    DATA_RANGE = int(30 / COLLECTION_INTERVAL)

    #Initializes stock_data to be a 2D array
    stock_data = {}
    for i in range(0, len(STOCK_CODES)):
        stock_data[STOCK_CODES[i]] = {KEYS[0]: [], KEYS[1]: False}

    def is_market_open():
        var = time.gmtime()
        if var.tm_wday < 5:
            if var.tm_hour < 21:
                if var.tm_hour > 16 or (var.tm_hour == 16 and var.tm_min > 30):
                    return True
        return False

    def send_message(message):
        recipient = PHONE_NUMBER + CARRIER
        auth = (EMAIL, PASSWORD)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(auth[0], auth[1])

        server.sendmail(auth[0], recipient, message)

    #Checks the rate of change over the past 5 minutes against the average rate of change for today
    def check_rate_of_change(arr):
        current_roc = (arr[-1] - arr[-1 - TIME_ELAPSED])/arr[-1 - TIME_ELAPSED]

        sig_roc = False
        if abs(current_roc) > .005:
            sig_roc = True

        stable_stock = True
        for i in range(DATA_RANGE):
            roc = (arr[-1 - i] - arr[-1 - TIME_ELAPSED - i])/arr[-1 - TIME_ELAPSED - i]

            if abs((current_roc-roc)/roc) > 1:
                stable_stock = False
                break

        return sig_roc, stable_stock

    #Checks the current stock for relevant data
    def check_stock(code, price_history, stable):
        if(len(price_history) > DATA_RANGE + TIME_ELAPSED):
            tup = check_rate_of_change(price_history)
            if(stable):
                print(code + " is currently a stable stock.")
                if tup[0]:
                    send_message(code + " has a significant rate of change")
                if not tup[1]:
                    send_message(code + " just went from a stable stock to unstable")
            else:
                print("C")

            stable = tup[1]
        else:
            print("N")

    #Downloads stock price every interval and checks the data
    while True:
        start = time.time()

        if(is_market_open()):
            for i in range(0,len(STOCK_CODES)):
                ticker = yf.Ticker(STOCK_CODES[i])
                stock_data[STOCK_CODES[i]][KEYS[0]].append(ticker.info["currentPrice"])
                check_stock(STOCK_CODES[i], 
                            stock_data[STOCK_CODES[i]][KEYS[0]], 
                            stock_data[STOCK_CODES[i]][KEYS[1]])

        end = time.time()
        process_time = end - start
        time.sleep((COLLECTION_INTERVAL * 60) - process_time)