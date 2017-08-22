import zscript as zs
from zscript.zgraph import np, bokehstaticgraph, bokehtickgraph
from program import zscript_code



test = '''a := (1, 0)
a_ = a * (3, 4)/5 + 0.1
trace a
next 0'''
stuff = zs.compilerun(test, zs.Env())
print(stuff)


def complexprotect(data):
    ndata = {}
    for var, val in data.items():
        if type(val) is list:
            if sum([num.imag**2 for num in val]) > 0:
                ndata[var+'m'] = [abs(num) for num in val]
                ndata[var+'d'] = [np.angle(num) for num in val]
                ndata[var+'x'] = [num.real for num in val]
                ndata[var+'y'] = [num.imag for num in val]
            else:
                ndata[var] = val
        else:
            if type(val) is complex:
                ndata[var+'m'] = abs(val)
                ndata[var+'d'] = np.angle(val)
                ndata[var+'x'] = val.real
                ndata[var+'y'] = val.imag
            else:
                ndata[var] = val
    return ndata


def rangetick(data):
    data = complexprotect(data)
    keys = list(data.keys())
    yield {key: [] for key in keys}
    i = 0
    mod = len(list(data.values())[0])
    print(mod)
    while True:
        yield {key: [data[key][i % mod]] for key in keys}
        i += 1


def infintick(data):
    first = complexprotect(next(data))
    yield {var: [] for var in first.keys()}
    yield {var: [val] for var, val in first.items()}
    while True:
        yield {var: [val] for var, val in complexprotect(next(data)).items()}


data = stuff[0]
if type(data) is dict:
    data = complexprotect(data)
    bokehstaticgraph('am', 'ad', data)
else:
    tick = infintick(data)
    bokehtickgraph('am', 'ad', tick)


env = zs.Env(repl=True)
zs.compilerun(zscript_code, env)

zs.repl(env)
zs.compilerun(zscript_code, env)
zs.compilerun('next 10', env)