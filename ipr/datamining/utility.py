from json_manager import combo_adv, audience_adv

def get_combo_adv(current_combo: int) -> int:
    """获取指定combo时的分数奖励\n
    Args:
        current_combo: 指定的连击数
    Returns: 
        连击奖励千分率"""
    bonus = 1000
    for it in combo_adv():
        if current_combo >= it.comboCount:
            bonus = it.advantagePermil
            break
    return bonus - 1000

def get_audience_adv(audience: int, max_capacity: int) -> int:
    """获取指定audience时的分数奖励\n
    Args:
        audience: 单个爱抖露的来场fans人数
        max_capacity: 会场最多容纳人数
    Returns:
        观众奖励千分率"""
    bonus = 1000
    aud = min(int(max_capacity / 5), audience)
    for it in audience_adv():
        if aud >= it.audienceAmount:
            bonus = it.advantagePermil
            break
    return bonus - 1000
