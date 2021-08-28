from . import lookup
from .enums import FQ, Content, Special, Determinant, Card, ZScore

from decimal import Decimal


def d_score(score):
    for min_, max_, d in (
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
        if min_ <= score <= max_:
            return d


def human_representation(response):
    """Assigns good or poor designations to human representational responses.
    From Table 10, p. 77:
        1. Score GHR for answers containing a Pure H coding that also have all of the following:
            (a) Form Quality of FQ+, FQo or FQu
            (b) No cognitive special scores except DV
            (c) No special scores of AG or MOR
        2. Score PHR for answers that have either:
            (a) FQ minus or FQnone (No Form), or
            (b) FQ+, FQo or FQu and have an ALOG, CONTAM, or any Level 2 cognitive special score
        3. Score GHR for any remaining human representational answers that have the special score COP, but do not have
        the special score AG
        4. Score PHR for any remaining human representational answers that have either:
            (a) The special scores FABCOM or MOR
            (b) The content score An
        5. Score GHR for any remaining human representational answers to Cards III, IV, VII, and IX that are coded
        Popular
        6. Score PHR for any remaining human representional answers that have any of the following:
            (a) The special scores AG, INCOM, or DR
            (b) An Hd coding [**not** (Hd) coding]
        7. Score GHR for all remaining human representational answers

    ---

    These steps are followed in order until a coding decision is made. Assume, for instance, that an answer is coded
    Do Fo H. It meets the criteria listed in Step 1 for GHR. It is a Pure H response, with o form quality, and has no
    Special Scores. Conversely, if the coding were Do Fo Hd, the decision would not be made at Step 1 because the
    content is Hd, rather than Pure H. The answer would finally be classified as PHR at Step 6 because of the Hd
    content coding. Other illustrations, showing the step at which the coding decision is made, are shown below:

    | Card | Response Coding                 | GHR/PHR Decision    |
    | :--- | :------------------------------ | :------------------ |
    | III  | D+ Ma.FYo 2 H,Cg P 3.0 FABCOM   | Coded GHR at Step 7 |
    | IX   | DSo FC’o (Hd)                   | Coded PHR at Step 2 |
    | VIII | W+ FMa.FCo 2 A,Bt 4.5 COP, ALOG | Coded GHR at Step 5 |
    | VII  | D+ Ma.mpo 2 Hd, Art P 3.0 DV    | Coded PHR at Step 4 |
    """

    if not any([
        any(content in [
            Content.WHOLE_HUMAN,
            Content.WHOLE_HUMAN_FICTIONAL,
            Content.HUMAN_DETAIL,
            Content.HUMAN_DETAIL_FICTIONAL,
            Content.HUMAN_EXPERIENCE,
        ] for content in response.contents),
        any(determinant in [
            Determinant.MOVEMENT_HUMAN_ACTIVE,
            Determinant.MOVEMENT_HUMAN_PASSIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE,
        ] for determinant in response.determinants),
        all([
            any(determinant in [
                Determinant.MOVEMENT_ANIMAL_ACTIVE,
                Determinant.MOVEMENT_ANIMAL_PASSIVE,
                Determinant.MOVEMENT_ANIMAL_ACTIVE_PASSIVE,
            ] for determinant in response.determinants),
            any(special in [
                Special.AGGRESSIVE_MOVEMENT,
                Special.COOPERATIVE_MOVEMENT
            ] for special in response.special)
        ])
    ]):
        return None

    # 1. Score GHR for answers containing a Pure H coding that also have all of the following:
    #     (a) Form Quality of FQ+, FQo or FQu
    #     (b) No cognitive special scores except DV
    #     (c) No special scores of AG or MOR

    if Content.WHOLE_HUMAN in response.contents and all([
        response.fq not in (FQ.MINUS, FQ.NONE),
        not any(item in [
                Special.DEVIANT_VERBALIZATION_2,
                Special.DEVIANT_RESPONSE_1,
                Special.DEVIANT_RESPONSE_2,
                Special.INCONGRUOUS_COMBINATION_1,
                Special.INCONGRUOUS_COMBINATION_2,
                Special.FABULIZED_COMBINATION_1,
                Special.FABULIZED_COMBINATION_2,
                Special.CONTAMINATION,
                Special.INAPPROPRIATE_LOGIC,
                Special.AGGRESSIVE_MOVEMENT,
                Special.MORBID_CONTENT
            ] for item in response.special)]):
        return Special.HUMAN_REPRESENTATION_GOOD

    # 2. Score PHR for answers that have either:
    #     (a) FQ minus or FQnone (No Form), or
    #     (b) FQ+, FQo or FQu and have an ALOG, CONTAM, or any Level 2 cognitive special score

    elif response.fq in (FQ.MINUS, FQ.NONE) or any(item in [
                Special.INAPPROPRIATE_LOGIC,
                Special.CONTAMINATION,
                Special.DEVIANT_VERBALIZATION_2,
                Special.DEVIANT_RESPONSE_2,
                Special.INCONGRUOUS_COMBINATION_2,
                Special.FABULIZED_COMBINATION_2
            ] for item in response.special):
        return Special.HUMAN_REPRESENTATION_POOR

    # 3. Score GHR for any remaining human representational answers that have the special score COP, but do not have
    # the special score AG

    elif Special.COOPERATIVE_MOVEMENT in response.special and Special.AGGRESSIVE_MOVEMENT not in response.special:
        return Special.HUMAN_REPRESENTATION_GOOD

    # 4. Score PHR for any remaining human representational answers that have either:
    #     (a) The special scores FABCOM or MOR
    #     (b) The content score An

    elif any(item in [
        Special.FABULIZED_COMBINATION_1,
        Special.FABULIZED_COMBINATION_2,
        Special.MORBID_CONTENT
    ] for item in response.special) and Content.ANATOMY in response.contents:
        return Special.HUMAN_REPRESENTATION_POOR

    # 5. Score GHR for any remaining human representational answers to Cards III, IV, VII, and IX that are coded
    # Popular

    elif response.card in [
        Card.III,
        Card.IV,
        Card.VII,
        Card.IX
    ] and response.popular:
        return Special.HUMAN_REPRESENTATION_GOOD

    # 6. Score PHR for any remaining human representional answers that have any of the following:
    #     (a) The special scores AG, INCOM, or DR
    #     (b) An Hd coding [**not** (Hd) coding]

    elif any(item in [
        Special.AGGRESSIVE_MOVEMENT,
        Special.INCONGRUOUS_COMBINATION_1,
        Special.INCONGRUOUS_COMBINATION_2,
        Special.DEVIANT_RESPONSE_1,
        Special.DEVIANT_RESPONSE_2,
    ] for item in response.special) or Content.HUMAN_DETAIL in response.contents:
        return Special.HUMAN_REPRESENTATION_POOR

    else:
        return Special.HUMAN_REPRESENTATION_GOOD
