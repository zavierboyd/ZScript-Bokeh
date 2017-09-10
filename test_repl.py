import zscript as zs
from program import zscript_code
from zgraph import bokehstaticgraph, bokehtickgraph

test = '''a := 1
b := 1
a_ = a + b
b_ = a
trace a
trace b
next 1'''
stuff = zs.compilerun(test, zs.Env())
print(stuff)

def rangetick(data):
    keys = list(data.keys())
    yield {key: [] for key in keys}
    i = 0
    mod = len(list(data.values())[0])
    print(mod)
    while True:
        yield {key: [data[key][i % mod]] for key in keys}
        i += 1


def infintick(data):
    first = next(data)
    yield {var: [] for var in first.keys()}
    yield {var: [val] for var, val in first.items()}
    while True:
        yield {var: [val] for var, val in next(data).items()}


data = stuff[0]
if type(data) is dict:
    bokehstaticgraph('a', 'b', data)
else:
    tick = infintick(data)
    bokehtickgraph('a', 'b', tick)


# def update():
#     global working
#     graphtick()
#     working = False
#     print('asdfdsaf')
#
# working = False
#
#
# def nexttick():
#     global working
#     if not working:
#         working = True
#         curdoc().add_next_tick_callback(update)
#     else:
#         print('Working')
#
#
# curdoc().add_periodic_callback(nexttick, 1000)


env = zs.Env(repl=True)
zs.compilerun(zscript_code, env)

zs.repl(env)
zs.compile(zscript_code, env)
zs.compilerun('next 10', env)