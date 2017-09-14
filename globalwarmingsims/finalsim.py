from bokeh.io import curdoc

import zscript as zs
from data import *
from zgraph import *
from zscript.zsyntaxtree import Unknown

constants = '''
;; Time ;;
dt := 3*24*60*60 ;; seconds -> 1 day
t := 0
t_+ = dt + t
dtyears = dt/(365*24*60*60) ;; years
tyears = t/(365*24*60*60) ;; years


;; Conversion Calculations ;; Values from: https://spacemath.gsfc.nasa.gov/books.html# -> Earth Math (2009) and Wikipedia
Ma := 5.1e6 ;; gigatons ;; total mass of atmosphere
Mola := 28.97 ;; grams/AMU ;; 1 mole of atmosphere

Molco2 := 44.009 ;; grams/AMU ;; mole
MtoCco2 := (1e6/Ma) * (Mola/Molco2) ;; gton -> ppmv

Molch4 := 16.043 ;; grams/AMU ;; mole
MtoCch4 := (1e9/Ma) * (Mola/Molch4) ;; gton -> ppbv

Moln2o := 46.005 ;; grams/AMU ;; mole
MtoCn2o := (1e9/Ma) * (Mola/Moln2o) ;; gton -> ppbv

'''

concentrationdefualt = '''
;; Starting Concentrations ;; Values from: Recent Greenhouse Gas Concentrations, DOI: 10.3334/CDIAC/atg.032
Cco2 := 399.5 ;; ppmv
Cch4 := 1834 ;; ppbv
Cn2o := 328 ;; ppbv

;; Formula from: Myhrvold and Caldeira (2012) Supporting Information
Gbase := ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 := 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)
'''

oceandefault = '''
;; Ocean Calculations ;; Values from: Myhrvold and Caldeira (2012) Supporting Information ... pg.13 and Testing best values
layers := 60 ;; number of layers
layerdepth := 2000/layers ;; meters
k := 1e-4 ;; m^2/s
lambda := 1.25 ;; W/m^2 K
;; surface index
surface := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] ;; 60 layers
'''

srcdefualt = '''
Srcco2 := 0 ;; gigatons
Srcch4 := 0 ;; gigatons ;; ch4 source
Srcn2o := 0 ;; gigatons ;; n2o source
'''

ocean = '''
;; Ocean Calculations ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
ocean := 1..layers * 0
ocean_+ = ocean + dTemp * dt

Cheat := layerdepth * 4.2*1000^2 ;; K m^2/J ;; Heat Capacity

dTempocean = (diff2 ocean) * k / layerdepth^2
dTemp = dTempocean + dTempsurfacerf * surface
dTempsurfacerf = (Frel - Tempsurface * lambda)/Cheat
Tempsurface = ocean . surface

intestart = (tempsurface if Tempsurface >= 2 else 0)

Tempinte := 0.1
Tempinte_+ = Tempinte + intestart

Tempmax := 0
Tempmax_+ = Tempmax if Tempmax > Tempsurface else Tempsurface

Frel = Fco2rel + Fch4rel + Fn2orel

Frelinte := 0
Frelinte_+ = Frelinte + Frel

Frelmax := 0
Frelmax_+ = Frelmax if Frelmax > Frel else Frel

'''

co2concentrationrcp = '''
Mco2a := 0 ;; gigatons above current levels
Mco2a_+ = Mco2a + dMco2a * dtyears
dMco2a = Srcco2 - dMa-oco2

tc := 1/50 ;; time constant for ocean uptake
dMa-oco2 = (Pco2a - Pco2o)*tc

Ra = 0.458 ;; atmosphere reservoir
Pco2a = Mco2a/Ra

;; ocean co2 content
Ro = 0.542 ;; ocean reservoir
Mco2o := 0
Mco2o_+ = Mco2o + (dMa-oco2 - Dco2) * dtyears
Pco2o = Mco2o/Ro
;; deep ocean sequestration
Dco2 = 0.005 * (Mco2o if Mco2o > 0 else 0)
'''

co2concentrationmethaneadd = '''
Mco2a := 0 ;; gigatons above current levels
Mco2a_+ = Mco2a + (dMco2a + dMco2-ch4)*dtyears
dMco2-ch4 = (Sinkch4 - Srcch4)*molco2/molch4
dMco2a = Srcco2 - dMa-oco2

tc := 1/50 ;; time constant for ocean uptake
dMa-oco2 = (Pco2a - Pco2o)*tc

Ra = 0.458 ;; atmosphere reservoir
Pco2a = Mco2a/Ra

;; ocean co2 content
Ro = 0.542 ;; ocean reservoir
Mco2o := 0
Mco2o_+ = Mco2o + (dMa-oco2 - Dco2) * dtyears
Pco2o = Mco2o/Ro
;; deep ocean sequestration
Dco2 = 0.005 * (Mco2o if Mco2o > 0 else 0)
'''

