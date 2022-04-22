import json
from pathlib import Path
from types import SimpleNamespace

directory = "master_json"

_audience_advantage: list = None
_combo_advantage: list = None

def audience_adv() -> list:
    global _audience_advantage
    if _audience_advantage is None:
        _audience_advantage = json.load(open(f"{directory}/QuestAudienceAdvantage.json", encoding="utf8"), object_hook=lambda d: SimpleNamespace(**d))
        _audience_advantage.sort(key=lambda it: it.audienceAmount, reverse=True)
    return _audience_advantage

def combo_adv() -> list:
    global _combo_advantage
    if _combo_advantage is None:
        _combo_advantage = json.load(open(f"{directory}/ComboAdvantage.json", encoding="utf8"), object_hook=lambda d: SimpleNamespace(**d))
        _combo_advantage.sort(key=lambda it: it.comboCount, reverse=True)
    return _combo_advantage

def music_pattern() -> list:
    global _combo_advantage
    if _combo_advantage is None:
        _combo_advantage = json.load(open(
            f"{directory}/ComboAdvantage.json", encoding="utf8"), object_hook=lambda d: SimpleNamespace(**d))
        _combo_advantage.sort(key=lambda it: it.comboCount, reverse=True)
    return _combo_advantage

if __name__ == "__main__":
    a = combo_adv()
    pass
