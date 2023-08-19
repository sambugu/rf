#======================================================================================================================================
#======================================================================================================================================
# satellite [polar orbiter] view angles algorithm - Niu et al. (2001) - https://doi.org/10.1080/01431160119571
# Calculation of view angles (zenith and azimuth) given a polar orbiting satellite's altitude, orbit inclination,
#	satellite's subtrack/nadir coordinates, and pixel's ground coordinates 
#	
#        .This is free software under the GNU General Public License v3.0.
#        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
#	
#-- ufu -- R from 190823
#======================================================================================================================================

rm(list=ls(all=TRUE))   # clear workspace

polarorbiter_angles   <- function(sat_alt,orb_incl,lon_nad,lat_px,lon_px){

  # constants
  rad_earth 	        <- 6371                                                                                          # radius of the earth [Km]
  
  # variables
  orb_incl_rads     	<- orb_incl*pi/180										                                    # orbit inclination in radians
  phi 		            <- lat_px*pi/180										                                      # latitude in radians
  OP_bar 		          <- abs(((lon_px - lon_nad)*pi/180)*cos(phi)) 
  delta 		          <- asin(sin(pi - orb_incl_rads)*sin(OP_bar))					                    # length of arc OP_bar
  
  # calculation of view angles
  vza 		            <- atan(sin(delta)/(cos(delta) - rad_earth/(rad_earth + sat_alt))) 	      # view zenith angle (VZA) in radians
  vza_deg 		        <- vza*180/pi	                                                            # VZA in degrees 
  
  if (lon_px < lon_nad){
    vaa 		          <- acos(-cos(orb_incl_rads)/cos(delta)) 						                      # view azimuth angle (VAA) in radians
  } else {
    vaa 		          <- pi + acos(-cos(orb_incl_rads)/cos(delta)) 				                      # view azimuth angle (VAA) in radians
  }
  
  vaa_deg 		        <- vaa*180/pi;										                                        # VAA in degrees
  
  return (list(vza_deg=vza_deg,vaa_deg=vaa_deg))
}

#--uΓu--    

#======================================================================================================================================
### test - see https://runningfingers.com/viewangles.php
#

sat_alt 		          <- 761
orb_incl 		          <- 81.3        
lon_nad 		          <- 4
lat_px 		            <- 40
lon_px 		            <- 7

polVars               =  polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px)
vza_deg 		          <- polVars$vza_deg
vaa_deg 		          <- polVars$vaa_deg

###