ch4concentration = '''
Mch4 := 0 ;; gigatons above current levels
dMch4 = Srcch4 - Sinkch4
Mch4_+ = Mch4 + dMch4 * dtyears
Sinkch4 = Mch4/12.5 ;; gigatons ;; ch4 sink
'''

n2oconcentration = '''
Mn2o := 0 ;; gigatons above current levels
dMn2o = Srcn2o - Sinkn2o
Mn2o_+ = Mn2o + dMn2o * dtyears
Sinkn2o = Mn2o/114.1 ;; n2o sink
'''

co2radiativeforcing = ''';; co2 Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cco2abs = Cco2 + Mco2a * MtoCco2
Gcurrent = ln (1 + 1.2*Cco2abs + 0.005*Cco2abs^2 + 1.4e-6*Cco2abs^3)
Fco2rel = 3.35(Gcurrent - Gbase)
'''

ch4radiativeforcing = ''';; ch4 Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cch4abs = Cch4 + Mch4 * MtoCch4
Fn2o0ch4 = 0.47*ln (1 + 2.01e-5*(Cch4abs * Cn2o)^0.75 + 5.31e-15*Cch4abs*(Cch4abs * Cn2o)^1.52)
Fch4rel = 0.036(Cch4abs^0.5 - Cch4^0.5) - Fn2o0ch4 + Fn2o0ch40
'''

n2oradiativeforcing = ''';; n2o Radiative Forcing ;; Formulas from: Myhrvold and Caldeira (2012) Supporting Information
Cn2oabs = Cn2o + Mn2o * MtoCn2o
Fn2och40 = 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2oabs)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2oabs)^1.52)
Fn2orel = 0.12(Cn2oabs^0.5 - Cn2o^0.5) - Fn2och40 + Fn2o0ch40
'''

runsim = '''
trace Cch4abs
trace Cco2abs
trace Cn2oabs
trace Cch4
trace Cco2
trace Cn2o
trace Mch4
trace Mco2a
trace Mn2o
trace Srcco2
trace Srcch4
trace Srcn2o
trace Tempsurface
trace Tempmax
trace Tempinte
trace Fco2rel
trace Fch4rel
trace Fn2orel
trace Frel
trace Frelinte
trace Frelmax
trace tyears
'''


concentration1750 = '''
;; Starting Concentrations ;; Values from: Recent Greenhouse Gas Concentrations, DOI: 10.3334/CDIAC/atg.032
Cco2 := 280 ;; ppmv
Cch4 := 722 ;; ppbv
Cn2o := 270 ;; ppbv

;; Formula from: Myhrvold and Caldeira (2012) Supporting Information
Gbase := ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 := 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)
'''

concentration2000 = '''
;; Starting Concentrations ;; Values from: Recent Greenhouse Gas Concentrations, DOI: 10.3334/CDIAC/atg.032
Cco2 := 368.865 ;; ppmv
Cch4 := 1751.0225 ;; ppbv
Cn2o := 315.85 ;; ppbv

;; Formula from: Myhrvold and Caldeira (2012) Supporting Information
Gbase := ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 := 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)
'''

concentration2017 = '''
;; Starting Concentrations ;; Values from: Recent Greenhouse Gas Concentrations, DOI: 10.3334/CDIAC/atg.032
Cco2 := 405.25182 ;; ppmv
Cch4 := 1767.1513 ;; ppbv
Cn2o := 327.49559 ;; ppbv

;; Formula from: Myhrvold and Caldeira (2012) Supporting Information
Gbase := ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 := 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)
'''

oceanbase = '''ocean := [0.24595278, 0.24661186, 0.24793011, 0.2499077, 0.25254492, 0.2558421, 0.25979966, 0.26441808, 0.2696979, 0.27563967, 0.28224398, 0.28951141, 0.29744255, 0.30603792, 0.315298, 0.32522318, 0.33581377, 0.34706991, 0.35899161, 0.37157869, 0.38483075, 0.39874717, 0.41332704, 0.42856916, 0.44447201, 0.46103371, 0.47825198, 0.49612417, 0.51464714, 0.53381733, 0.55363065, 0.57408251, 0.59516777, 0.61688075, 0.63921515, 0.66216408, 0.68572004, 0.70987486, 0.73461973, 0.75994519, 0.78584107, 0.81229654, 0.83930006, 0.8668394, 0.89490165, 0.92347316, 0.95253964, 0.98208607, 1.01209677, 1.04255539, 1.07344491, 1.10474769, 1.13644545, 1.16851931, 1.20094981, 1.23371694, 1.26680015, 1.30017839, 1.33383014, 1.36773344]'''

