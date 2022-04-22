import json
from proto_enums import eLiveAbilityType, eSkillEfficacyType, eAttributeType, eMusicChartType
from types import SimpleNamespace
from utility import get_combo_adv, get_audience_adv

status_buff = [
    eSkillEfficacyType.DanceUp,
    eSkillEfficacyType.VocalUp,
    eSkillEfficacyType.VisualUp,
    eSkillEfficacyType.DanceDown,
    eSkillEfficacyType.VocalDown,
    eSkillEfficacyType.VisualDown
]

ng_buff = [
    eSkillEfficacyType.ScoreUp,
    eSkillEfficacyType.BeatScoreUp,
    eSkillEfficacyType.ActiveSkillScoreUp,
    eSkillEfficacyType.CriticalBonusPermilUp,
    eSkillEfficacyType.AudienceAmountIncrease,
    eSkillEfficacyType.AudienceAmountReduction,
    eSkillEfficacyType.SpecialSkillScoreUp,
    eSkillEfficacyType.TensionUp,
    eSkillEfficacyType.ComboScoreUp,
    eSkillEfficacyType.PassiveSkillScoreUp
]

beat_ng_buff = [
    eSkillEfficacyType.ScoreUp,
    eSkillEfficacyType.BeatScoreUp,
    eSkillEfficacyType.CriticalBonusPermilUp,
    eSkillEfficacyType.AudienceAmountIncrease,
    eSkillEfficacyType.AudienceAmountReduction,
    eSkillEfficacyType.ComboScoreUp,
    eSkillEfficacyType.PassiveSkillScoreUp
]

class Yell:
    type: eLiveAbilityType
    name: str
    value: int

class Effect:
    skill_efficacy_type: eSkillEfficacyType
    value: int
    value2: int
    grade: int
    max_grade: int
    
    def is_status_buff(self) -> bool:
        if (self.skill_efficacy_type in status_buff):
            return True
        return False

    def is_ng_buff(self) -> bool:
        if (self.skill_efficacy_type in ng_buff):
            return True
        return False

    def is_beat_ng_buff(self) -> bool:
        if (self.skill_efficacy_type in beat_ng_buff):
            return True
        return False

class PhotoAbility:
    photo_ability_id: str
    effect_value: int
    is_available: bool
    type: eLiveAbilityType

class Photo:
    photo_id: str
    abilities: list[PhotoAbility]
    
    def get_value(self, type: eLiveAbilityType) -> int:
        return sum([it.effect_value for it in self.abilities if it.type == type and it.is_available == True])
    
    def init_abilities(self, jphoto):
        self.abilities = []
        for jab in jphoto.abilities:
            ability = PhotoAbility()
            ability.photo_ability_id = jab.photoAbilityId
            ability.effect_value = jab.effectValue
            ability.is_available = jab.isAvailable
            ability.type = eLiveAbilityType(jab.type)
            self.abilities.append(ability)

class Chart:
    chart_type: eMusicChartType
    attribute_type: eAttributeType
    number: int
    score: int
    is_critical: bool
    combo: int
    dance: int
    vocal: int
    visual: int
    stamina: int
    effects: list[Effect]

    def init_effects(self, jeffects):
        self.effects = []
        for jeffect in jeffects:
            effect = Effect()
            effect.skill_efficacy_type = eSkillEfficacyType(jeffect.skillEfficacyType)
            effect.value = jeffect.value
            effect.value2 = jeffect.value2
            effect.grade = jeffect.grade
            effect.max_grade = jeffect.maxGrade
            self.effects.append(effect)

    def get_combo_bonus(self) -> int:
        return get_combo_adv(self.combo)
    
    def get_def_buff_value(self, _type: eSkillEfficacyType) -> float:
        for ef in self.effects:
            if ef.skill_efficacy_type == _type:
                return ef.value / 1000
        return 0
    
    def get_def_buff_value2(self, _type: eSkillEfficacyType) -> float:
        for ef in self.effects:
            if ef.skill_efficacy_type == _type:
                return ef.value2 / 1000
        return 0

    def is_buffed(self) -> bool:
        return self.effects.__len__() == 0

    def is_ng_buffed(self) -> bool:
        return sum([it.is_ng_buff() for it in self.effects]) > 0

    def is_beat_ng_buffed(self) -> bool:
        return sum([it.is_beat_ng_buff() for it in self.effects]) > 0
    
    def is_def_buffed(self, enm: list[eSkillEfficacyType]) -> bool:
        for ef in self.effects:
            if ef.skill_efficacy_type in enm:
                return True
        return False

class SkillEfficacy:
    id: str
    name: str
    type: eSkillEfficacyType
    description: str
    grade: int
    maxGrade: int
    skillTargetId: str

class Skill:
    id: str
    name: str
    categoryType: int
    level: int
    stamina: int
    triggerId: str
    probabilityPermil: int
    limitCount: int
    coolTime: int
    skillDetails: list[SkillEfficacy] 

