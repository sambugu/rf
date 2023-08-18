'''
satellite [polar orbiter] view angles algorithm - Niu et al. (2001) - https://doi.org/10.1080/01431160119571
	Calculation of view angles (zenith and azimuth) given a polar orbiting satellite's altitude, orbit inclination,
	satellite's subtrack/nadir coordinates, and pixel's ground coordinates 
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- py from 170823
'''

import math

def polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px):
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

# test
sat_alt             = 761
orb_incl            = 81.3        
lon_nad             = 4
lat_px              = 40
lon_px              = 7

[vza_deg,vaa_deg]   = polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px)
    
