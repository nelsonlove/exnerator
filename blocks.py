from table import *
from variables import *

class Block:
	def __init__(self):
		pass
	def __str__(self):
		return Table(self.data,style="d1",name="Core").out

class Core(Block):
	def __init__(self,c):
		self.R = R(c)
		self.L = L(c)
		self.WSumC = WSumC(c)
		self.EB = EB(c,self.WSumC)
		self.EA = EA(self.EB)
		self.EBPer = EBPer(self.EB,self.L)
		self.SumAC = SumAC(c)
		self.FM = FM(c)
		self.m = m(c)
		self.SumT = SumT(c)
		self.SumV = SumV(c)
		self.SumY = SumY(c)
		self.FMm = FMm(c)
		self.SumShd = SumShd(c)
		self.eb = eb(self.FMm,self.SumShd,self.SumAC)
		self.es = es(self.eb)
		self.D = D(c,self.EA,self.es)
		self.AdjEs = AdjEs(self.D)
		self.AdjD = AdjD(self.D)
		self.data = [
			[self.R.c(),	self.L.c(),		[""]],
			[],
			[self.EB.c(),	self.EA.c(),	self.EBPer.c()],
			[self.eb.c(),	self.es.c(),	self.D.c()],
			[[''],			self.AdjEs.c(),	self.AdjD.c()],
			[],
			[self.FM.c(),	self.SumAC.c(),	self.SumT.c()],
			[self.m.c(),	self.SumV.c(),	self.SumY.c()]]