
import unittest
import math

STR=0;CON=1;DEX=2;INT=3;WIS=4;CHA=5

FORT=0;REF=1;WILL=2; 
AT=3;AC=4

SKILROGU=0;BABROGU=1

BARB=0;MONK=1;PALA=2;RANG=3;ROGU=4;SAGE=5;SHAM=6;TACT=7

DWA=0;ELF=1;GNO=2;HAL=3;HUM=4;ORC=5;

CELES=10;DEMON=11;DRAGO=12;SENTCON=13;
GHOU=14;LICH=15;MUMM=16;SKEL=17;VAMP=18;
UTTBRU=19

ACRO=0;ATHL=1;LARC=2;STEA=3;RIDE=4;VIGO=5;
ARCA=6;ENGI=7;GEOG=8;HIST=9;MEDI=10;NATU=11;
BLUF=12;DIPL=13;INTI=14;PERC=15;

ItemsTrack=-1

PathWarRage=0;PathWarDervish=1;PathDestruction=2;PathAncestors=3
DisciplineSerpent=4;DisciplineCrane=5;DisciplineDragon=6
JudgmentKnowing=7;BastionProtection=8;HeroicaEndings=9;SmitingWar=10;VirtueRenewal=11;
ProfessionalSoldier=12;ReignArrows=13;IronMagi=14;BattleTempering=15;
EsotericaRadica=16;OffensiveAssassin=17;OffensiveSwashbuckler=18;OffensiveDemoman=19;DefensiveAcrobatic=20;DefensiveNinjas=21;DefensiveFortune=22;
WrathJustBlade=23;WrathArcaneLore=24;ForceWill=25;ArcaneSecrets=26;
Incantation=27;ShamanSpells=28;
TacticalInsight=29;BagOfTricks=30;TacticianSpells=31

Celestial=32;Demon=33;Dragon=34;SentientConstruct=35;
UndeadGhoul=36;UndeadLich=37;UndeadMummy=38;UndeadSkeleton=39;UndeadVampire=40;
UtterBrute=41;

def statBonus(stat):
	return int((stat-10)/2)

