import ODDcharRules as char

player = char.character("fighter")
player.setRandomStats()
monster = char.character("fighter")
monster.setAverageStats()

if player.getAttackRoll(char.STR) > monster.getArmor():
	monster.attackedBy(player)

monster.logCharacter()
