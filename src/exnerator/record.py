from decimal import Decimal

from . import lookup, calculate
from .enums import Determinant, ZScore, Location, Special, Content, Card, FQ
from .response import Response


# noinspection PyPep8Naming,SpellCheckingInspection
class Record:
    def __init__(self, data, age):
        self.responses = [Response(row) for row in data]
        self.age = age

    def __len__(self):
        return len(self.responses)

    def __iter__(self):
        return iter(self.responses)

    def __next__(self):
        return next(self.responses)

    def count(self, *codes):
        count_ = 0
        for response in self:
            for code in codes:
                if code in response.codes:
                    count_ += 1
        return count_

    @property
    def Zf(self):
        """[T]he number of times a Z response has occurred in the record.
        (Exner p.91)"""
        return self.count(
            ZScore.WHOLE_RESPONSE,
            ZScore.ADJACENT_OBJECTS,
            ZScore.DISTANT_OBJECTS,
            ZScore.INTEGRATED_WHITE_SPACE
        )

    @property
    def ZSum(self):
        """[T]he summation of the weighted Z scores that have been assigned.
        (Exner p.91)"""
        zsum = 0
        for response in self.responses:
            if any(z_score in response
                   for z_score in [ZScore.WHOLE_RESPONSE,
                                   ZScore.ADJACENT_OBJECTS,
                                   ZScore.DISTANT_OBJECTS,
                                   ZScore.INTEGRATED_WHITE_SPACE]
                   ):
                zsum += lookup.z_values[response.card][response.z_score]
        return zsum

    @property
    def Zest(self):
        """[T]he estimated weighted Z Sum (Zest) which is derived from a Table of Estimates [...] The
        Zest value is the one that corresponds to the Zf for the protocol.
        (Exner p.91)"""
        return lookup.z_est[self.Zf]

    @property
    def W(self):
        """Each of the three basic location codes are tallied separately. An entry is also required for the frequency
        of the S responses. The S frequency is not subtracted from the tallies for the three basic location codes of W,
        D, or Dd.
        (Exner p.91)"""
        return self.count(
            Location.WHOLE,
            Location.WHOLE_WHITESPACE
        )

    @property
    def D(self):
        """Each of the three basic location codes are tallied separately. An entry is also required for the frequency
        of the S responses. The S frequency is not subtracted from the tallies for the three basic location codes of W,
        D, or Dd.
        (Exner p.91)"""
        return self.count(
            Location.DETAIL_COMMON,
            Location.DETAIL_COMMON_WHITESPACE
        )

    @property
    def W_D(self):
        """Each of the three basic location codes are tallied separately. An entry is also required for the frequency
        of the S responses. The S frequency is not subtracted from the tallies for the three basic location codes of W,
        D, or Dd.
        (Exner p.91)"""
        return self.W + self.D

    @property
    def Dd(self):
        """Each of the three basic location codes are tallied separately. An entry is also required for the frequency
        of the S responses. The S frequency is not subtracted from the tallies for the three basic location codes of W,
        D, or Dd.
        (Exner p.91)"""
        return self.count(
            Location.DETAIL_UNUSUAL,
            Location.DETAIL_UNUSUAL_WHITESPACE
        )

    @property
    def S(self):
        """Each of the three basic location codes are tallied separately. An entry is also required for the frequency
        of the S responses. The S frequency is not subtracted from the tallies for the three basic location codes of W,
        D, or Dd.
        (Exner p.91)"""
        return self.count(
            Location.WHOLE_WHITESPACE,
            Location.DETAIL_COMMON_WHITESPACE,
            Location.DETAIL_UNUSUAL_WHITESPACE
        )

    @property
    def Mminus(self):
        """Number of Human Movement responses in which form use is not commensurate with the blot features.
        (Exner p.92)"""
        return len([
            r for r in self.responses
            if any(code in r for code in [
                Determinant.MOVEMENT_HUMAN_ACTIVE,
                Determinant.MOVEMENT_HUMAN_PASSIVE,
                Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE
            ]) and FQ.MINUS in r
        ])

    @property
    def WSum6(self):
        """Weighted sum for the first six special scores (WSum6). Each of the six Special Scores receives a weight:
            WSum6 = 1 * DV
                  + 2 * DV2
                  + 2 * INCOM
                  + 4 * INCOM2
                  + 3 * DR
                  + 6 * DR2
                  + 4 * FABCOM
                  + 7 * FABCOM2
                  + 5 * ALOG
                  + 7 * CONTAM
        (Exner p.92)"""
        return sum([
            self.count(Special.DEVIANT_VERBALIZATION_1),
            2 * self.count(
                Special.DEVIANT_VERBALIZATION_2,
                Special.INCONGRUOUS_COMBINATION_1
            ),
            3 * self.count(Special.DEVIANT_RESPONSE_1),
            4 * self.count(
                Special.INCONGRUOUS_COMBINATION_2,
                Special.FABULIZED_COMBINATION_1
            ),
            5 * self.count(Special.INAPPROPRIATE_LOGIC),
            6 * self.count(Special.DEVIANT_RESPONSE_2),
            7 * self.count(
                Special.FABULIZED_COMBINATION_2,
                Special.CONTAMINATION
            )
        ])

    @property
    def L(self):
        """This is a ratio that compares the frequency of pure F responses to all other answers in the record. It
        relates to issues of economizing the use of resources. It is calculated as:
            L = F      (Number of Responses having only Pure F determinants)
              ÷ R - F  (Total R minus Pure Form answers)
        (Exner p.93)"""

        f = self.count(Determinant.PURE_FORM)

        return Decimal(
            f / (len(self) - f)
        ).quantize(Decimal('.01'))

    @property
    def WSumC(self):
        """The Weighted Sum Color (WSumC) is obtained by multiplying each type of chromatic color response by a weight.
        Color naming responses, Cn, are not included in the WSumC.
        (Exner p.93)"""

        FC = self.count(Determinant.FORM_COLOR)
        CF = self.count(Determinant.COLOR_FORM)
        C = self.count(Determinant.PURE_COLOR)

        return Decimal(
            FC * 0.5 + CF + C * 1.5
        ).quantize(Decimal('.1'))

    @property
    def SumM(self):
        """Sum of human movement determinants"""

        return self.count(
            Determinant.MOVEMENT_HUMAN_ACTIVE,
            Determinant.MOVEMENT_HUMAN_PASSIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE
        )

    @property
    def EB(self):
        """Erlebnistypus (EB). This is a relationship between two major variables, human movement (M), and the weighted
        sum of the chromatic color responses. It is entered as Sum M : Weighted Sum Color.
        (Exner p.93)"""
        return self.SumM, self.WSumC

    @property
    def EA(self):
        """Experience Actual (EA). This is a derivation that relates to available resources, It is obtained by adding
        the two sides of the EB together, that is, Sum M + WSumC.
        (Exner p.93)"""

        return Decimal(
            self.SumM + self.WSumC
        ).quantize(Decimal('.1'))

    @property
    def EBPer(self):
        """EB Pervasive (EBPer). From Exner p. 94:
        This is a ratio concerning the dominance of an EB style in decision making activity. EBPer is calculated only
        when a marked style is indicated by the EB. This is determined by three criteria. First, the value for EA must
        be 4.0 or greater. Second, the value for Lambda *must be less* than 1.0. Finally, when the value of EA falls
        between 4.0 and 10.0, one side of the EB must be *at least two points* greater than the other side. If the
        value of EA is more than 10.0, one side of the EB must be *at least* 2.5 points greater than the other.

        When all three criteria are met, EBPer is calculated by dividing the larger number in the EB by the smaller
        number. In the sample protocol, EA = 11.0, Lambda = 0.55, and the difference between the two values in the EB
        is 3.0. Thus, the larger EB value of 7 is divided by the smaller, 4.0, with a result of 1.8.
        (Exner p.94)"""

        if not all([
            self.EA >= 4,  # the value for EA must be 4.0 or greater
            self.L < 1,  # the value for Lambda must be less than 1.0
        ]):
            return None
        elif (
                4.0 <= self.EA <= 10.0  # the value of EA falls between 4.0 and 10.0

                and abs(self.SumM - self.WSumC) < 2  # one side of the EB must be at least two points greater than the
                # other side
        ):
            return None
        elif (
                self.EA > 10.0  # the value of EA is more than 10.0

                and abs(self.SumM - self.WSumC) < 2.5  # one side of the EB must be at least 2.5 points greater than
                # the other
        ):
            return None
        else:
            # noinspection PyTypeChecker
            # EBPer is calculated by dividing the larger number in the EB by the smaller number
            return Decimal(
                max(self.SumM, self.WSumC) / min(self.SumM, self.WSumC)
            ).quantize(Decimal('.1'))

    @property
    def SumFM(self):
        """Sum of animal color determinants"""
        return self.count(
            Determinant.MOVEMENT_ANIMAL_ACTIVE,
            Determinant.MOVEMENT_ANIMAL_PASSIVE,
            Determinant.MOVEMENT_ANIMAL_ACTIVE_PASSIVE,
        )

    @property
    def Sum_m(self):
        """Sum of inanimate movement determinants"""
        return self.count(
            Determinant.MOVEMENT_INANIMATE_ACTIVE,
            Determinant.MOVEMENT_INANIMATE_PASSIVE,
            Determinant.MOVEMENT_INANIMATE_ACTIVE_PASSIVE
        )

    @property
    def SumFMm(self):
        """Sum of nonhuman movement determinants"""
        return self.SumFM + self.Sum_m

    @property
    def SumAC(self):
        """Sum of achromatic color determinants"""
        return self.count(
            Determinant.ACHROMATIC_COLOR_FORM,
            Determinant.FORM_ACHROMATIC_COLOR,
            Determinant.PURE_ACHROMATIC_COLOR
        )

    @property
    def SumT(self):
        """Sum of texture determinants"""
        return self.count(
            Determinant.ACHROMATIC_COLOR_FORM,
            Determinant.FORM_ACHROMATIC_COLOR,
            Determinant.PURE_ACHROMATIC_COLOR
        )

    @property
    def SumV(self):
        """Sum of vista determinants"""
        return self.count(
            Determinant.VISTA_FORM,
            Determinant.FORM_VISTA,
            Determinant.PURE_VISTA
        )

    @property
    def SumY(self):
        """Sum of diffuse shading determinants"""
        return self.count(
            Determinant.SHADING_FORM,
            Determinant.FORM_SHADING,
            Determinant.PURE_SHADING
        )

    @property
    def SumShd(self):
        """Sum of all shading determinants"""
        return self.SumT + self.SumV + self.SumY + self.SumAC

    @property
    def eb(self):
        """Experience Base (eb). This is a relationship comparing all nonhuman movement determinants (FM and m) to the
        shading and achromatic color determinants. It provides information concerning stimulus demands experienced by
        the subject. It is entered as Sum FM+m : Sum of SumC’+ SumT + SumY + SumV.
        (Exner p.94)"""
        return self.SumFMm, self.SumShd

    @property
    def es(self):
        """Experienced Stimulation (es). This is 4 derivation obtained from the data in the eb. It relates to current
        stimulus demands. !t is obtained by adding the two sides of the eb together, that is, the sum of:
        FM+m + SumC’+ SumT + SumY + SumV.
        (Exner p.94)"""
        return self.SumFMm + self.SumShd

    @property
    def D_score(self):
        """D Score (D). The D Score provides information concerning the relationship between EA and es. This concerns
        stress tolerance and elements of control. It is obtained by first calculating the raw score difference between
        the two variables, that is, EA — es, and including the appropriate sign. The raw difference score is then
        converted into a scaled difference score, based on standard deviations, in which each SD has been rounded to
        equal 2.5.
        (Exner p.94)"""
        return calculate.d_score(self.EA - self.es)

    @property
    def Adj_es(self):
        """Adjusted es (Adj es). Whereas the D Score provides information concerning stress tolerance and available
        resources, it is important to determine if the score has been influenced by situational elements. The first
        step in doing this is to subtract from the es most of the elements that are related to situational phenomena.
        The tactic is simple. All but 1 m and 1 SumY are subtracted from the es to create the Adj es.
        (Exner p.95)"""

        adj_Sum_m = max(0, self.Sum_m - 1)
        adj_SumY = max(0, self.SumY - 1)

        return self.es - adj_Sum_m - adj_SumY

    @property
    def AdjD(self):
        """Adjusted D Score (Adj D). The Adj D is obtained by using the formula EA — Adj es. The result is applied
        against the D Score Conversion Table.
        (Exner p.95)"""
        return calculate.d_score(self.EA - self.Adj_es)

    @property
    def a_p(self):
        """Active:Passive Ratio (Ma:Mp). This relationship concerns flexibility in ideation and attitudes. It is
        entered as the total number of Active movement answers (Ma + FMa + ma) on the left and the total number of
        Passive movement responses (Mp + FMp + mp) on the right. Movement determinants with a-p superscripts are added
        to both sides.
        (Exner pp.95)"""

        active = self.count(
            Determinant.MOVEMENT_HUMAN_ACTIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE,
            Determinant.MOVEMENT_ANIMAL_ACTIVE,
            Determinant.MOVEMENT_ANIMAL_ACTIVE_PASSIVE,
            Determinant.MOVEMENT_INANIMATE_ACTIVE,
            Determinant.MOVEMENT_INANIMATE_ACTIVE_PASSIVE
        )

        passive = self.count(
            Determinant.MOVEMENT_HUMAN_PASSIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE,
            Determinant.MOVEMENT_ANIMAL_PASSIVE,
            Determinant.MOVEMENT_ANIMAL_ACTIVE_PASSIVE,
            Determinant.MOVEMENT_INANIMATE_PASSIVE,
            Determinant.MOVEMENT_INANIMATE_ACTIVE_PASSIVE
        )

        return active, passive


    @property
    def Ma_Mp(self):
        """M Active:Passive Ratio (Ma:Mp). This variable concerns some characteristics of thinking. It includes only
        human movement responses with total Active entered on the left and total Passive entered on the right. Ma-p
        answers are added to both sides.
        (Exner pp.95–96)"""

        active = self.count(
            Determinant.MOVEMENT_HUMAN_ACTIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE
        )

        passive = self.count(
            Determinant.MOVEMENT_HUMAN_PASSIVE,
            Determinant.MOVEMENT_HUMAN_ACTIVE_PASSIVE
        )

        return active, passive

    @property
    def Art_Ay(self):
        """The Intellectualization Index - 2AB+(Art+Ay). This index includes the Special Score AB (Abstract) and the
        contents Art and Anthropology (Ay). It is calculated as two times the number of AB answers plus the number of
        Art and Ay contents.
        (Exner p.96)"""

        abstract = self.count(Special.ABSTRACT_CONTENT)
        Art_Ay = self.count(Content.ART, Content.ANTHROPOLOGY)

        return abstract * 2 + Art_Ay

    @property
    def form_color_ratio(self):
        """Form-Color Ratio (FC:CF+C). This ratio relates to the modulation of affect. It is entered as shown, with the
        total number of FC determinants on the left and the sum of the CF+C+Cn determinants on the right. Each of the
        chromatic color determinants are weighed equally in this ratio, as contrasted with the WSumC used in the EB and
        EA in which Cn responses are not included.
        (Exner p.96)"""

        FC = self.count(Determinant.FORM_COLOR)
        CF_C_Cn = self.count(
            Determinant.COLOR_FORM,
            Determinant.PURE_COLOR,
            Determinant.COLOR_NAMING,
        )

        return FC, CF_C_Cn

    @property
    def constriction_ratio(self):
        """Constriction Ratio (SumC’:WSumC). This ratio relates to excessive internalization of affect. It is entered
        with the total number of C’ determinants (SumC’) on the left and the weighted sum of chromatic color (WSumC) on
        the right.
        (Exner p.96)"""
        return self.SumAC, self.WSumC

    @property
    def Afr(self):
        """Affective Ratio (Afr). This is a ratio that compares the number of answers to the last three cards with
        those given to the first seven cards. It relates to interest in emotional stimulation. It is calculated as:
            Afr = Number Responses to Cards VIII + IX + X
                ÷ Number Responses to Cards I + II + III + IV + V + VIII + VII
        (Exner p.96)"""

        cards_7_thru_10 = self.count(
            Card.VIII,
            Card.IX,
            Card.X
        )

        cards_1_thru_6 = len(self) - cards_7_thru_10
        return Decimal(
            cards_7_thru_10 / cards_1_thru_6
        ).quantize(Decimal('1.00'))

    @property
    def blends(self):
        """From Exner p.45:
        Most records will contain at least one response in which more than one determinant exists. This is the Blend.
        Each determinant is shown in the coding, separated from each other by a dot (.) or Blend sign. For instance,
        Mp.FC.Fr notes that the response contains passive human movement, a form dominated color feature, and a
        reflection.

        :return: a list of lists of determinants from blended responses. Pair determinants are not included.
        """

        blends = []
        for r in self.responses:
            determinants_copy = r.determinants.copy()
            if Determinant.PAIR in determinants_copy:
                determinants_copy.remove(Determinant.PAIR)
            if len(determinants_copy) > 1:
                blends.append(determinants_copy)
        return blends

    @property
    def BlendsR(self):
        """Complexity Ratio (Blends:R). This relationship is not reduced to a ratio. Instead, it is entered as
        indicated, with the total number of blends on the left and the number of responses on the right.
        (Exner p.96)"""

        return len(self.blends), len(self)

    @property
    def XApercent(self):
        """Form Appropriate Extended (XA%). This variable concerns the proportion of responses in which there is an appropriate use of form features. It
        is calculated as:
            XA% = Sum of responses that have an FQ coding of +, 0, or u
                ÷ R (total number of responses)
        (Exner p.97)"""

        XA = self.count(
            FQ.SUPERIOR,
            FQ.ORDINARY,
            FQ.UNUSUAL
        )

        return Decimal(
            XA / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def WDApercent(self):
        """Form Appropriate - Common Areas (WDA%). This variable concerns the proportion of responses given to W and D
        areas in which there is an appropriate use of form features. It is calculated as:
            WDA% = Sum of responses that have an FQ coding of +, 0, or u
                 ÷ Sum of W + D
        (Exner p.97)"""

        WDA = len([
            r for r in self.responses
            if any(code in r for code in [
                Location.WHOLE,
                Location.WHOLE_WHITESPACE,
                Location.DETAIL_COMMON,
                Location.DETAIL_COMMON_WHITESPACE
            ]) and any(code in r for code in [
                FQ.SUPERIOR,
                FQ.ORDINARY,
                FQ.UNUSUAL
            ])
        ])

        return Decimal(
            WDA / self.W_D
        ).quantize(Decimal('1.00'))

    @property
    def Xminus(self):
        """Distorted Form (X-%). This variable concerns the proportion of answers in which form use is not commensurate
        with the blot features. It is calculated as:
            X-% = Sum FQx-
                ÷ R (total number of responses)
        (Exner p.97)"""

        Xminus = len([
            r for r in self.responses
            if any(code in r for code in [
                FQ.MINUS
            ])
        ])

        return Decimal(
            Xminus / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def P(self):
        """From Exner p.97: [T]he number of Popular (P) responses."""
        return len([r for r in self.responses if r.popular])

    @property
    def Xplus(self):
        """Conventional Form Use (X+%). This variable concerns the extent to which the appropriate use of form features
        has included common object definitions. It is calculated as:
            X+% = Sum FQx + and o
                ÷ R (total number of responses)
        (Exner p.97)"""

        Xplus = len([
            r for r in self.responses
            if any(code in r for code in [
                FQ.SUPERIOR,
                FQ.ORDINARY
            ])
        ])
        return Decimal(
            Xplus / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def Xu(self):
        """Unusual Form Use (Xu%). This variable concerns the extent to which the appropriate use of form features has
        included uncommon object definitions. It is calculated as:
            Xu% = Sum FQxu
                ÷ R (total number of responses)
        (Exner p.98)"""

        Xu = len([
            r for r in self.responses
            if any(code in r for code in [
                FQ.UNUSUAL
            ])
        ])
        return Decimal(
            Xu / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def economy_index(self):
        """Economy Index (W:D:Dd). This relationship is entered as shown, with the total number of W responses on the
        left, the total number of D responses in the center, and the total number of Dd answers at the right.
        (Exner p.98)"""
        return self.W, self.D, self.Dd

    @property
    def aspirational_ratio(self):
        """Aspirational Ratio (W:M). This relationship is not reduced to a ratio but, instead, entered as indicated with
        the total number of W responses on the left and the total number of M answers at the right.
        (Exner p.98)"""
        return self.W, self.SumM

    @property
    def Zd(self):
        """Processing Efficiency (Zd). The Zd is a difference score obtained by the formula ZSum — Zest, with the
        appropriate sign recorded.
        (Exner p.98)"""

        return Decimal(
            self.ZSum - self.Zest
        ).quantize(Decimal('1.0'))

    @property
    def human_cont(self):
        """Interpersonal Interest (Human Cont). This entry provides information about interest in people. The entry is
        calculated as:
            Human Cont = The sum H + (H) + Hd + (Hd) [Hx is not included]
        (Exner p.98)"""

        return self.count(
            Content.WHOLE_HUMAN,
            Content.WHOLE_HUMAN_FICTIONAL,
            Content.HUMAN_DETAIL,
            Content.HUMAN_DETAIL_FICTIONAL
        )

    @property
    def PureH(self):
        """From Exner p.98: Sum of Pure H answers."""
        return self.count(Content.WHOLE_HUMAN)

    @property
    def isolate_R(self):
        """Isolation Index (Isolate/R). This variable is related to social isolation. It involves the contents in five
        categories (Botany, Clouds, Geography, Landscape, and Nature), with the raw sum for two categories being
        doubled. It is calculated as:
            Isolate/R = Bt + 2Cl + Ge + Ls + 2Na
                      ÷ R
        (Exner p.99)"""

        isolate = sum([
            self.count(Content.BOTANY),
            self.count(Content.CLOUDS) * 2,
            self.count(Content.GEOGRAPHY),
            self.count(Content.LANDSCAPE),
            self.count(Content.NATURE) * 2,
        ])
        return Decimal(
            isolate / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def egocentricity_index(self):
        """Egocentricity Index (3r+(2)/R). This index relates to self esteem. It represents the proportion of
        reflection and pair responses in the total record, with each reflection determinant weighed as being equal to
        three pair responses. It is calculated as:
            3r + (2)/R = 3 * (Fr + rF) + Sum (2)
                       ÷ R
        (Exner p.99)"""

        egocentricity = 3 * self.count(
            Determinant.FORM_REFLECTION,
            Determinant.REFLECTION_FORM
        ) + self.count(Determinant.PAIR)
        return Decimal(
            egocentricity / len(self)
        ).quantize(Decimal('1.00'))

    @property
    def ColShdBld(self):
        """Blends combining color determinant (FC, CF, C) with shading determinant (F'C, C'F, C', FT, TF, T, FV, VF, V,
        FY, YF, Y). Used for S-Constellation"""

        return len([
            blend for blend in self.blends
            if any(item in blend for item in [
                Determinant.FORM_COLOR,
                Determinant.COLOR_FORM,
                Determinant.PURE_COLOR
            ]) and any(item in blend for item in [
                Determinant.FORM_ACHROMATIC_COLOR,
                Determinant.ACHROMATIC_COLOR_FORM,
                Determinant.PURE_ACHROMATIC_COLOR,
                Determinant.FORM_TEXTURE,
                Determinant.TEXTURE_FORM,
                Determinant.PURE_TEXTURE,
                Determinant.FORM_VISTA,
                Determinant.VISTA_FORM,
                Determinant.PURE_VISTA,
                Determinant.FORM_SHADING,
                Determinant.SHADING_FORM,
                Determinant.PURE_SHADING
            ])
        ])

    @property
    def s_constellation(self):
        """S-Constellation (Suicide Potential): Positive if 8 or more conditions are true. Note: Applicable only for
        subjects over 14 years old.

        Conditions:
            - FV + VF + V+ FD > 2
            - Color-Shading Blends > 0
            - 3r + (2) / R < .31 or > .44
            - MOR > 3
            - Zd > +3.5 or Zd < -3.5
            - es > EA
            - CF + C > FC
            - X+% < .70
            - S > 3
            - P < 3 or P > 8
            - Pure H < 2
            - R < 17
        (Exner p.101)"""

        if self.age <= 14:
            return False

        conditions = [
            # FV + VF + V + FD > 2
            self.SumV + self.count(Determinant.FORM_DIMENSION) > 2,

            # Color-Shading Blends > 0
            self.ColShdBld > 0,

            # 3r + (2) / R < .31 or > .44
            self.egocentricity_index < 0.31 or self.egocentricity_index > 0.44,

            # MOR > 3
            self.count(Special.MORBID_CONTENT) > 3,

            # Zd > +3.5 or Zd < -3.5
            self.Zd > 3.5 or self.Zd < -3.5,

            # es > EA
            self.es > self.EA,

            # CF + C > FC
            self.count(
                Determinant.COLOR_FORM,
                Determinant.PURE_COLOR
            ) > self.count(
                Determinant.FORM_COLOR
            ),

            # X+% < .70
            self.Xplus < 0.70,

            # S > 3
            self.S > 3,

            # P < 3 or P > 8
            self.P < 3 or self.P > 8,

            # Pure H < 2
            self.PureH < 2,

            # R < 17
            len(self) < 17
        ]
        return sum(conditions) >= 8, sum(conditions)

    @property
    def DEPI(self):
        """DEPI (Depression Index): Positive if 5 or more conditions are true.

        Conditions:
            - (FV + VF + V > 0) OR (FD > 2)
            - (Col-Shd Blends > 0) OR (S > 2)
            - (3r + (2) / R > .44 and Fr + rF = 0) OR (3r + (2) / R < .33)
            - (Afr < .46) OR (Blends < 4)
            - (SumShading > FM+m) OR (SumC’ > 2)
            - (MOR > 2) OR (2 * AB + Art + Ay > 3)
            - (Cop < 2) OR ([Bt + 2 * Cl + Ge + Ls + 2 * Na]/R > .24)

        Note: Significance thresholds for the Affective Ratio (Afr) and Egocentricity Index (3r + (2) / R) in the DEPI
         are adjusted for age.
        (Exner p.101)"""

        if self.age <= 16:
            min_ego, max_ego = lookup.age_adjusted_egocentricity_index_cutoffs[self.age]
        else:
            min_ego, max_ego = 0.33, 0.44

        if self.age <= 13:
            afr_threshold = lookup.age_adjusted_Afr[self.age]
        else:
            afr_threshold = 0.46

        conditions = [
            # (FV + VF + V > 0) OR (FD > 2)
            self.SumV > 0 or self.count(Determinant.FORM_DIMENSION) > 2,

            # (Col-Shd Blends > 0) OR (S > 2)
            self.ColShdBld > 0 or self.S > 2,

            # (3r + (2) / R > .44 and Fr + rF = 0) OR (3r + (2) / R < .33)
            all([
                self.egocentricity_index > max_ego,
                self.count(
                    Determinant.FORM_REFLECTION, Determinant.REFLECTION_FORM
                ) == 0
            ]) or self.egocentricity_index < min_ego,

            # (Afr < .46) OR (Blends < 4)
            self.Afr < afr_threshold or len(self.blends) < 4,

            # (SumShading > FM+m) OR (SumC’ > 2)
            self.SumShd > self.SumFMm or self.SumAC > 2,

            # (MOR > 2) OR (2 * AB + Art + Ay > 3)
            self.count(Special.MORBID_CONTENT) > 2 or self.Art_Ay > 3,

            # (Cop < 2) OR ([Bt + 2 * Cl + Ge + Ls + 2 * Na]/R > .24)
            self.count(Special.COOPERATIVE_MOVEMENT) < 2 or self.isolate_R > 0.24
        ]
        return sum(conditions) >= 5, sum(conditions)

    @property
    def HVI(self):
        """HVI (Hypervigilance Index). Positive if condition 1 is true and at least 4 of the others are true.

        Conditions:
            1. FT + TF + T = 0
            2. Zf > 12
            3. Zd > +3.5
            4. S > 3
            5. H + (H) + Hd + (Hd) > 6
            6. (H) + (A) + (Hd) + (Ad) > 3
            7. H + A : Hd + Ad < 4 : 1
            8. Cg > 3
        (Exner p.101)"""

        conditions = [
            # FT + TF + T = 0
            self.SumT == 0,

            # Zf > 12
            self.Zf > 12,

            # Zd > +3.5
            self.Zd > 3.5,

            # S > 3
            self.S > 3,

            # H + (H) + Hd + (Hd) > 6
            self.count(
                Content.WHOLE_HUMAN,
                Content.WHOLE_HUMAN_FICTIONAL,
                Content.HUMAN_DETAIL,
                Content.HUMAN_DETAIL_FICTIONAL
            ) > 6,

            # (H) + (A) + (Hd) + (Ad) > 3
            self.count(
                Content.WHOLE_HUMAN_FICTIONAL,
                Content.WHOLE_ANIMAL_FICTIONAL,
                Content.HUMAN_DETAIL_FICTIONAL,
                Content.ANIMAL_DETAIL_FICTIONAL
            ) > 3,

            # H + A : Hd + Ad < 4 : 1
            self.count(
                Content.HUMAN_DETAIL,
                Content.ANIMAL_DETAIL
            ) * 4 >= self.count(
                Content.WHOLE_HUMAN,
                Content.WHOLE_ANIMAL
            ),  # Altered to prevent dividing by zero

            # Cg > 3
            self.count(Content.CLOTHING) > 3
        ]
        return conditions[0], sum(conditions)

    @property
    def PTI(self):
        """PTI (Perceptual-Thinking Index). Contains one age-adjusted variable, WSum6.

        Conditions:
            - XA% < .70 and WDA% < .75
            - X-% > .29
            - LVL2 > 2 and FAB2 > 0
            - R < 17 and WSUM6 > 12 OR R > 16 and WSUM6 > 17
            - M- > 1 OR X-% > .40
        (Exner p.101)"""
        if self.age <= 13:
            low_r_WSum6, high_r_WSum6 = lookup.age_adjusted_WSum6_cutoffs[self.age]
        else:
            low_r_WSum6, high_r_WSum6 = 12, 17

        conditions_met = sum(condition is True for condition in [
            # XA% < .70 and WDA% < .75
            self.XApercent < 0.7 and self.WDApercent < 0.75,

            # X-% > .29
            self.Xminus > 0.29,

            # LVL2 > 2 and FAB2 > 0
            self.count(
                Special.DEVIANT_VERBALIZATION_2,
                Special.DEVIANT_RESPONSE_2,
                Special.INCONGRUOUS_COMBINATION_2,
                Special.FABULIZED_COMBINATION_2
            ) > 2 and self.count(Special.FABULIZED_COMBINATION_2) > 0,

            # R < 17 and WSUM6 > 12 OR R > 16 and WSUM6 > 17
            len(self) < 17 and self.WSum6 > low_r_WSum6 or len(self) > 16 and self.WSum6 > high_r_WSum6,

            # M- > 1 OR X-% > .40
            self.Mminus > 1 or self.Xminus > 0.40

        ])
        return conditions_met

    # noinspection DuplicatedCode
    @property
    def CDI(self):
        """CDI (Coping Deficit Index): Positive if 4 or 5 conditions are true. Significance threshold for the Affective
        Ratio (Afr) is adjusted for age.

        Conditions:
            - (EA < 6) OR (AdjD < 0)
            - (COP < 2) and (AG < 2)
            - (Weighted Sum C < 2.5) OR (Afr < .46)
            - (Passive > Active + 1) OR (Pure H < 2)
            - (Sum T > 1) OR (Isolate/R > .24) OR (Food > 0)
        (Exner p.101)"""

        if self.age <= 13:
            afr_threshold = lookup.age_adjusted_Afr[self.age]
        else:
            afr_threshold = 0.46

        conditions_met = sum(condition is True for condition in [
            # (EA < 6) OR (AdjD < 0)
            self.EA < 6 or self.AdjD < 0,

            # (COP < 2) and (AG < 2)
            self.count(Special.COOPERATIVE_MOVEMENT) < 2 and self.count(Special.AGGRESSIVE_MOVEMENT) < 2,

            # (Weighted Sum C < 2.5) OR (Afr < .46)
            self.WSumC < 2.5 or self.Afr < afr_threshold,

            # (Passive > Active + 1) OR (Pure H < 2)
            self.a_p[1] > self.a_p[0] + 1 or self.PureH < 2,

            # (Sum T > 1) OR (Isolate/R > .24) OR (Food > 0)
            self.SumT > 1 or self.isolate_R > 0.24 or self.count(Content.FOOD) > 0
        ])
        return conditions_met >= 4, conditions_met

    # noinspection DuplicatedCode
    @property
    def OBS(self):
        """OBS (Obsessive Style Index)): Positive if 4 or 5 conditions are true. Significance threshold for the Affective
        Ratio (Afr) is adjusted for age.

        Conditions:
            1. Dd > 3
            2. Zf > 12
            3. Zd > +3.0
            4. Populars > 7
            5. FQ+ > 1
        Positive if one or more is true:
            - Conditions 1 to 5 are all true
            - 2 or more of 1 to 4 are true AND FQ+ > 3
            - 3 or more of 1 to 5 are true AND X+% > 0.89
            - FQ+ > 3 AND X+% > 0.89
        (Exner p.101)"""

        if self.age in (5, 6):
            afr_threshold = 0.57
        elif 7 <= self.age <= 9:
            afr_threshold = 0.55
        elif 10 <= self.age <= 13:
            afr_threshold = 0.53
        else:
            afr_threshold = 0.46

        conditions = [
            # Dd > 3
            self.Dd > 3,

            # Zf > 12
            self.Zf > 12,

            # Zd > +3.0
            self.Zd > 3.0,

            # Populars > 7
            self.P > 7,

            # FQ+ > 1
            self.count(FQ.SUPERIOR) > 1
        ]

        # Positive if one or more is true:
        return any([

            # Conditions 1 to 5 are all true
            all(conditions),

            # 2 or more of 1 to 4 are true AND FQ+ > 3
            sum(conditions[:4]) >= 2 and self.count(FQ.SUPERIOR) > 3,

            # 3 or more of 1 to 5 are true AND X+% > 0.89
            sum(conditions) >= 3 and self.Xplus > 0.89,

            # FQ+ > 3 AND X+% > 0.89
            self.count(FQ.SUPERIOR) > 3 and self.Xplus > 0.89

        ]), sum(conditions)
