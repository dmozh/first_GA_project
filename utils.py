import random
import static, Enums


def get_asc_user():
    try:
        val = int(input("Not enough parents\nWould you like set new population?\n1: Yes\n2: No\n"))
        if val > 2:
            print("You can answer 1 or 2")
            return get_asc_user()
        else:
            return val
    except Exception as e:
        print("Not int")
        return get_asc_user()


def set_matrix_size():
    try:
        val = int(input("Set count nodes: "))
        if val < 2:
            print("Less then two or equal two nodes")
            return set_matrix_size()
        else:
            return val
    except Exception as e:
        print("Not int")
        return set_matrix_size()


def set_throughput():
    try:
        val = int(input("Set throughput power: "))
        if val <= 0:
            print("Less then zero or equal zero")
            return set_throughput()
        else:
            return val
    except Exception as e:
        print("Not int")
        return set_throughput()


def set_node(param, matrix_size):
    try:
        val = int(input(f"Input {param} node between 1 and {matrix_size}: "))
        if 0 > val:
            print("Less then zero or equal zero")
            return set_node(param, matrix_size)
        elif val > matrix_size:
            print("To large value")
            return set_node(param, matrix_size)
        else:
            return val
    except Exception as e:
        print("Not int")
        return set_node(param, matrix_size)


def set_pop_size():
    try:
        val = int(input("Set population size (count chrome in population), min 10: "))
        if val < 10:
            print("Less then 10")
            return set_pop_size()
        else:
            return val
    except Exception as e:
        print("Not int")
        return set_pop_size()


def set_chrome_size(matrix_size):
    return matrix_size


def set_chance_to_mutations():
    try:
        val = int(input("Set chance for mutations between 0 and 100: "))
        if 0 <= val <= 100:
            return val
        else:
            print("Out of range")
            return set_chance_to_mutations()

    except Exception as e:
        print("Not int")
        return set_chance_to_mutations()


def set_count_genetations():
    try:
        val = int(input("Set count generations to populations, min 5: "))
        if val >= 5:
            return val
        else:
            print("Less then 5")
            return set_count_genetations()
    except Exception as e:
        print("Not int")
        return set_count_genetations()


def set_limiter_to_select_truncation(len):
    try:
        val = int(input(f"Set count generations to populations, max {len}: "))
        if val <= len:
            return val
        else:
            print(f"More then {len}")
            return set_limiter_to_select_truncation(len)
    except Exception as e:
        print("Not int")
        return set_limiter_to_select_truncation(len)


def set_mode():
    try:
        val = int(input("Set mode to work program\n1: Cyclical\n2: Steps: \n"))
        if val == 1 or val == 2:
            if val == 1:
                return Enums.ModeWork.CYCLICAL
            if val == 2:
                return Enums.ModeWork.STEPS
        else:
            print("Not mode")
            return set_mode()
    except Exception as e:
        print("Not int")
        return set_mode()


def set_type_selection():
    try:
        val = int(input("Set mode to selection\n1: Truncations\n2: Tournament: \n"))
        if val == 1 or val == 2:
            if val == 1:
                return Enums.SelectionsTypes.TRUNCATIONS
            if val == 2:
                return Enums.SelectionsTypes.TOURNAMENT
        else:
            print("Not mode")
            return set_type_selection()
    except Exception as e:
        print("Not int")
        return set_type_selection()


def set_type_recombination():
    try:
        val = int(input("Set mode to reproduction\n1: one pointer crossover\n2: uniform \n"))
        if val == 1 or val == 2:
            if val == 1:
                return Enums.Recombination.ONE_POINTER
            if val == 2:
                return Enums.Recombination.UNIFORM
        else:
            print("Not mode")
            return set_type_recombination()
    except Exception as e:
        print("Not int")
        return set_type_recombination()


def write_graphs(matrix):
    n = 0
    head = "\t#|"
    for i in range(len(matrix[0])):
        head += f"\t{i + 1}"
    print(head)
    print("\t-" * len(matrix[0]) + "\t-")
    for i in matrix:
        print(f"\t{n + 1}|", end='')
        for j in i:
            print(f"\t{j}", end='')
        print("\n")
        n += 1


def write_arrs(array):
    n = 1
    for i in array:
        print(f"{n}|{i}")
        n += 1


def gen_matrix(matrix_size, throughput):
    matrix = []
    for col in range(matrix_size):
        row = []
        for symb in range(matrix_size):
            if random.uniform(0, 1) < 0.9996666:
                tmp = random.randint(1, throughput)
            else:
                tmp = static.Static.NO_PATH_VALUE
            if col == symb:
                row.append(0)
            if col < symb:
                row.append(tmp)
            if col > symb:
                row.append(matrix[symb][col])
        matrix.append(row)
    return matrix


def fitness_function(population, matrix):
    fitness = []
    for i in range(len(population)):
        summary = 0
        for j in range(len(population[i]) - 1):
            summary += matrix[population[i][j] - 1][population[i][j + 1] - 1]
        fitness.append(summary)
    return fitness


def qsort_special(els, left, right):
    '''
    Quick sort
    :param els: list these els using how key to sort
    :param left: int left limiter
    :param right: int right limiter
    :return:
    '''
    pivot = els[left][0]
    l_hold = left
    r_hold = right
    while left < right:
        while (els[right][0] >= pivot) and (left < right):
            right -= 1
        if left != right:
            els[left][0] = els[right][0]
            left += 1
        while (els[left][0] <= pivot) and (left < right):
            left += 1
        if left != right:
            els[right][0] = els[left][0]
            right -= 1
    els[left][0] = pivot
    pivot = left
    left = l_hold
    right = r_hold

    if left < pivot:
        qsort(els, left, pivot - 1)

    if right > pivot:
        qsort(els, pivot + 1, right)

    return els


def qsort(els, left, right, key='asc'):
    '''
    Quick sort
    :param els: list these els using how key to sort
    :param left: int left limiter
    :param right: int right limiter
    :return:
    '''
    pivot = els[left]
    l_hold = left
    r_hold = right
    while left < right:
        while (els[right] >= pivot) and (left < right):
            right -= 1
        if left != right:
            els[left] = els[right]
            left += 1
        while (els[left] <= pivot) and (left < right):
            left += 1
        if left != right:
            els[right] = els[left]
            right -= 1
    els[left] = pivot
    pivot = left
    left = l_hold
    right = r_hold

    if left < pivot:
        qsort(els, left, pivot - 1, key=key)

    if right > pivot:
        qsort(els, pivot + 1, right, key=key)

    if key == 'desc':
        return list(reversed(els))
    else:
        return els
