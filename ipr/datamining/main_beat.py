import json
import numpy as np
from pathlib import Path
from types import SimpleNamespace
from proto_enums import eSkillEfficacyType
from proto_enums import eAttributeType
from one_live import OneLive
from utility import get_audience_adv
from proto_enums import eMusicChartType, eLiveAbilityType

def get_realtime_aud_bonus(audience: int, cap: int, index: int, order: int, live: OneLive) -> float:
    """目前只适用于整个line中只有单个集中的情况"""
    buff_audience = get_audience_adv(audience, cap) / 1000
    all_aud = 0
    this_line = live.lines[index - 1]
    has_eff = []
    for line in live.lines:
        chart = line.charts[order]
        all_aud += line.audience
        for eff in chart.effects:
            if eff.skill_efficacy_type == eSkillEfficacyType.AudienceAmountIncrease:
                has_eff.append(line.index)
                aud_eff = eff
                _type = "inc"
            if eff.skill_efficacy_type == eSkillEfficacyType.AudienceAmountReduction:
                has_eff.append(line.index)
                aud_eff = eff
                _type = "dec"
    if has_eff.__len__() == 0:
        return buff_audience
    
    permil1 = aud_eff.value
    permil2 = aud_eff.value2
    bearer_aud = live.lines[has_eff[0] - 1].audience
    diff_amnt = bearer_aud * (permil1 / 1000)
    if index in has_eff:
        if _type == "inc":
            final_amnt = diff_amnt + bearer_aud
        elif _type == "dec":
            final_amnt = bearer_aud - diff_amnt
        return get_audience_adv(final_amnt, 999999999) / 1000
    else:
        if _type == "inc":
            rate_aud = audience / (all_aud - bearer_aud)
            amnt_dec = rate_aud * diff_amnt
            return get_audience_adv(audience - amnt_dec, cap) / 1000
        elif _type == "dec":
            amnt_inc = diff_amnt / 4
            return get_audience_adv(audience + amnt_inc, 999999999) / 1000

files = Path("data").glob("*.json")
files = Path(
    "../ProtobufNet/bin/Debug/net6.0/json").glob("queststart220415180728618_attached.json")
