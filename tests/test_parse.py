from unittest import TestCase
from src.exnerator import enums
from src.exnerator import parse
from src.exnerator import exceptions


class Test(TestCase):
    def test_match(self):
        self.assertEqual(parse.match('Ma-p', enums.Determinant), enums.Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE)
        self.assertRaises(exceptions.CodeError, parse.match, 'asdf', enums.Determinant)

    def test_match_multiple(self):
        self.assertEqual(parse.match_multiple('TF.Ma-p', enums.Determinant, delimiter='.'),
                         {enums.Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE,
                          enums.Determinant.TEXTURE_FORM})
        self.assertRaises(exceptions.CodeError, parse.match_multiple, 'asdf.TF', enums.Determinant, delimiter='.')
        self.assertRaises(exceptions.CodeError, parse.match_multiple, 'TF.Ma-p', enums.Determinant, delimiter=',')

    def test_card(self):
        self.assertEqual(parse.card('IX'), enums.Card.IX)
        self.assertNotEqual(parse.card('X'), enums.Card.IX)

    def test_dq(self):
        self.assertEqual(parse.dq('Wo'), enums.DQ.ORDINARY)
        self.assertNotEqual(parse.dq('Wv'), enums.DQ.ORDINARY)

    def test_location(self):
        self.assertEqual(parse.location('Wo'), enums.Location.WHOLE)
        self.assertEqual(parse.location('WSo'), enums.Location.WHOLE_WHITESPACE)
        self.assertEqual(parse.location('DdSo'), enums.Location.DETAIL_UNUSUAL_WHITESPACE)
        self.assertNotEqual(parse.location('Ddv'), enums.Location.WHOLE)

    def test_determinants(self):
        self.assertEqual(parse.determinants('TF.FC'), [enums.Determinant.TEXTURE_FORM, enums.Determinant.FORM_COLOR])
        self.assertEqual(parse.determinants('TF.FC-'), [enums.Determinant.TEXTURE_FORM, enums.Determinant.FORM_COLOR])

    def test_fq(self):
        self.assertEqual(parse.fq('TF.FC-'), enums.FQ.MINUS)
        self.assertEqual(parse.fq('TF.FC'), enums.FQ.NONE)
        self.assertEqual(parse.fq('F-'), enums.FQ.MINUS)
        self.assertEqual(parse.fq('Mp.CF-'), enums.FQ.MINUS)

    def test_contents(self):
        self.assertEqual(parse.contents('H,Hh'), {enums.Content.WHOLE_HUMAN, enums.Content.HOUSEHOLD})

    def test_z_score(self):
        self.assertEqual(parse.z_score(''), enums.ZScore.NONE)
        self.assertEqual(parse.z_score('ZA'), enums.ZScore.ADJACENT_OBJECTS)

    def test_special(self):
        self.assertEqual(parse.special('MOR,AB'), {enums.Special.MORBID_CONTENT, enums.Special.ABSTRACT_CONTENT})