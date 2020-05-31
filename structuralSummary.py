from exnerator import *
from codes import *
from record import *
from decimal import Decimal

structuralSummary = {}
structuralSummary['upper'] = {
	'locationFeatures': {
		'Zf': 0,
		'ZSum': 0,
		'W': 0,
		'D': 0,
		'W+D': 0,
		'Dd': 0,
		'S': 0
	},
	'devQuality': {
		'+': 0,
		'o': 0,
		'v/+': 0,
		'v': 0,
	},
	'formQuality': {
		'+': {
			'FQx': 0,
			'MQual': 0,
			'W+D': 0
		},
		'o': {
			'FQx': 0,
			'MQual': 0,
			'W+D': 0
		},
		'u': {
			'FQx': 0,
			'MQual': 0,
			'W+D': 0
		},
		'-': {
			'FQx': 0,
			'MQual': 0,
			'W+D': 0
		},
		'None': {
			'FQx': 0,
			'MQual': 0,
			'W+D': 0
		}
	},
	'determinants': {
		'blends': [],
		'single': {
			"M": 0,
			"FM": 0,
			"m": 0,
			"FC": 0,
			"CF": 0,
			"C": 0,
			"Cn": 0,
			"FC'": 0,
			"C'F": 0,
			"C'": 0,
			"FT": 0,
			"TF": 0,
			"T": 0,
			"FV": 0,
			"VF": 0,
			"V": 0,
			"FY": 0,
			"YF": 0,
			"Y": 0,
			"Fr": 0,
			"rF": 0,
			"FD": 0,
			"F": 0,
			"(2)": 0
		}
	},
	'contents': {
		"H": 0,
		"(H)": 0,
		"Hd": 0,
		"(Hd)": 0,
		"Hx": 0,
		"A": 0,
		"(A)": 0,
		"Ad": 0,
		"(Ad)": 0,
		"An": 0,
		"Art": 0,
		"Ay": 0,
		"Bl": 0,
		"Bt": 0,
		"Cg": 0,
		"Cl": 0,
		"Ex": 0,
		"Fi": 0,
		"Fd": 0,
		"Ge": 0,
		"Hh": 0,
		"Ls": 0,
		"Na": 0,
		"Sc": 0,
		"Sx": 0,
		"Xy": 0,
		"Id": 0
	},
	'approach': {
		"I": [],
		"II": [],
		"III": [],
		"IV": [],
		"V": [],
		"VI": [],
		"VII": [],
		"VIII": [],
		"IX": [],
		"X": []
	},
	'special': {
		"DV1": 0,
		"DV2": 0,
		"DR1": 0,
		"DR2": 0,
		"INCOM1": 0,
		"INCOM2": 0,
		"FABCOM1": 0,
		"FABCOM2": 0,
		"CONTAM": 0,
		"ALOG": 0,
		"PSV": 0,
		"AB": 0,
		"AG": 0,
		"COP": 0,
		"MOR": 0,
		"PER": 0,
		"CP": 0,
		"GHR": 0,
		"PHR": 0
	}
}
structuralSummary['lower'] = {
	'core': {
		'R': 0,
		'L': 0,
		'EB': [0,0],
		'eb': [0,0],
		'EA': 0,
		'EBPer': 0,
		'es': 0,
		'D': 0,
		'AdjEs': 0,
		'AdjD': 0,
		"SumC'": 0,
		'SumV': 0,
		'SumT': 0,
		'SumY': 0
	},
	'ideation': {
		'a:p':[0,0],
		'Ma:Mp':[0,0],
		'Intell':0,
		'MOR':0,
		'Sum6':0,
		'Lv2':0,
		'WSum6':0,
		'M-':0,
		'Mnone':0
	},
	'affect': {
		'FC:CF+C':0,
		'Pure C':0,
		"SumC'WSumC":0,
		'Afr':0,
		'S':0,
		'Blends:R':0,
		'CP':0
	},
	'mediation': {
		'XA%': 0,
		'WDA%': 0,
		'X-%': 0,
		'X+%': 0,
		'Xu%': 0
	},
	'processing': {
		'Zf':0,
		'W:D:Dd': "0:0:0",
		"W:M":"0:0",
		"Zd":0,
		"PSV":0,
		"DQ+":0,
		"DQv":0
	},
	'interpersonal': {
		'COP':0,
		'GHR:PHR':0,
		'a:p':0,
		'Food':0,
		'SumT':0,
		'Human': 0,
		'PureH':0,
		'PER':0,
		'Isol':0
	},
	'self-perception': {
		'3r+(2)/R':0,
		'Fr+r': 0,
		'SumV': 0,
		'FD': 0,
		'An+Xy': 0,
		'MOR': 0,
		'H:(H)+Hd+(Hd)' : 0
	}
}

