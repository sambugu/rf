'''
Estimate surface turbulent fluxes using the SPARSE model (Boulet et al., 2015) : https://doi.org/10.5194/hess-19-4653-2015
    .requires meteo, radiation, biophysical, and other ancillary input data to run

-- ufu -- py from 170823
'''

import pySPARSE as pySP

### test - see https://runningfingers.com/seb.php

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
rtrmode         = 'Retrieval'
betav           = 0.99;betas=0.99

[LE,H,rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf] = pySP.pySPARSE(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode,betav,betas,rtrmode)

#--uΓu--
