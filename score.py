from codes import Card, DevelopmentalQuality, Location, Determinants, FormQuality, Contents, ZScore, SpecialScores


class Score:
    def __init__(self, data):
        self.data = data
        self.card = Card(data[0])
        self.location = Location(data[1])
        self.developmental_quality = DevelopmentalQuality(data[1])
        self.location_number = data[2]
        self.determinants = Determinants(data[3], data[4])
        self.form_quality = FormQuality(data[3])
        self.contents = Contents(data[5])
        self.popular = True if data[6] == 'P' else False
        self.z_score = ZScore(data[7] or '')
        self.special_scores = SpecialScores(data[8])

    def __str__(self):
        return ''.join([
            str(self.card), ' ',
            str(self.location), str(self.location_number), str(self.developmental_quality), ' ',
            '2 ' if '(2)' in self.determinants else '',
            str(self.determinants),
            str(self.form_quality), ' ',
            str(self.contents), ' ',
            'P ' if self.popular else '',
            str(self.z_score) + ' ' if self.z_score else '',
            str(self.special_scores) + ' ' if self.special_scores else '',
        ])

    # @property
    # def z_value(self):
    #     z_values = [
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
    #     ]
    #     return None