#!/usr/bin/env python

"""
In this example, the program establishes a websocket connection with the GDAX exchange,
retrieves the latest snapshot of the GDAX orderbook, and then continuously updates the
orderbook by retrieving and parsing exchange messages sent from the GDAX server.

The program updates the orderbook displayed in the terminal after every 20th received
exchange message to prevent constant flicker of the terminal.

The user can specify which currency pair the orderbook displays by changing the 'currencyPair'
variable below.
"""

from orderBook import GDAXOrderBook
import os

currencyPair = 'BTC-USD'

# Initiate the websocket connection with the GDAX server.
GDAXOrderBook = GDAXOrderBook(currencyPair)

# Retrieve a snapshot of the oderbook.
GDAXOrderBook.getSnapshot()

# Update the orderbook continuously.
i = 0
while True:
        GDAXOrderBook.update()
        i += 1
        if i % 20 == 0:
                i = 0
                os.system('cls')
                print(GDAXOrderBook)
