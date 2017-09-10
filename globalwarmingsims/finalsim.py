import zscript as zs
from zgraph import *

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
ocean_+ = ocean + dTemp

Cheat := layerdepth * 4.2*1000^2 ;; K m^2/J ;; Heat Capacity

dTempocean = (diff2 ocean) * k * dt / layerdepth^2
dTemp = dTempocean + dTempsurfacerf * surface
dTempsurfacerf = dt*(Frel - Tempsurface * lambda)/Cheat
Tempsurface = ocean . surface

Tempinte := 0
Tempinte_+ = Tempinte + Tempsurface

Tempmax := 0
Tempmax_+ = Tempmax if Tempmax > Tempsurface else Tempsurface

Frel = Fco2rel + Fch4rel + Fn2orel

Frelinte := 0
Frelinte_+ = Frelinte + Frel

Frelmax := 0
Frelmax_+ = Frelmax if Frelmax > Frel else Frel

'''

co2concentration = '''
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
Sinkch4 = Mch4/12 ;; gigatons ;; ch4 sink
'''

n2oconcentration = '''
Mn2o := 0 ;; gigatons above current levels
dMn2o = Srcn2o - Sinkn2o
Mn2o_+ = Mn2o + dMn2o * dtyears
Sinkn2o = Mn2o/114 ;; n2o sink
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

simulation = constants + srcdefualt + concentration1750 + oceandefault + ch4concentration + co2concentration + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + runsim

if __name__ == '__main__':
    simbase1750 = constants + concentration1750 + oceandefault + ch4concentration + co2concentration + co2radiativeforcing + ch4radiativeforcing + n2oconcentration + n2oradiativeforcing + ocean + runsim

    time = 20

    srcch4 = lambda time: '''
    Srcco2 := 0 ;; gigatons ;; co2 source
    Srcch4 = 1 if tyears < '''+ str(time) +''' else 0 ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    simulation1ch4 = srcch4(time) + simbase1750
    env2 = zs.Env()
    zs.compilerun(simulation1ch4, env2)
    zs.compilerun('next ' + str(round(100 / env2['dtyears', 'cur'])), env2)

    scrco2 = lambda co2, time: '''
    Srcco2 = ''' + str(co2) + ''' if tyears < '''+ str(time) +''' else 0;; gigatons ;; co2 source
    Srcch4 := 0  ;; gigatons ;; ch4 source
    Srcn2o := 0 ;; gigatons ;; n2o source
    '''

    maxtemp = env2['tempmax', 'cur']
    print(maxtemp, 'ch4')

    spike = 1
    spikes = []
    temps = []
    for i in range(10):
        simulation1co2 = scrco2(spike, time) + simbase1750
        env1 = zs.Env()
        zs.compilerun(simulation1co2, env1)
        zs.compilerun('next ' + str(round(100/env1['dtyears', 'cur'])), env1)
        maxtempco2 = env1['tempmax', 'cur']
        spikes.append(spike)
        temps.append(maxtempco2)
        print('test', i, maxtempco2, 'co2', spike)
        percent = (maxtemp-maxtempco2)/maxtemp
        if abs(percent) < 0.02:
            break
        spike = spike * (1 + percent)

    print(spikes)
    print(temps)


    # row = rcp3data[0]
    # time = 't := ' + str(row['year']) + '/dtyears;'
    # src = '''
    # Srcco2 := ''' + str(row['fossilco2 (gt/y)'] + row['otherco2 (gt/y)']) + ''' * dtyears
    # Srcch4 := ''' + str(float(row['ch4 (mt/y)'])/1e3) + ''' * dtyears
    # Srcn2o := ''' + str(float(row['n2o (mt/y)'])/1e3) + ''' * dtyears
    # '''
    # year = round(1/env['dtyears', 'cur'])
    # year = 'next ' + str(year)
    # zs.compilerun(time + src, env)
    # data = zs.compilerun(year, env)[-1]
    # for row in rcp3data[1:100]:
    #     src = '''
    #     Srcco2 := ''' + row['fossilco2 (gt/y)'] + '+' + row['otherco2 (gt/y)'] + ''' * dtyears
    #     Srcch4 := ''' + str(float(row['ch4 (mt/y)']) / 1e3) + ''' * dtyears
    #     Srcn2o := ''' + str(float(row['n2o (mt/y)']) / 1e3) + ''' * dtyears
    #     '''
    #     zs.compilerun(src, env)
    #     yeardata = zs.compilerun(year, env)[-1]
    #     data = {idx: data[idx] + yeardata[idx] for idx in data.keys()}


    # data = zs.compilerun('next 12167', env)[-1]
    # data = complexprotect(data)
    # zs.repl(env)