class character:
	clas = None
	race = None
	classhp = None
	goodbab = False
	stats = None
	kom = None
	kdm = None
	level = None
	badsave = None
	trained = None
	skillorbab = None
	humanbonus = None
	
	def getbab(s):
		bab = 0
		if s.goodbab: bab = s.level
		else: bab = int(s.level*0.75)
		babarray = [bab-5] * (int(bab/5.0)+1)
		babarray[0] = bab
		return babarray
	
	def getbonus(s, stat):
		return statBonus(s.stats[stat])
		
	def getmove(s):
		if s.race == GNO: return 25; # TODO plus increases per level
		else: return 30; # TODO plus increases per level
	
	def gethp(s):
		return (s.classhp+s.getbonus(s.kdm)) * (s.level+1)
	
	def getac(s):
		return 10 + s.getbab()[0] + s.getbonus(s.kdm) + (1 if s.issmall() else 0) + (1 if s.humanbonus == AC else 0)
	
	def issmall(s):
		return (s.race == HAL or s.race == GNO)
	
	def getdamagereduction(s):
		return int(s.getbonus(CON)/2)
	
	def getsave(s, frw, vscombatmaneuver=False):
		save = max(s.getbonus(2*frw),s.getbonus(2*frw+1)) - (2 if s.issmall() else 0)
		if s.race == HAL and frw == WILL: save += 1
		if s.humanbonus == frw: save += 1
		if s.badsave == frw: return save + int(s.level/2)
		else: return save + int(s.level*(2.0/3.0)+2) 
			
	def getattackbonus(s):
		return [(x + s.getbonus(s.kom) + (1 if s.issmall() else 0) + (1 if s.humanbonus == AT else 0)) for x in s.getbab()] 
	
	def getdamage(s):
		return s.getbonus(s.kom) + int(s.getbonus(STR)/2)
	
	def getskill(s,skill):
		total = 0
		if skill in [ACRO,LARC,STEA,RIDE]: total += s.getbonus(DEX)
		elif skill == VIGO: total += s.getbonus(CON)
		elif skill == ATHL: total += s.getbonus(STR)
		elif skill in [ARCA,ENGI,GEOG,HIST,MEDI,NATU]: total += s.getbonus(INT)
		elif skill in [BLUF,DIPL,INTI]: total += s.getbonus(CHA)
		elif skill == PERC: total += s.getbonus(WIS)
		if skill in s.trained: total += s.level
		if s.race == DWA and skill == ENGI: total += 1+int(math.floor(s.level/8.0))
		elif s.race == ELF and skill == NATU: total += 1+int(math.floor(s.level/8.0))
		elif s.race == GNO and skill == DIPL: total += 1+int(math.floor(s.level/8.0))
		elif s.race == ORC and skill == ATHL: total += 1+int(math.floor(s.level/8.0))
		elif s.race == LICH and skill == ARCA: total += 1+int(math.floor(s.level/8.0))
		return total
		# TODO human's skill bonus
		
	def show(s):
		print("strength "+str(s.stats[STR])+" (+"+str(s.getbonus(STR))+")")
		print("constitution "+str(s.stats[CON])+" (+"+str(s.getbonus(CON))+")")
		print("dexterity "+str(s.stats[DEX])+" (+"+str(s.getbonus(DEX))+")")
		print("intelligence "+str(s.stats[INT])+" (+"+str(s.getbonus(INT))+")")
		print("wisdom "+str(s.stats[WIS])+" (+"+str(s.getbonus(WIS))+")")
		print("charisma "+str(s.stats[CHA])+" (+"+str(s.getbonus(CHA))+")")
		print("hp "+str(s.gethp())+", damage reduction "+str(s.getdamagereduction()))
		print("ac "+str(s.getac()))
		print("attack +"+str(s.getattackbonus()) + ", damage 1d6+"+str(s.getdamage()))
		print("fort "+str(s.getsave(FORT))+" ref "+str(s.getsave(REF))+" will "+str(s.getsave(WILL)))
		print("acrobatics "+str(s.getskill(ACRO))+", athletics "+str(s.getskill(ATHL))+", larceny "+str(s.getskill(LARC)))
		print("stealth "+str(s.getskill(STEA))+", ride "+str(s.getskill(RIDE))+", vigor "+str(s.getskill(VIGO)))
		print("arcana "+str(s.getskill(ARCA))+", engineering "+str(s.getskill(ENGI))+", geography "+str(s.getskill(GEOG)))
		print("history "+str(s.getskill(HIST))+", medicine "+str(s.getskill(MEDI))+", nature "+str(s.getskill(NATU)))
		print("bluff "+str(s.getskill(BLUF))+", diplomacy "+str(s.getskill(DIPL))+", intimidate "+str(s.getskill(INTI))+", perception "+str(s.getskill(PERC)))
	
	def setlevel(s,level):
		s.level = level;
	
	def setclass(s,clas,choiceone=None,choicetwo=None):
		#choiceone is for rogue's save. choicetwo is for rogue's bab or skills.
		#choiceone is for sage's kom. choicetwo is for sage's kdm. 
		if (clas == MONK or clas == SAGE) and choiceone not in [FORT, REF, WILL]:
			raise Exception("Choose any save as your bad save")
		if clas == ROGU and choiceone not in [FORT, WILL]:
			raise Exception("Choose FORT or WILL as your bad save")
		if clas == ROGU and choicetwo not in [SKILROGU, BABROGU]:
			raise Exception("Choose between skills or base attack bonus")
		if clas == SAGE and (choiceone not in [INT,WIS,CHA] or choicetwo not in [STR,CON,DEX]): 
			raise Exception("Choose a mental stat for KOM and a physical stat for KDM")
		if clas == SKEL and choiceone not in [DEX,INT]: 
			raise Exception("Choose DEX or INT as KDM")
		
		s.clas = clas
		if clas == ROGU: s.skillorbab = choicetwo
		
		if clas == BARB or clas == PALA or clas == RANG: s.classhp = 10
		elif clas == GHOU or clas == LICH or clas == MUMM or clas == SKEL or clas == VAMP: s.classhp = 10
		else: s.classhp = 8
		
		if clas == SAGE or clas == SHAM or clas == TACT: s.goodbab = False
		elif clas == ROGU and choicetwo == SKILROGU: s.goodbab = False
		else: s.goodbab = True
		
		if clas == RANG: s.badsave = WILL
		elif clas == TACT: s.badsave = FORT
		elif clas == MONK or clas == ROGU or clas == SAGE: s.badsave = choiceone
		elif clas == GHOU or clas == LICH or clas == MUMM or clas == SKEL or clas == VAMP: s.badsave = REF
		else: s.badsave = REF
		
		if clas == MONK or clas == SHAM: s.kom = WIS
		elif clas == RANG or clas == VAMP: s.kom = DEX
		elif clas == TACT or clas == LICH: s.kom = INT
		elif clas == SAGE: s.kom = choiceone
		elif clas == PALA or clas == GHOU or clas == MUMM or clas == SKEL: s.kom = STR
		else: s.kom = None # Rogue and Barbarian's kom are set later
		
		if clas == PALA or clas == SHAM or clas == MUMM or clas == VAMP: s.kdm = CHA
		elif clas == RANG: s.kdm = INT
		elif clas == SAGE: s.kdm = choicetwo
		elif clas == BARB or clas == MONK or clas == TACT or clas == GHOU: s.kdm = CON
		elif clas == LICH: s.kdm = WIS
		elif clas == SKEL: s.kdm = choiceone
		else: s.kdm = None # Rogue's kdm is set later
		
	def setrace(s,race, choiceone=None, choicetwo=None):
		if race == ELF and choiceone not in [INT,WIS,CHA]:
			raise Exception("Choose INT, WIS or CHA to raise by 2")
		if race == HUM and choiceone not in [STR,CON,DEX,INT,WIS,CHA]:
			raise Exception("Choose any one stat to raise by 2")
		if race == HUM and choicetwo not in [FORT,REF,WILL,AT,AC]:
			raise Exception("Choose AT, AC or any save to raise by 1")
		if race == LICH and choiceone not in [INT,WIS]:
			raise Exception("Choose INT or WIS to raise by 2")
		if race == SKEL and choiceone not in [STR,CON,DEX]:
			raise Exception("Choose STR, CON or DEX to raise by 2")
		if race == VAMP and choiceone not in [STR,CON,DEX,INT,WIS,CHA]:
			raise Exception("Choose any one stat to raise by 2")

		s.race = race
		
		if race == DWA: s.stats[CON] += 2; s.stats[INT] += 2; s.stats[CHA] -= 2
		elif race == ELF: s.stats[DEX] += 2; s.stats[choiceone] += 2; s.stats[CON] -= 2
		elif race == GNO: s.stats[CON] += 2; s.stats[CHA] += 2; s.stats[STR] -= 2
		elif race == HAL: s.stats[DEX] += 2
		elif race == HUM: 
			s.stats[choiceone] += 2 
			s.humanbonus = choicetwo
		elif race == ORC: s.stats[STR] += 2; s.stats[CON] += 2; s.stats[CHA] -= 2
		elif race == GHOU: s.stats[STR] += 2; s.stats[CON] += 2; s.stats[WIS] -= 2
		elif race == LICH: s.stats[choiceone] += 2
		elif race == MUMM: s.stats[CHA] += 2
		elif race == SKEL: s.stats[choiceone] += 2
		elif race == VAMP: s.stats[choiceone] += 2
		
	def settracks(s,tracks):
		for track in tracks:
			if track == PathWarRage: s.kom = STR
			elif track in (PathWarDervish, OffensiveAssassin, OffensiveSwashbuckler): s.kom = DEX
			elif track == OffensiveDemoman: s.kom = INT
			
			if track == DefensiveAcrobatic: s.kdm = CON
			elif track == DefensiveNinjas: s.kdm = WIS
			elif track == DefensiveFortune: s.kdm = CHA

	def setskills(s,skills):
		skills = set(skills)
		if (s.clas == BARB or s.clas == PALA) and len(skills) != 5:
			raise Exception("You chose " +len(skills)+ " skills but you get 5")
		if (s.clas == MONK or s.clas == RANG or s.clas == SAGE or s.clas == SHAM) and len(skills) != 6:
			raise Exception("You chose " +len(skills)+ " skills but you get 6")
		if s.clas == TACT and (len(skills) != 9 or not set([ARCA,ENGI,GEOG,HIST,MEDI,NATU]).issubset(skills)):
			raise Exception("You didn't choose 9 skills or didn't choose every knowledge skill")
		if s.clas == ROGU and skillorbab == SKILROGU and len(skills) != 8:
			raise Exception("You chose " +len(skills)+ " skills but you get 8")
		if s.clas == ROGU and skillorbab == BABROGU and len(skills) != 6:
			raise Exception("You chose " +len(skills)+ " skills but you get 6")
			
		s.trained = skills

