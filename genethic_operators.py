import random, utils
import Enums, static


def random_generate_value(start, end, checking=False, value=0, from_gen=1):
    while True:
        if not checking:
            if start < end:
                return random.randint(from_gen, end)
            else:
                return random.randint(from_gen, start)
        else:
            if start < end:
                tmp = random.randint(from_gen, end)
            else:
                tmp = random.randint(from_gen, start)
            if value != tmp:
                return tmp
            else:
                continue


def select_parents(selecting, coefficients, n):
    par_1 = random.randint(0, n - 1)
    par_2 = random.randint(0, n - 1)
    sel_1, coef_1, sel_2, coef_2 = selecting[par_1], coefficients[par_1], selecting[par_2], coefficients[par_2]
    return sel_1, coef_1, sel_2, coef_2, selecting, coefficients, n


def gen_two_child(parent_1, parent_2, point, type_crossover):
    child_1, child_2 = [], []
    length = len(parent_1)
    if type_crossover == Enums.Recombination.ONE_POINTER:
        for i in range(length):
            if i < point:
                child_1.append(parent_2[i])
                child_2.append(parent_1[i])
            else:
                child_1.append(parent_1[i])
                child_2.append(parent_2[i])
    elif type_crossover == Enums.Recombination.UNIFORM:
        for i in range(length):
            if i == 0:
                child_1.append(parent_1[0])
                child_2.append(parent_2[0])
            elif i == length:
                child_1.append(parent_1[length - 1])
                child_2.append(parent_2[length - 1])
            else:
                if i % 2 != 0:
                    child_1.append(parent_2[i])
                    child_2.append(parent_1[i])
                else:
                    child_1.append(parent_1[i])
                    child_2.append(parent_2[i])
    else:
        pass
    yield child_1, child_2


def generate_population(start_node, end_node, pop_size, chrome_size):
    population = []
    for i in range(pop_size):
        chrome = []
        for j in range(chrome_size):
            val = random_generate_value(1, chrome_size)
            if j == 0:
                chrome.append(start_node)
            elif j == chrome_size - 1:
                chrome.append(end_node)
            else:
                if j != chrome_size and val == end_node:
                    val = random_generate_value(1, chrome_size, checking=True, value=val)
                if j == 1 and val == start_node:
                    val = random_generate_value(1, chrome_size, checking=True, value=val)
                chrome.append(val)
        population.append(chrome)
    return population


def get_sorted_select_and_coeffs(population, matrix):
    selecting = []
    coefficients = []
    broken = []
    fitness = utils.fitness_function(population, matrix)
    copy = fitness.copy()
    n = 0
    # print(fitness)
    # delete chrome where fitness > no_path_value
    for i in range(len(copy)):
        if copy[i] < static.Static.NO_PATH_VALUE:
            selecting.append([copy[i], population[i]])
        else:
            broken.append(population[i])
            del fitness[i - n]
            n += 1
        # selecting.append([copy[i], population[i]])
    obr = 0
    for i in fitness:
        obr += (1 / i)
    selecting = utils.qsort_special(selecting, 0, len(selecting) - 1)
    for i in range(len(selecting)):
        coefficients.append(((1 / selecting[i][0]) / obr) * 100)
    n = 0
    copy = selecting.copy()
    selecting = []
    for i in range(len(copy)):
        selecting.append(copy[i][1])
        n += 1
    return selecting, coefficients, broken


def selection(population, type_selection, pop_size, key=0, matrix=None):
    selecting, coefficients, broken = get_sorted_select_and_coeffs(population, matrix)
    print(len(selecting), len(broken))
    #########################################################################################
    ###########################
    ###################################################################################################################
    ###################################################################################################################
    if type_selection == Enums.SelectionsTypes.TRUNCATIONS:
        T = 1  # truncate limiter
        n = 0
        copy = selecting.copy()
        selecting = []
        for i in range(len(copy) // 2, len(copy)):
            selecting.append(copy[i])
            del coefficients[i - n]
            n += 1
    elif type_selection == Enums.SelectionsTypes.TOURNAMENT:
        n = len(selecting)
        if n % 2 != 0 and n != 1:
            n -= 1
        elif n == 1:
            return selecting
        groups = []
        # print(n)
        while n > 0:
            try:
                par_1, coef_1, par_2, coef_2, selecting, coefficients, n = select_parents(selecting, coefficients, n)
                groups.append([par_1, coef_1, par_2, coef_2])
                # del selecting[selecting.index(par_1)], coefficients[coefficients.index(coef_1)], \
                #     coefficients[coefficients.index(coef_2)], selecting[selecting.index(par_2)]
                n -= 2
            except RecursionError:
                continue
        # print()
        selecting = []
        coefficients = []
        for group in groups:
            if group[1] > group[3]:
                selecting.append(group[0])
                coefficients.append(group[1])
            else:
                selecting.append(group[2])
                coefficients.append(group[3])
    else:
        pass
    return selecting


def recombination(population, type_crossover, chrome_size, population_size):
    parents = population
    childs = []
    recombination_ = []
    if type_crossover == Enums.Recombination.ONE_POINTER:
        n = 0
        try:
            for i in range(len(parents)):
                point = random_generate_value(1, chrome_size - 1, from_gen=0)
                childs.append(gen_two_child(parents[i], parents[i + 1 - n], point, type_crossover))
                n += 1
        except RecursionError as e:
            print(e.args)
    elif type_crossover == Enums.Recombination.TWO_POINTER:
        pass
    elif type_crossover == Enums.Recombination.UNIFORM:
        n = 0
        for i in range(len(parents) - 1):
            point = random_generate_value(1, chrome_size, from_gen=0)
            childs.append(gen_two_child(parents[i], parents[i + 1 - n], point, type_crossover))
            n += 1
    else:
        pass
    copy = childs.copy()
    childs = []
    for child in copy:
        for generator in child:
            for i in generator:
                childs.append(i)
    recombination_.extend(childs)
    if len(recombination_) < population_size:
        recombination_.extend(parents)
    return recombination_


def mutation(population, chance, chrome_size):
    for chrome in range(len(population)):
        for gen in range(len(population[chrome])):
            tmp = random.randint(0, 10000)
            if tmp < chance:
                # print('mutation is done')
                population[chrome][gen] = random_generate_value(1, chrome_size, checking=True, value=gen)
            else:
                pass
    return population


def reduction(population, matrix):
    population, coefficients, broken = get_sorted_select_and_coeffs(population, matrix)
    sum = 0
    for i in coefficients:
        sum += i
    middle = sum / len(coefficients)
    copy = population
    population = []
    broken = []
    for i in range(len(copy)):
        if coefficients[i] >= middle:
            population.append(copy[i])
        else:
            broken.append(copy[i])
    if len(population) < 5:
        population.extend(broken[:len(broken)//2])
    return population
