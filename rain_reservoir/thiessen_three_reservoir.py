import os
import numpy as np
import argparse
from netCDF4 import Dataset
import datetime
from PyFuncemeClimateTools import Thiessen                                          
import xarray as xr
import pandas as pd

from hidropy.utils.write_thiessen import write_thiessen
from matplotlib import pyplot as plt

# open netcdf
input_data = Dataset('/dados/sao_francisco_drought/data/pr_monthly_inmet_ana_obs_19610101_20161231_thiessen_sao_francisco_high.nc')

#init_date = 19610101

time = input_data.variables['time']
variable = input_data.variables['pr'][:]

#date_index = date2index(time)
variable = input_data.variables['pr'][:]

dtime = pd.date_range('1961/01/01', periods=time.size, freq='MS')

# novo xarray para a var sst com o eixo do tempo correto.
pcp = xr.DataArray(variable, coords=[dtime],
               dims=['time'])

plt.figure(figsize=(15, 8))

clim = pcp.sel(time=slice('1981-01-01', '2010-12-01')).groupby('time.month').mean('time')

dates = [datetime.date(1900, f, 1).strftime('%b') for f in range(1,13) ]

plt.plot(range(1,13),clim.values,'-o',color='black',label="obs")

#plt.legend(fontsize=14, loc='best')
plt.xticks(range(1,13),dates,rotation=45)
plt.title('Monthly Precipitation High Sao Francisco - Annual Cycle',fontsize=20)
plt.grid()
plt.xlim(0,13)
plt.ylim([0,400])
plt.xlabel("months",fontsize=16)
plt.ylabel("mm",fontsize=20)
plt.tick_params(labelsize=12)
plt.savefig('rainfall_high_Sao_Francisco.png',bbox_inches='tight', dpi=130)

#plt.show()

#cal_year = np.

#cal_mon = 

#cal_day = 


#plt.plot(variable)