simulationcurrent = constants + srcdefualt + concentration2017 + oceandefault + ch4concentration + co2concentrationmethaneadd + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + runsim
simbase1750rcp = constants + concentration1750 + oceandefault + ch4concentration + co2concentrationrcp + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + runsim
simbase2000rcp = constants + concentration2000 + oceandefault + ch4concentration + co2concentrationrcp + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + runsim
simbase2000rcp1 = '''index := 0.0;
dt := 259200.0;
t := 0.0;
ma := 5100000.0;
mola := 28.97;
molco2 := 44.009;
mtocco2 := 0.12907342036544217;
molch4 := 16.043;
mtocch4 := 354.07293878094777;
moln2o := 46.005;
mtocn2o := 123.47336500082045;
cco2 := 368.865;
cch4 := 1751.0225;
cn2o := 315.85;
gbase := 7.0852389342126525;
fn2o0ch40 := 0.16235993795083287;
layers := 60.0;
layerdepth := 33.333333333333336;
k := 0.0001;
lambda := 1.25;
surface := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0];
mch4 := 0.0;
mco2a := 0.0;
tc := 0.02;
mco2o := 0.0;
mn2o := 0.0;
ocean := [1.409793017051717, 1.4099475679842974, 1.4102565907558426, 1.4107199272195947, 1.4113373402565905, 1.4121085138970046, 1.4130330534818509, 1.4141104858649494, 1.4153402596550626, 1.4167217454980745, 1.4182542363990616, 1.419936948084106, 1.4217690194016499, 1.4237495127631936, 1.4258774146231152, 1.4281516359973578, 1.4305710130207219, 1.4331343075424841, 1.4358402077600261, 1.4386873288901634, 1.4416742138778127, 1.4447993341416538, 1.4480610903563924, 1.4514578132712275, 1.4549877645641034, 1.4586491377313118, 1.462440059011985, 1.4663585883470107, 1.4704027203718755, 1.4745703854429273, 1.4788594506965385, 1.4832677211406196, 1.4877929407779289, 1.492432793760605, 1.4971849055753257, 1.5020468442584942, 1.5070161216408238, 1.5120901946206895, 1.5172664664655906, 1.5225422881410613, 1.5279149596663488, 1.5333817314961655, 1.5389398059278045, 1.5445863385329042, 1.5503184396131233, 1.5561331756789856, 1.5620275709511389, 1.5679986088832516, 1.5740432337057781, 1.5801583519897966, 1.58634083423012, 1.5925875164468684, 1.5988952018046894, 1.6052606622487926, 1.6116806401569572, 1.6181518500066767, 1.6246709800565819, 1.6312346940412816, 1.6378396328787548, 1.6444824163894196];
cheat := 140000000.00000003;
tempinte := 0;
tempmax := 0;
frelinte := 0;
frelmax := 0;
frelrcp := 2.139736101307685;
srcco2 := 0.0;
srcch4 := 0.0;
srcn2o := 0.0;
dtyears = dt / (365.0 * 24.0 * 60.0 * 60.0);
tyears = t / (365.0 * 24.0 * 60.0 * 60.0);
dmch4 = srcch4 - sinkch4;
sinkch4 = mch4 / 12.5;
dmco2a = srcco2 - dma-oco2;
dma-oco2 = (pco2a - pco2o) * tc;
ra = 0.458;
pco2a = mco2a / ra;
ro = 0.542;
pco2o = mco2o / ro;
dco2 = 0.005 * (mco2o if mco2o > 0.0 else 0.0);
cco2abs = cco2 + mco2a * mtocco2;
gcurrent = ln (1.0 + 1.2 * cco2abs + 0.005 * cco2abs^2.0 + 1.4e-06 * cco2abs^3.0);
fco2rel = 3.35(gcurrent - gbase);
cch4abs = cch4 + mch4 * mtocch4;
fn2o0ch4 = 0.47 * ln (1.0 + 2.01e-05 * (cch4abs * cn2o)^0.75 + 5.31e-15 * cch4abs * (cch4abs * cn2o)^1.52);
fch4rel = 0.036(cch4abs^0.5 - cch4^0.5) - fn2o0ch4 + fn2o0ch40;
dmn2o = srcn2o - sinkn2o;
sinkn2o = mn2o / 114.1;
cn2oabs = cn2o + mn2o * mtocn2o;
fn2och40 = 0.47 * ln (1.0 + 2.01e-05 * (cch4 * cn2oabs)^0.75 + 5.31e-15 * cch4 * (cch4 * cn2oabs)^1.52);
fn2orel = 0.12(cn2oabs^0.5 - cn2o^0.5) - fn2och40 + fn2o0ch40;
dtempocean = diff2 ocean * k / layerdepth^2.0;
dtemp = dtempocean + dtempsurfacerf * surface;
dtempsurfacerf = (frel - tempsurface * lambda) / cheat;
tempsurface = ocean . surface;
frel = fco2rel + fch4rel + fn2orel + frelrcp;
t_+ = dt + t;
mch4_+ = mch4 + dmch4 * dtyears;
mco2a_+ = mco2a + dmco2a * dtyears;
mco2o_+ = mco2o + (dma-oco2 - dco2) * dtyears;
mn2o_+ = mn2o + dmn2o * dtyears;
ocean_+ = ocean + dtemp * dt;
tempinte_+ = tempinte + tempsurface;
tempmax_+ = tempmax if tempmax > tempsurface else tempsurface;
frelinte_+ = frelinte + frel;
frelmax_+ = frelmax if frelmax > frel else frel;
trace cch4abs;
trace cco2abs;
trace cn2oabs;
trace cch4;
trace cco2;
trace cn2o;
trace mch4;
trace mco2a;
trace mn2o;
trace srcco2;
trace srcch4;
trace srcn2o;
trace tempsurface;
trace tempmax;
trace tempinte;
trace fco2rel;
trace fch4rel;
trace fn2orel;
trace frel;
trace frelinte;
trace frelmax;
trace tyears;
'''

