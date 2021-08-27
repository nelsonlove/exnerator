from codes import Determinants
from score import Score


class Record:
    def __init__(self, data):
        self.scores = [Score(row) for row in data]

    def all(self, attribute):
        return [item for score in self.scores
                for item in getattr(score, attribute).value]

    def tallies(self, attribute):
        tally_dict = {k: 0 for k in self.all(attribute)}
        for k in self.all(attribute):
            tally_dict[k] += 1
        return tally_dict

    def tally(self, attribute, *codes):
        cls = getattr(self.scores[0], attribute)
        tally = 0
        for code in codes:
            index = cls.index(code)
            tally += self.tallies(attribute)[index]
        return tally

    @property
    def r(self):
        """Number of Responses:
        Number of responses in the record"""
        return len(self.scores)

    @property
    def l(self):
        """Lambda:
        Ratio of pure F to all other determinants"""
        f = self.tally('determinants', 'F')
        return f / (self.r - f)

    @property
    def w_sum_c(self):
        """Weighted Sum Color:
        Weighted sum of chromatic color determinants"""
        fc = self.tally('determinants', 'FC')
        cf = self.tally('determinants', 'CF')
        c = self.tally('determinants', 'C')
        return fc * 0.5 + cf + c * 1.5

    @property
    def sum_M(self):
        """Sum of human movement determinants"""
        return self.tally('determinants', 'Ma', 'Mp', 'Ma-p')

    @property
    def EB(self):
        """Erlebnistypus:
        Ratio of human movement to chromatic color determinants"""
        return self.sum_M / self.w_sum_c

    @property
    def ea(self):
        """Experience Actual:
        Sum of human movement and chromatic color determinants"""
        return self.sum_M + self.w_sum_c

    @property
    def EB_per(self):
        """EB Pervasive:
        Ratio measuring dominance of EB style"""
        if not all([
            self.ea >= 4,
            self.l < 1,
            any([
                self.ea <= 10 and abs(self.sum_M - self.w_sum_c) >= 2,
                self.ea > 10 and abs(self.sum_M - self.w_sum_c) >= 2.5
            ])
        ]):
            return max(self.sum_M, self.w_sum_c) / min(self.sum_M, self.w_sum_c)
        return None

    @property
    def sum_ac(self):
        """Sum of achromatic color determinants"""
        return self.tally('determinants', "FC'", "C'F", "C'")

    @property
    def sum_FM(self):
        """Sum of achromatic color determinants"""
        return self.tally('determinants', 'FMa', 'FMp', 'FMa-p')

    @property
    def sum_m(self):
        """Sum of inanimate movement determinants"""
        return self.tally('determinants', 'ma', 'mp', 'ma-p')

    @property
    def sum_FMm(self):
        """Sum of nonhuman movement determinants"""
        return self.sum_FM + self.sum_m

    @property
    def sum_t(self):
        """Sum of texture determinants"""
        return self.tally('determinants', 'TF', 'FT', 'T')

    @property
    def sum_v(self):
        """Sum of vista determinants"""
        return self.tally('determinants', 'VF', 'FV', 'V')

    @property
    def sum_y(self):
        """Sum of diffuse shading determinants"""
        return self.tally('determinants', 'YF', 'FY', 'Y')

    @property
    def sum_shd(self):
        """Sum of all shading determinants"""
        return self.sum_t + self.sum_v + self.sum_y

    @property
    def eb(self):
        """Experience Base:
        Ratio of nonhuman movement to shading and achromatic determinants"""
        return self.sum_FMm / self.sum_shd + self.sum_ac

    @property
    def es(self):
        """Experienced Stimulation:
        Sum of nonhuman movement, shading, and achromatic determinants"""
        return self.sum_FMm + self.sum_shd + self.sum_ac

    @property
    def adj_es(self):
        """Adjusted es:
        Experienced Stimulation adjusted for situational phenomena"""
        return self.es - max(1, (self.sum_m - 1)) - max(1, (self.sum_y - 1))

    @staticmethod
    def calc_d(d):
        for min_, max_, score in (
            (13, 999, 5),
            (10.5, 12.5, 4),
            (8.0, 10.0, 3),
            (5.5, 7.5, 2),
            (3.0, 5.0, 1),
            (-2.5, 2.5, 0),
            (-5.0, -3.0, -1),
            (-7.5, -5.5, -2),
            (-10.0, -8.0, -3),
            (-12.5, -10.5, -4),
            (-999, -13.0, -5)
        ):
            if min_ <= d <= max_:
                return score

    @property
    def d(self):
        """D Score:
        Scaled difference between Experience Actual and Experienced Stimulation"""
        return self.calc_d(self.ea - self.es)

    @property
    def adj_d(self):
        """Adjusted D:
        D score adjusted for situational phenomena"""
        return self.calc_d(self.ea - self.adj_es)

