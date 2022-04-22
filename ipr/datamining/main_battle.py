import json
from live_ob import CardBeat
from pathlib import Path
from live_ob import LiveOb

def main():
    dir = Path(
        "../ProtobufNet/bin/Debug/net6.0/json")
    for file in dir.glob("pvp*.json"):
        with file.open("r", encoding="utf8") as fp:
            jdict = json.load(fp)
        live = LiveOb(jdict, "pvp")
        live.analyze_battle()
        for row in live.rows:
            act_card = row.beats[row.act - 1]
            sil_card = row.beats[act_opp[row.act] - 1]
            act_power = calc_power(act_card, row.attribute, row.chart_type)
            sil_power = calc_power(sil_card, row.attribute, row.chart_type)
            assert act_power > sil_power
                
def calc_power(card: CardBeat, attr: int, chart_type: int) -> int:
    param = card.get_param(attr)
    stamina = card.stamina
    max_stamina = card.max_stamina
    bonus = card.get_skill_rate_bonus()
    possible = card.is_possible(chart_type)
    rate = 1 - int(int(max_stamina - stamina) / int(max_stamina * 0.05)) * 0.025 + bonus
    return param * rate * possible

act_opp = {
    1: 6,
    2: 7,
    3: 8,
    4: 9,
    5: 10,
    6: 1,
    7: 2,
    8: 3,
    9: 4,
    10: 5
}

if __name__ == "__main__":
    main()
    

