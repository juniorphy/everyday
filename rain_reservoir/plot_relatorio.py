# -*- coding: utf-8 -*-

from glob import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import shiftgrid, Basemap
import numpy as np

files = glob('/home/musf/liana/relatorio_201711/ANA/*.asc')
fig = plt.figure(figsize=(10,10))
ax  = fig.add_subplot(111)

m = Basemap(projection='cyl',llcrnrlat=-18,urcrnrlat=-1,\
	    llcrnrlon=-48,urcrnrlon=-34,resolution='h',area_thresh = 1000.)

m.fillcontinents(color='0.9',lake_color='none',zorder=0)
m.drawparallels(np.arange(-90.,91.,5.),labels=[1,0,0,1],fontsize=10,linewidth=0.1,zorder=10, fontweight='bold')
m.drawmeridians(np.arange(0.,360.,5.),labels=[1,0,0,1],fontsize=10,linewidth=0.1,zorder=10, fontweight='bold')
m.drawstates(color='k', linewidth=1)
m.drawcoastlines(linewidth=0.5)

for file in files:
	co_line = np.loadtxt(file,delimiter=',')
	co_lon  = co_line[:,0]
	co_lat  = co_line[:,1]
	xm,ym   = m(co_lon,co_lat)
	xym     = zip(xm,ym)
	# path_co = Polygon(xym, facecolor='b', lw=0.5)
	path_co = Polygon(xym, facecolor='#ADD8E6', lw=0.5)
	ax.add_patch(path_co)

plt.title(u'Sistemas hídricos do Nordeste - Projeto PISF', fontsize=19, fontweight='bold')
plt.show(path_co)
plt.savefig('/home/musf/liana/relatorio_201711/sistemas_hidricos_PISF.png')