# import parse_old as Parse
# from table import Columns, Table
#
#
# class Score:
#     def __init__(self, d):
#         self.__dict__.update(d)
#         self.form = Parse.form(self.locType, self.formQuality)
#         print(self.form)
#         self.iso = self.isolate()
#         self.rawDeterminants = self.determinants
#         self.determinants, self.movement = Parse.movement(self.rawDeterminants)
#         if self.zScore:
#             self.zValue = Parse.zValue(self.card, self.zScore)
#         else:
#             self.zValue = None
#         self.humanCheck()
#
#     def isolate(self):
#         iso = 0
#         for d in self.determinants:
#             if d in ['Bt', 'Ge', 'Ls']:
#                 self.iso += 1
#             elif d in ['Na', 'Cl']:
#                 iso += 2
#         return iso
#
#     def __str__(self):
#         out = []
#         out.append(self.locType)
#         out.append(self.devQuality)
#         if self.locNum > 1: out.append(str(self.locNum))
#         out.extend([' ', '.'.join(self.rawDeterminants)])
#         if self.formQuality: out.extend(self.formQuality)
#         out.extend(' ')
#         if self.pair: out.extend(['2', ' '])
#         out.extend([','.join(self.contents), ' '])
#         if self.popular: out.extend(['P', ' '])
#         if self.zValue: out.extend([self.zValue, ' '])
#         if self.special != '':
#             out.extend(','.join(self.special))
#         return ''.join(out)
#
#     def humanCheck(self):
#         if "H" in self.contents or \
#                 "M" in self.determinants or \
#                 "FM" in self.determinants and any(item in ['COP', 'AG'] for item in self.special):
#             ruleouts = ["AG", "MOR", "DR1", "DR2", "FABCOM1",
#                         "FABCOM2", "INCOM1", "INCOM2", "ALOG", "CONTAM"]
#             if 'appropriate' in self.form and \
#                     "H" in self.contents and \
#                     not any(item in ruleouts for item in self.special):
#                 self.special.append('GHR')
#             elif 'appropriate' not in self.form or \
#                     any(item in ["DV2", "DR2", "INCOM2", "FABCOM2", "CONTAM", "ALOG"] for item in self.special):
#                 self.special.append('PHR')
#             elif "COP" in self.special and "AG" not in self.special:
#                 self.special.append('GHR')
#             elif any(item in ["FABCOM1", "FABCOM2", "MOR"] for item in self.special) or \
#                     "An" in self.contents:
#                 self.special.append('PHR')
#             elif self.popular == True and self.card in ["III", "IV", "VII", "IX"]:
#                 self.special.append('GHR')
#             elif any(item in ["AG", "INCOM1", "INCOM2", "DR1", "DR2"] for item in self.special) or \
#                     "Hd" in self.contents:
#                 self.special.append('PHR')
#             else:
#                 self.special.append('GHR')
#
#
# class Record:
#     def __init__(self, data):
#         self.scores = []
#         for row in data:
#             self.scores.append(self.Score(row))

#
#     def table(self):
#         dtype = ['t', 'i', 't', 't', 'i', 't', 't', 't', 't', 't', 't', 't']
#         align = ["l", "l", "l", "l", "l", "l", "l", "c", "l", "c", "c", "l"]
#         chars = ['', '', '', '=']
#         header = ["Card", "#", "Loc", "DQ", "Loc#", "Det", "FQ", "2", "Cont", "Pop", "Z", "Spec"]
#         rows = []
#         for i, score in enumerate(self.scores):
#             row = [score.card]
#             if i > 0:
#                 if score.card == self.scores[i - 1].card:
#                     row = [' ']
#             row.append(i + 1)
#             row.append(score.locType)
#             row.append(score.devQuality)
#             row.append(score.locNum)
#             row.append('.'.join(score.rawDeterminants))
#             row.append(score.formQuality)
#             if score.pair == True:
#                 row.append('2')
#             else:
#                 row.append('')
#             row.append(','.join(score.contents))
#             if score.popular == True:
#                 row.append('P')
#             else:
#                 row.append('')
#             if score.zValue:
#                 row.append(score.zValue)
#             else:
#                 row.append('')
#             row.append(','.join(score.special))
#             rows.append(row)
#         return Table(
#             rows, None, name="Sequence of Scores", header=header,
#             align=align, dtype=dtype, chars=chars).out
#
#     def __str__(self):
#         data = {}
#         layout = []
#         for i, v in enumerate(self.scores):
#             n = str(i + 1) + '.'
#             data.update({n: str(v)})
#             layout.append(n)
#         return Columns(data, [layout], name="Sequence of Scores",
#                        align=['r', 'l'], dtype=['t', 't']).out
#
#
