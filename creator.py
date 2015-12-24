
STR=0;CON=1;DEX=2;INT=3;WIS=4;CHA=5
FORT=0;REF=1;WILL=2
BARB=0;MONK=1;PALA=2;RANG=3;ROGU=4;SAGE=5;SHAM=6;TACT=7
SKILROGU=0;BABROGU=1

def statBonus(stat):
	return int((stat-10)/2)

class character:
	classhp = 8
	goodbab = False
	stats = [10,10,10,10,10,10]
	kom = STR
	kdm = CON
	level = 1
	badsave = WILL
	
	def bab(s):
		if s.goodbab: return s.level
		else: return int(s.level*0.75)
	def hp(s):
		return (s.classhp+statBonus(s.stats[s.kdm])) * (s.level+1)
	def ac(s):
		return 10 + s.bab() + statBonus(s.stats[s.kdm])
	def damagereduction(s):
		return int(statBonus(s.stats[CON])/2)
	def save(s, frw):
		save = statBonus(max(s.stats[2*frw],s.stats[2*frw+1]))
		if s.badsave == frw: return save + int(s.level/2)
		else: return save + int(s.level*(2/3)+2)
	def damage(s):
		return statBonus(s.stats[s.kom]) + int(statBonus(s.stats[STR])/2)
	
	def show(s):
		print("hp "+str(c.hp())+", damage reduction "+str(c.damagereduction()))
		print("ac "+str(c.ac()))
		print("damage 1d6+"+str(c.damage()))
		print("fort "+str(c.save(FORT))+" ref "+str(c.save(REF))+" will "+str(c.save(WILL)))

	def setclass(s,clas,savechoice=-1,roguechoice=-1): 
		if (clas == MONK or clas == SAGE or clas == ROGU) and savechoice not in [FORT, REF, WILL]:
			raise Exception("bad arguments")
		if clas == ROGU and (savechoice == REF or roguechoice not in [SKILROGU, BABROGU]): 
			raise Exception("bad arguments")
		
		if clas == BARB or clas == PALA or clas == RANG: s.classhp = 10
		else: s.classhp = 8
		
		if clas == SAGE or clas == SHAM or clas == TACT: s.goodbab = False
		elif clas == ROGU and roguechoice == SKILROGU: s.goodbab = False
		else: s.goodbab = True
		
		if clas == RANG: s.badsave = WILL
		elif clas == TACT: s.badsave = FORT
		elif clas == MONK or clas == ROGU or clas == SAGE: s.badsave = savechoice
		else: s.badsave = REF
	
c = character()
c.stats = [16,14,14,10,12,10]
c.setclass(BARB)
c.show()

c.setclass(ROGU,WILL,BABROGU)
c.show()

