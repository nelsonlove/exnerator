from unittest import TestCase

from src.exnerator.file import ExcelFile
from src.exnerator.response import Response
from src.exnerator import enums


class TestResponse(TestCase):
    def setUp(self):
        file = ExcelFile('valid.xlsx')
        self.response = Response(file.data[0])

    def test_response(self):
        self.assertEqual(self.response.card, enums.Card.I)
        self.assertEqual(self.response.location, enums.Location.WHOLE)
        self.assertEqual(self.response.dq, enums.DQ.ORDINARY)
        self.assertEqual(self.response.location_number, 1)
        self.assertEqual(self.response.determinants, [enums.Determinant.PURE_FORM])
        self.assertEqual(self.response.fq, enums.FQ.ORDINARY)
        self.assertEqual(self.response.contents, {enums.Content.WHOLE_ANIMAL})
        self.assertEqual(self.response.popular, True)
        self.assertEqual(self.response.z_score, enums.ZScore.WHOLE_RESPONSE)
