## Introduction

This program establishes a websocket connection with the Coinbase Pro API and then replicates the Coinbase Pro orderbook in the user's terminal.

A live/online version of the orderbook can be viewed here: https://pro.coinbase.com/trade/BTC-USD

## Example

To run the example, download the project into a local directory and then run:
```
python example.py
```
in your terminal.


To change which currency pair is displayed in the orderbook, edit the `example.py` file by changing the variable:
```
currencyPair = 'BTC-USD'
```
to reflect the desired currency pair (e.g. 'BTC-EUR').
