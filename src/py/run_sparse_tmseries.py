'''
Estimate surface turbulent fluxes using the SPARSE model (Boulet et al., 2015) : https://doi.org/10.5194/hess-19-4653-2015
    .requires meteo, radiation, biophysical, and other ancillary input data to run

-- ufu -- py from 170823
'''

import pySPARSE as pySP
import numpy as np
import matplotlib.pyplot as plt 

### test - see https://runningfingers.com/seb.php

'''
import csv
with open('sparse_data/meteoBS.csv') as csv_file:
    incsv_read  = csv.reader(csv_file, delimiter=',')
    meteoNrad   = [row for row in incsv_read]
'''

'''
Tsurf           = 297.24
vza             = 0
rg              = 630
Ta              = 293.15
rh              = 50
ua              = 2
za              = 3
lai             = 1.5; glai = 1.5
zf              = 1
rstmin          = 100
albv            = 0.18
emisv           = 0.98; emiss = 0.96; emissf = 0.97
albe            = 0.3
xg              = 0.315
sigmoy          = 0.5
albmode         = 'UnCapped'
'''

import pandas as pd
meteoNrad       = pd.read_csv('sparse_data/meteoBS_hdr_enuse.csv')                  # meteoNrad.head()
#biophysical     = pd.read_csv('sparse_data/meteoBS_hdr.csv')


Tsurf           = np.array(meteoNrad['tsobs']) + 273.15                             # tsobs loaded in [C]
vza             = 0                                                                 # np.array(meteoNrad['vza'])
rg              = np.array(meteoNrad['rg'])
Ta              = np.array(meteoNrad['ta']) + 273.15                                # ta loaded in [C]
rh              = np.array(meteoNrad['rh'])
ua              = np.array(meteoNrad['ua'])
#za              = 2.32
za              = np.array(meteoNrad['za'])
lai             = np.array(meteoNrad['lai']); glai = np.array(meteoNrad['glai'])    # temporally varying surface leaf areas                                               # np.array(biophysical['lai'])
zf              = np.array(meteoNrad['zf'])                                         # temporally varying vegetation height
rstmin          = np.array(meteoNrad['rstmin'])
albv            = np.array(meteoNrad['albv'])
emisv           = 0.98; emiss = 0.96; emissf = 0.97
albe            = np.array(meteoNrad['albedo'])                                     # np.array(meteoNrad['albe'])
xg              = np.array(meteoNrad['xG'])
sigmoy          = 0.5
albmode         = 'UnCapped'
doy             = np.array(meteoNrad['doy'])

xx              = {'le':[]}; xx['h'] = []; xx['rn'] = []; xx['g'] = []; xx['lev'] = []; xx['les'] = []; xx['hv'] = []; xx['hs'] = []; xx['tv'] = []; xx['ts'] = []; xx['tsf'] = []; xx['doy'] = []
#le              = []; h = []; rn =[]; g = []; lev = []; les = []; hv = []; hs = []; tv = []; ts = []; tsf = []

for i in range(len(Tsurf)):
    [LE,H,Rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf] = pySP.pySPARSE(Tsurf[i],vza,rg[i],Ta[i],rh[i],ua[i],za[i],lai[i],glai[i],zf[i],rstmin[i],albv[i],emisv,emiss,emissf,albe[i],xg[i],sigmoy,albmode) ###= _fxn_.pySPARSE(Tsurf[i],vza[i],rg[i],Ta[i],rh[i],ua[i],za,lai[i],glai[i],zf[i],rstmin,albv,emisv,emiss,emissf,albe[i],xg,sigmoy,albmode)

    '''
    le[len(le):] = [LE]; h[len(h):] = [H]; rn[len(rn):] =[Rn]; g[len(g):] = [G];
    lev[len(lev):] = [LEv]; les[len(les):] = [LEs]; hv[len(hv):] = [Hv]; hs[len(hs):] = [Hs];
    tv[len(tv):] = [Tv]; ts[len(ts):] = [Ts]; tsf[len(tsf):] = [Tsf]
    '''
    
    xx['le'][len(xx['le']):]            = [LE]; xx['h'][len(xx['h']):] = [H]; xx['rn'][len(xx['rn']):] = [Rn]; xx['g'][len(xx['g']):] = [G];
    xx['lev'][len(xx['lev']):]          = [LEv]; xx['les'][len(xx['les']):] = [LEs]; xx['hv'][len(xx['hv']):] = [Hv]; xx['hs'][len(xx['hs']):] = [Hs];
    xx['tv'][len(xx['tv']):]            = [Tv]; xx['ts'][len(xx['ts']):] = [Ts]; xx['tsf'][len(xx['tsf']):] = [Tsf]; xx['doy'][len(xx['doy']):] = [doy[i]]

output          = xx

### plot #
plt.plot(xx['doy'], xx['le'], 'blue');plt.ylabel('$\lambda$E [W.m$^{-2}$]')
plt.show()

plt.plot(np.array(meteoNrad['rnobs']),xx['rn'],'b.',[-200,800],[-200,800],'k-');plt.title('Est. vs Obs. Rn [W.m$^{-2}$]')
plt.show()
#--uΓu--