def calc(record):
	StructuralSummary(record)

class StructuralSummary:
	def __init__(self,record):
		self.R = record.numResponses
		self.responses = record.responses
		self.upper = structuralSummary['upper']
		self.calcUpperSummary()
		self.lower = structuralSummary['lower']
		self.afr = self.calcAfr()
		self.sMinus = self.calcSminus()
		self.P = self.calcPopulars()
		self.clear()
		self.WSumC = 0
		self.movement = self.calcMovement()
		self.a = self.movement[0]
		self.p = self.movement[1]
		self.Ma = self.movement[2]
		self.Mp = self.movement[3]
		self.calcLowerSummary()

	def round_half_up(n, decimals=0):
		multiplier = 10 ** decimals
		return math.floor(n*multiplier + 0.5) / multiplier

	def calcPopulars(self):
		output = 0
		for response in self.responses:
			if response.popular.value == True:
				output += 1
		return output

	def calcSminus(self):
		output = 0
		for response in self.responses:
			if "S" in response.locType.value and response.formQuality.value == "-":
				output += 1
		return output

	def calcAfr(self):
		backThree = 0
		frontSeven = 0
		for response in self.responses:
			if response.card.value in ["VIII","IX","X"]:
				backThree += 1
			else:
				frontSeven += 1
		output = str(Decimal(int(backThree)/int(frontSeven)).quantize(Decimal("1.00")))
		return output

	def calcMovement(self):
		a = 0
		p = 0
		Ma = 0
		Mp = 0
		for response in self.responses:
			a += response.determinants.a
			p += response.determinants.p
			Ma += response.determinants.Ma
			Mp += response.determinants.Mp
		return[a,p,Ma,Mp]

	def calcLowerSummary(self):
		d=True #self.yes_or_no("Pause for lower summary tables?")
		self.clear()
		self.lower['core'].update(self.calcCore())
		if d: self.pressEnter()
		self.lower['ideation'].update(self.calcIdeation())
		if d: self.pressEnter()
		self.lower['affect'].update(self.calcAffect())
		if d: self.pressEnter()
		self.lower['mediation'].update(self.calcMediation())
		if d: self.pressEnter()
		self.lower['processing'].update(self.calcProcessing())
		if d: self.pressEnter()
		self.lower['interpersonal'].update(self.calcInterpersonal())
		if d: self.pressEnter()	
		self.lower['self-perception'].update(self.calcSelfPerception())
		if d: self.pressEnter()	

	def calcUpperSummary(self):
		d = True #self.yes_or_no("Pause for upper summary tables?")
		self.clear()
		print("Location Features:\n")
		self.upper['locationFeatures'].update(self.calcZ())
		self.upper['locationFeatures'].update(self.calcLocTypes())
		if d: self.pressEnter()
		self.upper['devQuality'].update(self.calcDevQuality())
		if d: self.pressEnter()
		self.upper['formQuality'].update(self.calcFormQuality())
		if d: self.pressEnter()
		self.upper['determinants'].update(self.calcDeterminants(d))
		if d: self.pressEnter()
		self.upper['contents'].update(self.calcContents())
		if d: self.pressEnter()
		self.upper['approach'].update(self.calcApproach())
		if d: self.pressEnter()
		self.upper['special'].update(self.calcSpecial())
		if d: self.pressEnter()
		self.clear()

	def clear(self):
		# for windows 
		if name == 'nt': 
			_ = system('cls') 
		# for mac and linux(here, os.name is 'posix') 
		else: 
			_ = system('clear')

	def ratio(self,x,y):
		return str(x)+":"+str(y) 

	def table2(self,header,dict):
		print(header,":\n",sep='')
		rows = []
		for key in dict.keys():
			rows.append([key,dict[key]])
		table = Texttable()
		table.set_cols_align(["l","l"])
		table.set_cols_dtype(["t", "t"])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return dict	

	def calcSelfPerception(self):
		determinants = self.upper['determinants']['single']
		contents = self.upper['contents']
		pair = (determinants['(2)'])
		reflections = determinants['Fr']+determinants['rF']
		output = {



			'3r+(2)/R': str(Decimal((3*reflections+pair)/self.R).quantize(Decimal("1.00"))),
			'Fr+rF': reflections,
			'SumV': self.lower['core']['SumV'],
			'FD': determinants['FD'],
			'An+Xy': contents['An']+contents['Xy'],
			'MOR': self.upper['special']['MOR'],
			'H:(H)+Hd+(Hd)': self.ratio(contents['H'],contents['(H)']+contents['Hd']+contents['(Hd)'])
		}
		return(self.table2("Self-Perception",output))

	def calcInterpersonal(self):
		R=self.R
		contents = self.upper['contents']
		determinants = self.upper['determinants']['single']
		COP = self.upper['special']['COP']
		GHRtoPHR = self.ratio(self.upper['special']['GHR'],self.upper['special']['PHR'])
		ap = self.ratio(self.a,self.p)
		food = contents['Fd']
		pureH = contents['H']
		sumT = self.lower['core']['SumT']
		human = contents['H']+contents['(H)']+contents['Hd']+contents['(Hd)']
		PER = self.upper['special']['PER']
		isol = (contents['Bt']+2*contents['Cl']+contents['Ge']+contents['Ls']+2*contents['Na'])/R
		
		print("Interpersonal:\n")
		rows = []
		rows.append(['COP',COP])
		rows.append(['GHR:PHR',GHRtoPHR])
		rows.append(['a:p',ap])
		rows.append(['Food',food])
		rows.append(['SumT',sumT])
		rows.append(['Human', human])
		rows.append(['PureH', pureH])
		rows.append(['PER', PER])
		rows.append(['Isol', isol])
		table = Texttable()
		table.set_cols_align(["l","l"])
		table.set_cols_dtype(["t", "t"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")

		output = {
			'COP':COP,
			'GHR:PHR':GHRtoPHR,
			'a:p':ap,
			'Food':food,
			'SumT':sumT,
			'Human': human,
			'PureH': pureH,
			'PER': PER,
			'Isol': isol
		}
		return output

	def calcProcessing(self):
		Zf = self.upper['locationFeatures']['Zf']
		locType = self.upper['locationFeatures']
		M = self.upper['determinants']['single']['M']
		econIndex = self.ratio(locType['W'],self.ratio(locType['D'],locType['Dd']))
		aspirationalRatio = self.ratio(locType['W'],M)
		Zd = self.upper['locationFeatures']['ZSum'] - self.upper['locationFeatures']['Zest']
		PSV = self.upper['special']['PSV']
		DQplus = self.upper['devQuality']['+']
		DQv = self.upper['devQuality']['v']

		print("Processing:\n")
		rows = []
		rows.append(['Zf',Zf])
		rows.append(['W:D:Dd',econIndex])
		rows.append(["W:M",aspirationalRatio])
		rows.append(["Zd",Zd])
		rows.append(["PSV",PSV])
		rows.append(["DQ+",DQplus])
		rows.append(["DQv",DQv])
		table = Texttable()
		table.set_cols_align(["l","l"])
		table.set_cols_dtype(["t", "t"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")

		output = {
			'Zf': Zf,
			'W:D:Dd': econIndex,
			"W:M": aspirationalRatio,
			"Zd": Zd,
			"PSV": PSV,
			"DQ+": DQplus,
			"DQv": DQv
		}
		return output

	def calcMediation(self):
		R = self.R
		P = self.P
		sMinus = self.sMinus
		FQ = self.upper['formQuality']
		WD = self.upper['locationFeatures']['W+D']
		appropriate = ['+','o','u']
		WDappropriate = 0
		for key in appropriate:
			WDappropriate += self.upper['formQuality'][key]['W+D']
		FQxAppropriate = 0
		for key in appropriate:
			FQxAppropriate += self.upper['formQuality'][key]['FQx']
		XA = str(Decimal(FQxAppropriate/R).quantize(Decimal("1.00")))
		WDA = str(Decimal(WDappropriate/WD).quantize(Decimal("1.00")))
		Xminus = str(Decimal(self.upper['formQuality']['-']['FQx']/R).quantize(Decimal("1.00")))
		Xplus = str(Decimal((self.upper['formQuality']['+']['FQx']+self.upper['formQuality']['o']['FQx'])/R).quantize(Decimal("1.00")))
		Xu = str(Decimal(self.upper['formQuality']['u']['FQx']/R).quantize(Decimal("1.00")))

		print("Mediation:\n")
		rows = []
		rows.append(['XA%',XA])
		rows.append(['WDA%',WDA])
		rows.append(["X-%",Xminus])
		rows.append(["S-",sMinus])
		rows.append(["P",P])
		rows.append(["X+%",Xplus])
		rows.append(["Xu%",Xu])
		table = Texttable()
		table.set_cols_align(["l","l"])
		table.set_cols_dtype(["t", "t"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")

		output = {
			'XA%': XA,
			'WDA%': WDA,
			"X-%": Xminus,
			"S-": sMinus,
			"P": P,
			"X+%": Xplus,
			"Xu%": Xu
		}
		return output

	def calcAffect(self):
		determinants = self.upper['determinants']['single']
		core = self.lower['core']
		FC = determinants['FC']
		CF = determinants['CF']
		C = determinants['C']
		R = self.R
		formColorRatio = self.ratio(FC,CF+C)
		wSumC = self.WSumC
		sumCprime = core["SumC'"]
		constrictionRatio = self.ratio(sumCprime,wSumC)
		afr = str(self.lower['affect']['Afr'])
		S = self.upper['locationFeatures']['S']
		blends = len(self.upper['determinants']['blends'])
		complexityRatio = self.ratio(blends,R)
		CP = self.upper['special']['CP']

		print("Affect:\n")
		rows = []
		rows.append(['FC:CF+C',formColorRatio])
		rows.append(['Pure C',C])
		rows.append(["SumC':WSumC",constrictionRatio])
		rows.append(["Afr",str(self.afr)])
		rows.append(["S",S])
		rows.append(["Blends:R",complexityRatio])
		rows.append(["CP",CP])
		table = Texttable()
		table.set_cols_align(["l","l"])
		table.set_cols_dtype(["t", "t"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")

		output = {
			'FC:CF+C': formColorRatio,
			'Pure C': C,
			"SumC':WSumC": constrictionRatio,
			"Afr":afr,
			"S":S,
			"Blends:R":complexityRatio,
			"CP":CP
		}
		return output	

	def calcIdeation(self):
		determinants = self.upper['determinants']['single']
		a = self.a
		p = self.p
		Ma = self.Ma
		Mp = self.Mp
		special = self.upper['special']
		AB = special['AB']
		MOR= special['MOR']
		Art = self.upper['contents']['Art']
		Ay = self.upper['contents']['Ay']
		ap = self.ratio(a,p)
		MaMp = self.ratio(Ma,Mp)
		intell = 2*AB+Art+Ay
		sum6 = special['rawSum6']
		lv2 = special['DV2']+special['INCOM2']+special['DR2']+special['FABCOM2']
		wSum6 = special['WSum6']
		Mminus = self.upper['formQuality']['-']['MQual']
		Mnone = self.upper['formQuality']['None']['MQual']
		print("Ideation:\n")
		rows = []
		rows.append(["a:p",ap,"Sum6",sum6])
		rows.append(['Ma:Mp','MaMp','Lv2',lv2])
		rows.append(['INTELL',intell,'WSum6',wSum6])
		rows.append(['MOR',MOR,"M-",Mminus])
		rows.append(['','',"Mnone",Mnone])
		table = Texttable()
		table.set_cols_align(["l","l","l","l"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		output = {
			'a:p':ap,
			'Ma:Mp': MaMp,
			'Intell': intell,
			'MOR': MOR,
			'Sum6':sum6,
			'Lv2': lv2,
			'WSum6':wSum6,
			'M-':Mminus,
			'Mnone': Mnone
		}
		return output

	def calcCore(self):
		output = self.lower['core']
		determinants = self.upper['determinants']['single']
		R = self.R
		F = determinants['F']
		FM = determinants['FM']
		M = determinants['M']
		m = determinants['m']
		L = F/(R-F)
		FC = determinants['FC']
		CF = determinants['CF']
		C = determinants['C']
		sumCprime = determinants["C'"] + determinants["C'F"] + determinants["FC'"]
		sumY = determinants["Y"] + determinants["YF"] + determinants["FY"]
		sumT = determinants["T"] + determinants["TF"] + determinants["FT"]
		sumV = determinants["V"] + determinants["VF"] + determinants["FV"]
		self.WSumC = 0.5*FC + CF + 1.5*FC
		EB = [determinants['M'],self.WSumC]
		EA = EB[0]+EB[1]
		EBPer = "N/A"
		if EA >= 4 and L < 1:
			if (EA <= 10 and abs(EB[0]-EB[1]) >= 2) or (EA > 10 and abs(EB[0]-EB[1]) >= 2.5):
				if EB[0] >= EB[1]:
					EBPer = EB[0] / EB[1]
				elif EB[0] < EB[1]:
					EBPer = EB[1] / EB[0]
				else:
					EBPer = "N/A"
			else:
				EBPer = "N/A"
		eb = [FM+m,sumCprime+sumT+sumY+sumV]
		es = eb[0]+eb[1]
		Draw = EA - es
		def calcD(d):
			Dtable = [[[13,      999], 5],
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
				if Dtable[x][0][0] <= Draw and Dtable[x][0][1] >= Draw:
					D = Dtable[x][1]
			return D
		D = calcD(EA - es)
		adjEs = es - max(0,(m-1)) - max(0,(sumY-1))
		adjD = calcD(adjEs)
		print("Core:\n")
		rows = []
		rows.append(["R",R,"L",L,"",""])
		rows.append(['','','','','',''])
		rows.append(["EB",self.ratio(EB[0],EB[1]),"EA",EA,"EBPer",EBPer])
		rows.append(["eb",self.ratio(eb[0],eb[1]),"es",es,"D",D])
		rows.append(["","","Adj es",adjEs,"AdjD",adjD])
		rows.append(['','','','','',''])
		rows.append(["FM",FM,"SumC'",sumCprime,"SumT",sumT])
		rows.append(["m",m,"SumV",sumV,"SumY",sumY])
		table = Texttable()
		table.set_cols_align(["l","l","l","l","l","l"])
		#table.set_cols_width([2,9,6,4,5,4])
		table.set_deco(Texttable.HEADER)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		output = {
			'R': R,
			'L': L,
			'EB': EB,
			'eb': eb,
			'EA': EA,
			'EBPer': EBPer,
			'es': es,
			'D': D,
			'AdjEs': adjEs,
			'AdjD': adjD,
			"SumC'": sumCprime,
			'SumV': sumV,
			'SumT': sumT,
			'SumY': sumY
		}
		return output

	def pressEnter(self):
		while True:
			if input("Press enter to continue:") ==  '':
				break
		self.clear()

	def printValues(self,input):
		for key in input.keys():
			print(key,": ",input[key],sep='')

	def calcZ(self):
		Zf = 0
		ZSum = 0
		for response in self.responses:
			if response.zScore.value != 0 and response.zScore.value > 0:
				Zf += 1
				ZSum += response.zScore.value
		ZestTable = [0,0,2.5,6.0,10.0,13.5,17.0,20.5,24.0,27.5,31.0,34.5,38.0,41.5,45.5,49.0,52.5,56.0,59.5,63.0,66.5,70.0,81.0,84.5,88.0,91.5,95.0,98.5,102.5,105.5,109.5,112.5,116.5,120.0,123.5,127.0,130.5,134.0,137.5,141.0,144.5,148.0,152.0,155.5,159.0,162.5,166.0,169.5,173.0]
		output = {'Zf': Zf, 'ZSum': ZSum, 'Zest': ZestTable[Zf]}
		table = Texttable()
		table.set_header_align(["l","l"])
		table.set_cols_align(["l","l"])
		table.set_cols_width([4,2])
		table.set_deco(Texttable.HEADER)
		rows = []
		for row in output.keys():
			rows.append([row,output[row]])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def calcLocTypes(self):
		output = {'W': 0, 'D': 0, 'W+D': 0, 'Dd': 0, 'S': 0}
		for response in self.responses:
			output['W'] += response.locType.W
			output['D'] += response.locType.D
			output['Dd'] += response.locType.Dd
			output['S'] += response.locType.S
		output['W+D'] = output['W'] + output['D']
		table = Texttable()
		table.set_header_align(["l","l"])
		table.set_cols_align(["l","l"])
		table.set_cols_width([4,2])
		table.set_deco(Texttable.HEADER)
		rows = []
		for row in output.keys():
			rows.append([row,output[row]])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def calcDevQuality(self):
		output = self.upper['devQuality']
		for response in self.responses:
			output[response.devQuality.strValue] += 1
		print("Developmental Quality:\n")
		table = Texttable()
		table.set_header_align(["l","l"])
		table.set_cols_align(["l","l"])
		table.set_cols_width([4,2])
		table.set_deco(Texttable.HEADER)
		rows = []
		for row in output.keys():
			rows.append([row,output[row]])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output
		return output

	def calcFormQuality(self):
		output = self.upper['formQuality']
		for formQuality in output.keys():
			for response in self.responses:
				if formQuality == response.formQuality.value:
					output[response.formQuality.strValue]['FQx'] += 1
					if response.locType.value in ['W','WS','D','DS']:
						output[formQuality]['W+D'] += 1
					if response.determinants.M > 0:
						output[formQuality]['MQual'] += 1
		print("Form Quality:\n")
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l", "l", "l", "l"])
		table.set_cols_align(["l", "l", "l", "l"])
		table.set_cols_width([4,5,5,5])
		sideheader = ['+','o','u','-','None']
		topheader = ['','FQx','MQual','W+D']
		rows = []
		rows.append(topheader)
		for cell in sideheader:
			row = []
			row.append(cell)
			row.append(output[cell]['FQx'])
			row.append(output[cell]['MQual'])
			row.append(output[cell]['W+D'])
			rows.append(row)
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def calcDeterminants(self,d):
		output = {}
		single = self.upper['determinants']['single']
		blends = self.upper['determinants']['blends']
		for response in self.responses:
			single['M'] += response.determinants.M
			single['FM'] += response.determinants.FM
			single['m'] += response.determinants.m
			if response.pair.value == True: single['(2)'] += 1
			for determinant in single.keys():
				if determinant in response.determinants.value:
					single[determinant] += 1
			if len(response.determinants.value) > 1:
					blends.append(response.determinants.strValue)
		output['single'] = single
		print("Determinants (Single):\n")

		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l", "l","l", "l"])
		table.set_cols_align(["l", "l","l", "l"])
		table.set_cols_width([4,2,4,2])
		rows = []
		k = list(single.keys())
		x = range(0,len(k)-12)
		for i in x:
			rows.append([k[i],single[k[i]],k[i+12],single[k[i+12]]])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")

		output['blends'] = blends
		if d: self.pressEnter()
		print("Determinants (Blends):\n")
		for blend in blends:
			print(blend,'\n')
		return output

	def calcContents(self):
		output = self.upper['contents']
		for response in self.responses:
			for content in output.keys():
				if content in response.contents.value:
					output[content] += 1
		print("Contents:\n")
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l", "l","l", "l"])
		table.set_cols_align(["l", "l","l", "l"])
		table.set_cols_width([4,2,4,2])
		rows = []
		k = list(output.keys())
		x = range(0,len(k)-13)
		for i in x:
			rows.append([k[i],output[k[i]],k[i+12],output[k[i+12]]])
		rows.append([k[26],output[k[26]],'',''])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def calcSpecial(self):
		output = self.upper['special']
		for response in self.responses:
			if response.special.value != None:
				for special in output.keys():
					if special in response.special.value:
						output[special] += 1
		print("Special Scores:\n")
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l","c","c"])
		table.set_cols_align(["l","c","c"])
		table.set_cols_width([6,3,3])
		rows = []
		rows.append(['',"Lv1","Lv2"])
		rows.append(['DV',output['DV1'],output['DV2']])
		rows.append(['INCOM',output['INCOM1'],output['INCOM2']])
		rows.append(['DR',output['DR1'],output['DR2']])
		rows.append(['FABCOM',output['FABCOM1'],output['FABCOM2']])
		rows.append(['ALOG',output['ALOG'],''])
		rows.append(['CONTAM',output['CONTAM'],''])
		table.add_rows(rows,header=False)
		print(table.draw()+"\n")

		output['rawSum6'] = output['DV1'] + output['DV2'] + output['DR1'] + output['DR2'] + output['INCOM1'] + output['INCOM2'] + output['FABCOM1'] + output['FABCOM2'] + output['ALOG'] + output['CONTAM']
		output['WSum6'] = output['DV1'] + output['DV2']*2 + output['DR1']*3 + output['DR2']*6 + output['INCOM1']*2 + output['INCOM2']*4 + output['FABCOM1']*4 + output['FABCOM2']*7 + output['ALOG']*5 + output['CONTAM']*7
		table = Texttable()
		table.set_header_align(["l","l"])
		table.set_cols_align(["l","l"])
		table.set_cols_width([7,2])
		table.set_deco(Texttable.HEADER)
		rows = []
		rows.append(["RawSum6",output['rawSum6']])
		rows.append(["WSum6",output['WSum6']])
		table.add_rows(rows,header=False)
		print(table.draw()+"\n")

		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l","l","l","l"])
		table.set_cols_align(["l","l","l","l"])
		table.set_cols_width([4,2,4,2])
		rows = []
		rows.append(['AB',output['AB'],'GHR',output['GHR']])
		rows.append(['AG',output['AG'],'PHR',output['PHR']])
		rows.append(['COP',output['COP'],'MOR',output['MOR']])
		rows.append(['CP',output['CP'],'PER',output['PER']])
		rows.append(['','','PSV',output['PSV']])		

		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def calcApproach(self):
		output = self.upper['approach']
		for response in self.responses:
			output[response.card.value].append(response.locType.value)
		print("Approach:\n")
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_header_align(["l", "l"])
		table.set_cols_align(["l", "l"])
		table.set_cols_width([4,20])
		rows = []
		for card in output.keys():
			rows.append([card,','.join(output[card])])
		table.add_rows(rows,header=False)
		print (table.draw()+"\n")
		return output

	def yes_or_no(self,question):
	    while "Invalid response!":
	        reply = str(input(question+' (y/n): ')).lower().strip()
	        if reply == 'y':
	            return True
	        if reply == 'n':
	            return False
	        else:
	        	pass