c = character()
c.setlevel(1)
c.stats = [10,14,16,12,10,14]
c.setclass(VAMP)
c.setrace(VAMP,DEX)
c.setskills([ATHL,PERC,INTI,ACRO,LARC])
c.settracks([UndeadVampire, EsotericaRadica, OffensiveAssassin,DefensiveNinjas])
c.show()

c = character()
c.setlevel(1)
c.stats = [10,14,16,12,14,10]
c.setclass(VAMP)
c.setrace(VAMP,DEX)
c.setskills([ATHL,PERC,INTI,ACRO,LARC])
c.settracks([UndeadVampire, EsotericaRadica, OffensiveAssassin,DefensiveNinjas])
c.show()

#TODO when setting new stats, racial stats are overwritten. 

class Tests(unittest.TestCase):

	def setUp(s):
		global c 
		c = character()
		c.setlevel(1)
		c.stats = [16,14,14,12,10,10]

	def testmonk(s):
		c.setclass(MONK,FORT)
		s.assertEqual(c.gethp(), (8+2)*2); s.assertEqual(c.getdamagereduction(), int(2/2))
		s.assertEqual(c.getac(), 10+2+1)
		s.assertEqual(c.getsave(FORT), 0+3); s.assertEqual(c.getsave(REF), 2+2); s.assertEqual(c.getsave(WILL), 2+0)
		s.assertEqual(c.getdamage(), 0+int(3/2))
		
	def testorcpaladin(s):
		c.setclass(PALA)
		c.setrace(ORC)
		c.setskills([ATHL,PERC,INTI,ACRO,LARC])
		s.assertEqual(c.gethp(), (10-1)*2); s.assertEqual(c.getdamagereduction(), int(2/2))
		s.assertEqual(c.getac(), 10-1+1)
		s.assertEqual(c.getsave(FORT), 2+4); s.assertEqual(c.getsave(REF), 0+2); s.assertEqual(c.getsave(WILL), 2+0)
		s.assertEqual(c.getdamage(), 4+int(4/2))
		s.assertEqual(c.getskill(ATHL), 4+1+1)
		
	def testvampirerogue(s):
		c.stats = [10,14,16,12,10,14]
		c.setclass(VAMP)
		c.setrace(VAMP,DEX)
		c.setskills([ATHL,PERC,INTI,ACRO,LARC])
		c.settracks([UndeadVampire, EsotericaRadica, OffensiveAssassin,DefensiveNinjas])
		s.assertEqual(c.gethp(), (10+0)*2); s.assertEqual(c.getdamagereduction(), int(2/2.0))
		s.assertEqual(c.getac(), 10+0+1)
		s.assertEqual(c.getsave(FORT), 2+2); s.assertEqual(c.getsave(REF), 0+4); s.assertEqual(c.getsave(WILL), 2+2)
		s.assertEqual(c.getdamage(), 4+int(0/2.0))

if __name__ == '__main__':
	unittest.main()
