'''
General/miscellaneous tools/functions

        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- py from 170823
'''

import math


###===================================================================================================================
def polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px):
    '''
    satellite [polar orbiter] view angles algorithm - Niu et al. (2001) - https://doi.org/10.1080/01431160119571
            Calculation of view angles (zenith and azimuth) given a polar orbiting
            satellite's altitude, orbit inclination, satellite's subtrack/nadir
            coordinates, and pixel's ground coordinates 
            
    -- ufu -- py from 170823
    '''
    
    # constants
    rad_earth 	        = 6371                                                                                          # radius of the earth [Km]
    
    # variables
    orb_incl_rads	= orb_incl*math.pi/180										# orbit inclination in radians
    phi 		= lat_px*math.pi/180										# latitude in radians
    OP_bar		= abs(((lon_px - lon_nad)*math.pi/180)*math.cos(phi)) 
    delta 		= math.asin(math.sin(math.pi - orb_incl_rads)*math.sin(OP_bar))					# length of arc OP_bar

    # calculation of view angles
    vza			= math.atan(math.sin(delta)/(math.cos(delta) - rad_earth/(rad_earth + sat_alt))) 	        # view zenith angle (VZA) in radians
    vza_deg 		= vza*180/math.pi	                                                                        # VZA in degrees 

    if lon_px<lon_nad:
        vaa 	        = math.acos(-math.cos(orb_incl_rads)/math.cos(delta)) 						# view azimuth angle (VAA) in radians
    else:
        vaa 	        = math.pi + math.acos(-math.cos(orb_incl_rads)/math.cos(delta)) 				# view azimuth angle (VAA) in radians

    vaa_deg 		= vaa*180/math.pi;										# VAA in degrees
    
    return [vza_deg,vaa_deg]

#--uΓu--

###===================================================================================================================
def solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px):
    '''
    solar angles algorithm - Iqbal (1983) ; Spencer (1971) ; Campbell and Norman (1998)
            Calculation of solar angles (zenith and azimuth) given a pixel's/point's
            ground coordinates and the local UTC time 
            
    -- ufu -- py from 170823
    '''
    
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

###===================================================================================================================
def leafprj(incl,anglerads):
    '''
    Leaf Projection Factor - (Nilson, 1971; Ross, 1981; Roujean, 1996,2000)
            Calculation of the projection factor given the [view] zenith angle
            and the leaf distribution (i.e., leaf geometry in terms of zenith
            inclination and azimuth orientation (uniform orientation assumed here)) 
            
    -- ufu -- py from 190823
    '''
    
    # Projection factor/function for : 1) spherical/random/isotropic ; 2) erectophile/vertical ; 3) planophile/horizontal 4) specific foliage/leaf inclination
    match incl:                                                                 # anglerads(1)[0] = zenith angle of a direction (solar or view); anglerads(2)[1] = leaf inclination angle (from 0 for horizontal to pi/2 for vertical)
        case 'spherical':                                                       # Nilson (1971), eq. 6c
            G   = 1/2
        case 'vertical':                                                        # ~ eq. 6b
            G   = 2/math.pi*math.sin(abs(anglerads[0]))
        case 'horizontal':                                                      # ~ eq. 6a
            G   = abs(math.cos(anglerads[0]))
        case 'specific':                                                        # ~ eqs. 6d,e,f                                                        
            if (abs(anglerads[0]) + anglerads[1]) <= math.pi/2:
                G = math.cos(abs(anglerads[0]))*math.cos(anglerads[1])
            else:
                G = 2/math.pi*(math.cos(abs(anglerads[0]))*math.cos(anglerads[1])
                          *math.asin(1/(math.tan(abs(anglerads[0])))*1/(math.tan(anglerads[1])))
                          + math.sqrt(1 - math.cos(abs(anglerads[0]))**2 - math.cos(anglerads[1])**2))
                
    return G

#--uΓu--

###===================================================================================================================
