'''
Test the various algorithms in misctools.py

-- ufu -- py from 170823
'''

from misctools import polarorbiter_angles, solar_pos, BoaTocRg, leafprj, brightnessT_814N105125

### test - polar orbiter view angles
sat_alt             = 761
orb_incl            = 81.3        
lon_nad             = 4
lat_px              = 40
lon_px              = 7

[vza_deg,vaa_deg]   = polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px)
    


### test - solar algorithm
doy             = 228
time            = 13
tz_bool         = 'Yes'
tm_zn           = 3
lat_px          = 0
lon_px          = 37.1

[sza_deg,saa_deg,sunrise,sunset,da] = solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)



### test - top of canopy/bottom of atmosphere incoming S-W radiance
doy             = 228
time            = 13
tz_bool         = 'Yes'
tm_zn           = 3
lat_px          = 0
lon_px          = 37.1

tauDat          = ['constant',0.76]

Rg              = BoaTocRg(tauDat,doy,time,tz_bool,tm_zn,lat_px,lon_px)



### test - leaf projection function
anglerads       = [1,1]                         # zenith angle [view/sun], and leaf inclination [zenith] in radians
incl            = 'specific'                    # 'spherical' . 'vertical' . 'horizontal' . 'specific'
G               = leafprj(incl,anglerads)



### test - sky irradiance scaling to spectral sensing range of TIR sensor 
dat             = {'TIRband':'TIR814'}          # 'TIR814' or 'TIR105125'
dat['rh']       = 50
dat['airT']     = 295                           # [K]
dat['tsobs']    = 305 - 273.15                  # [C]
TBdat           = brightnessT_814N105125(dat)



#--uΓu--
