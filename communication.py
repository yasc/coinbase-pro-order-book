#!/usr/bin/env python

"""
Communication classes and functions.
"""

import datetime
import json as js
import websocket as ws

class Connection(object):
	
	def __init__(self,exchange):
		self.dateTimeStarted = datetime.datetime.now()
		self.exchange = exchange
		
class webSocketConnection(Connection):
	
	def __init__(self,exchange, product, channel):
		Connection.__init__(self,exchange)
		self.serverURL = getServerURL(exchange)
		self.subscriptionMessage = getSubscriptionMessage(exchange, product, channel)
		self.wsConnection = ws.create_connection(self.serverURL)
		
	def start(self):
		self.wsConnection.send(self.subscriptionMessage)
		
	def getLatestMessage(self):
		return  js.loads(self.wsConnection.recv())
		
	def close(self):
		self.wsConnection.close()
	
def getServerURL(exchange):
	"""Retrieve the server URL for a given exchange."""
	
	if exchange == 'GDAX':
		return 'wss://ws-feed.gdax.com/'
		
	raise NameError("Exchange symbol not recognized.")
		
def getSubscriptionMessage(exchange,product,channel):
	"""Retrieve the websocket subscription message for a given exchange."""
	
	if exchange == 'GDAX':
		subscriptionMessage = js.dumps({
			"type": "subscribe",
			"product_ids": [product],
			"channels": [channel]
		})
		return subscriptionMessage
		
	raise NameError("Exchange symbol not recognized.")