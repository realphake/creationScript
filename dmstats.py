import creator
import random

c = creator.character()
c.setlevel(10)
c.stats = [sum(sorted([random.randint(1,6) for _ in range(5)])[-3:]) for _ in range(6)]
c.setclass(creator.VAMP)
c.setrace(creator.VAMP,creator.DEX)
c.setskills([creator.ATHL,creator.PERC,creator.INTI,creator.ACRO,creator.LARC])
c.settracks([creator.UndeadVampire,creator.EsotericaRadica,creator.OffensiveAssassin,creator.DefensiveNinjas])
c.show()