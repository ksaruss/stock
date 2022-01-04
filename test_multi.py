import multiprocessing

def func(x, paral=True):

    result = 0
    start_time = time.time()
    for i in range(x[0], x[1]):
        result += i
    print('finish_function', time.time() - start_time)


    return result

if __name__ == '__main__' :
    start_program = time.time()

    value = 1000000000

    pros = 6

    pool = multiprocessing.Pool(processes=pros)

    one_val = int(value / pros)

    mass = []
    for i in range(pros):
        if i != (pros - 1):
            mass.append((one_val * i, one_val * (i+1)))
        else:
            mass.append((one_val * (pros-1), value))
    # print(mass)

    s = pool.map(func, mass)
    f = 0
    for i in s:
        f += i
    print(f)
    print('finish program', time.time() - start_program)
