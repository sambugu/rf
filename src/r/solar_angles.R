#======================================================================================================================================
#======================================================================================================================================
# solar angles algorithm - Iqbal (1983) ; Spencer (1971) ; Campbell and Norman (1998)
# Calculation of solar angles (zenith and azimuth) given a pixel's/point's ground coordinates and the local UTC time 
#
#   .This is free software under the GNU General Public License v3.0.
#   .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
#
#-- ufu -- R from 190823
#======================================================================================================================================

rm(list=ls(all=TRUE))   # clear workspace

solar_pos           <- function(doy,time,tz_bool,tm_zn,lat_px,lon_px){

  # constants --- from Fourier series analysis by Spencer (1971) - https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
  A0 		            <- 229.18
  # a1          	  = 0.000075;     a2  = 0.001868;     a3 	= -0.032077;
  a1 		            <- 0.0000075;    a2  <- 0.001868;     a3 	<- -0.032077                                                  # see correction for var a1 in https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
  a4 		            <- -0.014615;    a5  <- -0.040849;    a6 	<- 0.006918
  a7 		            <- -0.399912;    a8  <- 0.070257;     a9 	<- -0.006758
  a10 		          <- 0.000907;     a11 <- -0.002697;    a12 <- 0.00148
  b0 		            <- 90.833
  
  denom             <- 365                                                                                                   # should consider leap years according to the Gregorian calendar for exactness (i.e., leapyr IF ((mod(yr/4)==0 EXCEPT mod(yr/100)==0) || mod(yr/400)==0) --- left AS IS here
  
  # variables
  da 		            <- 2*pi*(doy - 1 + (floor(time) - 12)/24)/denom                                                          # Fractional year / day angle
  
  if (tz_bool == 'Yes'){
    std_lon 		    <- tm_zn*15
  } else {
    std_lon 		    <- round(lon_px/15)*15
  }
  
  lon_corr 		      <- 4*(std_lon - lon_px)
  lat_px 		        <- lat_px*pi/180
  eq_time 		      <- A0*(a1 + a2*cos(da) + a3*sin(da)+a4*cos(2*da) + a5*sin(2*da))                                          # Equation of time (minutes)
  declin 		        <- a6 + a7*cos(da) + a8*sin(da) + a9*cos(2*da) + a10*sin(2*da) + a11*cos(3*da) + a12*sin(3*da)            # Solar declination - in radians
  solar_time 		    <- time + eq_time/60 - lon_corr/60 											                                                  # Solar time (hours)
  ha 		            <- 15*(solar_time-12) 													                                                          # Hour angle (degrees)
  
  # solar zenith angle in radians and degrees
  sza_rads 		      <- acos(sin(lat_px)*sin(declin) + cos(declin)*cos(lat_px)*cos(ha*pi/180))				
  sza_deg 		      <- sza_rads*180/pi
  sol_alt 		      <- 90 - sza_deg
  
  saa_rads 		      <- acos((sin(sol_alt*pi/180)*sin(lat_px) - sin(declin))/(cos(sol_alt*pi/180)*cos(lat_px)))
  
  if (ha > 0){
    saa_deg 		    <- 180 + saa_rads*180/pi
  } else {
    saa_deg 		    <- 180 - saa_rads*180/pi
  }
  
  ha2 		          <- acos(cos(b0*pi/180)/(cos(lat_px)*cos(declin)) - tan(lat_px)*tan(declin))               # Sunrise/sunset hour angle
  
  sunrs 		        <- 720 - 4*(lon_px + ha2*180/pi) - eq_time               							            # Sunrise (UTC) in minutes
  sunrise 		      <- std_lon/15 + sunrs/60                          									    # Sunrise (local time) in hours
  sunst 		        <- 720 - 4*(lon_px+(-ha2*180/pi)) - eq_time            							            # Sunset (UTC) in minutes
  sunset 		        <- std_lon/15 + sunst/60                           									    # Sunset (local time) in hours
  
  return (list(sza_deg=sza_deg,saa_deg=saa_deg,sunrise=sunrise,sunset=sunset))
  
}

#--uΓu--     

#======================================================================================================================================
### test - see https://runningfingers.com/solar.php
#

doy 		            <- 228
time 		            <- 13
tz_bool 		        <- 'Yes'
tm_zn 		          <- 3
lat_px 		          <- 0
lon_px 		          <- 37.1

solVars 		        =  solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)
sza_deg 		        <- solVars$sza_deg
saa_deg 		        <- solVars$saa_deg

###
