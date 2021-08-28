from pathlib import Path
from unittest import TestCase
from src.exnerator.file import ExcelFile
from src.exnerator.exceptions import InvalidColumnsError, NoResponsesError


class TestExcelFile(TestCase):
    def setUp(self):
        self.valid_file = ExcelFile('valid.xlsx')
        self.missing_col = Path('missing_cols.xlsx')
        self.extra_col = Path('extra_cols.xlsx')
        self.no_responses = Path('no_responses.xlsx')

    def test_open(self):
        self.assertEqual(len(self.valid_file.data), 17)

    def test_validate_columns(self):
        self.assertRaises(InvalidColumnsError, ExcelFile, self.missing_col)
        self.assertRaises(InvalidColumnsError, ExcelFile, self.extra_col)

    def test_validate_responses(self):
        self.assertRaises(NoResponsesError, ExcelFile, self.no_responses)

    def test_columns(self):
        self.assertEqual(self.valid_file.columns, 9)

    def test_responses(self):
        self.assertEqual(self.valid_file.responses, len(self.valid_file.data))

    def test_data(self):
        self.assertEqual(self.valid_file.data[0][0], 'I')
