from exnerator import *
from codes import *

class Score:
	def __init__(self,row):
		self.row = row
		self.card = row[0]
		self.number = row[1]
		self.locationAndDevQuality = row[2]
		self.locationNumber = row[3]
		self.determinantsAndFormQuality = row[4]
		self.pair = row[5]
		self.contents = row[6]
		self.popular = row[7]
		self.zScore = row[8]
		self.special = row[9]

	def printScore(self):
		print(self.card,'. ',sep='',end='')
		print(self.locationAndDevQuality,self.locationNumber,sep='',end=' ')
		print(self.determinantsAndFormQuality,end=' ')
		if self.pair != None:
			print(self.pair,end=' ')
		print(self.contents,end=' ')
		if self.popular != None:
			print(self.popular,end=' ')
		if self.zScore != None:
			print(self.zScore,end=' ')
		if self.special != None:
			print(self.special,end='')
		print('')

	def check(self):
		pass

class Record:
	def __init__(self,data):
		self.scores = []
		self.responses = []
		self.numResponses = 0
		for row in data:
			self.numResponses += 1
			row.insert(1,self.numResponses)
			score = Score(row)
			score.number = self.numResponses
			self.scores.append(score)
		if False: #yes_or_no("Print unparsed scores?"):
			m = menu("Select a display format:",["List","Table"])
			if m == 1:
				self.printScores()
			elif m == 2:
				self.printUnparsedTable()
			else:
				pass
		else:
			pass
		self.parse()
		self.errors = 0
		self.errorCount()
	def errorCount(self):
		for response in self.responses:
			self.errors += response.error
		if self.errors > 0: print(self.errors,"Errors found!")

	def printScores(self):
		for score in self.scores:
			score.printScore()
			time.sleep(0.01)

	def printUnparsedTable(self):
		clear()
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_cols_dtype(['t',  # card number
							  'i',  # response number
							  't',  # location and DQ
							  'i',  # location number
							  't',  # determinants and FQ
							  't',  # pair
							  't',  # contents
							  't',  # popular
							  't',  # z-score
							  't']) # special scores
		table.set_cols_align(["l", "l", "l", "l","l", "c", "l", "c", "c", "l"])
		table.set_cols_width([4,4,4,4,10,3,8,4,2,10])
		rows = [["Card", "#", "Loc", "Loc#", "Deter/FQ", "(2)", "Cont", "Pop","Z","Sp. Scores"]]
		for score in self.scores:
			rows.append(score.row)
			formRows = []
		for row in rows:
			formRow = []
			for cell in row:
				if cell == None: cell = " "
				formRow.append(cell)
			formRows.append(formRow)
		table.add_rows(formRows)
		print(table.draw())

	def parse(self):
		#manual = yes_or_no("Manually advance responses during parsing?")
		self.responses = []
		for score in self.scores:
			print("Parsing response ",score.number,"...",sep='',end='')
			self.responses.append(Response(score))
		#	if manual == True:
		#		while True:
		#			if input("Press enter to continue:") ==  '':
		#				break


	def printTable(self):
		clear()
		table = Texttable()
		table.set_deco(Texttable.HEADER)
		table.set_cols_dtype(['t',  # card number
							  'i',  # response number
							  't',  # location type
							  't',  # DQ
							  'i',  # location number
							  't',  # determinants
							  't',  # FQ
							  't',  # pair
							  't',  # contents
							  't',  # popular
							  't',  # z-score
							  't']) # special scores
		table.set_cols_align(["l","l","l","l","l","l","l","c","l","c","c","l"])
		table.set_cols_width([4,2,3,2,4,7,2,1,7,3,3,7])
		rows = [["Card","#","Loc","DQ","Loc#","Det","FQ","2","Cont","Pop","Z","Spec"]]
		for response in self.responses:
			row = []
			row.append(response.card.strValue)
			row.append(response.number)
			row.append(response.locType.strValue)
			row.append(response.devQuality.strValue)
			row.append(response.locNum.strValue)
			row.append(response.determinants.strValue)
			row.append(response.formQuality.strValue)
			row.append(response.pair.strValue)
			row.append(response.contents.strValue)
			row.append(response.popular.strValue)
			row.append(response.zScore.strValue)
			row.append(response.special.strValue)
			rows.append(row)
		table.add_rows(rows)
		print(table.draw())

class Response:
	def __init__(self,score):
		self.number = score.number
		self.card = Card(score.card)
		self.devQuality = DevQuality(score.locationAndDevQuality)
		self.locType = LocType(score.locationAndDevQuality)
		self.locNum = LocationNumber(score.locationNumber)
		self.determinants = Determinants(score.determinantsAndFormQuality)
		self.formQuality = FormQuality(score.determinantsAndFormQuality)
		self.pair = Pair(score.pair)
		self.contents = Contents(score.contents)
		self.popular = Popular(score.popular)
		self.zScore = ZScore(score.zScore,self.card)
		self.special = Special(score.special)
		self.humanCheck()
		self.error = 0
		self.error += self.card.error
		self.error += self.devQuality.error
		self.error += self.locType.error
		self.error += self.locNum.error
		self.error += self.determinants.error
		self.error += self.formQuality.error
		self.error += self.pair.error
		self.error += self.contents.error
		self.error += self.popular.error
		self.error += self.zScore.error
		self.error += self.special.error
		if self.error > 0: print(self.error,"errors found!")
		print("")
	def humanCheck(self):
		if "H" in self.contents.value or \
				self.determinants.M > 0 or \
				self.determinants.FM > 0 and any(item in [COP,AG] for item in self.special.value):
			step1ruleouts = ["AG","MOR","DR1","DR2","FABCOM1","FABCOM2","INCOM1","INCOM2","ALOG","CONTAM"]
			if self.formQuality.value in ["+","o","u"] and \
					"H" in self.contents.value and \
					not any(item in step1ruleouts for item in self.special.value):
				self.special.addGHR()
			elif self.formQuality.value in ["-", "None"] or \
					any(item in ["DV2","DR2","INCOM2","FABCOM2","CONTAM","ALOG"] for item in self.special.value):
				self.special.addPHR()
			elif "COP" in self.special.value and "AG" not in self.special.value:
				self.special.addGHR()
			elif any (item in ["FABCOM1","FABCOM2","MOR"] for item in self.special.value) or \
					"An" in self.contents.value:
				self.special.addPHR()
			elif self.popular == 1 and self.card.value in ["III","IV","VII","IX"]:
				self.special.addGHR()
			elif any(item in ["AG","INCOM1","INCOM2","DR1","DR2"] for item in self.special.value) or \
						"Hd" in self.contents.value:
				self.special.addPHR()
			else:
				self.special.addGHR()
