from unittest import TestCase
from decimal import Decimal


from src.exnerator.file import ExcelFile
from src.exnerator.record import Record
from src.exnerator import calculate
from src.exnerator.enums import DQ


class TestCalculate(TestCase):
    def setUp(self):
        file = ExcelFile('valid.xlsx')
        self.record = Record(file.data)
    #
    # def test_L(self):
    #     expected = Decimal(0.55).quantize(Decimal('1.00'))
    #     self.assertEqual(expected, calculate.L(self.record))
    #
    # def test_w_sum_c(self):
    #     self.assertEqual(4.0, calculate.w_sum_c(self.record))

    # def test_EB_per(self):
    #     """From Exner p. 94:
    #     In the sample protocol, EA = 11.0, Lambda = 0.55, and the difference between the two values in the EB is 3.0.
    #     Thus, the larger EB value of 7 is divided by the smaller, 4.0, with a result of 1.8."""
    #     self.assertEqual(1.8, calculate.EB_per(self.record, DQ.ORDINARY), 9)
