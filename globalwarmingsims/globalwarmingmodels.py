idealprogram5 = '''
a := 0.0225
dt := 1
rf2015mask := -0.75
b := -0.3
tempresponsetime := 20
x := 1 / dt
climatesensitivity2x := 3
pco2 := 290
temptra := 0
tempeq := 0
rfscaledmask := 0
rfco2 := 0

pco2_ = 280 + (pco2 - 280) * (1 + a * dt)
rfco2_ = 4 * ln ( pco2 / 280 ) / ln ( 2 )
rfscaledmask_ = b * (pco2_ - pco2) / 1
rfmask = rfscaledmask * (rfscaledmask > rf2015mask) + rf2015mask * (rfscaledmask <= rf2015mask)
rftotal = rfmask + rfco2
climatesensitivity = climatesensitivity2x / 4
tempeq = climatesensitivity * rftotal
dtemptra = ((tempeq - temptra) / tempresponsetime) * x
temptra_ = dtemptra + temptra

trace temptra, tempeq, pco2, rftotal, rfco2, rfmask
graph temptra
graph rftotal
graph pco2

next 115

save env2015

next 85

load env2015

rfmask := rfscaledmask * (rfscaledmask > rf2015mask) + rf2015mask * (rfscaledmask <= rf2015mask)
min := rfmask/10
rfmask_ = (rfmask - min)*(rfmask > 0)

next 85
'''
