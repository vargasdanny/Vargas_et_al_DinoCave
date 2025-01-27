#!/bin/bash
#
#===============================================================================

removeoutliers -i removeoutliers_acc.ctl -graph
removeoutliers -i removeoutliers_gyr.ctl -graph

estimatetrend -i estimatetrend_acc.ctl -graph -png
estimatespectrum -i estimatespectrum_acc.ctl -graph -png -model

estimatetrend -i estimatetrend_gyr.ctl -graph -png
estimatespectrum -i estimatespectrum_gyr.ctl -graph -png -model
