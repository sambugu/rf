
/* solar angles algorithm - Iqbal (1983) ; Spencer (1971) ; Campbell and Norman (1998)
	Calculation of solar angles (zenith and azimuth) given a pixel's/point's ground coordinates and the local UTC time 
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- JS from 140823
*/
	
function solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px){

	// constants --- from Fourier series analysis by Spencer (1971) - https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
	const A0 			= 229.18;
	//const a1          	= 0.000075;      	const a2 	= 0.001868;		const a3 	= -0.032077; 
	const a1          	= 0.0000075;      	const a2 	= 0.001868;		const a3 	= -0.032077; 			// see correction for var a1 in https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
	const a4          	= -0.014615;     	const a5 	= -0.040849;	const a6 	= 0.006918;
	const a7          	= -0.399912;     	const a8 	= 0.070257;		const a9 	= -0.006758;
	const a10         	= 0.000907;     	const a11 	= -0.002697;	const a12 	= 0.00148;
	const b0          	= 90.833;
	
	let denom 			= 365; 																				// should consider leap years according to the Gregorian calendar for exactness (i.e., leapyr IF ((mod(yr/4)==0 EXCEPT mod(yr/100)==0) || mod(yr/400)==0) --- left AS IS here
	
	// variables
	let da          	= 2*Math.PI*(doy - 1 + (Math.floor(time) - 12)/24)/denom; 							// Fractional year / day angle
	
		if (tz_bool=='Yes'){
			std_lon 	= tm_zn*15;
		} else {
			std_lon 	= Math.round(lon_px/15)*15;
		}
	
	let lon_corr 		= 4*(std_lon - lon_px);
	lat_px				= lat_px*Math.PI/180;
	let eq_time 		= A0*(a1 + a2*Math.cos(da) + a3*Math.sin(da)+a4*Math.cos(2*da) + a5*Math.sin(2*da));// Equation of time (radians) - see https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
	let declin      	= a6 + a7*Math.cos(da) + a8*Math.sin(da) + a9*Math.cos(2*da) + a10*Math.sin(2*da) + a11*Math.cos(3*da) + a12*Math.sin(3*da); // Solar declination - in radians
	let solar_time  	= time + eq_time/60 - lon_corr/60; 													// Solar time (hours)
	let ha          	= 15*(solar_time-12); 																// Hour angle (degrees)
	
	// solar zenith angle in radians and degrees
	let sza_rads        = Math.acos(Math.sin(lat_px)*Math.sin(declin) + Math.cos(declin)*Math.cos(lat_px)*Math.cos(ha*Math.PI/180));				
	let sza_deg 		= sza_rads*180/Math.PI;
	
	let sol_alt 		= 90 - sza_deg;
	
	let saa_rads		= Math.acos((Math.sin(sol_alt*Math.PI/180)*Math.sin(lat_px) - Math.sin(declin))/(Math.cos(sol_alt*Math.PI/180)*Math.cos(lat_px)));
		
		if (ha>0){
			var saa_deg = 180 + saa_rads*180/Math.PI; 
		} else {
			var saa_deg	= 180 - saa_rads*180/Math.PI;
		}

	let ha2         	= Math.acos(Math.cos(b0*Math.PI/180)/(Math.cos(lat_px)*Math.cos(declin)) - Math.tan(lat_px)*Math.tan(declin)); // Sunrise/sunset hour angle
	
	let sunrs     		= 720 - 4*(lon_px + ha2*180/Math.PI) - eq_time;               							// Sunrise (UTC) in minutes
	let sunrise     	= std_lon/15 + sunrs/60;                          									// Sunrise (local time) in hours
	let sunst      		= 720 - 4*(lon_px+(-ha2*180/Math.PI)) - eq_time;            							// Sunset (UTC) in minutes
	let sunset      	= std_lon/15 + sunst/60;                           									// Sunset (local time) in hours

	return [sza_deg,saa_deg,sunrise,sunset];
}

//--uΓu--
