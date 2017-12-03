import numpy as np
from glob import glob
from scipy import stats as st
from matplotlib import pyplot as plt
from sys import argv
#from PyFuncemeClimateTools.ClimateStats import compute_rpss

np.set_printoptions(precision=3)

seas = argv[1]
sett = { 'fmam' : [1, 5] , 'fma' : [1,4] , 'mam' : [2,5]}

beg=sett[seas][0]
edn=sett[seas][1]

pathmod = '/home/junior/ownCloud/data/echam_flow_season_forecast_models_pet-ok_new/'

basins = ['armando_ribeiro','banabuiu', 'castanhao', 'coremas_maedagua',  'oros']

basins = sorted(basins)
t=1
ff = sorted(glob('obs/flow*1981*20170531.asc'))


#rpss_prev = np.full((30),np.nan)
#rpss_clim = np.full((30),np.nan)

prob_bas_prev = np.full((5,7,3), np.nan)
prob_bas_obs  = np.full((5,7,3), np.nan)
prob_bas_clim = np.full((5,7,3), np.nan)

prob_acu_prev = np.full((35,3), np.nan)
prob_acu_obs  = np.full((35,3), np.nan)
prob_acu_clim = np.full((35,3), np.nan)
d = 0 
rps_fcst = []
rps_f = []
rps_clim = []
rps_c = []

for ii,f in enumerate(ff):
    #model
    fgen = glob(pathmod+'jan_{1}_2011-2017/{0}/qvaz*{0}*_ECHAM4.6*7.txt'.format(basins[ii],seas))
#    print 'begin'
#   print fgen

    vaz_mod = np.loadtxt(fgen[0], skiprows=1, usecols=range(2,22))
    #vaz_mod = vaz_mod[0:-1,:]
    #vazfma_mod = vaz_mod
    #obs
    vaz_obs = np.loadtxt(f)
    print
    

    vaz_obs = np.reshape(vaz_obs, [37,12])
    vaz8110_obs = vaz_obs[0:30, :]
    fma8110_obs = np.mean(vaz8110_obs[:, beg:edn], axis=1) # climatology period 1981-2010
    vazfma_obs  = np.mean(vaz_obs[30:,beg:edn], axis=1)    # forecast period 2011-2016

    mean = np.mean(fma8110_obs)
    std = np.std(fma8110_obs)

    y_obs = st.norm(loc=mean, scale=std)

    p33 = y_obs.ppf(q=1./3.)
    p66 = y_obs.ppf(q=2./3.)

    for y in range(7):
        #print 'ano =', y+1
        a = float(np.sum(vaz_mod[y,:] < p33)) / 20
        b = float(np.sum(vaz_mod[y,:] < p66)) / 20
        c = 1.
        prob_acu_prev[d, :] = np.array([a, b, c])
        prob_bas_prev[ii,y,:] = np.array([a, b, c])
        
        #print prob_acu_prev

        a = int(vazfma_obs[y] < p33)
        b = int(vazfma_obs[y] < p66)
        c = 1.
         
        prob_acu_obs[d, :] = np.array([a, b, c])
        prob_acu_clim[d, :] = np.array([1./3., 2./3., 1.])
        d += 1

        prob_bas_obs[ii, y, :] = np.array([a, b, c])
        prob_bas_clim[ii, y, :] = np.array([1./3., 2./3., 1.])


        rps_f.append((np.sum((prob_bas_prev[ii,y,...] - prob_bas_obs[ii,y,...])**2,
        axis=0))/2)
    
        rps_c.append((np.sum((prob_bas_clim[ii,y,...] - prob_bas_obs[ii,y,...])**2,
        axis=0))/2)
    
#    print rps_f
#    print rps_c
    
    print 'RPSS :', basins[ii]
    print 1 - np.mean(rps_f,axis=0) / np.mean(rps_c,axis=0)
    rps_f = []
    rps_c = []


rps_fcst.append((np.sum((prob_acu_prev[...] - prob_acu_obs[...])**2,
    axis=0))/2) # dividing by 2

    # categories and dividing by 6 years of analysing

rps_clim.append((np.sum((prob_acu_clim[...] - prob_acu_obs[...])**2,
    axis=0))/2)

    #t += 1
print '-----------------------------------------------------------------'
print 
print 'RPSS all basins'
print 1 - np.mean(rps_fcst[:]) / np.mean(rps_clim[:])

#print 1 - np.mean(rps_fcst[:]) / np.mean(rps_clim[:])

#print rps_fcst

#flattened_list = [y for x in rps_fcst for y in x]

#print np.mean(flattened_list)
exit()
RPSS = 1 - np.mean(rps_fcst) / np.mean(rps_clim)
