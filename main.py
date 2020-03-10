import utils, genethic_operators, static, Enums
import matplotlib.pyplot as plt

matrix_size = utils.set_matrix_size()
throughput = utils.set_throughput()

start_node = utils.set_node("start", matrix_size)
end_node = utils.set_node("end", matrix_size)

pop_size = utils.set_pop_size()
chrome_size = utils.set_chrome_size(matrix_size)
count_generations = utils.set_count_genetations()

static.Static.CHANCE_MUTATION = utils.set_chance_to_mutations()
static.Static.MODE_WORK = utils.set_mode()
type_selection = utils.set_type_selection()
type_recombination = utils.set_type_recombination()

population = []
matrix = []


def launch_set_matrix():
    global matrix
    print("Init graph network\n")
    matrix = utils.gen_matrix(matrix_size, throughput)
    utils.write_graphs(matrix)


def launch_set_population():
    global population
    print("Init start population\n")
    population = genethic_operators.generate_population(start_node, end_node, pop_size, chrome_size)
    utils.write_graphs(population)


def launch_get_selection(pop_size, selection_type=Enums.SelectionsTypes.TOURNAMENT, key=0):
    global matrix
    global population
    population = genethic_operators.selection(population, selection_type, pop_size, key=key, matrix=matrix)
    if static.Static.MODE_WORK == Enums.ModeWork.STEPS:
        print("Selecting to recombination\n")
        utils.write_graphs(population)


def launch_get_recombination(recombination_type=Enums.Recombination.UNIFORM):
    global population
    population = genethic_operators.recombination(population, recombination_type, chrome_size, pop_size)
    if static.Static.MODE_WORK == Enums.ModeWork.STEPS:
        print("Recombination population\n")
        utils.write_graphs(population)


def launch_mutation(chance=static.Static.CHANCE_MUTATION):
    global population
    population = genethic_operators.mutation(population,  chance * 100, chrome_size)
    if static.Static.MODE_WORK == Enums.ModeWork.STEPS:
        print("Mutation population\n")
        utils.write_graphs(population)


def launch_reduction(matrix):
    global population
    population = genethic_operators.reduction(population, matrix)
    if static.Static.MODE_WORK == Enums.ModeWork.STEPS:
        print("Reduction population\n")
        utils.write_graphs(population)


launch_set_matrix()

result = []


def main_algorithm():
    global population
    n = 0
    while True:
        launch_get_selection(pop_size, selection_type=type_selection)
        launch_get_recombination(recombination_type=type_recombination)
        launch_mutation()
        launch_reduction(matrix)

        print(n, 'main', 'len pop', len(population))
        if len(population) < pop_size:
            copy = population.copy()
            while len(population) <= pop_size:
                # тут вызов скрещивания родителей с потомками (да, да, я конченный извращенец)
                # если популяции недостаточно, это вызывает преждевременную мутацию с высоким шансом
                # от чего новая популяция может стать либо гениальной, либо отсталой
                # все как в реальной жизни
                print(len(population), "поп сайз")
                launch_get_recombination(recombination_type=type_recombination)
                population.extend(copy)
                launch_mutation(chance=20)
            continue
            # return main_algorithm()
        else:
            if len(population) > pop_size:
                population = population[:pop_size]
            n += 1
            return True


def start():
    launch_set_population()
    n = 0
    while n < count_generations:
        print(n)
        if main_algorithm():
            x = []
            y = []
            m = 0
            for i in utils.qsort(utils.fitness_function(population, matrix), 0, len(population) - 1, key='desc'):
                # print(i)
                y.append(i)
                x.append(m)
                m += 1
            # i = input()
            result.append([x, y])
            n += 1
        else:
            # asc = utils.get_asc_user()
            # if asc == 1:
            #     return start()
            # else:
            print("Shutdown")
            exit(0)


start()

n = 1
fig = plt.figure()
ax = fig.add_subplot(111)

# y2 = np.random.random(N)
# print(x, y2)
for i in result:
    # for j in range(len(i[0])):
    ax.plot(i[0], i[1], label=str(f"Поколение {n}"))
    print(i[0], i[1])
    n += 1
ax.legend()
plt.savefig(f'plot.png', fmt='png')
plt.show()

for chrome in population:
    print(chrome)
