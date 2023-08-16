
/* satellite [polar orbiter] view angles algorithm - Niu et al. (2001) - https://doi.org/10.1080/01431160119571
	Calculation of view angles (zenith and azimuth) given a polar orbiting satellite's altitude, orbit inclination,
	satellite's subtrack/nadir coordinates, and pixel's ground coordinates 
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- JS from 260723
*/
	
function polarorbiter_angles(sat_alt,orb_incl,lon_nad,lat_px,lon_px){

	// constants
	const rad_earth 	= 6371;																				// radius of the earth [Km]

	// variables
	let orb_incl_rads	= orb_incl*Math.PI/180;																// orbit inclination in radians
	let phi 			= lat_px*Math.PI/180;																// latitude in radians
	let OP_bar			= Math.abs(((lon_px - lon_nad)*Math.PI/180)*Math.cos(phi)); 
	let delta 			= Math.asin(Math.sin(Math.PI - orb_incl_rads)*Math.sin(OP_bar));					// length of arc OP_bar

	// calculation of view angles
	let vza				= Math.atan(Math.sin(delta)/(Math.cos(delta) - rad_earth/(rad_earth + sat_alt))); 	// view zenith angle (VZA) in radians
	let vza_deg 		= vza*180/Math.PI;														  			// VZA in degrees 

		if (lon_px<lon_nad){
			var vaa 	= Math.acos(-Math.cos(orb_incl_rads)/Math.cos(delta)); 								// view azimuth angle (VAA) in radians
		} else {
			var vaa 	= Math.PI + Math.acos(-Math.cos(orb_incl_rads)/Math.cos(delta));					// view azimuth angle (VAA) in radians
		}

	let vaa_deg 		= vaa*180/Math.PI;																	// VAA in degrees

	return [vza_deg,vaa_deg];
}

/*
// Standard Normal variate using Box-Muller transform.
function randn_bm() {
    var u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}
*/
//--uÎ“u--