def spikecalc(base, time):

    ch4 = lambda time: '''
    Srcco2 := 0 ;; gigatons ;; co2 source
    Srcch4 = 1 if tyears < '''+ str(time) +''' else 0 ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    simulation1ch4 = base + ch4(time)
    env2 = zs.Env()
    zs.compilerun(simulation1ch4, env2)
    zs.compilerun('next ' + str(round(100 / env2['dtyears', 'cur'])), env2)

    co2 = lambda co2, time: '''
    Srcco2 = ''' + str(co2) + ''' if tyears < '''+ str(time) +''' else 0;; gigatons ;; co2 source
    Srcch4 := 0  ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    maxtemp = env2['tempmax', 'cur']
    print(maxtemp, 'ch4')

    # spike = 1
    # spikes = []
    # temps = []
    # for i in range(10):
    #     simulation1co2 = base + scrco2(spike, time)
    #     env1 = zs.Env()
    #     zs.compilerun(simulation1co2, env1)
    #     zs.compilerun('next ' + str(round(100/env1['dtyears', 'cur'])), env1)
    #     maxtempco2 = env1['tempmax', 'cur']
    #     spikes.append(spike)
    #     temps.append(maxtempco2)
    #     print('test', i, maxtempco2, 'co2', spike)
    #     percent = (maxtemp-maxtempco2)/maxtemp
    #     if abs(percent) < 0.02:
    #         break
    #     spike = spike * (1 + percent)

    low = 0
    lowtemp = 0
    high = 1000
    hightemp = None

    env1 = zs.Env(repl=True)
    zs.compilerun(base, env1)
    zs.compilerun(co2(high, time), env1)
    zs.compilerun('next ' + str(round(100 / env1['dtyears', 'cur'])), env1)

    hightemp = env1['tempmax', 'cur']
    spike = 1

    for x in range(10):
        env1 = zs.Env(repl=True)
        zs.compilerun(base, env1)
        zs.compilerun(co2(spike, time), env1)
        ordata = zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)[-1]
        data = {idx: [ordata[idx][0]] for idx in ordata.keys()}
        for idx in ordata.keys():
            data[idx].append(ordata[idx][-1])
        for i in range(1, 100):
            yeardata = zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)[-1]
            [data[idx].append(yeardata[idx][-1]) for idx in data.keys()]
        maxtempco2 = env1['tempmax', 'cur']
        print('test', x, maxtempco2, 'co2', spike)
        percent = (maxtemp - maxtempco2) / maxtemp
        if abs(percent) < 0.01:
            break
        if percent > 0:
            low = spike
            lowtemp = maxtempco2
        else:
            high = spike
            hightemp = maxtempco2
        gradient = (hightemp - lowtemp) / (high - low)
        spike = low + (maxtemp - lowtemp) / gradient



