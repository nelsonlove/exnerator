
import parse as Parse
from table import Columns, Table

class Record:
	def __init__(self,data):
		self.scores = []
		for row in data:
			self.scores.append(self.Score(row))
		self.R = len(self.scores)

	def table(self):
		dtype = ['t','i','t','t','i','t','t','t','t','t','t','t']
		align = ["l","l","l","l","l","l","l","c","l","c","c","l"]
		chars = ['', '', '', '=']
		header = ["Card","#","Loc","DQ","Loc#","Det","FQ","2","Cont","Pop","Z","Spec"]
		rows = []
		for i, score in enumerate(self.scores):
			row = [score.card]
			if i > 0:
				if score.card == self.scores[i-1].card:
					row = [' ']
			row.append(i+1)
			row.append(score.locType)
			row.append(score.devQuality)
			row.append(score.locNum)
			row.append('.'.join(score.rawDeterminants))
			row.append(score.formQuality)
			if score.pair == True: row.append('2')
			else: row.append('')
			row.append(','.join(score.contents))
			if score.popular == True: row.append('P')
			else: row.append('')
			if score.zValue: row.append(score.zValue)
			else: row.append('')
			row.append(','.join(score.special))
			rows.append(row)
		return Table(
			rows,None, name="Sequence of Scores",header=header,
			align=align,dtype=dtype,chars=chars).out

	def __str__(self):
		data = {}
		layout = []
		for i, v in enumerate(self.scores):
			n = str(i+1)+'.'
			data.update({n:str(v)})
			layout.append(n)
		return Columns(data,[layout], name="Sequence of Scores",
			align=['r','l'],dtype=['t','t']).out

	class Score:
		def __init__(self,d):
			self.__dict__.update(d)
			self.form = Parse.form(self.locType,self.formQuality)
			print(self.form)
			self.iso = self.isolate()
			self.rawDeterminants = self.determinants
			self.determinants, self.movement = Parse.movement(self.rawDeterminants)
			if self.zScore:
				self.zValue = Parse.zValue(self.card,self.zScore)
			else: self.zValue = None
			self.humanCheck()

		def isolate(self):
			iso = 0
			for d in self.determinants:
				if d in ['Bt','Ge','Ls']: self.iso += 1
				elif d in ['Na','Cl']: iso += 2
			return iso

		def __str__(self):
			out = []
			out.append(self.locType)
			out.append(self.devQuality)
			if self.locNum > 1: out.append(str(self.locNum))
			out.extend([' ','.'.join(self.rawDeterminants)])
			if self.formQuality: out.extend(self.formQuality)
			out.extend(' ')
			if self.pair: out.extend(['2',' '])
			out.extend([','.join(self.contents),' '])
			if self.popular: out.extend(['P',' '])
			if self.zValue: out.extend([self.zValue,' '])
			if self.special is not '': out.extend(','.join(self.special))
			return(''.join(out))

		def humanCheck(self):
			if "H" in self.contents or \
					"M" in self.determinants or \
					"FM" in self.determinants and any(item in ['COP','AG'] for item in self.special):
				ruleouts = ["AG","MOR","DR1","DR2","FABCOM1",
								"FABCOM2","INCOM1","INCOM2","ALOG","CONTAM"]
				if 'appropriate' in self.form and \
						"H" in self.contents and \
						not any(item in ruleouts for item in self.special):
					self.special.append('GHR')
				elif 'appropriate' not in self.form or \
						any(item in ["DV2","DR2","INCOM2","FABCOM2","CONTAM","ALOG"] for item in self.special):
					self.special.append('PHR')
				elif "COP" in self.special and "AG" not in self.special:
					self.special.append('GHR')
				elif any (item in ["FABCOM1","FABCOM2","MOR"] for item in self.special) or \
						"An" in self.contents:
					self.special.append('PHR')
				elif self.popular == True and self.card in ["III","IV","VII","IX"]:
					self.special.append('GHR')
				elif any(item in ["AG","INCOM1","INCOM2","DR1","DR2"] for item in self.special) or \
							"Hd" in self.contents:
					self.special.append('PHR')
				else:
					self.special.append('GHR')
