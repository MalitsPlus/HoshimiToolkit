## 1. Params
### 1.1 base param
$baseParam = \lfloor \lfloor paramValue \cdot \frac {paramRatioPermil} {1000} \rfloor \cdot {paramBonusPermil \over 1000} \rfloor$

### 1.2 pannel display param
$pannelParam = baseParam \cdot \lfloor {\sum yellPermil \over 1000} \rfloor + staffValue$

### 1.3 deck param
$deckParam = \lfloor baseParam \cdot (1 + {\min(\overbrace{\sum bonusPermil}^{\text{yell, accessories, photos}}, 1000000) \over 1000}) \rfloor + \overbrace{\sum bonusValue}^{\text{staff, accessories, photos}}$

### 1.4 live param
$liveParam = \lfloor deckParam \cdot (1 + {\sum \min(grade, maxGrade) \cdot value \over 1000}) \rfloor$