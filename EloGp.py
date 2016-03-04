from Elo import *
from ncaa import *

import random
from deap import creator, base, tools, algorithms

creator.create("FitnessMulti", base.Fitness, weights=(-1.0,1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

toolbox.register("attr_k", random.uniform, 1, 100)
toolbox.register("attr_beta", random.uniform, 1.0/10000, 1)
toolbox.register("attr_base", random.uniform, 2, 20)
toolbox.register("attr_r0", random.uniform, 800, 2000)
toolbox.register("individual", tools.initCycle, creator.Individual, 
                 (toolbox.attr_k, toolbox.attr_beta, toolbox.attr_base, toolbox.attr_r0),
                 n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_this(individual):
    elo = Elo(individual[0], individual[1], individual[2], individual[3])
    elo.build_ratings(tourney[2012])
    return elo.eval_fitness(tourney[2012])


toolbox.register("evaluate", eval_this)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=400
for gen in range(NGEN):
    print gen
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
    
best = tools.selBest(population, k=1)
print best

elo = Elo(*(best[0]))
elo.build_ratings(tourney[2012])
elo.eval_fitness(tourney[2012])
    
print("%f, %f" % (elo.logloss, elo.accuracy))
