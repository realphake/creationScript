
import unittest
import math

STR=0;CON=1;DEX=2;INT=3;WIS=4;CHA=5
FORT=0;REF=1;WILL=2
BARB=0;MONK=1;PALA=2;RANG=3;ROGU=4;SAGE=5;SHAM=6;TACT=7
SKILROGU=0;BABROGU=1
DWA=0;ELF=1;GNO=2;HAL=3;HUM=4;ORC=5;
ACRO=0;ATHL=1;LARC=2;STEA=3;RIDE=4;VIGO=5;ARCA=6;ENGI=7;GEOG=8;HIST=9;MEDI=10;NATU=11;BLUF=12;DIPL=13;INTI=14;PERC=15;

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
	
	def bab(s):
		if s.goodbab: return s.level
		else: return int(s.level*0.75)
	
	def bonus(s, stat):
		return statBonus(s.stats[stat])
	
	def hp(s):
		return (s.classhp+s.bonus(s.kdm)) * (s.level+1)
	
	def ac(s):
		return 10 + s.bab() + s.bonus(s.kdm)
	
	def damagereduction(s):
		return int(s.bonus(CON)/2)
	
	def save(s, frw):
		save = max(s.bonus(2*frw),s.bonus(2*frw+1))
		if s.race == HAL and frw == WILL: save += 1;
		if s.badsave == frw: return save + int(s.level/2)
		else: return save + int(s.level*(2/3)+2)
		
	def attackbonus(s):
		return s.bab() + s.bonus(s.kom)
	
	def damage(s):
		return s.bonus(s.kom) + int(s.bonus(STR)/2)
	
	def getskill(s,skill):
		total = 0
		if skill in [ACRO,LARC,STEA,RIDE]: total += s.bonus(DEX)
		elif skill == VIGO: total += s.bonus(CON)
		elif skill == ATHL: total += s.bonus(STR)
		elif skill in [ARCA,ENGI,GEOG,HIST,MEDI,NATU]: total += s.bonus(INT)
		elif skill in [BLUF,DIPL,INTI]: total += s.bonus(CHA)
		elif skill == PERC: total += s.bonus(WIS)
		if skill in s.trained: total += s.level
		if s.race == DWA and skill == ENGI: total += int(math.ceil(s.level/8.0))
		elif s.race == ELF and skill == NATU: total += int(math.ceil(s.level/8.0))
		elif s.race == GNO and skill == DIPL: total += int(math.ceil(s.level/8.0))
		elif s.race == ORC and skill == ATHL: total += int(math.ceil(s.level/8.0))
		return total
		# TODO human's skill bonus
		
	def show(s):
		print("strength "+str(s.stats[STR])+" (+"+str(s.bonus(STR))+")")
		print("constitution "+str(s.stats[CON])+" (+"+str(s.bonus(CON))+")")
		print("dexterity "+str(s.stats[DEX])+" (+"+str(s.bonus(DEX))+")")
		print("intelligence "+str(s.stats[INT])+" (+"+str(s.bonus(INT))+")")
		print("wisdom "+str(s.stats[WIS])+" (+"+str(s.bonus(WIS))+")")
		print("charisma "+str(s.stats[CHA])+" (+"+str(s.bonus(CHA))+")")
		print("hp "+str(s.hp())+", damage reduction "+str(s.damagereduction()))
		print("ac "+str(s.ac()))
		print("attack +"+str(s.attackbonus()) + ", damage 1d6+"+str(s.damage()))
		print("fort "+str(s.save(FORT))+" ref "+str(s.save(REF))+" will "+str(s.save(WILL)))
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
		if (clas == MONK or clas == SAGE or clas == ROGU) and choiceone not in [FORT, REF, WILL]:
			raise Exception("bad arguments")
		if clas == ROGU and (choiceone == REF or choicetwo not in [SKILROGU, BABROGU]): 
			raise Exception("bad arguments")
		if clas == SAGE and (choiceone not in [INT,WIS,CHA] or choicetwo not in [STR,CON,DEX]): 
			raise Exception("bad arguments")
		
		s.clas = clas
		if clas == ROGU: s.skillorbab = choicetwo
		
		if clas == BARB or clas == PALA or clas == RANG: s.classhp = 10
		else: s.classhp = 8
		
		if clas == SAGE or clas == SHAM or clas == TACT: s.goodbab = False
		elif clas == ROGU and choicetwo == SKILROGU: s.goodbab = False
		else: s.goodbab = True
		
		if clas == RANG: s.badsave = WILL
		elif clas == TACT: s.badsave = FORT
		elif clas == MONK or clas == ROGU or clas == SAGE: s.badsave = choiceone
		else: s.badsave = REF
		
		if clas == MONK or clas == SHAM: s.kom = WIS
		elif clas == RANG: s.kom = DEX
		elif clas == TACT: s.kom = INT
		elif clas == SAGE: s.kom = choiceone
		elif clas == PALA: s.kom = STR
		else: s.kom = None # Rogue and Barbarian's kom are set later
		
		if clas == PALA or clas == SHAM: s.kdm = CHA
		elif clas == RANG: s.kdm = INT
		elif clas == SAGE: s.kdm = choicetwo
		elif clas == BARB or clas == MONK or clas == TACT: s.kdm = CON
		else: s.kdm = None # Rogue's kdm is set later
		
	def setrace(s,race, choiceone=None):
		if race == ELF and choiceone not in [INT,WIS,CHA]:
			raise Exception("bad arguments")
		if race == HUM and choiceone not in [STR,CON,DEX,INT,WIS,CHA]:
			raise Exception("bad arguments")
		
		s.race = race
		
		if race == DWA: s.stats[CON] += 2; s.stats[INT] += 2; s.stats[CHA] -= 2
		elif race == ELF: s.stats[DEX] += 2; s.stats[choiceone] += 2; s.stats[CON] -= 2
		elif race == GNO: s.stats[CON] += 2; s.stats[CHA] += 2; s.stats[STR] -= 2
		elif race == HAL: s.stats[DEX] += 2
		elif race == HUM: s.stats[choiceone] += 2
		elif race == ORC: s.stats[STR] += 2; s.stats[CON] += 2; s.stats[CHA] -= 2
		
		#	dwa + con int - cha
		#	elf + dex mental - con
		#gno + con cha - str / small
		#hal + dex / small / +1 will / move 30
		#hum + any / +1 att, ac, or save
		#	orc + str con - cha
		
		# also racial skill bonuses
		
	def setskills(s,skills):
		skills = set(skills)
		if (s.clas == BARB or s.clas == PALA) and len(skills) != 5:
			raise Exception("bad arguments")
		if (s.clas == MONK or s.clas == RANG or s.clas == SAGE or s.clas == SHAM) and len(skills) != 6:
			raise Exception("bad arguments")
		if s.clas == TACT and len(skills) != 9 and not set([ARCA,ENGI,GEOG,HIST,MEDI,NATU]).issubset(skills):
			raise Exception("bad arguments")
		if s.clas == ROGU and skillorbab == SKILROGU and len(skills) != 8:
			raise Exception("bad arguments")
		if s.clas == ROGU and skillorbab == BABROGU and len(skills) != 6:
			raise Exception("bad arguments")
			
		s.trained = skills

