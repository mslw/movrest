from multiprocessing import Pool


def f(x):
    result = x*x
    print(result)


def g(x, y):
    result = x * y
    print(result)


if __name__ == '__main__':
    with Pool(5) as p:
        [p.apply(f, args=(x,)) for x in (1, 2, 3, 4, 5, 6, 7)]

    print('---')

    pairs = [[1, 2], [3, 3], [4, 5], [9, 3], [2, 8], [5, 5]]
    with Pool(5) as p:
        [p.apply(g, args=arglist) for arglist in pairs]

# import multiprocessing as mp
#
#
# def cube(x):
#     return x**3
#
#
# pool = mp.Pool(processes=4)
# results = [pool.apply(cube, args=(x,)) for x in range(1, 7)]
# print(results)
