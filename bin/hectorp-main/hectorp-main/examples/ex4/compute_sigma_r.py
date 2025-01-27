#!/usr/bin/env python
#
# simply compute sigma_r
#
# 30/7/2022 Machiel Bos, Santa Clara
#===============================================================================

from scipy.special import gamma
import math

#===============================================================================
# Subroutines
#===============================================================================

def compute_sigma_r(N,T,kappa,sigma_pl):
    """ Apply Eq. 29 of Bos et al. (2008)

    Args:
        N (int) : number of observations
        T (float) : fraction of sampling period / 365.25
        kappa (float) : spectral index
        sigma_pl : noise amplitude, scaled with T^(-kappa/4)

    Returns:
        sigma_r : trend uncertainty in mm/yr
    """

    return math.sqrt(pow(sigma_pl,2)/pow(T,2+kappa/2) * \
                (gamma(3+kappa)*gamma(4+kappa)) / pow(gamma(2+kappa/2),2.0) * \
                                                            pow(N-1,-kappa-3))


def compute_sigma_r_flicker(N,T,sigma_pl):
    """ Apply Eq. 32 of Bos et al. (2008)

    Args:
        N (int) : number of observations
        T (float) : fraction of sampling period / 365.25
        sigma_pl : noise amplitude, scaled with T^(-kappa/4)

    Returns:
        sigma_r : trend uncertainty in mm/yr
    """

    return math.sqrt(8.0*pow(sigma_pl,2)/pow(T,1.5) * 1.0/(math.pi*(N*(N-1))))



#===============================================================================
# Main program 
#===============================================================================


for sampling in ['monthly','yearly']:

    if sampling=='monthly':
        sigma_pl = 82.72360  # mm/yr^-kappa/4
        T        = 1/12
        kappa    = -0.344
        N        = 1280
    else:
        sigma_pl = 25.6858  # mm/yr^-kappa/4
        T        = 1/1   
        kappa     = -0.4640
        N        = 104

    #--- Print out final trend uncertainty
    print('NEWLYN ({0:7s}), sigma_r = {1:8.3f} mm/yr'.\
                        format(sampling,compute_sigma_r(N,T,kappa,sigma_pl)))

print('Synthetic daily  21000, sigma_r = {0:8.3f} ({1:8.3f}) mm/yr'.\
                      format(compute_sigma_r(21000,1/365.25,-1.0,10.0), \
                             compute_sigma_r_flicker(21000,1/365.25,10.0)))
print('Synthetic weekly  3000, sigma_r = {0:8.3f} ({1:8.3f}) mm/yr'.\
                      format(compute_sigma_r(3000,7/365.25,-1.0,10.0), \
                             compute_sigma_r_flicker(3000,7/365.25,10.0)))
