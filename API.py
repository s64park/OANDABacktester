from fxObjects import Trade
class API:

	def __init__(self):
		self.snapShots = []
		self.positions = {} # dictionary of a list of trades
		self.pnl = 0

	def API_newSnapShot(self, snapShot):
		self.snapShots.append(snapShot)


	def API_getRate(self, instrumentName):
		return self.snapShots[-1].getRate(instrumentName)


	def API_postTrade(self, instrumentName, units, side):
		if instrumentName in self.positions:
			curposition = self.positions[instrumentName]
			if curposition[0].side != side:
				diffUnits = curposition[0].units - units #Number of units in trade object subtract number of units selling/buying
				if diffUnits > 0:
					curposition[0].units = diffUnits
					self.pnl += units * (curposition[0].price - self.snapShots[-1].getRate(instrumentName).getAsk())
				elif diffUnits == 0:
					self.pnl += units * (curposition[0].price - self.snapShots[-1].getRate(instrumentName).getAsk())
					curposition.pop(0)
					if len(curposition) == 0:
						del self.positions[instrumentName]
				else:
					self.pnl += units * (curposition[0].price - self.snapShots[-1].getRate(instrumentName).getAsk())
					curposition.pop(0)
					if len(curposition) == 0:
						del self.positions[instrumentName]
					self.API_postTrade(instrumentName, diffUnits * -1, side) 
			else:
				trade = Trade.Trade(0, units, side, instrumentName, self.snapShots[-1].getRate(instrumentName).getAsk())
				curposition = trade				
				self.positions[instrumentName].append(trade)
		else:
			trade = Trade.Trade(0, units, side, instrumentName, self.snapShots[-1].getRate(instrumentName).getAsk())
			curposition = trade
			self.positions[instrumentName] = []
			self.positions[instrumentName].append(trade)
			
		return 1.00

	def API_movingAverage10(self, instrumentName):
		return API_abstractmovingAverage(self, 10, instrumentName)

	def API_movingAverage50(self, instrumentName):
		return API_abstractmovingAverage(self, 50, instrumentName)

	def API_movingAverage100(self, instrumentName):
		return API_abstractmovingAverage(self, 100, instrumentName)

	def API_abstractMovingAverage(self, interval, instrumentName):
		if interval > len(self.snapShots):
			self.API_abstractmovingAverage(self, len(self.snapShots), instrumentName)
		else:
			movingAverage = 0
			for x in range(interval, (len(self.snapShots) - interval)):
				i = -1*x
				movingAverage = movingAverage + self.snapShots[i]
			return float(movingAverage)/interval
