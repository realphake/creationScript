import creator

c = creator.character()
c.setlevel(10)
c.stats = [14,10,16,10,14,12]
c.setclass(creator.VAMP)
c.setrace(creator.VAMP,creator.DEX)
c.setskills([creator.ATHL,creator.PERC,creator.INTI,creator.ACRO,creator.LARC])
c.settracks([creator.UndeadVampire,creator.EsotericaRadica,creator.OffensiveAssassin,creator.DefensiveNinjas])
c.show()
