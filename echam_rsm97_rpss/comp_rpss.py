import numpy as np
from glob import glob
from scipy import stats as st
from matplotlib import pyplot as plt
#from PyFuncemeClimateTools.ClimateStats import compute_rpss

np.set_printoptions(precision=3)

pathmod = '/home/junior/ownCloud/data/flow_season_forecast_models_pet-ok_new/'

basins = ['armando_ribeiro','banabuiu', 'castanhao', 'coremas_maedagua',  'oros']

basins = sorted(basins)
t=1
ff = sorted(glob('obs/*.asc'))


rpss_prev = np.full((6,5),np.nan)
rpss_clim = np.full((6,5),np.nan)


prob_acu_prev = np.full((6,6,3), np.nan)
prob_acu_obs  = np.full((6,6,3), np.nan)
prob_acu_clim = np.full((6,6,3), np.nan)

rps_fcst = []

rps_clim = []

for ii,f in enumerate(ff):
    #model
    fgen = glob(pathmod+'jan_fma_2011-2017/{0}/qvaz*{0}*_ECHAM4.6*7_corr-flow.txt'.format(basins[ii]))
    vaz_mod = np.loadtxt(fgen[0], skiprows=1, usecols=range(2,22))
    vaz_mod = vaz_mod[0:-1,:]
    vazfma_mod = np.mean(vaz_mod[1:4,:], axis=0)
    #obs
    vaz_obs = np.loadtxt(f)
    print
    print
    print basins[ii]

    vaz_obs = np.reshape(vaz_obs, [40,12])
    vaz8110_obs = vaz_obs[4:34, :]
    fma8110_obs = np.mean(vaz8110_obs[:, 1:4], axis=1) # climatology period 1981-2010
    vazfma_obs  = np.mean(vaz_obs[34:,1:4], axis=1)    # forecast period 2011-2016

    mean = np.mean(fma8110_obs)
    std = np.std(fma8110_obs)

    y_obs = st.norm(loc=mean, scale=std)

    p33 = y_obs.ppf(q=1./3.)
    p66 = y_obs.ppf(q=2./3.)

    for y in range(6):
        a = float(np.sum(vaz_mod[y,:] < p33)) / 20
        b = float(np.sum(vaz_mod[y,:] < p66)) / 20
        c = 1.
        prob_acu_prev[ii, y, :] = np.array([a, b, c])
        #print prob_acu_prev

        a = int(vazfma_obs[y] < p33)
        b = int(vazfma_obs[y] < p66)
        c = 1.

        prob_acu_obs[ii, y, :] = np.array([a, b, c])
        prob_acu_clim[ii, y, :] = np.array([1./3., 2./3., 1.])

    rps_fcst.append((np.sum((prob_acu_prev[ii, ...] - prob_acu_obs[ii, ...])**2, axis=1))/2) # dividing by 2

    # categories and dividing by 6 years of analysing

    rps_clim.append((np.sum((prob_acu_clim[ii, ...] - prob_acu_obs[ii, ...])**2, axis=1))/2)

    t += 1
    print t

    print 1 - np.mean(rps_fcst[:]) / np.mean(rps_clim[:])

rps_fcst

#flattened_list = [y for x in rps_fcst for y in x]

#print np.mean(flattened_list)

exit()

print np.mean(rps_fcst), np.mean(rps_clim)

RPSS = 1 - np.mean(rps_fcst) / np.mean(rps_clim)


    #fma8110 = vaz811


#vaz_mod = np.loadtxt('FMA/basin/')
