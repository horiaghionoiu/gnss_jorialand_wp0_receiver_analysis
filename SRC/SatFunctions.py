## Copyright (C) GNSS ACADEMY 
##
## Name          : SatFunctions.py
## Purpose       : Satellite Analyses functions
## Project       : WP0-JSNP
## Component     : 
## Author        : GNSS Academy
## Creation date : 2021
## File Version  : 1.0
## Version date  : 
##

import sys, os
from pandas import unique
from interfaces import LOS_IDX
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
from COMMON.Plots import generatePlot
import numpy as np
# from pyproj import Transformer
from COMMON.Coordinates import xyz2llh


# Plot Satellite Visibility Figures
def plotSatVisibility(LosData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Satellite Visibility from TLSA on Year 2015"\
        " DoY 006"

    PlotConf["yLabel"] = "GPS-PRN"
    PlotConf["yTicks"] = sorted(unique(LosData[LOS_IDX["PRN"]]))
    PlotConf["yTicksLabels"] = sorted(unique(LosData[LOS_IDX["PRN"]]))
    PlotConf["yLim"] = [0, max(unique(LosData[LOS_IDX["PRN"]])) + 1]

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '|'
    PlotConf["LineWidth"] = 15

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    for prn in sorted(unique(LosData[LOS_IDX["PRN"]])):
        Label = "G" + ("%02d" % prn)
        FilterCond = LosData[LOS_IDX["PRN"]] == prn
        PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][Label] = LosData[LOS_IDX["PRN"]][FilterCond]
        PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'SAT_VISIBILITY_TLSA_D006Y15.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)


# Plot Satellite Geometrical Range Figures
def plotSatGeomRnge(LosData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,7.6)
    PlotConf["Title"] = "Satellite Geometical Range from TLSA on Year 2015"\
        " DoY 006"

    PlotConf["yLabel"] = "Range [m]"

    PlotConf["xLabel"] = "Hour of DoY 006"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 0.75

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    Label = 0
    PlotConf["xData"][Label] = LosData[LOS_IDX["SOD"]] / GnssConstants.S_IN_H
    PlotConf["yData"][Label] = LosData[LOS_IDX["RANGE[m]"]]
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]

    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'SAT_GEOMETRICAL_RANGE_TLSA_D006Y15.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)


# Plot Satellite Tracks Figures
def plotSatTracks(LosData):
    PlotConf = {}

    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (16.8,15.2)
    PlotConf["Title"] = "Satellite Tracks during visibility periods from "\
        "TLSA on Year 2015 DoY 006"

    PlotConf["LonMin"] = -135
    PlotConf["LonMax"] = 135
    PlotConf["LatMin"] = -35
    PlotConf["LatMax"] = 90
    PlotConf["LonStep"] = 15
    PlotConf["LatStep"] = 10

    # PlotConf["yLabel"] = "Latitude [deg]"
    PlotConf["yTicks"] = range(PlotConf["LatMin"],PlotConf["LatMax"]+1,10)
    PlotConf["yLim"] = [PlotConf["LatMin"], PlotConf["LatMax"]]

    # PlotConf["xLabel"] = "Longitude [deg]"
    PlotConf["xTicks"] = range(PlotConf["LonMin"],PlotConf["LonMax"]+1,15)
    PlotConf["xLim"] = [PlotConf["LonMin"], PlotConf["LonMax"]]

    PlotConf["Grid"] = True

    PlotConf["Map"] = True

    PlotConf["Marker"] = '.'
    PlotConf["LineWidth"] = 0.75

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    # Transform ECEF to Geodetic
    LosData[LOS_IDX["SAT-X[m]"]].to_numpy()
    LosData[LOS_IDX["SAT-Y[m]"]].to_numpy()
    LosData[LOS_IDX["SAT-Z[m]"]].to_numpy()
    DataLen = len(LosData[LOS_IDX["SAT-X[m]"]])
    Longitude = np.zeros(DataLen)
    Latitude = np.zeros(DataLen)
    # transformer = Transformer.from_crs('epsg:4978', 'epsg:4326')
    for index in range(DataLen):
        x = LosData[LOS_IDX["SAT-X[m]"]][index]
        y = LosData[LOS_IDX["SAT-Y[m]"]][index]
        z = LosData[LOS_IDX["SAT-Z[m]"]][index]
        Longitude[index], Latitude[index], h = xyz2llh(x, y, z)
        # Latitude[index], Longitude[index], h = transformer.transform(x, y, z)

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}
    Label = 0
    PlotConf["xData"][Label] = Longitude
    PlotConf["yData"][Label] = Latitude
    PlotConf["zData"][Label] = LosData[LOS_IDX["ELEV"]]

    PlotConf["Path"] = sys.argv[1] + '/OUT/LOS/SAT/' + 'SAT_TRACKS_TLSA_D006Y15.png'

    # Call generatePlot from Plots library
    generatePlot(PlotConf)
