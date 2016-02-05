import ODDcharRules as char

player = char.character("fighter", 1)
player.giveEquipment(["breastplate", "helmet"])
monster = char.character("fighter", 0)

monster.attackedBy(player,player.stats.STR)

player.logCharacter()
monster.logCharacter()
