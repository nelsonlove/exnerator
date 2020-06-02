#!/usr/bin/python
#Exnerator 2.2

version = 2.2

import ui
import sys
import load
from record import Record

def main():
	ui.splash(version)
	if len(sys.argv) < 2:
		filename = ui.chooseFile("No file specified!")
	else:
		filename = sys.argv[1]

	#	r = test.Record(filename)

	data = load.Excel(filename)
	print("Successfully parsed record!")
	r = Record(data)

	if ui.ask("Print response table?"):
		ui.clear()
		print(r.table())
	if ui.ask("Calculate structural summary?"):
		s = structuralSummary.calc(r)
			
if __name__ == "__main__":
	main()