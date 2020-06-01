from decimal import Decimal

class Variable:
	def __init__(self):
		self.name = "Unknown"
		self.abbreviation = "ERR"
		self.v = self.calc()
		self.s = self.string(0.01)
	def calc(self): #would be called with args
		#variables need to be calculated in order btw
		#999 indicates child has no calc method
		return 999
	def c(self):
		return [self.ab, str(self)]
	def ratio(self):
		return ':'.join([str(elem) for elem in self.value])
	def __str__(self):
		return str(self.value)
	def dec(self):
		return str(Decimal(self.value).quantize(Decimal("1.0")))
	def cent(self):
		return str(Decimal(self.value).quantize(Decimal("1.00")))
	def string(self,*args):
		v = self.v
		if args:
			t = args[0]
		else:
			t = .1
		if type(v) is int:
			return str(v)
		elif type(v) is float:
			if t == .1:
				return self.ten()
			elif t == .01:
				return self.dec()
			else:
				return "ERR"
		elif v == None:
			return "None"
		else:
			return "ERR"

class R(Variable):
	def __init__(self,c):
		self.name = "Number of Responses"
		self.ab = "R"
		self.description = "Ratio of pure F to all other determinants"
		self.value = c['R']

class L(Variable):
	def __init__(self,c):
		self.name = "Lambda"
		self.ab = "L"
		self.value = c['F']/(c['R']-c['F'])
	def __float__(self):
		return self.cent()

class WSumC(Variable):
	def __init__(self,c):
		self.name = "Weighted Sum Color"
		self.ab = "WSumC"
		self.description = "Weighted sum of chromatic color determinants"
		self.value = 0.5*c['FC'] + c['CF'] + 1.5*c['C']
	def __str__(self):
		return self.dec()

class EB(Variable):
	def __init__(self,c,WSumC):
		self.name = "Erlebnistypus"
		self.ab = "EB"
		self.description = "Ratio of human movement to chromatic color determinants"
		self.value = [c['M'],WSumC]
		self.sum = c['M']+WSumC.value
	def __str__(self):
		return self.ratio()

class EA(Variable):
	def __init__(self,EB):
		self.name = "Experience Actual"
		self.ab = "EA"
		self.description = "Sum of human movement and chromatic color determinants"
		self.value = EB.sum

class EBPer(Variable):
	def __init__(self,EB,L):
		self.name = "EB Pervasive"
		self.ab = "EBPer"
		self.description = "Ratio measuring dominance of EB style"
		self.value = self.calc(EB,L)
	def calc(self,EB,L):
		EA = EB.sum
		if EA >= 4 and L.value < 1:
			if ((EA <= 10 and abs(EB[0]-EB[1]) >= 2)
					or (EA > 10 and abs(EB[0]-EB[1]) >= 2.5)):
				return max(EB.value)/min(EB.value)
		return None
	def __str__(self):
		if self.value == None: return "None"
		else: return self.dec()

class SumAC(Variable):
	def __init__(self,c):
		self.name = "Achromatic Color"
		self.ab = "SumC'"
		self.description = "Sum of achromatic color determinants"
		self.value = c["FC'"]+c["C'F"]+c["C'"]

class FM(Variable):
	def __init__(self,c):
		self.name = "Animal Movement"
		self.ab = "FM"
		self.description = "Sum of animal movement determinants"
		self.value = c['FM']

class m(Variable):
	def __init__(self,c):
		self.name = "Inanimate Movement"
		self.ab = "m"
		self.description = "Sum of inanimate movement determinants"
		self.value = c['m']

class FMm(Variable):
	def __init__(self,c):
		self.name = "Nonhuman Movement"
		self.ab = "FM+m"
		self.description = "Sum of nonhuman movement determinants"
		self.value = c['FM']+c['m']

class SumT(Variable):
	def __init__(self,c):
		self.name = "Texture Determinants"
		self.ab = "SumT"
		self.description = "Sum of texture determinants"
		self.value = c['T']

class SumV(Variable):
	def __init__(self,c):
		self.name = "Vista Determinants"
		self.ab = "SumV"
		self.description = "Sum of vista determinants"
		self.value = c['V']

class SumY(Variable):
	def __init__(self,c):
		self.name = "Sum of Diffuse Shading"
		self.ab = "SumY"
		self.description = "Sum of diffuse determinants"
		self.value = c['Y']

class SumShd(Variable):
	def __init__(self,c):
		self.name = "Sum of Shading"
		self.ab = "SumShd"
		self.description = "Sum of all shading determinants"
		self.value = c['T']+c['V']+c['Y']

class eb(Variable):
	def __init__(self,FMm,SumShd,SumAC):
		self.name = "Experience Base"
		self.ab = "eb"
		self.description = "Ratio of nonhuman movement to shading and achromatic determinants"
		self.value = [FMm,SumShd.value + SumAC.value]
		self.sum = FMm.value+SumShd.value+SumAC.value
	def __str__(self):
		return self.ratio()

class es(Variable):
	def __init__(self,eb):
		self.name = "Experienced Stimulation"
		self.ab = "es"
		self.description = "Sum of nonhuman movement, shading, and achromatic determinants"
		self.value = eb.sum

class D(Variable):
	def __init__(self,c,EA,es):
		self.name = "D Score"
		self.ab = "D"
		self.description = "Scaled difference between Experience Actual and Experienced Stimulation"
		self.Adjes = es.value - max(1,(c['m']-1)) - max(1,(c['Y']-1))
		self.value = self.calc(EA.value-es.value)
		self.AdjD = self.calc(EA.value-self.Adjes)
	def calc(self,d):
		Dtable = [
			[[13,      999], 5],
			[[10.5,   12.5], 4],
			[[8.0 ,   10.0], 3],
			[[5.5 ,    7.5], 2],
			[[3.0 ,    5.0], 1],
			[[-2.5,    2.5], 0],
			[[-5.0,   -3.0],-1],
			[[-7.5,   -5.5],-2],
			[[-10.0,  -8.0],-3],
			[[-12.5, -10.5],-4],
			[[-999,  -13.0],-5]]
		for x in range(len(Dtable)):
			if Dtable[x][0][0] <= d and Dtable[x][0][1] >= d:
				D = Dtable[x][1]
		return D
	def __str__(self):
		return self.dec()

class AdjEs(Variable):
	def __init__(self,D):
		self.name = "Adjusted es"
		self.ab = "Adj es"
		self.description = "Experienced Stimulation adjusted for situational phenomena"
		self.value = D.Adjes

class AdjD(Variable):
	def __init__(self,D):
		self.name = "Adjusted D Score"
		self.ab = "Adj D"
		self.description = "D score adjusted for situational phenomena"
		self.value = D.AdjD
	def __str__(self):
		return self.dec()