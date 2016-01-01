
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
		if race == HAL and frw == WILL: save += 1;
		if s.badsave == frw: return save + int(s.level/2)
		else: return save + int(s.level*(2/3)+2)
		
	def attackbonus(s):
		return s.bab() + s.bonus(s.kom)
	
	def damage(s):
		return s.bonus(s.kom) + int(s.bonus(STR)/2)
	
	def getSkill(s,skill):
		total = 0
		if skill in [ACRO,LARC,STEA,RIDE]: total += s.bonus(DEX)
		elif skill == VIGO: total += s.bonus(CON)
		elif skill == ATHL: total += s.bonus(STR)
		elif skill in [ARCA,ENGI,GEOG,HIST,MEDI,NATU]: total += s.bonus(INT)
		elif skill in [BLUF,DIPL,INTI]: total += s.bonus(CHA)
		elif skill == PERC: total += s.bonus(WIS)
		if skill in s.trained: total += s.level
		if s.race == DWA and skill == ENGI: int(math.ceil(s.level/8.0))
		elif s.race == ELF and skill == NATU: int(math.ceil(s.level/8.0))
		elif s.race == GNO and skill == DIPL: int(math.ceil(s.level/8.0))
		elif s.race == ORC and skill == ATHL: int(math.ceil(s.level/8.0))
		# TODO human's skill bonus
		
	def show(s):
		print("hp "+str(c.hp())+", damage reduction "+str(c.damagereduction()))
		print("ac "+str(c.ac()))
		print("damage 1d6+"+str(c.damage()))
		print("fort "+str(c.save(FORT))+" ref "+str(c.save(REF))+" will "+str(c.save(WILL)))
	
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
		else: s.kom = None
		
		if clas == PALA or clas == SHAM: s.kdm = CHA
		elif clas == RANG: s.kdm = INT
		elif clas == SAGE: s.kdm = choicetwo
		elif clas == BARB or clas == MONK or clas == TACT: s.kdm = CON
		else: s.kdm = None
		
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
		
	def setSkills(skills):
		skills = set(skills)
		if (clas == BARB or clas == PALA) and len(skills) != 5:
			raise Exception("bad arguments")
		if (clas == MONK or clas == RANG or clas == SAGE or clas == SHAM) and len(skills) != 6:
			raise Exception("bad arguments")
		if clas == TACT and len(skills) != 9 and not set([ARCA,ENGI,GEOG,HIST,MEDI,NATU]).issubset(skills):
			raise Exception("bad arguments")
		if clas == ROGU and skillorbab == SKILROGU and len(skills) != 8:
			raise Exception("bad arguments")
		if clas == ROGU and skillorbab == BABROGU and len(skills) != 6:
			raise Exception("bad arguments")
			
		s.trained = skills

c = character()
c.stats = [16,14,14,12,10,10]
c.setrace(HUM, STR)
c.setclass(BARB)

class Tests(unittest.TestCase):

	def setUp(s):
		global c 
		c = character()
		c.stats = [16,14,14,12,10,10]

	def testmonk(s):
		c.setclass(MONK,FORT)
		s.assertEqual(c.hp(), (8+2)*2); s.assertEqual(c.damagereduction(), int(2/2))
		s.assertEqual(c.ac(), 10+2+1)
		s.assertEqual(c.save(FORT), 0+3); s.assertEqual(c.save(REF), 2+2); s.assertEqual(c.save(WILL), 2+0)
		s.assertEqual(c.damage(), 0+int(3/2))
		
	def testpaladin(s):
		c.setclass(PALA)
		s.assertEqual(c.hp(), (10+0)*2); s.assertEqual(c.damagereduction(), int(2/2))
		s.assertEqual(c.ac(), 10+0+1)
		s.assertEqual(c.save(FORT), 2+3); s.assertEqual(c.save(REF), 0+2); s.assertEqual(c.save(WILL), 2+0)
		s.assertEqual(c.damage(), 3+int(3/2))

if __name__ == '__main__':
	unittest.main()