for file in files:
    with file.open(encoding="utf8") as fp:
        jlive = json.load(fp, object_hook=lambda d: SimpleNamespace(**d))
    live = OneLive(jlive)

    # ⭐入参：当场live的总beat数
    count_beat = live.beat_count
    # 参考参数：当场live的总A技能数（应该无关）
    count_a = live.a_skill_count
    # 参考参数：当场live的总SP技能数（应该无关）
    count_sp = live.sp_skill_count
    # 参考参数：当场live的所有节点数（应该无关）
    count_all = count_beat + count_a + count_sp 

    # ⭐入参：玩家卡池中所有的beat乘算应援（千分比）
    buff_beat_yell_mul = live.get_yell_buff(eLiveAbilityType.BeatScoreMultiply) / 1000
    # 参考参数：玩家卡池中所有的beat加算应援（不需要当作入参，后续有合计）
    buff_beat_yell_add = live.get_yell_buff(eLiveAbilityType.BeatScoreAdd) 
    # A技能应援乘算千分比 
    buff_a_yell_mul = live.get_yell_buff(eLiveAbilityType.ActiveSkillScoreMultiply) / 1000
    # SP技能应援成算千分比
    buff_sp_yell_mul = live.get_yell_buff(eLiveAbilityType.SpecialSkillScoreMultiply) / 1000
    # CriBonus
    buff_crib_yell_mul = live.get_yell_buff(eLiveAbilityType.CriticalScoreMultiply) / 1000

    # 一个line包括一条轴上所有节点的快照
    for line in live.lines:

        # 参考参数：当前line位置 1: center. 2: center左. 3: center右. 4: 最左. 5: 最右.
        index = line.index      
        # ⭐入参：当前位置爱抖露所带photo中所有的beat乘算加成（千分率）
        buff_beat_photo_mul = line.get_photo_buff(eLiveAbilityType.BeatScoreMultiply) / 1000
        # 参考参数：当前位置爱抖露所带photo中所有的beat加算加成（不需要当作入参，后续有合计）
        buff_beat_photo_add = line.get_photo_buff(eLiveAbilityType.BeatScoreAdd) 
        # A技能photo乘算加成千分率
        buff_a_photo_mul = line.get_photo_buff(eLiveAbilityType.ActiveSkillScoreMultiply) / 1000
        # A技能photo加算千分比
        buff_a_photo_add = line.get_photo_buff(eLiveAbilityType.ActiveSkillScoreAdd) / 1000
        # SP技能photo成算千分比
        buff_sp_photo_mul = line.get_photo_buff(eLiveAbilityType.SpecialSkillScoreMultiply) / 1000
        # SP技能加算千分比
        buff_sp_photo_add = line.get_photo_buff(eLiveAbilityType.SpecialSkillScoreAdd) / 1000
        # CriBonus
        buff_crib_photo_mul = line.get_photo_buff(eLiveAbilityType.CriticalScoreMultiply) / 1000
        # 测试用参数，可删掉
        ratios = list[float]()
        ratios_plain = list[float]()
        ratios_buffed = list[float]()
        score_plain = list[int]()
        score_buffed = list[int]()

        cri_no_ratios = list[float]()
        cri_yes_ratios = list[float]()
        cri_yes_buf_ratios = list[float]()

        i = -1
        # 一个chart包含一个节点上的快照
        for chart in line.charts:
            i += 1
            # 当这个节点是A、SP技能节点时跳过
            # if chart.chart_type != eMusicChartType.Beat:
            #     # ratios.append(0)
            #     continue
            # 暂时先不考虑身上带有加分等会影响计算的buff和critical的复杂情况
            # if chart.is_critical: #or chart.is_beat_ng_buffed():
            #     continue

            # 参考参数：当前combo数（不需要当作入参，后续有combo->奖励值的映射值）
            combo = chart.combo 
            # 参考参数：当前节点在整场live中的序号
            number = chart.number
            # ⭐输出：当前节点获得的beat分数
            score = chart.score
            # 🚩可选参数：爱抖露在当前的体力值
            stamina = chart.stamina
            
            # ⭐入参：根据爱抖露当前的三围属性和当场live固定的三围权重计算出的基础属性值
            beat_base = chart.dance * live.beat_dance_weight_permil / 1000\
                + chart.vocal * live.beat_vocal_weight_permil / 1000\
                + chart.visual * live.beat_visual_weight_permil / 1000

            # ⭐入参：当前combo对应的combo奖励（千分比）
            buff_combo = chart.get_combo_bonus() / 1000
            # ⭐入参：当前位置的爱抖露对应的fans奖励（千分比）
            buff_audience = get_audience_adv(line.audience, live.max_capacity) / 1000

            # 参考参数：当前爱抖露所有beat分数乘算奖励合计
            # 不建议当作入参，因为不能确定这个游戏的乘算奖励是加起来再乘还是直接累乘
            # 应该将四个值分别当作单独的参数输入
            all_beat_bonus_permil = buff_beat_yell_mul + buff_audience + buff_beat_photo_mul + buff_combo

            # ⭐入参：当前位置爱抖露所持有beat分数的加算buff合计
            all_beat_bonus_add = buff_beat_yell_add + buff_beat_photo_add
            
            score_no_add = chart.score - all_beat_bonus_add

            # 参考参数：累乘情况下beat分数的白值
            # score_plain_mul = score_no_add / (1 + buff_combo) / (1 + buff_beat_photo_mul) / (1 + buff_audience) / (1 + buff_beat_yell_mul)
            # score_plain_mul = score_no_add / (1 + buff_combo) / (1 + buff_beat_yell_mul + buff_beat_photo_mul + buff_audience)
            # score_plain_mul = score_no_add / (1 + buff_combo) / (1 + buff_beat_photo_mul) / (1 + buff_beat_yell_mul + buff_audience
            score_plain_mul = score_no_add / (1 + buff_combo) / (1 + buff_audience) / (1 + buff_beat_yell_mul + buff_beat_photo_mul)
            
            # 测试用参数，可删掉
            ratio = score_plain_mul / beat_base * count_beat
            ratios.append(ratio)

            flag = False
            for one_line in live.lines:
                one_chart = one_line.charts[i]
                for ef in one_chart.effects:
                    if ef.skill_efficacy_type in [eSkillEfficacyType.AudienceAmountIncrease, eSkillEfficacyType.AudienceAmountReduction]:
                        flag = True

            # 如果有加分技能 
            if chart.is_beat_ng_buffed() or flag:
                sum_permil = 0
                cmb_permil = 1
                for ef in chart.effects:
                    if ef.skill_efficacy_type in [eSkillEfficacyType.BeatScoreUp, eSkillEfficacyType.ScoreUp]:
                        sum_permil += ef.value
                    if ef.skill_efficacy_type == eSkillEfficacyType.ComboScoreUp:
                        cmb_permil = 1 + ef.value / 1000
                sum_permil = sum_permil / 1000

                buff_audience = get_realtime_aud_bonus(line.audience, live.max_capacity, index, i, live)

                score_plain_mul = score_no_add / (1 + buff_combo * cmb_permil) / (1 + buff_audience) \
                    / (1 + buff_beat_yell_mul + buff_beat_photo_mul + sum_permil)
                
                ratio = score_plain_mul / beat_base * count_beat
                ratios_buffed.append(ratio)
                score_buffed.append(score_no_add)
                if i == 34:
                    a = 1
            else:
                ratios_plain.append(ratio)
                score_plain.append(score_no_add)

            if chart.is_critical:
                crib = 1 + 0.5 + buff_crib_yell_mul + buff_crib_photo_mul
                if chart.is_def_buffed([eSkillEfficacyType.CriticalBonusPermilUp]):
                    for ef in chart.effects:
                        if ef.skill_efficacy_type == eSkillEfficacyType.CriticalBonusPermilUp:                            
                            cri_yes_buf_ratios.append(ratio / (crib + ef.value / 1000))
                else:
                    cri_yes_ratios.append(ratio / crib)
            else:
                cri_no_ratios.append(ratio)

            if chart.chart_type != eMusicChartType.Beat and chart.card_index == 3 and index == 3:
                if chart.chart_type == eMusicChartType.ActiveSkill:
                    a_coefficient = 2.8
                    para = chart.vocal
                    a_bonus_add = buff_a_photo_add
                    tension_buff = chart.get_def_buff_value(eSkillEfficacyType.TensionUp)
                    score_plain_mul = (1 + buff_combo) * (1 + buff_audience) * (1 + buff_a_yell_mul + buff_a_photo_mul + tension_buff) 
                    # score_plain_mul = (1 + buff_combo) * (1 + buff_audience) * (1 + buff_a_yell_mul + buff_a_photo_mul) * (1 + tension_buff)
                    calc_score = para * score_plain_mul * a_coefficient + a_bonus_add
                    if chart.is_critical:
                        calc_score = calc_score * 1.59
                    rate = chart.score / calc_score
                    asdf = 1
                if chart.chart_type == eMusicChartType.SpecialSkill:
                    a_coefficient = 10.2
                    para = chart.vocal / 1.2
                    a_bonus_add = buff_sp_photo_add
                    tension_buff = chart.get_def_buff_value(eSkillEfficacyType.TensionUp)
                    score_plain_mul = (1 + buff_combo) * (1 + buff_audience) * (1 + buff_sp_yell_mul + buff_sp_photo_mul + tension_buff) 
                    # score_plain_mul = (1 + buff_combo) * (1 + buff_audience) * (1 + buff_sp_yell_mul + buff_sp_photo_mul) * (1 + tension_buff)
                    calc_score = para * score_plain_mul * a_coefficient + a_bonus_add
                    if chart.is_critical:
                        calc_score = calc_score * 1.59
                    rate = chart.score / calc_score
                    asdf = 1

        # 测试用参数，可删掉
        avg = np.mean(ratios)
        med = np.median(ratios)
        med_plain = np.median(ratios_plain)
        med_buffed = np.median(ratios_buffed)
        med_rat = med_buffed / med_plain

        cri_no_med = np.median(cri_no_ratios)
        cri_yes_med = np.median(cri_yes_ratios)
        cri_yes_buffed = np.median(cri_yes_buf_ratios)
        pass
