import ODDcharRules as char

player = char.character("fighter")
player.setRandomStats()
monster = char.character("fighter")
monster.setAverageStats()

if player.getAttackRoll(char.STR) > monster.getArmor():
	monster.takeDamage(char.rollDice(6)+player.getDamageModifier(char.STR))