def spikecalcrpc100(base, time, spike, rpcdata, startyear, dataset):
    rf = {idx: {r: str(float(rpcdata[idx][r]) - float(rpcdata[startyear][r])) for r in rpcdata[idx].keys()} for idx in rpcdata.keys()}

    ch4 = lambda time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''
    Srcco2 := 0
    Srcch4 = (''' + str(spike) + ''' if tyears < ''' + str(time) + ''' else 0) ;; gigatons ;; ch4 source
    Srcn2o := 0
    '''

    simulation1ch4 = base
    env2 = zs.Env(repl=True)
    zs.compilerun(simulation1ch4, env2)
    zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env2)
    zs.compilerun(ch4(time, startyear), env2)
    data = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
    datach4 = {idx: [data[idx][0]] for idx in data.keys()}
    for idx in data.keys():
        datach4[idx].append(data[idx][-1])
    for i in range(1, 101):
        zs.compilerun(ch4(time, startyear + i), env2)
        yeardata = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
        [datach4[idx].append(yeardata[idx][-1]) for idx in datach4.keys()]

    co2 = lambda co2, time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''

    Srcco2 = ''' + str(co2) + ''' if tyears < '''+ str(time) +''' else 0;; gigatons ;; co2 source
    Srcch4 := 0  ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    maxtemp = env2['tempmax', 'cur']
    print(maxtemp, 'ch4')

    spikes = []
    for x in range(10):
        simulation1co2 = base
        env1 = zs.Env(repl=True)
        zs.compilerun(simulation1co2, env1)
        zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env1)
        zs.compilerun(co2(spike, time, startyear), env1)
        ordata = zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)[-1]
        data = {idx: [ordata[idx][0]] for idx in ordata.keys()}
        for idx in ordata.keys():
            data[idx].append(ordata[idx][-1])
        for i in range(1,101):
            zs.compilerun(co2(spike, time, startyear + i), env1)
            yeardata = zs.compilerun('next ' + str(round(1/env1['dtyears', 'cur'])), env1)[-1]
            [data[idx].append(yeardata[idx][-1]) for idx in data.keys()]
        maxtempco2 = env1['tempmax', 'cur']
        spikes.append(data)
        print('test', x, maxtempco2, 'co2', spike)
        percent = (maxtemp - maxtempco2)/maxtemp
        if abs(percent) < 0.01:
            break
        spike = spike * (1 + max(-0.9, percent*2, percent*5))

    temp = Figure(title='Temperature ' + dataset + ' spike duration:' + str(time) + ' CH4 spike amount:' + str(spike))
    concentration = Figure(title='Mass of Gasses (Gigatons) ' + dataset + ' spike duration:' + str(time) + ' CH4 spike amount:' + str(spike))
    temp.line('tyears', 'tempsurface', source=datach4, color='black')
    concentration.line('tyears', 'mch4', source=datach4, color='black')
    colors = ['blue', 'purple', 'pink', 'brown', 'yellow', 'green', 'red', 'cyan', 'orange', 'grey']
    for data, color in zip(spikes, colors):
        temp.line('tyears', 'tempsurface', source=data, color=color)
        concentration.line('tyears', 'mco2a', source=data, color=color)

    curdoc().add_root(temp)
    curdoc().add_root(concentration)


def spikecalcrpcmax(base, time, spike, rpcrfdata, startyear, dataset, years):
    rf = rpcrfdata#{idx: {r: str(float(rpcrfdata[idx][r]) - float(rpcrfdata[startyear][r])) for r in rpcrfdata[idx].keys()} for idx in rpcrfdata.keys()}

    simulation = base + '; Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp'

    rcp = lambda year: '''
    Frelrcp := ''' + rf[year]['totalhuman']

    env = zs.Env(repl=True)
    zs.compilerun(simulation, env)
    zs.compilerun('''Srcco2 := 0
    Srcch4 := 0 ;; gigatons ;; ch4 source
    Srcn2o := 0''', env)
    zs.compilerun(rcp(startyear), env)
    data = zs.compilerun('next ' + str(round(1 / env['dtyears', 'cur'])), env)[-1]
    datarcp = {idx: [data[idx][0]] for idx in data.keys()}
    for idx in data.keys():
        datarcp[idx].append(data[idx][-1])
    for i in range(1, years):
        zs.compilerun(rcp(startyear + i), env)
        yeardata = zs.compilerun('next ' + str(round(1 / env['dtyears', 'cur'])), env)[-1]
        [datarcp[idx].append(yeardata[idx][-1]) for idx in datarcp.keys()]

    datarcp['tyears'] = [year + startyear for year in datarcp['tyears']]

    rcpmaxtemp = env['tempmax', 'cur']
    print(rcpmaxtemp, 'rcp')


    ch4 = lambda time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''
    Srcco2 := 0
    Srcch4 = (''' + str(spike) + ''' if tyears < ''' + str(time) + ''' else 0) ;; gigatons ;; ch4 source
    Srcn2o := 0
    '''

    env2 = zs.Env(repl=True)
    zs.compilerun(simulation, env2)
    zs.compilerun(ch4(time, startyear), env2)
    data = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
    datach4 = {idx: [data[idx][0]] for idx in data.keys()}
    for idx in data.keys():
        datach4[idx].append(data[idx][-1])
    for i in range(1, years):
        zs.compilerun(ch4(time, startyear + i), env2)
        yeardata = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
        [datach4[idx].append(yeardata[idx][-1]) for idx in datach4.keys()]

    datach4['tyears'] = [year + startyear for year in datach4['tyears']]

    co2 = lambda co2, time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''

    Srcco2 = ''' + str(co2) + ''' if tyears < '''+ str(time) +''' else 0;; gigatons ;; co2 source
    Srcch4 := 0  ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    maxtemp = env2['tempmax', 'cur'] - rcpmaxtemp
    print(maxtemp, 'ch4')
    low = 0
    lowtemp = 0
    high = 1000
    hightemp = None

    env1 = zs.Env(repl=True)
    zs.compilerun(simulation, env1)
    zs.compilerun(co2(high, time, startyear), env1)
    zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)
    for i in range(1, years):
        zs.compilerun(co2(high, time, startyear + i), env1)
        zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)

    hightemp = env1['tempmax', 'cur'] - rcpmaxtemp

    for x in range(10):
        env1 = zs.Env(repl=True)
        zs.compilerun(simulation, env1)
        zs.compilerun(co2(spike, time, startyear), env1)
        ordata = zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)[-1]
        data = {idx: [ordata[idx][0]] for idx in ordata.keys()}
        for idx in ordata.keys():
            data[idx].append(ordata[idx][-1])
        for i in range(1, years):
            zs.compilerun(co2(spike, time, startyear + i), env1)
            yeardata = zs.compilerun('next ' + str(round(1/env1['dtyears', 'cur'])), env1)[-1]
            [data[idx].append(yeardata[idx][-1]) for idx in data.keys()]
        maxtempco2 = env1['tempmax', 'cur'] - rcpmaxtemp
        print('test', x, maxtempco2, 'co2', spike)
        percent = (maxtemp - maxtempco2)/maxtemp
        if abs(percent) < 0.01:
            break
        if percent > 0:
            low = spike
            lowtemp = maxtempco2
        else:
            high = spike
            hightemp = maxtempco2
        gradient = (hightemp-lowtemp)/(high-low)
        spike = low + (maxtemp-lowtemp)/gradient

    data['tyears'] = [year + startyear for year in data['tyears']]

    temp = Figure(title='Temperature Reletive to Baseline' + dataset + ' spike duration:' + str(time) + ' CO2 spike amount:' + str(spike) + ' Spike calculated by Max Temperature')
    # concentration = Figure(title='Mass of Gasses (Gigatons) ' + dataset + ' spike duration:' + str(time) + ' CO2 spike amount:' + str(spike) + ' Spike calculated by Max Temperature', legend_location='bottom_right')
    temp.line('tyears', 'tempsurface', source=datach4, color='black', line_dash='dashed', legend='Methane Temp')
    temp.line('tyears', 'tempsurface', source=datarcp, color='black', line_dash='solid', legend=dataset + ' Temp')
    temp.line('tyears', 'tempsurface', source=data, color='black', line_dash='dotted', legend='Carbon Dioxide Temp')

    temp.legend.location = "bottom_right"
    # concentration.line('tyears', 'mch4', source=datach4, color='black', line_dash='dashed', legend='Gtons of Methane')
    # concentration.line('tyears', 'mco2a', source=data, color='black', line_dash='dotted', legend='Gtons of Carbon Dioxide')

    curdoc().add_root(temp)
    # curdoc().add_root(concentration)
    return spike