c = character()
c.setlevel(1)
c.stats = [16,14,14,12,10,10]
c.setrace(HUM, STR)
c.setclass(SHAM)
c.setskills([ATHL,PERC,INTI,ACRO,LARC,ARCA])
c.show()

class Tests(unittest.TestCase):

	def setUp(s):
		global c 
		c = character()
		c.setlevel(1)
		c.stats = [16,14,14,12,10,10]

	def testmonk(s):
		c.setclass(MONK,FORT)
		s.assertEqual(c.hp(), (8+2)*2); s.assertEqual(c.damagereduction(), int(2/2))
		s.assertEqual(c.ac(), 10+2+1)
		s.assertEqual(c.save(FORT), 0+3); s.assertEqual(c.save(REF), 2+2); s.assertEqual(c.save(WILL), 2+0)
		s.assertEqual(c.damage(), 0+int(3/2))
		
	def testpaladin(s):
		c.setclass(PALA)
		c.setrace(ORC)
		c.setskills([ATHL,PERC,INTI,ACRO,LARC])
		s.assertEqual(c.hp(), (10-1)*2); s.assertEqual(c.damagereduction(), int(2/2))
		s.assertEqual(c.ac(), 10-1+1)
		s.assertEqual(c.save(FORT), 2+4); s.assertEqual(c.save(REF), 0+2); s.assertEqual(c.save(WILL), 2+0)
		s.assertEqual(c.damage(), 4+int(4/2))
		s.assertEqual(c.getskill(ATHL), 4+1+1)

if __name__ == '__main__':
	unittest.main()
