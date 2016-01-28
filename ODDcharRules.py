import math
import random

STR=0;CON=1;DEX=2;INT=3;WIS=4;CHA=5;

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

class character:
	job = "";
	stats = [];

	spellsUsed = [0,0,0,0,0,0];
	experience = 0;
	
	def __init__(c, givenJob):
		c.job = givenJob;
		
	def setStats(c,givenStats):
		c.stats = [0,0,0,0,0,0]
		c.stats[STR] = givenStats[STR]
		c.stats[CON] = givenStats[CON]
		c.stats[DEX] = givenStats[DEX]
		c.stats[INT] = givenStats[INT]
		c.stats[WIS] = givenStats[WIS]
		c.stats[CHA] = givenStats[CHA]
		
	def getStats(c):
		return c.stats;
		
	def setRandomStats(c):
		c.stats = [sum([random.randint(1,6) for _ in range(3)]) for _ in range(6)]
	
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
		return 1 if c.stats[CON] >= 15 else (-1 if c.stats[CON] <= 6 else 0);
		
	def getHitPoints(c):
		return 6 + ((c.getHitDice() - 1) * 4) + (c.getHitDice() * c.getHPModifier())

c = character("cleric")
c.setExperience(500)
c.setRandomStats()
print(c.getLevel())
print(c.getHitDice())
print(c.getHitPoints())
print(c.getStats())
