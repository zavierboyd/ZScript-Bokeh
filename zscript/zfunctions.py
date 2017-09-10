import numpy as np

def differentiate(x):
    return x[1:] - x[:-1]

center = lambda x: (x[2:] - x[:-2])/2

def doublediff(x):
    d = differentiate(x)
    dd = differentiate(d)
    return np.concatenate(([d[0]], dd, [-d[-1]]))


if __name__ == '__main__':
    x2 = np.array([x**3 for x in range(-3, 4)])

    # print(x2[1:])
    # print(x2[:-1])
    # print(x2[2:])
    # print(x2[:-2])

    print(x2)
    print(differentiate(x2))
    print(center(x2))
    print(doublediff(x2))
