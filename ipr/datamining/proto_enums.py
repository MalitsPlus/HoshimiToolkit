from enum import Enum

class eLiveAbilityType(Enum):
    Unknown = 0
    DanceAdd = 1
    DanceMultiply = 2
    VocalAdd = 3
    VocalMultiply = 4
    VisualAdd = 5
    VisualMultiply = 6
    StaminaAdd = 7
    StaminaMultiply = 8
    MentalAdd = 9
    MentalMultiply = 10
    TechniqueAdd = 11
    TechniqueMultiply = 12
    PassiveSkill = 13
    ManagerExp = 14
    Gold = 15
    CardExp = 16
    BeatScoreAdd = 17
    BeatScoreMultiply = 18
    ActiveSkillScoreAdd = 19
    ActiveSkillScoreMultiply = 20
    SpecialSkillScoreAdd = 21
    SpecialSkillScoreMultiply = 22
    CriticalScoreMultiply = 23
    AudienceAmountUp = 24
    AccessoryParameterUp = 25
    PhotoLevelUp = 26

class eMusicChartType(Enum):
    Unknown = 0
    Beat = 1
    ActiveSkill = 2
    SpecialSkill = 3

class eAttributeType(Enum):
    Unknown = 0
    Dance = 1
    Vocal = 2
    Visual = 3

class eSkillEfficacyType(Enum):
    Unknown = 0
    ScoreGet = 1
    FixScoreGet = 2
    ScoreGetByMoreFanAmount = 3
    ScoreGetByLessFanAmount = 4
    ScoreGetByMoreFanEngage = 5
    ScoreGetByMoreStamina = 6
    ScoreGetByLessStamina = 7
    ScoreGetByMoreComboCount = 8
    ScoreGetByStrengthEffectCount = 9
    ScoreGetByTrigger = 10
    StaminaConsumptionReduction = 11
    ComboContinuation = 12
    DanceUp = 13
    VocalUp = 14
    VisualUp = 15
    ScoreUp = 16
    BeatScoreUp = 17
    ActiveSkillScoreUp = 18
    CriticalRateUp = 19
    CriticalBonusPermilUp = 20
    AudienceAmountIncrease = 21
    StaminaRecovery = 22
    FixStaminaRecovery = 23
    WeaknessEffectRecovery = 24
    StrengthEffectCountIncrease = 25
    StrengthEffectValueIncrease = 26
    CoolTimeReduction = 27
    AudienceAmountReduction = 28
    SkillImpossible = 29
    DanceDown = 30
    VocalDown = 31
    VisualDown = 32
    StaminaConsumptionIncrease = 33
    SpecialSkillScoreUp = 34
    TargetStaminaRecovery = 35
    ScoreGetByStatusEffectTypeGrade = 36
    SkillSuccessRateUp = 37
    TensionUp = 38
    ScoreGetBySkillActivationCount = 39
    WeaknessEffectPrevention = 40
    ComboScoreUp = 41
    PassiveSkillScoreUp = 42
    ScoreGetByMoreStaminaUse = 43
    WeaknessEffectInversion = 44
    StrengthEffectMigrationBeforeActiveSkill = 45
    StrengthEffectMigrationBeforeSpecialSkill = 46
    ScoreGetByDeckSupporter = 47
    ScoreGetByDeckBuffer = 48
    StaminaConsumption = 49