def spikecalcrpcinte(base, time, spike, rpcrfdata, startyear, dataset, years):
    rf = rpcrfdata#{idx: {r: str(float(rpcrfdata[idx][r]) - float(rpcrfdata[startyear][r])) for r in rpcrfdata[idx].keys()} for idx in rpcrfdata.keys()}

    simulation = base + '; Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp'

    rcp = lambda year: '''
    Frelrcp := ''' + rf[year]['totalhuman']

    env = zs.Env(repl=True)
    zs.compilerun(simulation, env)
    zs.compilerun('''Srcco2 := 0
        Srcch4 := 0 ;; gigatons ;; ch4 source
        Srcn2o := 0''', env)
    zs.compilerun(rcp(startyear), env)
    data = zs.compilerun('next ' + str(round(1 / env['dtyears', 'cur'])), env)[-1]
    datarcp = {idx: [data[idx][0]] for idx in data.keys()}
    for idx in data.keys():
        datarcp[idx].append(data[idx][-1])
    for i in range(1, years):
        zs.compilerun(rcp(startyear + i), env)
        yeardata = zs.compilerun('next ' + str(round(1 / env['dtyears', 'cur'])), env)[-1]
        [datarcp[idx].append(yeardata[idx][-1]) for idx in datarcp.keys()]

    datarcp['tyears'] = [year + startyear for year in datarcp['tyears']]

    rcpintetemp = env['tempinte', 'cur']
    print(rcpintetemp, 'rcp')


    ch4 = lambda time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''
    Srcco2 := 0
    Srcch4 = (''' + str(spike) + ''' if tyears < ''' + str(time) + ''' else 0) ;; gigatons ;; ch4 source
    Srcn2o := 0
    '''

    env2 = zs.Env(repl=True)
    zs.compilerun(simulation, env2)
    zs.compilerun(ch4(time, startyear), env2)
    data = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
    datach4 = {idx: [data[idx][0]] for idx in data.keys()}
    for idx in data.keys():
        datach4[idx].append(data[idx][-1])
    for i in range(1, years):
        zs.compilerun(ch4(time, startyear + i), env2)
        yeardata = zs.compilerun('next ' + str(round(1 / env2['dtyears', 'cur'])), env2)[-1]
        [datach4[idx].append(yeardata[idx][-1]) for idx in datach4.keys()]

    datach4['tyears'] = [year + startyear for year in datach4['tyears']]

    co2 = lambda co2, time, year: '''
    Frelrcp := ''' + rf[year]['totalhuman'] + '''

    Srcco2 = ''' + str(co2) + ''' if tyears < '''+ str(time) +''' else 0;; gigatons ;; co2 source
    Srcch4 := 0  ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    intetemp = env2['tempinte', 'cur'] - rcpintetemp
    print(intetemp, 'ch4')
    low = 0
    lowtemp = 0
    high = 1000
    hightemp = None

    env1 = zs.Env(repl=True)
    zs.compilerun(simulation, env1)
    zs.compilerun(co2(high, time, startyear), env1)
    zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)
    for i in range(1, years):
        zs.compilerun(co2(high, time, startyear + i), env1)
        zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)

    hightemp = env1['tempinte', 'cur'] - rcpintetemp

    for x in range(10):
        env1 = zs.Env(repl=True)
        zs.compilerun(simulation, env1)
        zs.compilerun(co2(spike, time, startyear), env1)
        ordata = zs.compilerun('next ' + str(round(1 / env1['dtyears', 'cur'])), env1)[-1]
        data = {idx: [ordata[idx][0]] for idx in ordata.keys()}
        for idx in ordata.keys():
            data[idx].append(ordata[idx][-1])
        for i in range(1, years):
            zs.compilerun(co2(spike, time, startyear + i), env1)
            yeardata = zs.compilerun('next ' + str(round(1/env1['dtyears', 'cur'])), env1)[-1]
            [data[idx].append(yeardata[idx][-1]) for idx in data.keys()]
        intetempco2 = env1['tempinte', 'cur'] - rcpintetemp
        print('test', x, intetempco2, 'co2', spike)
        percent = intetemp - intetempco2
        if abs(percent) < 0.01:
            break
        if percent > 0:
            low = spike
            lowtemp = intetempco2
        else:
            high = spike
            hightemp = intetempco2
        gradient = (hightemp-lowtemp)/(high-low)
        spike = low + (intetemp-lowtemp)/gradient

    data['tyears'] = [year + startyear for year in data['tyears']]

    temp = Figure(title='Temperature Reletive to Baseline' + dataset + ' spike duration:' + str(
        time) + ' CO2 spike amount:' + str(spike) + ' Spike calculated by Integrated Temperature')
    # concentration = Figure(
    #     title='Mass of Gasses (Gigatons) ' + dataset + ' spike duration:' + str(time) + ' CO2 spike amount:' + str(
    #         spike) + ' Spike calculated by Integrated Temperature')
    temp.line('tyears', 'tempsurface', source=datach4, color='black', line_dash='dashed', legend='Methane Temp')
    temp.line('tyears', 'tempsurface', source=datarcp, color='black', line_dash='solid', legend=dataset + ' Temp')
    temp.line('tyears', 'tempsurface', source=data, color='black', line_dash='dotted',
              legend='Carbon Dioxide Temp')

    # concentration.line('tyears', 'mch4', source=datach4, color='black', line_dash='dashed',
    #                    legend='Gtons of Methane')
    # concentration.line('tyears', 'mco2a', source=data, color='black', line_dash='dotted',
    #                         legend='Gtons of Carbon Dioxide')
    temp.legend.location = "bottom_right"
    curdoc().add_root(temp)
    # curdoc().add_root(concentration)
    return spike

