#!/usr/bin/env python
#
# This script creates a synthetic a post-seismic relaxation signal to test it.
#
# 26/10/2015 Machiel Bos, Santa Clara
# 21/ 8/2022 Machiel Bos, Santa Clara
#===============================================================================

import math
import sys
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

#===============================================================================
# Main program
#===============================================================================


n=5000
mjd0 = 51544.0
t=np.linspace(1,n,n)
x=np.zeros(n)
  
V              = 0.02/365.25   # vertical velocity
offsets        = [[450.0,3],[2000,-2],[3500.0,1]]
postseismiclog = [[450.0,10.0,0.2],[3500.0,10.0,-0.3]]
postseismicexp = [[2000.0,100.0,1.0]]

#--- Write header
fp = open('obs_files/TEST.mom','w')
fp.write('# sampling period 1.0\n')
for i in range(0,3):
    [tt,jump] = offsets[i]
    fp.write('# offset {0:8.1f}\n'.format(tt+mjd0))
  
for i in range(0,2):
    [tt,tau,jump] = postseismiclog[i]
    fp.write('# log {0:8.1f} {1:6.1f}\n'.format(tt+mjd0,tau))
  
for i in range(0,1):
    [tt,tau,jump] = postseismicexp[i]
    fp.write('# exp {0:8.1f} {1:6.1f}\n'.format(tt+mjd0,tau))

#--- Create power-law + white noise
d        = 0.5
sigma_pl = 0.1
sigma_w  = 0.05
h = np.zeros(n)
h[0] = 1;
for i in range(1,n):
    h[i] = (d+i-1.0)/i * h[i-1]
 
rng = np.random.default_rng()
w1 = sigma_pl*rng.standard_normal(n)
w2 = sigma_w *rng.standard_normal(n)
x  = signal.fftconvolve(h, w1)[0:n] + w2

#--- uplift
x += V*t

#--- Offsets
for i in range(0,n):
    for j in range(0,3):
        [tt,jump] = offsets[j]
        if i>tt:
            x[i] += jump
      
    
#--- Post-seismic logarithmic relaxation
for j in range(0,2):
    [tt,tau,jump] = postseismiclog[j]
    for i in range(0,n):
        if i>tt:
            x[i] += jump*math.log(1 + (i-tt)/tau)
    
#--- Post-seismic exponential relaxation
for j in range(0,1):
    [tt,tau,jump] = postseismicexp[j]
    for i in range(0,n):
        if i>tt:
            x[i] += jump*(1 - math.exp(-(i-tt)/tau))

#--- Save signal to file
for i in range(0,n):
    fp.write('{0:8.1f} {1:7.3f}\n'.format(t[i]+mjd0,x[i]))
fp.close()

#--- Make plot
fig = plt.figure(figsize=(6, 4), dpi=150)
plt.plot(2000 + t/365.25, x, 'b-', label='modelled')
plt.xlabel('Year')
plt.ylabel('mm')
plt.show()
