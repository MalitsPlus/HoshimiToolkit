from live_result import Card, Effect
from master_skill_efficacy import MasterSkillEfficacy
from proto_enums import eSkillEfficacyType

category_dict = {
    eSkillEfficacyType.StaminaConsumptionReduction: "LV",
    eSkillEfficacyType.DanceUp: "LV",
    eSkillEfficacyType.VocalUp: "LV",
    eSkillEfficacyType.VisualUp: "LV",
    eSkillEfficacyType.ScoreUp: "LV",
    eSkillEfficacyType.BeatScoreUp: "LV",
    eSkillEfficacyType.ActiveSkillScoreUp: "LV",
    eSkillEfficacyType.CriticalRateUp: "LV",
    eSkillEfficacyType.CriticalBonusPermilUp: "LV",
    eSkillEfficacyType.AudienceAmountIncrease: "LV",
    eSkillEfficacyType.StaminaRecovery: "O",
    eSkillEfficacyType.FixStaminaRecovery: "O",
    eSkillEfficacyType.WeaknessEffectRecovery: "O",
    eSkillEfficacyType.StrengthEffectValueIncrease: "O",
    eSkillEfficacyType.AudienceAmountReduction: "LV",
    eSkillEfficacyType.SkillImpossible: "L",
    eSkillEfficacyType.DanceDown: "LV",
    eSkillEfficacyType.VocalDown: "LV",
    eSkillEfficacyType.VisualDown: "LV",
    eSkillEfficacyType.StaminaConsumptionIncrease: "LV",
    eSkillEfficacyType.SpecialSkillScoreUp: "LV",
    eSkillEfficacyType.TargetStaminaRecovery: "O",
    eSkillEfficacyType.SkillSuccessRateUp: "LV",
    eSkillEfficacyType.TensionUp: "LV",
    eSkillEfficacyType.WeaknessEffectPrevention: "L",
    eSkillEfficacyType.ComboScoreUp: "LV",
    eSkillEfficacyType.PassiveSkillScoreUp: "LV"
}
eff_value = {
    eSkillEfficacyType.StaminaConsumptionReduction: 50,
    eSkillEfficacyType.DanceUp: 50,
    eSkillEfficacyType.VocalUp: 50,
    eSkillEfficacyType.VisualUp: 50,
    eSkillEfficacyType.ScoreUp: 25,
    eSkillEfficacyType.BeatScoreUp: 100,
    eSkillEfficacyType.ActiveSkillScoreUp: 50,
    eSkillEfficacyType.CriticalRateUp: 50,
    eSkillEfficacyType.CriticalBonusPermilUp: 50,
    eSkillEfficacyType.AudienceAmountIncrease: 50,
    eSkillEfficacyType.AudienceAmountReduction: 50,
    eSkillEfficacyType.DanceDown: 50,
    eSkillEfficacyType.VocalDown: 50,
    eSkillEfficacyType.VisualDown: 50,
    eSkillEfficacyType.StaminaConsumptionIncrease: 50,
    eSkillEfficacyType.SpecialSkillScoreUp: 30,
    eSkillEfficacyType.SkillSuccessRateUp: 50,
    eSkillEfficacyType.TensionUp: 50,
    eSkillEfficacyType.ComboScoreUp: 100,
    eSkillEfficacyType.PassiveSkillScoreUp: 0
}
eff_value2 = {

}
strength_list = [
    eSkillEfficacyType.StaminaConsumptionReduction,
    eSkillEfficacyType.ComboContinuation,
    eSkillEfficacyType.DanceUp,
    eSkillEfficacyType.VocalUp,
    eSkillEfficacyType.VisualUp,
    eSkillEfficacyType.ScoreUp,
    eSkillEfficacyType.BeatScoreUp,
    eSkillEfficacyType.ActiveSkillScoreUp,
    eSkillEfficacyType.CriticalRateUp,
    eSkillEfficacyType.CriticalBonusPermilUp,
    eSkillEfficacyType.AudienceAmountIncrease,
    eSkillEfficacyType.AudienceAmountReduction,
    eSkillEfficacyType.SpecialSkillScoreUp,
    eSkillEfficacyType.SkillSuccessRateUp,
    eSkillEfficacyType.TensionUp,
    eSkillEfficacyType.WeaknessEffectPrevention,
    eSkillEfficacyType.ComboScoreUp,
    eSkillEfficacyType.PassiveSkillScoreUp
]