# env = zs.Env(repl=True)
# zs.compilerun(simbase2000rcp1, env)
#
# zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env)
#
#
#
# row = rcp3data[0]
#
# env2 = zs.Env(repl=True)
# zs.compilerun(simbase1750rcp, env2)
# zs.compilerun('''
# Cco2abs := 368.865 ;; ppmv
# Cch4abs := 1751.0225 ;; ppbv
# Cn2oabs := 315.85 ;; ppbv''', env2)
#
# print(env['dtyears', 'cur'])
#
# env['frelrcp', 'val'] = Number(env2['frel', 'cur'])
# print(env['tyears', 'cur'])
# env['srcco2', 'val'] = Number(0.0)#Number(float(row['fossilco2 (gt/y)']) + float(row['otherco2 (gt/y)']))
# env['srcch4', 'val'] = Number(0.0)#Number(float(row['ch4 (mt/y)']) / 1e3)
# env['srcn2o', 'val'] = Number(0.0)#Number(float(row['n2o (mt/y)']) / 1e3)
# def updatercpemmisions(row, env):
#     # env['srcco2', 'val'] = Number(float(row['fossilco2 (gt/y)']) + float(row['otherco2 (gt/y)']))
#     # env['srcch4', 'val'] = Number(float(row['ch4 (mt/y)']) / 1e3)
#     # env['srcn2o', 'val'] = Number(float(row['n2o (mt/y)']) / 1e3)
#     pass
#
# updatercpemmisions(row, env)
#
# year = round(1/env['dtyears', 'cur'])
# year = 'next ' + str(year)
# data = zs.compilerun(year, env)[-1]
# for row in rcp3data[1:]:
#     updatercpemmisions(row, env)
#     yeardata = zs.compilerun(year, env)[-1]
#     data = {idx: data[idx] + yeardata[idx] for idx in data.keys()}
#
# base = repr(env)
# print(base)

