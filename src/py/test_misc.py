'''
Test the various algorithms in misctools.py

-- ufu -- py from 170823
'''

from misctools import polarorbiter_angles, solar_pos, BoaTocRg, leafprj, brightnessT_814N105125

###________________________________________________________________________________________________________________
### test - polar orbiter view angles
sat_alt             = 761
orb_incl            = 81.3        
lon_nad             = 4
lat_px              = 40
lon_px              = 7

[vza_deg,vaa_deg]   = polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px)
    


###________________________________________________________________________________________________________________
### test - solar algorithm
doy             = 228
time            = 13
tz_bool         = 'Yes'
tm_zn           = 3
lat_px          = 0
lon_px          = 37.1

[sza_deg,saa_deg,sunrise,sunset,da] = solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)



###________________________________________________________________________________________________________________
### test - top of canopy/bottom of atmosphere incoming S-W radiance
doy             = 228
time            = 13
tz_bool         = 'Yes'
tm_zn           = 3
lat_px          = 0
lon_px          = 37.1

tauDat          = ['constant',0.76]

Rg              = BoaTocRg(tauDat,doy,time,tz_bool,tm_zn,lat_px,lon_px)



###________________________________________________________________________________________________________________
### test - leaf projection function
anglerads       = [1,1]                         # zenith angle [view/sun], and leaf inclination [zenith] in radians
incl            = 'specific'                    # 'spherical' . 'vertical' . 'horizontal' . 'specific'
G               = leafprj(incl,anglerads)



###________________________________________________________________________________________________________________
### test - sky irradiance scaling to spectral sensing range of TIR sensor 
dat             = {'TIRband':'TIR814'}          # 'TIR814' or 'TIR105125'
dat['rh']       = 50
dat['airT']     = 295                           # [K]
dat['tsobs']    = 305 - 273.15                  # [C]
TBdat           = brightnessT_814N105125(dat)   # finally, sigma.TB^4 ≈ emisf.sigma.Tsf^4 + (1-emisf).TBdat['ratm']/TBdat['f']



###________________________________________________________________________________________________________________
### test lorenz butterfly model
import numpy as np
import matplotlib.pyplot as plt                 ### needed - if missing, please install _>> python -m pip install -U matplotlib
from misctools import lorenz

# error variances  
sig0            = 0.5  # initial forecast error variance

# Lorenz model parameters
sigma           = 10
rho             = 28
beta            = 8/3
dt              = 0.01

'''
# initial true state
xt0 = zeros(3,1);
xt0(1) =  1.508870;
xt0(2) = -1.531271;
xt0(3) = 25.46091;
'''

xt0             = np.zeros(shape = [3,1],dtype = np.float64)
xt0[0]          = 5*np.random.randn(1)
xt0[1]          = 5*np.random.randn(1)
xt0[2]          = 5*np.random.randn(1)

#x_rand = sig0*np.random.randn(3,1)
xf0             = xt0 + sig0*np.random.randn(3,1)
Xinit           = xf0; xin=Xinit                ## xin = np.swapaxes([xf0[:,0]],0,1)

tm_stp          = 10000;
Xout            = np.zeros(shape = [3,tm_stp],dtype = np.float64)


for i in range(tm_stp):

    xout        = lorenz(xin,sigma,rho,beta,dt)
    Xout[:,i]   = np.squeeze(xout)
    xin         = xout


### plot
fig             = plt.figure()
ax              = plt.axes(projection="3d")
ax.plot3D(Xout[0,:], Xout[1,:], Xout[2,:], 'gray')
plt.show()



###________________________________________________________________________________________________________________
### xxx



#--uΓu--
