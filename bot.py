#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Quick note: none of these functions were extensively tested.
Use at your own risk, maybe test a bit yourself and see what
happens with small ammounts.
'''

# Import hashlib for m5 encryption
import hashlib
# Import datetime for timestamps
import datetime
# Importing the requests library
# Used for GET and POST
import requests


# Functions:
#    get_ticker(ticker)                           #returns info
#    get_balance(ticker)                          #returns info
#    limit_order('buy'/'sell', quantity, price, symbol) #returns orderId as string
#    order_status(orderId)                        #returns info
#    cancel_order(orderId)                        #returns info


# API information
apiId = ''
secretId = ''



#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   PUBLIC BOIS    ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################


#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   GET TICKER     ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

#returns ticker information
def get_ticker(ticker):

     symbol = ticker

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/market/ticker"

     # Data to be sent to api
     parameters = {
          'symbol': symbol
          }

     # Send GET request and saving response as response object
     r = requests.get(url = API_ENDPOINT, params = parameters)
     output = r.json()

     if (output['status'] == 'ok'):
          return output['ticker'][0]
     else:
          print("ERROR: ", output['description'])
          return output

#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   GET ORDERBOOK    ~*~*~*~*~*~*~*~*~*##
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

#returns orderbook information
def get_orderbook(symbol):

     csymbol = symbol

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/market/orderbook"

     # Data to be sent to api
     parameters = {
          'symbol': csymbol
          }

     # Send GET request and saving response as response object
     r = requests.get(url = API_ENDPOINT, params = parameters)
     output = r.json()

     if (output['status'] == 'ok'):
          return output
     else:
          print("ERROR: ", output['description'])
          return output

#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   PRIVATE BOIS   ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################


# Encrypts a string into a 32-bit string using md5 hash
# Used for making the sign
def signEncrypt(s):
     m = hashlib.md5(s.encode('utf-8'))
     return m


#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   GET BALANCE    ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

# Constant
ACCOUNT = 'exchange'

# Returns balance information about inquired ticker
def get_balance():
     # Time in milliseconds since the last epoch in the UTC timezone
     time = int(datetime.datetime.utcnow().timestamp()*1000) - 50400000

     # Creates POST sign for checking balance
     string  = "ACCOUNT=" + ACCOUNT + "&APIID=" + apiId
     string += "&SECRET=" + secretId + "&TIMESTAMP=" + str(time)
     string = string.upper()
     sign = signEncrypt(string).hexdigest()

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/trade/balance"

     # Data to be sent to api
     data = {
          'account': ACCOUNT,
          'apiid': apiId,
          'timestamp': time,
          'sign': sign
     }

     print(data)

     # Send POST request and saving response as response object
     r = requests.post(url = API_ENDPOINT, data = data)
     output = r.json()

     return output

     '''
     # Function for requesting balance of (ticker)
     for index in range(0,len(output['balance'])):
          if (output['balance'][index]['asset'] == ticker):
               return (output['balance'][index])

     return "ERROR: could not find ticker"
    '''

#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   PLACE ORDER    ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

# Place order (type(buy/sell), quantity, price, symbol(ticker))
# Returns orderID for order tracking
def limit_order(t, q, p, s):

     price = p
     quantity = q
     symbol = s
     if (t == 'buy' or t == 'BUY' or t == 'Buy'):
          type1 = 'buy-limit'
     elif (t == 'sell' or t == 'SELL' or t == 'Sell'):
          type1 = 'sell-limit'

     # Time in milliseconds since the last epoch in the UTC timezone
     time = int(datetime.datetime.utcnow().timestamp()*1000) - 50400000

     # Creates POST sign for placing order
     string  = "APIID=" + apiId
     string += "&PRICE=" + str(price) + "&QUANTITY=" + str(quantity)
     string += "&SECRET=" + secretId + "&SYMBOL=" + symbol
     string += "&TYPE=" + type1 + "&TIMESTAMP=" + str(time)
     string = string.upper()
     sign = signEncrypt(string).hexdigest()

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/trade/order/place"

     # Data to be sent to api
     data = {
          'apiid': apiId,
          'price': price,
          'quantity': quantity,
          'symbol': symbol,
          'type': type1,
          'timestamp': time,
          'sign': sign
     }

     # Send POST request and saving response as response object
     r = requests.post(url = API_ENDPOINT, data = data)
     output = r.json()

     # return orderID for order tracking
     if (output['status'] == 'ok'):
          return output['orderid']
     else:
          return output


#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   ORDER STATUS   ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

# Returns order status information on input order ID
def order_status(o):

     orderId = o

     # Time in milliseconds since the last epoch in the UTC timezone
     time = int(datetime.datetime.utcnow().timestamp()*1000) - 50400000

     # Creates POST sign for checking order status
     string  = "APIID=" + apiId + "&ORDERID=" + orderId
     string += "&SECRET=" + secretId + "&TIMESTAMP=" + str(time)
     string = string.upper()
     sign = signEncrypt(string).hexdigest()

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/trade/order/info"

     # Data to be sent to api
     data = {
          'apiid': apiId,
          'orderid': orderId,
          'timestamp': time,
          'sign': sign
     }

     # Send POST request and saving response as response object
     r = requests.post(url = API_ENDPOINT, data = data)
     output = r.json()

     # return output
     if (output['status'] == 'error'):
          print("ERROR: ", output['decription'])
          return output
     else:
          #this might be output as a list instead of a dict...
          return output['order']


#############################################################
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
##~*~*~*~*~*~*~*~*~*~   CANCEL ORDER   ~*~*~*~*~*~*~*~*~*~*~*
#~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*
#############################################################

# Returns result information on attempted cancel order
def cancel_order(o):

     orderId = o

     # Time in milliseconds since the last epoch in the UTC timezone
     time = int(datetime.datetime.utcnow().timestamp()*1000) - 50400000

     # Creates POST sign for checking order status
     string  = "APIID=" + apiId + "&ORDERID=" + orderId
     string += "&SECRET=" + secretId + "&TIMESTAMP=" + str(time)
     string = string.upper()
     sign = signEncrypt(string).hexdigest()

     # Define the api-endpoint
     API_ENDPOINT = "https://api.coinbene.com/v1/trade/order/cancel"

     # Data to be sent to api
     data = {
          'apiid': apiId,
          'orderid': orderId,
          'timestamp': time,
          'sign': sign
     }

     # Send POST request and saving response as response object
     r = requests.post(url = API_ENDPOINT, data = data)
     output = r.json()

     # Return outcome of order cancel
     if (output['status'] == 'ok'):
          print("Cancellation Success")
     else:
          print("ERROR: ", output['description'])
     return output