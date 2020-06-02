# Functions for parsing Rorschach data.

def card(i):
	cards = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
	if i not in cards: return None
	else: return {'card':i}

def locDev(i):
	locTypes = ['DdS','Dd','WS','DS','W','D']
	devQualities = ['v/+','o','v','+']
	for l in locTypes:
		if i.startswith(l):	
			for d in devQualities:
				if i.endswith(d):
					loc = i.replace(d, '')
					return {'locType':loc,'devQuality':d}
	return None

def form(t,FQ):
	o = []
	if t.endswith('S'):
		o.append('S')
		t = t[:-1]
	if t == "Dd":
		o.append('Dd')
	else:
		o.append('W+D')
		o.append(t)
	if FQ in ['+','o','u']:
		o.append('appropriate')
		if FQ in ['+','o']:
			o.append('conventional')
	return o

def locNum(i):
	if not isinstance(i, int): return None
	return {'locNum': i}

def detFQ(i):
	formQualities = ['+', 'o', 'u', '-', '']
	determinants = ['Ma', 'Mp', 'Ma-p', 'FMa', 'FMp', 'FMa-p', 'ma', 'mp', 'ma-p', 'FC', 'CF', 'C', 'Cn', "FC'", "C'F", "C'", 'FT', 'TF', 'T', 'FV', 'VF', 'V', 'FY', 'YF', 'Y', 'Fr', 'rF', 'FD', 'F', '(2)']
	fq = ''
	if i[-1] in formQualities:
		fq = i[-1]
		i = i[:-1]
	l = i.split(".")
	for item in l:
		if item not in determinants:
			return None
	return{'formQuality': fq, 'determinants': l}

def pair(i):
	if i == None:
		return {'pair': False}
	elif i == 2:
		return {'pair': True}
	else:
		return None
	

def contents(i):
	contents = ['H', '(H)', 'Hd', '(Hd)', 'Hx', 'A', '(A)', 'Ad', '(Ad)', 'An', 'Art', 'Ay', 'Bl', 'Bt', 'Cg', 'Cl', 'Ex', 'Fi', 'Fd', 'Ge', 'Hh', 'Ls', 'Na', 'Sc', 'Sx', 'Xy', 'Id']
	l = i.split(",")
	for item in l:
		if item not in contents:
			return None
	return{'contents': l}

def popular(i):
	if i == None: o = False
	elif i == 'P': o = True
	else: return None
	return {'popular': o}

def zScore(i):
	zScores = ['ZW', 'ZA', 'ZD', 'ZS']
	if i == None: o = None
	elif i not in zScores: return None 
	else: o = i
	return {'zScore': o}
		

def special(i):
	if i == None: return {'special': []}
	special = ['DV1', 'DV2', 'DR1', 'DR2', 'INCOM1', 'INCOM2', 'FABCOM1', 'FABCOM2', 'CONTAM', 'ALOG', 'PSV', 'AB', 'AG', 'COP', 'MOR', 'PER', 'CP']
	l = i.split(",")
	for item in l:
		if item not in special:
			return None
	return{'special': l}

def movement(det):
	t = {'M':0, 'FM':0, 'm':0}
	ap = {'a':0, 'p':0}
	mD = []
	for d in t:
		for s in ap:
			mD.append(str(d+s))
		mD.append(str(d+'a-p'))
	ap.update({'Ma':0, 'Mp':0})
	#separate nonmovement determinants
	o = []
	movement = []
	for d in det:
		if d[-1] not in ['a','p']:
			o.append(d)
		else:
			movement.append(d)
	#deal with a-p
	for d in movement:
		if d.endswith('a-p'):
			ap['a'] += 1
			ap['p'] += 1
			if d.startswith('M'):
				ap['M'+'a'] += 1
				ap['M'+'p'] += 1
			o.append(d.replace('a-p', ''))
		else:
			ap[d[-1]] += 1
			if d.startswith('M'): ap['M'+d[-1]] += 1
			o.append(d[:-1])
	return o,ap

def zValue(card,zScore):
	zValues= {
		'I':{'ZW': 1.0,'ZA': 4.0,'ZD': 6.0,'ZS': 3.5},
		"II":{'ZW': 4.5,'ZA': 3.0,'ZD': 6.0,'ZS': 3.5},
		"III":{'ZW': 5.5,'ZA': 3.0,'ZD': 4.0,'ZS': 4.5},
		"IV":{'ZW': 2.0,'ZA': 4.0,'ZD': 3.5,'ZS': 5.0},
		"V":{'ZW': 1.0,'ZA': 2.5,'ZD': 5.0,'ZS': 4.0},
		"VI": {'ZW': 2.5,'ZA': 2.5,'ZD': 6.0,'ZS': 6.5},
		"VII": {'ZW': 2.5,'ZA': 1.0,'ZD': 3.0,'ZS': 4.0},
		"VIII": {'ZW': 4.5,'ZA': 3.0,'ZD': 3.0,'ZS': 4.0},
		"IX": {'ZW': 5.5,'ZA': 2.5,'ZD': 4.5,'ZS': 5.0},
		"X": {'ZW': 5.5,'ZA': 4.0,'ZD': 4.5,'ZS': 6.0}}
	return zValues[card][zScore]