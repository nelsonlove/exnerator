import ui

version = 2.3

import sys

from file import File
from table2 import print_score_table
from score import Score
from record import Record

#
# import load


# from record import Record


def main():
    ui.splash(version)
    if len(sys.argv) < 2:
        filename = ui.chooseFile("No file specified!")
    else:
        filename = sys.argv[1]

    #	r = test.Record(filename)

    # data = load.Excel(filename)
    data = File.load_from_excel(filename)
    print("Successfully parsed record!")

    record = Record(data)

    # if ui.ask("Print response table?"):
    #     ui.clear()
    #     print_score_table(data)
    # print(record.contents())
    print(record.tallies('determinants'))
    # print(record.r)
    # print(record.l)
    # if ui.ask("Calculate structural summary?"):
        # s = structuralSummary.calc(r)


if __name__ == "__main__":
    main()
