from texttable import Texttable

		#loc features: 1d1c, 1d1c
		#devQ: 1d1c
		#FQ: 2d
		#det(single): 1d1c
		#det(bld): list
		#cont: 1d2c
		#approach: 1d1c
		#sp: 2d, 1d1c, 1d2c
		#core: 1d2c, 1d3c, 1d3c
		#id: 1d3c
		#affect: 1d1c
		#med: 1d1c
		#proc: 1d1c
		#int: 1d1c
		#self: 1d1c

		#types: 1col with side (default)
		#3col with header and side
		#2col side from one list
		#just a list, no side
		#2col with side and head
		#3col with side
		#so
		#is it a 1dim list?
			#does it have a side?
		#n: does it have a header?
		#if header: how many columns?
		#so we need a function to deal with a 2d array
		#if no header: 
		#does it have a side?
		#

class page:
	pass
	#multiple tables on a page

class Table:
	def __init__(self, data, *args, **kwargs):
		#unnested dictionary EXCEPT for 2d table
		self.data = data
		#defaults to 1 dimension, 1 column
		self.p = {
			'name': None,
			'header': False,
			'style': 'd1',
			'align': ['l'],
			'breaks': [],
			'dtype': ['t'],
			'width': None
		}
		self.p.update(kwargs)
		style = self.p['style']
		if self.p['breaks'] != []:
			style = 'd1cols'
		self.rows = []
		#types of table
		self.styleIt = {
			'd1': self.d1(),
			'd2': self.d2(),
			'list': self.list(),
			'd1cols': self.d1cols(),
			'custom': self.custom()
		}

		self.styleIt[style]
		self.out = self.draw()

	def draw(self):
		name = ""
		if self.p['name']:
			name = self.p['name']+"\n"
		table = Texttable()
		#table.set_cols_align(self.p['align'] * (self.cols))
		#table.set_cols_dtype(self.p['dtype'] * (self.cols))
		if self.p['width']: table.set_cols_width(self.p['width'])
		table.set_deco(Texttable.HEADER)
		table.add_rows(self.rows,header=self.p['header'])
		return(name+table.draw()+"\n")

	def d1(self): #1d1c
		for key in self.data.keys():
			self.rows.append([key,self.data[key]])
		return(self.draw())

	def list(self): #list
		pass

	def d2(self): #2d
		pass

	def d1cols(self): #1dXc
		breaks = self.p['breaks']
		data = self.data
		cols = len(breaks)+1
		l = len(data.keys())
		lengths = []
		x = 0
		for key in data.keys():
			if key in breaks:
				lengths.append(x)
				x = 1
			else:
				x += 1
		lengths.append(x)
		maxLength = max(lengths)

		#create empty 2d array
		a = [["" for x in range(maxLength)] for x in range(cols)] 

		x = 0
		y = 0
		#now we populate the empty array
		for key in data.keys():
			if key in breaks:
				x += 1
				y = 0
			a[x][y] = key
			y += 1

		#nifty line to transpose the array
		aTrans =[[row[i] for row in a] for i in range(len(a[0]))] 

		#now we add values after the keys
		#newRows is a little kludgy but insert runs forever
		out = []
		for row in aTrans:
			newRow = []
			for item in row:
				newRow.append(item)
				if item != "":
					newRow.append(data[item])
				else:
					newRow.append("")
			out.append(newRow)
		self.rows = out

	def custom(self):
		pass