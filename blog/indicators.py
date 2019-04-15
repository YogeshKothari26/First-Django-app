from kiteconnect import KiteConnect
import pandas as pd
import numpy as np
import datetime


class KiteFetcher(object):

	def __init__(self, access_token):
		self.kite = KiteConnect(api_key="0ld4qxtvnif715ls")
		self.kite.set_access_token(access_token)		

# · minute
# · day
# · 3minute
# · 5minute
# · 10minute
# · 15minute
# · 30minute
# · 60minute		