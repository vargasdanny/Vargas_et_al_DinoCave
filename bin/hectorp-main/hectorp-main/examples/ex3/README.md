
In order to perform Monte Carlo simulations, one must create time series with synthetic coloured noise. This task can be performed with the program simulatenoise. It is based on the method described by Kasdin (1995) where an impulse response, different for each noise model, is convoluted with a white noise time series. The result is our desired synthetic noise time series. As usual, the convolution is performed using FFT. There might be some spin-up effects because implicitly it is assumed that the noise is zero before the first observation. To migitate this problem, the keyword ’TimeNoiseStart’ can have a large number, normally 1000 is enough, to specify the amount of extra points before the first observations need to be modelled. Note that this is based on my experience analysing GNSS daily position time series. Your milage may vary.

In the directory ex3 the control-file `simulatenoise.ctl` is given:

~~~
SimulationDir           ./obs_files
SimulationLabel         test_base
NumberOfSimulations     10
NumberOfPoints          5000
SamplingPeriod          1.0
TimeNoiseStart          1000
NoiseModels             GGM White
GGM_1mphi               6.9e-06
PhysicalUnit            mm
~~~


Some of these keywords are new. For example, ’SimulationDir’ specifies in which directory the created files should be stored. The keyword ’SimulationLabel’ specifies the base name of those files. The next keyword tells HectorP how many simulation runs are required. The filenames will in this case be: test_base0.mom, test_base1.mom, . . ., test_base9.mom.
The keyword ’NumberOfPoints’ specifies the number of points in the the time series and the keyword ’TimeNoiseStart’ was already discussed above.
When simulatenoise is run, it will ask the user to manually enter the parameter values of the chosen noise model. In this case it will ask the values of φ and d.
In some cases it is desirable to create the same set of synthetic time series each time simulatenoise is run. To achieve this, one can set the keyword ’RepeatableNoise’ to yes.

As before, the noise model GGM with GGM_1mphi fixed to a value is a trick to simulate power-law noise that only flattens at the very, very low frequencies.

When run, the screen looks like the following:
~~~
***************************************
    simulatenoise, version 0.1.1
***************************************

Filename                   : None
TS_format                  : mom
ScaleFactor                : 1.000000
spectral index kappa: -1
power-law noise amplitude: 10
white noise amplitude: 4
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_0.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_1.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_2.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_3.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_4.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_5.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_6.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_7.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_8.mom
--> /Users/msbos/projects/hectorp/code/examples/ex3/obs_files/test_base_9.mom
---   18.098 seconds ---
~~~


The user must provide the values -1, 10 and 4. These can also be put in a file, such as `simulatenoise.inp`.

The program can then be calles as follows:
~~~
simulatenoise < simulatenoise.inp
~~~

You can check by running `estimate_all_trends` we indeed again estimate a power-law noise with spectral index -1 and amplitude of 10 together with White noise with an amplitude of 4 mm.

For fun, you can run again `estimate_all_trend` but now with RMLE:
~~~
estimate_all_trends -useRMLE
~~~

To study the effect of using restricted MLE, see [Gobron et al. (2022)](https://link.springer.com/article/10.1007/s00190-022-01634-9).

# References

Kasdin, N. J. (1995). Discrete simulation of colored noise and stochastic processes and
1/fα power-law noise generation. Proc. IEEE, 83(5):802–827.