class OneLine:
    index: int 
    cardId: str
    audience: int
    skills: dict[int, Skill]
    photos: list[Photo]
    charts: list[Chart]
    def get_photo_buff(self, buff_type: eLiveAbilityType) -> int:
        return sum([it.get_value(buff_type) for it in self.photos])

    def init_skills(self, index: int, live):
        pass

    def init_photos(self, index: int, cardPhotos):
        self.photos = []
        for jcardphoto in cardPhotos:
            if jcardphoto.index == index and jcardphoto.photos is not None:
                for jphoto in jcardphoto.photos:
                    photo = Photo()
                    photo.photo_id = jphoto.photoId
                    photo.init_abilities(jphoto)
                    self.photos.append(photo)
    
    def init_charts(self, index: int, live):
        self.charts = []
        for jchart in live.result.charts:
            chart = Chart()
            chart.chart_type = eMusicChartType(jchart.chartType)
            chart.attribute_type = eAttributeType(jchart.attributeType)
            chart.number = jchart.number
            if jchart.beats is not None:
                for jbeat in jchart.beats:
                    if jbeat.cardIndex == index:
                        chart.score = jbeat.score
                        chart.is_critical = jbeat.isCritical
            else:
                chart.score = 0
                chart.is_critical = False

            if chart.chart_type != eMusicChartType.Beat:
                chart.card_index = jchart.activatedSkill.cardIndex
                chart.skill_index = jchart.activatedSkill.skillIndex
                chart.activated = jchart.activatedSkill.activated
                chart.score = jchart.activatedSkill.score
                chart.is_critical = jchart.activatedSkill.isCritical

            chart.combo = jchart.userStatuses[0].currentComboCount
            for jstatus in jchart.cardStatuses:
                if jstatus.cardIndex == index:
                    chart.dance = jstatus.dance
                    chart.vocal = jstatus.vocal
                    chart.visual = jstatus.visual
                    chart.stamina = jstatus.stamina
                    if jstatus.effects is not None:
                        chart.init_effects(jstatus.effects)
                    else:
                        chart.effects = []
            self.charts.append(chart)
        self.charts.sort(key=lambda c: c.number)


class OneLive:
    quest_id: str 
    music_chart_pattern_id: str
    difficulty_level: int                       # live level，应该会影响 critial 率
    position1_attribute_type: eAttributeType    # center 位置的 line 颜色
    position2_attribute_type: eAttributeType    # center 左边位置的 line 颜色
    position3_attribute_type: eAttributeType    # center 右边位置的 line 颜色
    position4_attribute_type: eAttributeType    # 最左位置的 line 颜色
    position5_attribute_type: eAttributeType    # 最右位置的 line 颜色
    active_skill_weight_permil: int             # A 技能得分率
    special_skill_weight_permil: int            # SP 技能得分率
    skill_stamina_weight_permil: int            # 体力消费率
    stamina_recovery_weight_permil: int         # 体力恢复率
    beat_dance_weight_permil: int               # 计算每个通常 beat 时，da 属性所占权重
    beat_vocal_weight_permil: int               # 计算每个通常 beat 时，vo 属性所占权重
    beat_visual_weight_permil: int              # 计算每个通常 beat 时，vi 属性所占权重
    max_capacity: int                           # 当前 live 会场最大容纳 fans 人数
    mental_threshold: int                       # 精神阈值
    yells: list[Yell]                           # 玩家当前所持 yells
    lines: list[OneLine]                        # 5 条线
    beat_count: int
    a_skill_count: int
    sp_skill_count: int

    def init_quest(self, live):
        self.quest_id = live.questId
        self.music_chart_pattern_id = live.quest.musicChartPatternId
        self.difficulty_level = live.quest.difficultyLevel
        self.position1_attribute_type = eAttributeType(live.quest.position1AttributeType)
        self.position2_attribute_type = eAttributeType(live.quest.position2AttributeType)
        self.position3_attribute_type = eAttributeType(live.quest.position3AttributeType)
        self.position4_attribute_type = eAttributeType(live.quest.position4AttributeType)
        self.position5_attribute_type = eAttributeType(live.quest.position5AttributeType)
        self.active_skill_weight_permil = live.quest.activeSkillWeightPermil
        self.special_skill_weight_permil = live.quest.specialSkillWeightPermil
        self.skill_stamina_weight_permil = live.quest.skillStaminaWeightPermil
        self.stamina_recovery_weight_permil = live.quest.staminaRecoveryWeightPermil
        self.beat_dance_weight_permil = live.quest.beatDanceWeightPermil
        self.beat_vocal_weight_permil = live.quest.beatVocalWeightPermil
        self.beat_visual_weight_permil = live.quest.beatVisualWeightPermil
        self.max_capacity = live.quest.maxCapacity
        self.mental_threshold = live.quest.mentalThreshold
        self.beat_count = live.quest.beatCount
        self.a_skill_count = live.quest.aSkillCount
        self.sp_skill_count = live.quest.spSkillCount

    def init_yells(self, live):
        self.yells = []
        for jyell in live.yells:
            yell = Yell()
            yell.name = jyell.name
            yell.value = jyell.value
            yell.type = eLiveAbilityType(jyell.type)
            self.yells.append(yell)

    def init_lines(self, live):
        self.lines = []
        for index in range(1, 6):
            one_line = OneLine()
            one_line.index = index
            # 初始化观众人数
            for jcard in live.result.userInfos[0].userDeck.cards:
                if jcard.index == index:
                    one_line.audience = jcard.audienceAmount
            one_line.init_photos(index, live.cardPhotos)
            one_line.init_charts(index, live)
            self.lines.append(one_line)

    def __init__(self, path: str) -> None:
        with open(path, encoding="utf8") as fp:
            live = json.load(fp, object_hook=lambda d: SimpleNamespace(**d))
        self.init_quest(live)
        self.init_yells(live)
        self.init_lines(live)

    def __init__(self, live) -> None:
        self.init_quest(live)
        self.init_yells(live)
        self.init_lines(live)
    
    def get_yell_buff(self, buff_type: eLiveAbilityType) -> int:
        return sum([it.value for it in self.yells if it.type == buff_type])
