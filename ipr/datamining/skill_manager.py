import json
from pathlib import Path
from singleton import singleton
from master_skill import MasterSkill, Level, master_skill_from_dict
from master_skill_efficacy import MasterSkillEfficacy, master_skill_efficacy_from_dict

class SkillOb:
    id: str
    name: str
    category_type: int
    level: Level
    description: str
    stamina: int
    trigger_id: str
    probability_permil: int
    limit_count: int
    cool_time: int
    skill_details: list[MasterSkillEfficacy]

@singleton
class SkillManager:
    skill_path = "../ProtobufNet/bin/Debug/net6.0/MasterJson/Skill.json"
    efficacy_path = "../ProtobufNet/bin/Debug/net6.0/MasterJson/SkillEfficacy.json"
    master_skills: list[MasterSkill]
    master_efficacy: list[MasterSkillEfficacy]

    def __init__(self) -> None:
        file = Path(self.skill_path)
        with file.open("r", encoding="utf8") as fp:
            d = json.load(fp)
            self.master_skills = master_skill_from_dict(d)
        file = Path(self.efficacy_path)
        with file.open("r", encoding="utf8") as fp:
            d = json.load(fp)
            self.master_efficacy = master_skill_efficacy_from_dict(d)

    def get_skill(self, id: str) -> MasterSkill:
        for skill in self.master_skills:
            if skill.id == id:
                return skill
    
    def get_efficacy(self, id: str) -> MasterSkillEfficacy:
        for eff in self.master_efficacy:
            if eff.id == id:
                return eff
    
    def get_skill_ob(self, id: str, level: int, init_details: bool = True) -> SkillOb:
        origin = self.get_skill(id)
        skill = SkillOb()
        skill.id = origin.id
        skill.name = origin.name
        skill.category_type = origin.category_type
        for skill_level in origin.levels:
            if skill_level.level == level:
                origin_lv = skill_level
        skill.level = origin_lv.level
        skill.description = origin_lv.description
        skill.stamina = origin_lv.stamina
        skill.trigger_id = origin_lv.trigger_id
        skill.probability_permil = origin_lv.probability_permil
        skill.limit_count = origin_lv.limit_count
        skill.cool_time = origin_lv.cool_time
        if init_details:
            skill.skill_details = list()
            for detail in origin_lv.skill_details:
                eff = self.get_efficacy(detail.efficacy_id)
                skill.skill_details.append(eff)
        return skill