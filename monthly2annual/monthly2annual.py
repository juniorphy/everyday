# -*- coding: utf-8 -*-

__author__ = ["Fco Vasconcelos Junior"]
__credits__ = ["José Marcelo, Jarbas Camurca"]
__license__ = "GPL"
__version__ = "1.0"
__email__ = "juniorphy@gmail.com"


import numpy as np
import datetime
from PyFuncemeClimateTools import Thiessen                                          
import xarray as xr
import pandas as pd

pcpday = np.loadtxt('/home/junior/Documents/programs/getthiessendb/pr_thiessen_daily_19730101_20171130_CE/pr_daily_funceme_thiessen_19730101_20171130_ce_23.asc')

cal_year = pcpday[:,0]
cal_mon = pcpday[:,1]
cal_day = pcpday[:,2]
pcpday = pcpday[:,3]

# creating datetime axis
dtime = pd.date_range('1973/01/01', periods=cal_day.shape[0], freq='DS')

# novo xarray para a var sst com o eixo do tempo correto.
pcp = xr.DataArray(pcpday, coords=dtime, \
            dims=['time'])





pcpmon = 
