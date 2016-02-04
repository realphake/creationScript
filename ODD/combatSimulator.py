import ODDcharRules as char

player = char.character("fighter")
player.setRandomStats()
player.giveEquipment(["breastplate", "helmet"])
monster = char.character("fighter")
monster.setAverageStats()

monster.attackedBy(player,char.STR)

player.logCharacter()
monster.logCharacter()
