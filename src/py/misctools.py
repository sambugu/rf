'''
General/miscellaneous tools/functions :

            - Polar orbiter [satellite] view angles algorithm - Niu et al. (2001)
            - Solar algorithm - Iqbal (1983) ; Spencer (1971)
            - Solar radiation at the bottom of atmosphere/top of canopy [BOA/TOC]
            - Leaf projection - Nilson (1971), ...
            - Spectral scaling of incident sky emission/radiance to within sensing range of TIR sensor  - Olioso (1995); Idso (1981)
            - Chaos Theory : Lorenz' Butterfly model - Lorenz (1963)
            
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu --
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

    vaa_deg 		= vaa*180/math.pi										# VAA in degrees
    
    return [vza_deg,vaa_deg]
###___________________________________________________________________________________________________________________


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
    eq_time 		= A0*(a1 + a2*math.cos(da) + a3*math.sin(da)+a4*math.cos(2*da) + a5*math.sin(2*da))                                         # Equation of time (radians) - see https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
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

    return [sza_deg,saa_deg,sunrise,sunset,da]
###___________________________________________________________________________________________________________________


###===================================================================================================================
def BoaTocRg(tauDat,doy,time,tz_bool,tm_zn,lat_px,lon_px):
    '''
    Bottom of Atmosphere, Top of Canopy short-wave solar radiation
            Calculation of the solar radiation available for driving the energy
            [thus water] cycle, and partitioning of terrestrial fluxes
            
    -- ufu -- py from 200823
    '''

    # constants
    Cs                  = 1361                                                                                                                      # solar constant [W.m-2] - incoming solar radiation as projected at the top of atmosphere (TOA)
        
    # variables
    [sza,saa,sunrise,sunset,da] = solar_pos(doy,time,tz_bool,tm_zn,lat_px,lon_px)
        
    E0                  = 1.000110 + 0.034221*math.cos(da) + 0.001280*math.sin(da) + 0.000719*math.cos(2*da) + 0.000077*math.sin(2*da)              # [1/r^2] - see https://www.mail-archive.com/sundial@uni-koeln.de/msg01050.html
    

    # Atmosphere's optical depth / transmissivity
    if tauDat[0] == 'constant':                                                                                                                     # user-defined transmissivity of the atmosphere
        tau_atm         = tauDat[1]
    elif tauDat[0] == 'Allen98':                                                                                                                    # atmosphere's transmissivity according to Allen et al. (1998) - FAO56
        tau_atm         = 0.75 + 2e-5*tauDat[1]                                                                                                     # tau[1] == Z [m] : the elevation [m]
        
    RgTOC               = Cs*math.cos(sza*math.pi/180)*E0*tau_atm

    return RgTOC
###___________________________________________________________________________________________________________________


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
    match incl:                                                                                                         # anglerads(1)[0] = zenith angle of a direction (solar or view); anglerads(2)[1] = leaf inclination angle (from 0 for horizontal to pi/2 for vertical)
        case 'spherical':                                                                                               # Nilson (1971), eq. 6c
            G           = 1/2
        case 'vertical':                                                                                                # ~ eq. 6b
            G           = 2/math.pi*math.sin(abs(anglerads[0]))
        case 'horizontal':                                                                                              # ~ eq. 6a
            G           = abs(math.cos(anglerads[0]))
        case 'specific':                                                                                                # ~ eqs. 6d,e,f                                                        
            if (abs(anglerads[0]) + anglerads[1]) <= math.pi/2:
                G       = math.cos(abs(anglerads[0]))*math.cos(anglerads[1])
            else:
                G       = 2/math.pi*(math.cos(abs(anglerads[0]))*math.cos(anglerads[1])
                              *math.asin(1/(math.tan(abs(anglerads[0])))*1/(math.tan(anglerads[1])))
                              + math.sqrt(1 - math.cos(abs(anglerads[0]))**2 - math.cos(anglerads[1])**2))
                
    return G
###___________________________________________________________________________________________________________________


###===================================================================================================================
def brightnessT_814N105125(dat):
    '''
    Ratm spectral scaling algorithm - Olioso (1995); Idso (1981)
            Scaling of the incoming sky radiance (atmospheric emission) to within 8-14 um
            and 10.5-12.5 um spectral bands [sensing range of most TIR sensors]
            
    -- ufu -- py from 220823
    '''

    # constants/variables
    sigma                = 5.67e-8
    tsobs                = dat['tsobs']                                                                                 # [C]
    ta                   = dat['airT']                                                                                  # [K]
    rh                   = dat['rh']
    ea                   = 0.01*rh*6.108*math.exp(17.27*(ta - 273.15)/(ta - 35.85))                                     # ta in K, rh %
    
    match dat['TIRband']:
        case 'TIR814':                                                                                                  # 8-14 um
            f814         = -0.6732 + 0.624*0.01*(tsobs + 273.15) - 0.914*10**(-5)*(tsobs + 273.15)**2                   # tsobs in C
            emis814      = 0.15 + 5.03*10**(-6)*ea*math.e**(2450/ta)                                                    # atmospheric apparent emissivity @8um-14um
            f814ta       = -0.6732 + 0.624*0.01*ta - 0.914*10**(-5)*ta**2
            ratm814      = emis814*sigma*f814ta*ta**4                                                                   # atmospheric emission @8um-14um
            TBdat        = {'f':f814}; TBdat['fta'] = f814ta
            TBdat['ratm']= ratm814
        case 'TIR105125':                                                                                               # 10.5-12.5 um
            f105125      = -0.2338 + 0.2288*0.01*(tsobs + 273.15) - 0.3617*10**(-5)*(tsobs + 273.15)**2
            emis105125   = 5.91*10**(-6)*ea*math.exp(2450/ta)                                                           # atmospheric apparent emissivity @10.5um-12.5um
            f105125ta    = -0.2338 + 0.2288*0.01*ta - 0.3617*10**(-5)*ta**2
            ratm105125   = emis105125*sigma*f105125ta*ta**4                                                             # atmospheric emission @10.5um-12.5um
            TBdat        = {'f':f105125}; TBdat['fta'] = f105125ta
            TBdat['ratm']= ratm105125
            
    return TBdat
###___________________________________________________________________________________________________________________


###===================================================================================================================
import numpy as np

def lorenz(Xin,sigma,rho,beta,dt):
    '''
    Chaos Theory : Lorenz Butterfly algorithm - Lorenz (1963) : https://doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2
    The deterministic non-periodic flow algorithm as presented in Lorenz (1963)
            one-step integration of the numerical solution of a simple system
            representing cellular convection :
                Inputs : initial state ; parameters - rho, sigma, beta ; timestep
            
            . translated from Lisa.Neef.13 matlab scripts  : https://github.com/LisaNeef/Data-Assimilation-Practicals-Matlab/blob/master/lorenz63.m
    -- ufu -- py from 240823
    '''

    # Integration of Xinit using the numerical solution of the Lorenz model
        # Mean trajectory calculation
    w1                  = 1/6; w2 = 1/3; w3 = 1/3; w4 = 1/6

    xin1                = Xin
    fp                  = lorenzRHS(xin1,sigma,rho,beta)
    x1                  = dt*fp

    xin2                = Xin + 0.5*x1
    fp                  = lorenzRHS(xin2,sigma,rho,beta)
    x2                  = dt*fp

    xin3                = Xin + 0.5*x2
    fp                  = lorenzRHS(xin3,sigma,rho,beta)
    x3                  = dt*fp

    # x4 = Xin + x3                                                                                                     ### corrected from xx4 = xin+ x3; in lisaneef's .m script -- commented out : throws overflow errors ...nans in both .py and .m

    # ADDED : correction for var x4 --- overflow errors disparu
    xin4                = Xin + 0.5*x3
    fp                  = lorenzRHS(xin4,sigma,rho,beta)
    x4                  = dt*fp
    
    X                   = Xin + w1*x1 + w2*x2 + w3*x3 + w4*x4

    return X

def lorenzRHS(xx,sigma,rho,beta):
    
        x               = xx[0]; y = xx[1]; z = xx[2]
        
        f               = np.zeros(shape = [3,1])

        f[0]            = sigma*(y - x); f[1] = rho*x - y - x*z; f[2] = x*y - beta*z                                    # RHS of eq. (5) of Lorenz (1986) p1550

        return f
###___________________________________________________________________________________________________________________


###===================================================================================================================

###___________________________________________________________________________________________________________________


#--uΓu--