def test(rcprf, rcpco, rcpid, spike, spikeduration, startyear):
    base = constants + srcdefualt + oceandefault + ch4concentration + co2concentrationmethaneadd + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + oceanbase + runsim

    costmax = []
    costinte = []
    env = zs.Env(repl=True)
    zs.compilerun(base, env)
    zs.compilerun(concentrationdefualt, env)
    zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env)
    zs.compilerun('Frelrcp := ' + rcprf[startyear]['totalhuman'], env)
    year = startyear - 2000
    if year > 0:
        zs.compilerun('next ' + str(round(year/env['dtyears', 'cur'])), env)

    oceannex = Unknown(env['ocean', 'cur'])
    oceannex = '\nocean := ' + repr(oceannex)
    base += oceannex
    nxt = 'next ' + str(round(5/env['dtyears', 'cur']))
    year = []
    costmax.append(spikecalcrpcmax(base, spikeduration, spike, rcprf, rcpco, startyear, rcpid, 100) / spike)
    costinte.append(spikecalcrpcinte(base, spikeduration, spike, rcprf, rcpco, startyear, rcpid, 20) / spike)
    year.append(startyear)
    for i in range(5, 2081 - startyear, 5):
        zs.compilerun('Frelrcp := ' + rcprf[startyear + i]['totalhuman'], env)
        zs.compilerun(nxt, env)
        oceannex = Unknown(env['ocean', 'cur'])
        oceannex = '\nocean := ' + repr(oceannex)
        base += oceannex
        costmax.append(spikecalcrpcmax(base, spikeduration, spike, rcprf, rcpco, startyear + i, rcpid, 100)/spike)
        costinte.append(spikecalcrpcinte(base, spikeduration, spike, rcprf, rcpco, startyear + i, rcpid, 20)/spike)
        year.append(startyear + i)




    fig = Figure(title='Methane Cost, 100 years, Measured by Max Temperature, ' + rcpid, x_axis_label='Spike Start Year', y_axis_label='CO2 Equivalent')
    fig.line('x', 'y', source=dict(x=year, y=costmax), color='black')
    curdoc().add_root(fig)

    fig = Figure(title='Methane Cost, 20 years, Measured by Integrated Temperature, ' + rcpid, x_axis_label='Spike Start Year', y_axis_label='CO2 Equivalent')
    fig.line('x', 'y', source=dict(x=year, y=costinte), color='black')
    curdoc().add_root(fig)

    return costmax, costinte, year


# env = zs.Env(repl=True)
# zs.compilerun(simbase2000rcp, env)
# zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env)
# zs.compilerun(srcdefualt, env)
# zs.compilerun('Frelrcp := 2.139736101307685', env)
# zs.compilerun('ocean := 1..layers * 0', env)
# zs.compilerun('next ' + str(round(250/env['dtyears', 'cur'])), env)
# print(env['ocean', 'cur'])

methanespike = 1  # 29244.16 / 34e6  # gt NZ cows methane emissions in Gtons
time = 1  # years

base = constants + concentration2017 + '''
Gbase = ln (1 + 1.2*Cco2 + 0.005*Cco2^2 + 1.4e-6*Cco2^3)
Fn2o0ch40 = 0.47*ln (1 + 2.01e-5*(Cch4 * Cn2o)^0.75 + 5.31e-15*Cch4*(Cch4 * Cn2o)^1.52)
''' + srcdefualt + oceandefault + ch4concentration + co2concentrationmethaneadd + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + oceanbase + runsim

# spikecalc(simulationcurrent, 2)

# costmax = []
# costinte = []
env = zs.Env(repl=True)
zs.compilerun(base, env)
zs.compilerun(concentrationdefualt, env)
zs.compilerun('Frel = Fco2rel + Fch4rel + Fn2orel + Frelrcp', env)
zs.compilerun('Frelrcp := ' + rcp45rfdata[2015]['totalhuman'], env)
year = 2015 - 2000
if year > 0:
    zs.compilerun('next ' + str(round(year/env['dtyears', 'cur'])), env)

oceannex = Unknown(env['ocean', 'cur'])
oceannex = '\nocean := ' + repr(oceannex)
base += oceannex
#
# spikecalcrpcinte(base, 2, 1, rcp45rfdata, rcp45codata, 2015, 'rcp4.5', 100)
spikecalcrpcmax(base, 2, 1, rcp45rfdata, 2015, 'rcp4.5', 100)
#
# spikecalcrpcinte(base, 2, 1, rcp3rfdata, rcp45codata, 2015, 'rcp3', 100)
spikecalcrpcmax(base, 2, 1, rcp3rfdata, 2015, 'rcp3', 100)

# costmax, costinte, year = test(rcp3rfdata, rcp3codata, 'rcp3', 1, 2, 2015)
# print(costmax)
# print(costinte)
# print(year)

# costmax, costinte, year = test(rcp45rfdata, rcp45codata, 'rcp4.5', 1, 2, 2015)
# print(costmax)
# print(costinte)
# print(year)
#
# costmax, costinte, year = test(rcp6rfdata, rcp6codata, 'rpc6', 1, 2, 2015)
# print(costmax)
# print(costinte)
# print(year)