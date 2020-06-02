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

		#also the damn thing won't justify right unless we can do newlines and empty space
		#which means not using a dict format, which makes sense since dict isn't ordered anyway
		#so they all have to be 2d arrays
		#but either sideheaders or key value pairs
		#maybe throw everything into a dictionary then specify the layout separate;y
		#instead of having the dict set the layout...makes sense

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
		self.style = self.p['style']
		if self.p['breaks'] != [] and type(rows[0]) == list:
			self.style = 'd1cols'
		self.rows = []
		#types of table
		if self.style == 'd1':
			self.rows = self.d1()
		elif self.style == 'd2':
			self.rows = self.d2()
		elif self.style == 'list':
			self.rows = self.list()
		elif self.style == 'dcols':
			self.rows = self.d1cols()
		else:
			self.rows = self.custom()
		self.out = self.draw()

	def draw(self):
		name = ""
		if self.p['name']:
			name = self.p['name']+":\n\n"
		table = Texttable()
		#table.set_cols_align(self.p['align'] * (self.cols))
		#table.set_cols_dtype(self.p['dtype'] * (self.cols))
		if self.p['width']: table.set_cols_width(self.p['width'])
		table.set_deco(Texttable.HEADER)
		table.add_rows(self.rows,header=False)
		return(name+table.draw()+"\n")

	def d1(self): #1d1c
		return self.unTuple(self.data)

	def list(self): #list
		out = []
		for item in self.data:
			out.append([item])
		return out

	def d2(self): #2d
		pass

	def d1cols(self): #1dXc
		print(self.style)
		if self.style != 'd1cols':
			return
		breaks = self.p['breaks']
		data = self.data
		cols = len(breaks)+1
		l = len(data)
		lengths = []
		x = 0
		for row in data:
			if row[0] in breaks:
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
		for row in data:
			if row[0] in breaks or row[0] == ["&BR"]:
				x += 1
				y = 0
			a[x][y] = row
			y += 1

		#nifty line to transpose the array
		aTrans =[[row[i] for row in a] for i in range(len(a[0]))] 

		#now we add values after the keys
		#newRows is a little kludgy but insert runs forever
		out = []
		return unTuple(aTrans)

	def unTuple(self,data):
		out = []
		maxWidth = max(len(x) for x in self.data)
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

	def custom(self):
		pass