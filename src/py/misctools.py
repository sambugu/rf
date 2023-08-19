'''
General/miscellaneous tools/functions

        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- py from 190823
'''

import math


def leafprj(incl,anglerads):
    '''
    Leaf Projection Factor - (Nilson, 1971; Ross, 1981; Roujean, 1996,2000)
            Calculation of the projection factor given the [view] zenith angle
            and the leaf distribution (i.e., leaf	geometry in terms of zenith
            inclination and azimuth orientation 
            
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

### test
anglerads       = [1,1]
G               = leafprj('specific',anglerads)
