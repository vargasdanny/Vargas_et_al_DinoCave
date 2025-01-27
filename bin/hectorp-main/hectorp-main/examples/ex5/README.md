After a large earth-quake, the Earth's surface slowly returns to a new
position. This post-seismic relaxation can be modelled with an
exponential or logarithmic function, see wiki pages on trajectory model. In the
directory ex5 we have created a synthetic time series with
various relaxation signals. We *know* when the synthetic earthquakes
occurred and therefore add offset epochs in the header of the
observation file `TEST.mom` in the directory `./obs\_files`.
Furthermore, add information about the relaxtion times (unit is days)
for each event:
```
# sampling period 1.0
# offset  51994.0
# offset  53544.0
# offset  55044.0
# log  51994.0   10.0
# log  55044.0   10.0
# exp  53544.0  100.0
```

To force `estimatetrend` model this signal, include the line
"estimatepostseismic   yes" in the control file:
```
DataFile              TEST.mom
DataDirectory         ./obs_files
OutputFile            ./fin_files/TEST.mom
estimateoffsets       yes
estimatepostseismic   yes
NoiseModels           GGM White
GGM_1mphi             6.9e-06
PhysicalUnit          mm
ScaleFactor           1.0
```

The observations and fitted model is plotted in Figure below.
To include slow-slip events the procedure is similar. You need to include
the line 'estimateslowslipevent yes' in the control file and add to
the mom-file in the header `# tanh MMMM DD` where MMM is the Modified
Julian Date and DD the relaxation time in days, see again the
wiki pages on trajectory models for more details. 

![Example of the synthetic time series plus the fitted
signal which include various exponential and logarithmic post-seismic
relaxations.](./PostSeismic.png)

Screen should show when running `estimatetrend`:
```
***************************************
    estimatetrend, version 0.0.8
***************************************

Filename                   : obs_files/TEST.mom
TS_format                  : mom
ScaleFactor                : 1.000000
Number of observations+gaps: 5000
Percentage of gaps         :   0.0
No extra periodic signals are included.
No Polynomial degree set, using offset + linear trend
0) White
Nparam : 0
useRMLE-> False
----------------
  Ordinary LS
----------------
Number of iterations : 0
min log(L)           : 1683.030317
ln_det_I             : 93.533877
ln_det_HH            : 65.445163
ln_det_C             : 0.000000
AIC                  : -3348.060634
BIC                  : -3289.405895
KIC                  : -3195.872018
driving noise        : 0.172813

Noise Models
------------
White:
fraction  = 1.00000
sigma     =  0.1728 mm
No noise parameters to show

bias : 0.509 +/- 0.027 (at 54044.50)
trend: 0.055 +/- 0.004 mm/yr
offset at 51994.0000 :    3.17 +/-  0.02 mm
offset at 53544.0000 :   -1.91 +/-  0.03 mm
offset at 55044.0000 :    0.79 +/-  0.02 mm
exp relaxation at 53544.0000 (T=  100.00) :    0.90 +/-  0.03 mm
log relaxation at 51994.0000 (T=   10.00) :    0.13 +/-  0.01 mm
log relaxation at 55044.0000 (T=   10.00) :   -0.30 +/-  0.01 mm
--> ./fin_files/TEST.mom
---    0.356 s ---

```
