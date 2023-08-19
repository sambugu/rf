'''
solar angles algorithm - Iqbal (1983) ; Spencer (1971) ; Campbell and Norman (1998)
	Calculation of solar angles (zenith and azimuth) given a pixel's/point's ground coordinates and the local UTC time 
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- py from 170823
'''

import math

def solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px):
    # constants --- from Fourier series analysis by Spencer (1971) - https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
    A0 			= 229.18
    # a1          	= 0.000075;     a2  = 0.001868;     a3 	= -0.032077;
    a1          	= 0.0000075;    a2  = 0.001868;     a3 	= -0.032077                                                                        # see correction for var a1 in https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
    a4          	= -0.014615;    a5  = -0.040849;    a6 	= 0.006918
    a7          	= -0.399912;    a8  = 0.070257;     a9 	= -0.006758
    a10         	= 0.000907;     a11 = -0.002697;    a12 = 0.00148
    b0          	= 90.833

    denom               = 365                                                                                                                       # should consider leap years according to the Gregorian calendar for exactness (i.e., leapyr IF ((mod(yr/4)==0 EXCEPT mod(yr/100)==0) || mod(yr/400)==0) --- left AS IS here
    

    # variables
    da          	= 2*math.pi*(doy - 1 + (math.floor(time) - 12)/24)/denom                                                                    # Fractional year / day angle

    if tz_bool=='Yes':
        std_lon 	= tm_zn*15
    else:
        std_lon 	= math.round(lon_px/15)*15

    lon_corr 		= 4*(std_lon - lon_px)
    lat_px              = lat_px*math.pi/180
    eq_time 		= A0*(a1 + a2*math.cos(da) + a3*math.sin(da)+a4*math.cos(2*da) + a5*math.sin(2*da))                                         # Equation of time (minutes)
    declin      	= a6 + a7*math.cos(da) + a8*math.sin(da) + a9*math.cos(2*da) + a10*math.sin(2*da) + a11*math.cos(3*da) + a12*math.sin(3*da) # Solar declination - in radians
    solar_time  	= time + eq_time/60 - lon_corr/60 											    # Solar time (hours)
    ha          	= 15*(solar_time-12) 													    # Hour angle (degrees)

    # solar zenith angle in radians and degrees
    sza_rads            = math.acos(math.sin(lat_px)*math.sin(declin) + math.cos(declin)*math.cos(lat_px)*math.cos(ha*math.pi/180))				
    sza_deg 		= sza_rads*180/math.pi
    sol_alt 		= 90 - sza_deg

    saa_rads		= math.acos((math.sin(sol_alt*math.pi/180)*math.sin(lat_px) - math.sin(declin))/(math.cos(sol_alt*math.pi/180)*math.cos(lat_px)))

    if ha>0:
        saa_deg         = 180 + saa_rads*180/math.pi
    else:
        saa_deg	        = 180 - saa_rads*180/math.pi

    ha2                 = math.acos(math.cos(b0*math.pi/180)/(math.cos(lat_px)*math.cos(declin)) - math.tan(lat_px)*math.tan(declin))               # Sunrise/sunset hour angle
	
    sunrs     		= 720 - 4*(lon_px + ha2*180/math.pi) - eq_time               							            # Sunrise (UTC) in minutes
    sunrise     	= std_lon/15 + sunrs/60                          									    # Sunrise (local time) in hours
    sunst      		= 720 - 4*(lon_px+(-ha2*180/math.pi)) - eq_time            							            # Sunset (UTC) in minutes
    sunset      	= std_lon/15 + sunst/60                           									    # Sunset (local time) in hours

    return [sza_deg,saa_deg,sunrise,sunset]

#--uΓu--    

### test
doy             = 228
time            = 13
tz_bool         = 'Yes'
tm_zn           = 3
lat_px          = 0
lon_px          = 37.1

[sza_deg,saa_deg,sunrise,sunset] = solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)
    
