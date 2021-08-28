from src.exnerator import parse, calculate
from src.exnerator.enums import Determinant


class Response:
    def __init__(self, data):
        self.data = data

        self.card = parse.card(data[0])

        self.location = parse.location(data[1])

        self.dq = parse.dq(data[1])

        self.location_number = data[2]

        self.determinants = parse.determinants(data[3])
        if str(data[4]) == '2':
            self.determinants.append(Determinant.PAIR)

        self.fq = parse.fq(data[3])

        self.contents = parse.contents(data[5])

        self.popular = True if data[6] == 'P' else False

        self.z_score = parse.z_score(data[7] or '')

        self.special = parse.special(data[8] or '')
        human_representation = calculate.human_representation(self)
        if human_representation:
            self.special.add(human_representation)

    @property
    def codes(self):
        return {
            self.card,
            self.location,
            self.dq,
            self.fq,
            self.z_score
        }.union(
            set(self.determinants),
            self.contents,
            self.special
        )

    def __contains__(self, code):
        return code in self.codes

    #
    # def __str__(self):
    #     return ''.join([
    #         str(self.card), ' ',
    #         str(self.location), str(self.location_number), str(self.developmental_quality), ' ',
    #         '2 ' if '(2)' in self.determinants else '',
    #         str(self.determinants),
    #         str(self.form_quality), ' ',
    #         str(self.contents), ' ',
    #         'P ' if self.popular else '',
    #         str(self.z_score) + ' ' if self.z_score else '',
    #         str(self.special_scores) + ' ' if self.special_scores else '',
    #     ])
    #
    # @property
    # def z_value(self):
    #     z_values = {
    #         [1.0, 4.0, 6.0, 3.5],
    #         [4.5, 3.0, 6.0, 3.5],
    #         [5.5, 3.0, 4.0, 4.5],
    #         [2.0, 4.0, 3.5, 5.0],
    #         [1.0, 2.5, 5.0, 4.0],
    #         [2.5, 2.5, 6.0, 6.5],
    #         [2.5, 1.0, 3.0, 4.0],
    #         [4.5, 3.0, 3.0, 4.0],
    #         [5.5, 2.5, 4.5, 5.0],
    #         [5.5, 4.0, 4.5, 6.0]
    #     }
    #     if self.z_score:
    #         return z_values[self.card.value][self.z_score.value + 1]
    #     return None