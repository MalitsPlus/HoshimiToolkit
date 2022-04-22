import json
from pathlib import Path

from sqlalchemy import true
from apply_eff import EffectBase
from proto_enums import eSkillEfficacyType
from skill_manager import SkillManager
from live_result import LiveResult, Result, Card, Chart, CardStatus, Effect, ActivatedSkill
from pvp_result import PvpResult
from gvg_result import GvgResult

class SkillStatusOb:
    skill_index: int
    cool_time: int
    category_type: int

class CardBeat:
    index: int
    level: int
    rarity: int
    dance: int
    vocal: int
    visual: int
    max_stamina: int
    stamina: int
    mental: int
    technique: int
    audience_amount: int
    effects: list[Effect]
    skill_status: list[SkillStatusOb]
    
    def __init__(self) -> None:
        self.effects = list()
        self.skill_status = list()

    def get_param(self, attr: int) -> int:
        if attr == 1:
            return self.dance
        elif attr == 2:
            return self.vocal
        elif attr == 3:
            return self.visual
        else:
            return 0
    
    def get_skill_rate_bonus(self) -> float:
        for eff in self.effects:
            if eff.skill_efficacy_type == eSkillEfficacyType.SkillSuccessRateUp.value:
                return eff.value2 / 1000
        return 0

    def is_possible(self, category: int) -> bool:
        if category == 3:
            return not self.is_sp_cooling() and not self.is_impossibled()
        elif category == 2:
            return not self.is_a_cooling() and not self.is_impossibled()

    def is_impossibled(self) -> bool:
        for eff in self.effects:
            if eff.skill_efficacy_type == eSkillEfficacyType.SkillImpossible.value:
                return True
        return False
    
    def is_a_cooling(self) -> bool:
        flag = True
        for skill in self.skill_status:
            if skill.category_type == 2 and skill.cool_time == 0:
                flag = False
        return flag

    def is_sp_cooling(self) -> bool:
        flag = True
        for skill in self.skill_status:
            if skill.category_type == 1 and skill.cool_time == 0:
                flag = False
        return flag

        

class Row:
    number: int
    combos: list[int]
    beats: list[CardBeat]
    act: int
    attribute: int
    chart_type: int
    def __init__(self) -> None:
        self.combos = list()
        self.beats = list()

class LiveOb:
    result: Result
    cards: list[Card]
    rows: list[Row]

    def __init__(self, d: dict, type: str) -> None:
        self.cards = list()
        self.rows = list()
        skill_manager = SkillManager()
        if type == "quest":
            self.result = LiveResult.from_dict(d).result
        elif type == "pvp":
            self.result = PvpResult.from_dict(d).result
        elif type == "gvg":
            self.result = GvgResult.from_dict(d).result
        # Initialize cards
        for user in self.result.user_infos:
            for card in user.user_deck.cards:
                self.cards.append(card)
        # Initialize skills
        for card in self.cards:
            card.skills_ob = list()
            for skill in card.skills:
                skill_ob = skill_manager.get_skill_ob(
                    skill.skill_id, skill.skill_level)
                card.skills_ob.append(skill_ob)

    def get_actived_skills_before_action(self, i: int) -> list[ActivatedSkill]:
        chart = self.get_result().charts[i]
        if chart.chart_type == 1:
            action_order = chart.beats[0].order
        elif chart.chart_type == 2 or chart.chart_type == 3:
            action_order = chart.activated_skill.order
        activated_skills = list[ActivatedSkill](filter(
            lambda x: x.activated == True and x.order < action_order), 
            chart.activated_passive_skills)
        return activated_skills

    def get_plain_card(self, index: int) -> CardBeat:
        card_beat = CardBeat()
        origin = self.cards[index - 1]
        card_beat.index = index
        card_beat.level = origin.level
        card_beat.rarity = origin.rarity
        card_beat.dance = origin.dance
        card_beat.vocal = origin.vocal
        card_beat.visual = origin.visual
        card_beat.max_stamina = origin.stamina
        card_beat.mental = origin.mental
        card_beat.technique = origin.technique
        card_beat.audience_amount = origin.audience_amount
        return card_beat

    def get_status(self, chart: Chart, index: int) -> CardStatus:
        for stat in chart.card_statuses:
            if stat.card_index == index:
                return stat

    def analyze_battle(self):
        pre_chart: Chart = None
        for chart in self.result.charts:
            if chart.chart_type == 1:
                pre_chart = chart
                continue

            row = Row()
            row.number = chart.number
            row.act = chart.activated_skill.card_index
            row.attribute = chart.attribute_type
            row.chart_type = chart.chart_type

            # Append user combo
            for user_stat in chart.user_statuses:
                row.combos.append(user_stat.current_combo_count)

            # For each index
            for status in chart.card_statuses:
                # Create a new CardBeat instance
                card_beat = self.get_plain_card(status.card_index)
                pre_stat = self.get_status(pre_chart, status.card_index)
                card_beat.vocal = pre_stat.vocal
                card_beat.dance = pre_stat.dance
                card_beat.visual = pre_stat.visual
                card_beat.stamina = pre_stat.stamina
                if pre_stat.effects is not None:
                    for eff in pre_stat.effects:
                        card_beat.effects.append(eff)
                if pre_stat.skill_statuses is not None:
                    for skill_stat in pre_stat.skill_statuses:
                        sk_index = skill_stat.skill_index
                        # Excludes photo skills
                        if sk_index > 3:
                            continue
                        skill_stat_ob = SkillStatusOb()
                        skill_stat_ob.skill_index = sk_index
                        skill_stat_ob.cool_time = skill_stat.cool_time
                        skill_stat_ob.category_type = self.cards[
                            status.card_index - 1].skills_ob[
                                sk_index - 1].category_type
                        card_beat.skill_status.append(skill_stat_ob)
                row.beats.append(card_beat)
            self.rows.append(row)
            pre_chart = chart

    def analyze_chart(self):
        pre_chart: Chart = None
        for chart in self.result.charts:
            if chart.chart_type == 1:
                continue
            row = Row()
            row.number = chart.number

            # Append user combo
            for user_stat in chart.user_statuses:
                row.combos.append(user_stat.current_combo_count)

            # Filter skills before action
            activated_order = chart.activated_skill.order
            passives = list[ActivatedSkill]()
            for passive in chart.activated_passive_skills:
                if passive.activated and passive.order < activated_order:
                    passives.append(passive)

            # For each index
            for status in chart.card_statuses:
                # Create a new CardBeat instance
                card_beat = self.get_plain_card(status.card_index)
                pre_stat = self.get_status(pre_chart, status.card_index)
                card_beat.stamina = pre_stat.stamina
                for eff in pre_stat.effects:
                    card_beat.effects.append(eff)
                row.beats.append(card_beat)

            for pskill in passives:
                index = pskill.card_index
                sk_index = pskill.skill_index
                act_card = self.cards[index - 1]
                skillob = act_card.skills_ob[sk_index - 1]
                # Consume stamina
                act_card.stamina -= pskill.stamina
                for detail in pskill.details:
                    eff_index = detail.efficacy_index
                    for target in detail.target_card_indexes:
                        card = row.beats[target - 1]
                        eff = skillob.skill_details[eff_index - 1]
                        EffectBase.of(eff.type).implement(card, eff)
            pre_chart = chart
            

if __name__ == "__main__":
    file = Path(
        "../ProtobufNet/bin/Debug/net6.0/json/queststart220413164324693.json")
    with file.open("r", encoding="utf8") as fp:
        jdict = json.load(fp)
        live = LiveOb(jdict)
        for chart in live.enum_charts():
            x = chart.chart_type
