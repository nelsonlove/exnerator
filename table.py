from texttable import Texttable

class Table:
	def __init__(self, data, layout, **properties):
		self.header = False
			# 'breaks': [],
			# 'dtype': ['t'],
		self.widths: None
		self.__dict__.update(properties)
		self.rows = self.tabulate(data, layout)
		self.out = self.draw()
	def draw(self):
		table = Texttable()
		header,name = False,""
		try: name = self.name+":\n"
		except: name = "Untitled Table"
		try: table.set_cols_width(self.widths)
		except: pass
		try: table.set_cols_align(self.align)
		except: pass
		try: table.set_cols_dtype(self.dtype)
		except: pass
		try: table.set_chars(self.chars)
		except: pass
		try: table.header(self.header)
		except: header = False
		table.set_deco(Texttable.HEADER)
		table.add_rows(self.rows,header=header)
		o = (table.draw()+"\n")
		l = o.split('\n')
		w = max(len(x) for x in l)
		d = '-'*w
		return(name+d+'\n'+o+d+'\n')
	def tabulate(self,data,layout): #list
		return data
		
	def unpair(self,data):
		out = []
		maxWidth = max(len(x) for x in data)
		for row in data:
			newRow = []
			if row == []:
				newRow = maxWidth*2*[""]
			else:
				for item in row:
					if len(item) == 2:
						newRow.append(item[0])
						newRow.append(item[1])
					else:
						newRow.append("")
						newRow.append("")
			out.append(newRow)
		return out

class Columns(Table):
	def tabulate(self,data,layout):

		ordered = []
		for column in layout:
			orderedColumn = []
			for cell in column:
				if cell is not None:
					orderedColumn.append([cell,data[cell]])
				else:
					orderedColumn.append(['',''])
			ordered.append(orderedColumn)

		numColumns = len(ordered)
		numRows = max(len(x) for x in ordered) 

		even = []
		for column in ordered:
			d = numRows - len(column)
			if d > 0:
				column.extend([['','']]*d)
			even.append(column)

		#nifty line to transpose the array
		aTrans =[[row[i] for row in even] for i in range(len(even[0]))] 
		
		#now we flatten the pairs into rows
		return self.unpair(aTrans)

