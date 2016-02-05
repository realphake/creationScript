import ODDcharRules as char

player = char.character("fighter")
player.giveEquipment(["breastplate", "helmet"])
monster = char.character("fighter", 1)

monster.attackedBy(player,player.stats['STR'])

player.logCharacter()
monster.logCharacter()
