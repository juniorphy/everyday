import numpy as np
from PyFuncemeClimateTools import Thiessen
from hidropy.utils.write_thiessen import write_thiessen

fin = '/home/junior/Documents/data/pet_daily_inmet/pet_daily_inmet_19610101_20161231.asc'

shape = '/home/junior/Documents/programs/shapes_funceme/bacia_hidro/bacia_hidro-31-litoral-CE.asc'

mmm = np.loadtxt(fin)

raw = mmm[:, 3:]

lat = mmm[:,2]
lon = mmm[:,1]

thi = Thiessen.thiessen(raw,lat,lon,shape,pf=3, num_proc=8)

#thi = np.squeeze(thi)

write_thiessen(thi, '19610101', '20161231', 'daily', 'pet', 'inmet', 'obs','litoral', '')

