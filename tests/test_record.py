from unittest import TestCase

from src.exnerator.enums import DQ, Determinant
from src.exnerator.file import ExcelFile
from src.exnerator.record import Record

from decimal import Decimal


# noinspection PyPep8Naming,SpellCheckingInspection
class TestRecord(TestCase):
    def setUp(self):
        file = ExcelFile('valid.xlsx')
        self.record = Record(file.data, 19)

    def test_count(self):
        self.assertEqual(9, self.record.count(DQ.ORDINARY))

    def test_Zf(self):
        self.assertEqual(15, self.record.Zf)

    def test_ZSum(self):
        self.assertEqual(51.0, self.record.ZSum)

    def test_Zest(self):
        self.assertEqual(49.0, self.record.Zest)

    def test_W(self):
        self.assertEqual(10, self.record.W)

    def test_D(self):
        self.assertEqual(5, self.record.D)

    def test_W_D(self):
        self.assertEqual(15, self.record.W_D)

    def test_Dd(self):
        self.assertEqual(2, self.record.Dd)

    def test_S(self):
        self.assertEqual(5, self.record.S)

    def test_Mminus(self):
        self.assertEqual(1, self.record.Mminus)

    def test_WSum6(self):
        self.assertEqual(3, self.record.WSum6)

    def test_L(self):
        expected = Decimal(0.55).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.L)

    def test_WSumC(self):
        expected = Decimal(4.0).quantize(Decimal('1.0'))
        self.assertEqual(expected, self.record.WSumC)

    def test_SumM(self):
        self.assertEqual(7, self.record.SumM)

    def test_EB(self):
        self.assertEqual((7, 4.0), self.record.EB)

    def test_EA(self):
        expected = Decimal(11.0).quantize(Decimal('1.0'))
        self.assertEqual(expected, self.record.EA)

    def test_EBPer(self):
        expected = Decimal(1.8).quantize(Decimal('1.0'))
        self.assertEqual(expected, self.record.EBPer)

    def test_SumFM(self):
        self.assertEqual(1, self.record.SumFM)

    def test_Sum_m(self):
        self.assertEqual(0, self.record.Sum_m)

    def test_SumFMm(self):
        self.assertEqual(1, self.record.SumFMm)

    def test_SumAC(self):
        self.assertEqual(0, self.record.SumAC)

    def test_SumT(self):
        self.assertEqual(0, self.record.SumT)

    def test_SumV(self):
        self.assertEqual(1, self.record.SumV)

    def test_SumY(self):
        self.assertEqual(1, self.record.SumY)

    def test_SumShd(self):
        self.assertEqual(2, self.record.SumShd)

    def test_eb(self):
        self.assertEqual((1, 2), self.record.eb)

    def test_es(self):
        self.assertEqual(3, self.record.es)

    def test_D_score(self):
        self.assertEqual(3, self.record.D_score)

    def test_Adj_es(self):
        self.assertEqual(3, self.record.Adj_es)

    def test_AdjD(self):
        self.assertEqual(3, self.record.AdjD)

    def test_a_p(self):
        self.assertEqual((6, 2), self.record.a_p)

    def test_Ma_Mp(self):
        self.assertEqual((5, 2), self.record.Ma_Mp)

    def test_Art_Ay(self):
        self.assertEqual(5, self.record.Art_Ay)

    def test_form_color_ratio(self):
        self.assertEqual((3, 2), self.record.form_color_ratio)

    def test_constriction_ratio(self):
        expected_WSumC = Decimal(4.0).quantize(Decimal('1.0'))
        self.assertEqual((0, expected_WSumC), self.record.constriction_ratio)

    def test_Afr(self):
        expected = Decimal(0.55).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.Afr)

    def test_blends(self):
        expected_blends = [
            [Determinant.MOVEMENT_HUMAN_PASSIVE, Determinant.COLOR_FORM],
            [Determinant.MOVEMENT_HUMAN_ACTIVE, Determinant.FORM_SHADING],
            [Determinant.MOVEMENT_ANIMAL_ACTIVE, Determinant.FORM_REFLECTION, Determinant.FORM_COLOR],
            [Determinant.FORM_COLOR, Determinant.FORM_VISTA],
            [Determinant.MOVEMENT_HUMAN_ACTIVE, Determinant.PURE_COLOR]
        ]
        self.assertEqual(expected_blends, self.record.blends)

    def test_BlendsR(self):
        self.assertEqual((5, 17), self.record.BlendsR)

    def test_XApercent(self):
        expected = Decimal(0.71).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.XApercent)

    def test_WDApercent(self):
        expected = Decimal(0.80).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.WDApercent)

    def test_Xminus(self):
        expected = Decimal(0.24).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.Xminus)

    def test_P(self):
        self.assertEqual(5, self.record.P)

    def test_Xplus(self):
        expected = Decimal(0.53).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.Xplus)

    def test_Xu(self):
        expected = Decimal(0.18).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.Xu)

    def test_economy_index(self):
        expected = (10, 5, 2)
        self.assertEqual(expected, self.record.economy_index)

    def test_aspirational_ratio(self):
        expected = (10, 7)
        self.assertEqual(expected, self.record.aspirational_ratio)

    def test_Zd(self):
        expected = Decimal(2.0).quantize(Decimal('1.0'))
        self.assertEqual(expected, self.record.Zd)

    def test_human_cont(self):
        self.assertEqual(8, self.record.human_cont)

    def test_isolate_R(self):
        expected = Decimal(0.18).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.isolate_R)

    def test_egocentricity_index(self):
        expected = Decimal(0.35).quantize(Decimal('1.00'))
        self.assertEqual(expected, self.record.egocentricity_index)

    def test_s_constellation(self):
        self.assertEqual((False, 3), self.record.s_constellation)

    def test_DEPI(self):
        self.assertEqual((True, 5), self.record.DEPI)

    def test_HVI(self):
        self.assertEqual((True, 6), self.record.HVI)

    def test_PTI(self):
        self.assertEqual(0, self.record.PTI)

    def test_CDI(self):
        self.assertEqual((False, 1), self.record.CDI)

    def test_OBS(self):
        self.assertEqual((False, 1), self.record.OBS)