class EffectBase:
    eff_type: eSkillEfficacyType

    def __init__(self, _type: eSkillEfficacyType) -> None:
        self.eff_type = _type
        
    @staticmethod
    def of(_type: int):
        t = eSkillEfficacyType(_type)
        if t in type_sub.keys:
            return type_sub[t](t)
        return EffectBase(eSkillEfficacyType(_type))

    def get_category(self) -> str:
        if self.eff_type in category_dict.keys:
            return category_dict[self.eff_type]
        else:
            return "U"

    def get_eff(self, card, _type: eSkillEfficacyType) -> Effect:
        for eff in card.effects:
            if eff.skill_efficacy_type == _type.value:
                return eff
        return None
    
    def get_self_eff(self, card) -> Effect:
        return self.get_eff(card, self.eff_type)

    def implement(self, card, eff: MasterSkillEfficacy, origin: Card) -> None:
        category = self.get_category()
        if category == "LV":
            new_eff = Effect()
            new_eff.skill_efficacy_type = self.eff_type.value
            new_eff.grade = eff.grade
            new_eff.max_grade = eff.max_grade
            grade = new_eff.grade
            if new_eff.max_grade < new_eff.grade:
                grade = new_eff.max_grade
            new_eff.value = eff_value[self.eff_type] * grade
            new_eff.value2 = eff_value[self.eff_type] * grade
            for live_eff in card.effects:
                if live_eff.skill_efficacy_type == self.eff_type.value:
                    live_eff.grade += new_eff.grade
                    grade = live_eff.grade
                    if live_eff.max_grade < live_eff.grade:
                        grade = live_eff.max_grade
                    live_eff.value = eff_value[self.eff_type] * live_eff.grade
                    live_eff.value2 += eff_value2[self.eff_type] * live_eff.grade
                    return
            card.effects.append(new_eff)
            return
        elif category == "L":
            for live_eff in card.effects:
                if live_eff.skill_efficacy_type == self.eff_type.value:
                    return
            new_eff = Effect()
            new_eff.skill_efficacy_type = self.eff_type.value
            card.effects.append(new_eff)
            return


class DanceUp(EffectBase):
    def implement(self, card, eff: MasterSkillEfficacy, origin: Card) -> None:
        super().implement(card, eff, origin)
        ef = self.get_self_eff(card)
        de_ef = self.get_eff(card, eSkillEfficacyType.DanceDown)
        card.dance = int(origin.dance * (1 + (ef.value - de_ef.value) / 1000))

class VocalUp(EffectBase):
    def implement(self, card, eff: MasterSkillEfficacy, origin: Card) -> None:
        super().implement(card, eff, origin)
        ef = self.get_self_eff(card)
        de_ef = self.get_eff(card, eSkillEfficacyType.VocalDown)
        card.vocal = int(origin.vocal * (1 + (ef.value - de_ef.value) / 1000))

class VisualUp(EffectBase):
    def implement(self, card, eff: MasterSkillEfficacy, origin: Card) -> None:
        super().implement(card, eff, origin)
        ef = self.get_self_eff(card)
        de_ef = self.get_eff(card, eSkillEfficacyType.VisualDown)
        card.visual = int(origin.visual * (1 + (ef.value - de_ef.value) / 1000))

class AudienceAmountIncrease(EffectBase):
    pass

class StaminaRecovery(EffectBase):
    def implement(self, card, eff: MasterSkillEfficacy, origin: Card) -> None:
        super().implement(card, eff, origin)
        card 

class FixStaminaRecovery(EffectBase):
    pass


class WeaknessEffectRecovery(EffectBase):
    pass


class StrengthEffectValueIncrease(EffectBase):
    pass


class AudienceAmountReduction(EffectBase):
    pass


class DanceDown(EffectBase):
    pass


class VocalDown(EffectBase):
    pass


class VisualDown(EffectBase):
    pass


class WeaknessEffectPrevention(EffectBase):
    pass


type_sub: dict[eSkillEfficacyType, EffectBase] = {
    eSkillEfficacyType.DanceUp: DanceUp,
    eSkillEfficacyType.VocalUp: VocalUp,
    eSkillEfficacyType.VisualUp: VisualUp,
    eSkillEfficacyType.AudienceAmountIncrease: AudienceAmountIncrease,
    eSkillEfficacyType.StaminaRecovery: StaminaRecovery,
    eSkillEfficacyType.FixStaminaRecovery: FixStaminaRecovery,
    eSkillEfficacyType.WeaknessEffectRecovery: WeaknessEffectRecovery,
    eSkillEfficacyType.StrengthEffectValueIncrease: StrengthEffectValueIncrease,
    eSkillEfficacyType.AudienceAmountReduction: AudienceAmountReduction,
    eSkillEfficacyType.DanceDown: DanceDown,
    eSkillEfficacyType.VocalDown: VocalDown,
    eSkillEfficacyType.VisualDown: VisualDown,
    eSkillEfficacyType.WeaknessEffectPrevention: WeaknessEffectPrevention
}
