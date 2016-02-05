import math
import random

statNames = ['STR', 'CON', 'DEX', 'INT', 'WIS', 'CHA']

fighterProgression = [0,20,40,80,160,320,640,1200,2400];
	
wizardProgression = [0,25,50,100,200,400,800,1600,3200,6400,12000];
wizardSpells = [[1],
				[2],
				[2,1],
				[3,2],
				[3,2,1],
				[3,3,2],
				[4,3,2,1],
				[4,3,3,2],
				[4,4,3,2,1],
				[4,4,3,3,2],
				[5,4,4,3,2,1]];
				   
clericProgression = [0,15,30,60,120,250,500,1000];
clericHitDice =	[1,1,2,3,4,4,5,6];
clericSpells = [[0],
				[1],
				[2],
				[2,1],
				[2,2],
				[2,2,1],
				[2,2,2,1],
				[2,2,2,2,1]];
				
armorPieces = ["breastplate","helmet","shield","tassets","greaves","gloves","buff coat"]

def rollDice(size):
	return random.randint(1,size)

class character:
	job = "";
	stats = {};

	spellsUsed = [0,0,0,0,0,0];
	damageTaken = 0;
	equipment = [];
	experience = 0;
	
	def __init__(c, givenJob, statTest = 0):
		c.stats = {};
		c.job = givenJob;
		if statTest == 0:
			for statName in statNames:
				c.stats[statName] = sum([random.randint(1,6) for _ in range(3)]);
		else:
			for statName in statNames:
				c.stats[statName] = 10;
		c.spellsUsed = [0,0,0,0,0,0];
		c.damageTaken = 0;
		c.equipment = [];
		c.experience = 0;
		
	def setStats(c,givenStats):
		c.stats = [0,0,0,0,0,0]
		c.stats = givenStats
		
	def getStats(c):
		return c.stats;
		
	def getJob(c):
		return c.job;
		
	def getExperience(c):
		return c.experience
	
	def setExperience(c, exp):
		c.experience = exp;
	
	def getProgression(c):
		if c.job == "fighter": return fighterProgression;
		elif c.job == "wizard": return wizardProgression;
		elif c.job == "cleric": return clericProgression;
	
	def getLevel(c):
		progression = c.getProgression();
		i = len(progression);
		while i > 0:
			if c.experience >= progression[i-1]: 
				return i;
			i-=1;
	
	def getHitDice(c):
		if c.job == "fighter": return c.getLevel();
		elif c.job == "wizard": return int(math.ceil(c.getLevel()/2.0));
		elif c.job == "cleric": return clericHitDice[c.getLevel()-1];
		
	def getHPModifier(c):
		return 1 if c.stats['CON'] >= 15 else (-1 if c.stats['CON'] <= 6 else 0);
		
	def getAttackModifier(c, stat):
		return c.getHitDice()+(1 if stat >= 13 else (-1 if stat <= 8 else 0));
		
	def getAttackRoll(c,stat):
		return rollDice(20) + c.getAttackModifier(stat)
		
	def getDamageModifier(c, stat):
		return 1 if stat >= 15 else (-1 if stat <= 6 else 0);
		
	def getDamageRoll(c,stat):
		return rollDice(6)+c.getDamageModifier(stat)
		
	def getHitPoints(c):
		return 6 + ((c.getHitDice() - 1) * 4) + (c.getHitDice() * c.getHPModifier())
		
	def giveEquipment(c,items):
		for item in items:
			c.equipment.append(item)
	
	def getArmor(c):
		armorClass = 10;
		for piece in armorPieces:
			if piece in c.equipment: 
				armorClass = armorClass + 1;
		return armorClass;
	
	def takeDamage(c, damage):
		c.damageTaken += damage;
		
	def getHPLeft(c):
		return c.getHitPoints()-c.damageTaken
		
	def attackedBy(c,opponent,stat):
		if opponent.getAttackRoll(stat) > c.getArmor():
			c.takeDamage(opponent.getDamageRoll(stat))
		
	def getSpells(c):
		if c.job == "fighter": return [];
		elif c.job == "wizard": return wizardSpells[c.getLevel()];
		elif c.job == "cleric": return clericSpells[c.getLevel()];
		
	def logCharacter(c):
		print("Level {} {} ({} XP)".format(c.getLevel(), c.getJob(), c.getExperience()))
		print("{} Hit Dice, Hit Points: {}/{}".format(c.getHitDice(), c.getHPLeft(), c.getHitPoints()))
		print("Melee attack: 1d20{}>AC --> 1d6{} damage".format('%+d' % c.getAttackModifier(c.stats['STR']), '%+d' % c.getDamageModifier(c.stats['STR'])))
		print("Ranged attack: 1d20{}>AC --> 1d6{} damage".format('%+d' % c.getAttackModifier(c.stats['DEX']), '%+d' % c.getDamageModifier(c.stats['DEX'])))
		print("Armor Class: {}".format(c.getArmor()))
		print("Spells per day: {}".format(c.getSpells()))
		print("STR: {}, CON: {}, DEX: {}".format(c.stats['STR'], c.stats['CON'], c.stats['DEX']))
		print("INT: {}, WIS: {}, CHA: {}".format(c.stats['INT'], c.stats['WIS'], c.stats['CHA']))

#c = character("cleric")
#c.setExperience(500)
#c.setRandomStats()
#c.logCharacter()
