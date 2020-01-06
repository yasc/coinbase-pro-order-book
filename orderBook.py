#!/usr/bin/env python

"""
Classes and functions used to parse and manage data receives from exchange.
"""

import communication as com
import os

ORDER_BOOK_DEPTH = None

class OrderBook(object):
	"""Base class for an orderbook."""
	def __init__(self, exchange,product):
		self.exchange = exchange
		self.product = product
		self.bids = []
		self.asks = []
		
	def __str__(self):
		askLevels = sorted(list(self.asks.keys()), key = lambda x: float(x))[0:10]
		bidLevels = sorted(list(self.bids.keys()), key = lambda x: float(x), reverse = True)[0:10]
		header = ["Size \t\t\t Bid       Ask \t\t\t Size \n"]
		for i in range(0,10):
                        header.append("{0:10} \t @ {1:12} || {3:4} \t @ {2:15} \n".format(
                        str(self.bids[bidLevels[i]]),str(bidLevels[i]),
                        str(self.asks[askLevels[i]]),str(askLevels[i]))
                        )
		return "".join(header)
		
class GDAXOrderBook(OrderBook):
	"""Class for the GDAX oderbook.""""
	
	def __init__(self, product):
		OrderBook.__init__(self, 'GDAX', product)	
		self.dataStream = com.webSocketConnection(self.exchange,product,'level2')

	def getSnapshot(self):
		""""Retrieve snapshot of orderbook from the exchange."""
		self.dataStream.start()
		snapshotMessage = self.dataStream.getLatestMessage()
		snapshotMessage = self.dataStream.getLatestMessage()
		self.bids = {float(k):float(v) for k,v in dict(snapshotMessage['bids'][0:ORDER_BOOK_DEPTH]).items()}
		#self.bids = sorted([[float(bids[i][0]),float(bids[i][1])] for i in range(0,len(bids))],key = lambda x: x[0])
		self.asks = {float(k):float(v) for k,v in dict(snapshotMessage['asks'][0:ORDER_BOOK_DEPTH]).items()}
		#self.asks = sorted([[float(asks[i][0]),float(asks[i][1])] for i in range(0,len(asks))],key = lambda x: x[0])
	
	def update(self):
		""""Retrieve the latest exchange message and apply the changes contained therein to the orderbook."""
		update = self.getUpdateMessage()
		if update[0] == 'buy':
			if update[2] == '0.00000000':
				del self.bids[float(update[1])]
			else:
				self.bids[float(update[1])] = float(update[2])
		if update[0] == 'sell':
			if update[2] == '0.00000000':
				del self.asks[float(update[1])]
			else:
				self.asks[float(update[1])] = float(update[2])
			
			
	def getUpdateMessage(self):
		"""Retrieve the latest exchange message from the exchange."""
		updateMessage = self.dataStream.getLatestMessage()
		while updateMessage['type'] != 'l2update':
			print("WARNING: Non-update message received. Getting next message...")
			updateMessage = self.dataStream.getLatestMessage()
		if updateMessage['type'] == 'l2update':
			return updateMessage['changes'][0]
		else:
			raise NameError("Unexpected message received.")

		
	def closeDataStream(self):
		self.dataStream.close()
			
