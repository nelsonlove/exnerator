from .enums import Card, ZScore

z_values = {
    Card.I: {
        ZScore.WHOLE_RESPONSE: 1.0,
        ZScore.ADJACENT_OBJECTS: 4.0,
        ZScore.DISTANT_OBJECTS: 6.0,
        ZScore.INTEGRATED_WHITE_SPACE: 3.5
    },
    Card.II: {
        ZScore.WHOLE_RESPONSE: 4.5,
        ZScore.ADJACENT_OBJECTS: 3.0,
        ZScore.DISTANT_OBJECTS: 6.0,
        ZScore.INTEGRATED_WHITE_SPACE: 3.5
    },
    Card.III: {
        ZScore.WHOLE_RESPONSE: 5.5,
        ZScore.ADJACENT_OBJECTS: 3.0,
        ZScore.DISTANT_OBJECTS: 4.0,
        ZScore.INTEGRATED_WHITE_SPACE: 4.5
    },
    Card.IV: {
        ZScore.WHOLE_RESPONSE: 2.0,
        ZScore.ADJACENT_OBJECTS: 4.0,
        ZScore.DISTANT_OBJECTS: 3.5,
        ZScore.INTEGRATED_WHITE_SPACE: 5.0
    },
    Card.V: {
        ZScore.WHOLE_RESPONSE: 1.0,
        ZScore.ADJACENT_OBJECTS: 2.5,
        ZScore.DISTANT_OBJECTS: 5.0,
        ZScore.INTEGRATED_WHITE_SPACE: 4.0
    },
    Card.VI: {
        ZScore.WHOLE_RESPONSE: 2.5,
        ZScore.ADJACENT_OBJECTS: 2.5,
        ZScore.DISTANT_OBJECTS: 6.0,
        ZScore.INTEGRATED_WHITE_SPACE: 6.5
    },
    Card.VII: {
        ZScore.WHOLE_RESPONSE: 2.5,
        ZScore.ADJACENT_OBJECTS: 1.0,
        ZScore.DISTANT_OBJECTS: 3.0,
        ZScore.INTEGRATED_WHITE_SPACE: 4.0
    },
    Card.VIII: {
        ZScore.WHOLE_RESPONSE: 4.5,
        ZScore.ADJACENT_OBJECTS: 3.0,
        ZScore.DISTANT_OBJECTS: 3.0,
        ZScore.INTEGRATED_WHITE_SPACE: 4.0
    },
    Card.IX: {
        ZScore.WHOLE_RESPONSE: 5.5,
        ZScore.ADJACENT_OBJECTS: 2.5,
        ZScore.DISTANT_OBJECTS: 4.5,
        ZScore.INTEGRATED_WHITE_SPACE: 5.0
    },
    Card.X: {
        ZScore.WHOLE_RESPONSE: 5.5,
        ZScore.ADJACENT_OBJECTS: 4.0,
        ZScore.DISTANT_OBJECTS: 4.5,
        ZScore.INTEGRATED_WHITE_SPACE: 6.0
    },
}

z_est = [0,
         0, 2.5, 6.0, 10.0, 13.5,
         17.0, 20.5, 24.0, 27.5, 31.0,
         34.5, 38.0, 41.5, 45.5, 49.0,
         52.5, 56.0, 59.5, 63.0, 66.5,
         70.0, 73.5, 77.0, 81.0, 84.5,
         88.0, 91.5, 95.0, 98.5, 102.5,
         105.5, 109.5, 112.5, 116.5, 120.0,
         123.5, 127.0, 130.5, 134.0, 137.5,
         141.0, 144.5, 148.0, 152.0, 155.5,
         159.0, 162.5, 166.0, 169.5, 173.0]


age_adjusted_egocentricity_index_cutoffs = {
    5: (0.55, 0.83),
    6: (0.52, 0.82),
    7: (0.52, 0.77),
    8: (0.48, 0.74),
    9: (0.47, 0.69),
    10: (0.47, 0.61),
    11: (0.46, 0.58),
    12: (0.46, 0.58),
    13: (0.41, 0.55),
    14: (0.37, 0.54),
    15: (0.33, 0.50),
    16: (0.33, 0.48),
}

age_adjusted_WSum6_cutoffs = {
    5: (16, 20),
    6: (16, 20),
    7: (16, 20),
    8: (15, 19),
    9: (15, 19),
    10: (15, 19),
    11: (14, 18),
    12: (14, 18),
    13: (14, 18),
}

age_adjusted_Afr = {
    5: 0.57,
    6: 0.57,
    7: 0.55,
    8: 0.55,
    9: 0.55,
    10: 0.53,
    11: 0.53,
    12: 0.53,
    13: 0.53,
}