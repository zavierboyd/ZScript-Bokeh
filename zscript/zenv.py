from zscript.zsyntaxtree import *
from collections import defaultdict


class EnvGetValExt:
    def __init__(self, parent, flag):
        self.flag = flag
        self.parent = parent

    def __getitem__(self, item):
        return self.parent.__getitem__(item, self.flag)


class EnvGetObjExt:
    def __init__(self, parent):
        self.parent = parent

    def __getitem__(self, flag):
        return self.parent.getobject(flag)

    def __setitem__(self, flag, value):
        if flag == 'val':
            self.parent.value = value
        else:
            raise Exception('Cannot change any thing other than the val library')


class FuncCall:
    def __init__(self, func):
        self.func = func

    def __call__(self, env):
        def call(inpt, flag):
            return self.func(inpt(env, flag))
        return call

    def __repr__(self):
        return 'FuncCall({0}, "{0}")'.format(self.func.__name__)


class Env:
    def __init__(self, repl=False):
        self.repl = repl
        self.value = {}
        self.nextval = {}
        self.current = {'True': Boolean(True), 'False': Boolean(False)}
        self.defdepent = defaultdict(list)
        self.trace = []
        self.functions = {'mag': FuncCall(abs)}
        self.graph = []
        self.object = EnvGetObjExt(self)

    def __getitem__(self, itemflag):
        item = itemflag[0]
        flag = itemflag[1]
        if flag == 'func' and item in self.functions:
            return self.functions[item](self)
        elif flag == 'nxt' and item in self.nextval:
            return self.nextval[item](self, None)
        elif (flag == 'nxt' or flag == 'cur') and item in self.current:
            return self.current[item](self, flag)
        elif (flag == 'nxt' or flag == 'cur') and item in self.value:
            return self.value[item](self, flag)
        else:
            if flag == 'nxt' or flag == 'cur' or flag == 'func':
                if flag == 'cur' and item in self.nextval:
                    raise NameError('The definition "%s" needs to be initalized first' % item)
                else:
                    raise NameError("I can't find the value corresponding to %s" % item)
            else:
                raise Exception('The flag "%s" is not a valid flag' % flag)

    def __setitem__(self, itemflag, value):
        item = itemflag[0]
        flag = itemflag[1]
        if flag == 'nxt' or flag == 'cur':
            if (item in self.current or item in self.nextval):  # Checks for Re-Definition of Next/Current Definitions
                if not (self.repl):
                    raise Exception('Cannot Redefine The Definition "%s"' % item)
                else:
                     ZWarning('You are changing a variable Definition. If you wish to change this regularly use :=')
            circle, future = self.circleref(item, value, flag)
            if circle:  # Checks for Circular Referencing
                raise Exception('Circular Reference found when defining "%s"' % item)
            elif flag == 'nxt':
                if self.repl and (item in self.current):
                    del self.current[item]
                self.nextval[item] = value
            elif flag == 'cur':
                if future:  # Checks for Future Definitions in Current Definitions
                    raise SyntaxError('Trying to reference a Future Definition in "%s"' % item)
                else:
                    if item in self.value:  # Deletes Old Value copy of New Current Definition
                        del self.value[item]
                    if item in self.nextval:
                        del self.nextval[item]
                    self.current[item] = value
        elif flag == 'val':
            if not(self.repl) and (item in self.current):  # Checks for a Current Definition by the same Identifier
                raise Exception("Can't change a Current Definition to a Variable '%s'" % item)
            else:
                if self.repl and (item in self.current):
                    del self.current[item]
                self.value[item] = value
        else:
            raise Exception('The flag "%s" is not a valid flag' % flag)

    def getobject(self, flag):
        if flag == 'nxt':
            return self.nextval
        elif flag == 'cur':
            return self.current
        elif flag == 'val':
            return self.value
        elif flag == 'trc':
            return self.trace
        elif flag == 'func':
            return self.functions
        elif flag == 'gph':
            return self.graph
        else:
            raise Exception('The flag "%s" is not a valid flag' % flag)

    def circleref(self, ident, prgr, flag):
        """ident: a String of the Definition Identifier
        prgr: an Object that contains the Definition Program

        Returns: a Tuple of Booleans
        First Bool tells if there is circle reference
        Second Bool tells if it references a future definition
        Example: (True, False)"""

        test = TestEnv()
        if flag == 'nxt':
            ident += '_'
        prgr(test)
        future = len(test.object['nxt']) != 0
        self.defdepent[ident] = list(test.object['nxt'].keys()) + list(test.object['cur'].keys())

        def findfuncs(dependent, ident, var):
            funcs = dependent[var]
            if ident in funcs:
                return True
            else:
                for func in funcs:
                    return findfuncs(dependent, ident, func)
        circle = findfuncs(self.defdepent, ident, ident)
        ident = ident[:-1]
        return circle, future

    def tracevar(self, item):
        if item not in self.trace:
            self.trace.append(item)


    def graphvars(self, x, y):
        if (x, y) not in self.graph:
            self.graph.append((x, y))


    def __repr__(self):
        current = self.current.copy()
        del current['True']
        del current['False']
        program = ''

        value = '\n'.join([repr(SetVar(var, val)) for var, val in self.value.items()])
        if value:
            program += value + '\n'

        current = '\n'.join([repr(SetDef(var, val, True)) for var, val in current.items()])
        if current:
            program += current + '\n'

        nextval = '\n'.join([repr(SetDef(var, val, False)) for var, val in self.nextval.items()])
        if nextval:
            program += nextval + '\n'

        for var in self.trace:
            program += repr(Trace(var)) + '\n'

        for x, y in self.graph:
            program += repr(Graph(x, y)) + '\n'

        return program


class TestEnv(Env):
    def __init__(self):
        def z(): return Literal(1)
        def func(env):
            def testcall():
                def thing2(inpt, flag):
                    return inpt(env)
                return thing2
            return testcall
        self.value = defaultdict(z)
        self.nextval = defaultdict(z)
        self.current = defaultdict(z)
        self.functions = defaultdict(func(self))
        self.object = EnvGetObjExt(self)

    def __getitem__(self, itemflag):
        item = itemflag[0]
        flag = itemflag[1]
        if flag == 'func':
            return self.functions[item]
        elif flag == 'nxt':
            return self.nextval[item+'_'](self, flag)
        elif flag == 'cur':
            return self.current[item](self, flag)
        else:
            raise Exception('The flag "%s" is not a valid flag' % flag)


if __name__ == '__main__':
    e = Env()
    b = TestEnv().current
    print(b)
    a = Function('mag', Literal(1 + 1j))
    print(a(e))
    print(e.nextval)

