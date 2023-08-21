'''
Test the various algorithms in misctools.py

-- ufu -- py from 170823
'''

from misctools import polarorbiter_angles, solar_pos, leafprj

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

[sza_deg,saa_deg,sunrise,sunset] = solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)



### test - leaf projection function
anglerads       = [1,1]
G               = leafprj('specific',anglerads)

#--uΓu--
