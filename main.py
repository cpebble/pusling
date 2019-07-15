import networkx as nx
import numpy as np
from pprint import pprint
from typing import AnyStr, Iterable
import random
np.random.seed(42)

# This generates an n x n matrix and populates it with values between 1-5
People = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
P = (np.random.rand(len(People), len(People)) * 5).astype(np.int) + 1


def Weight(a: AnyStr, b: AnyStr) -> int:
    global People
    global P
    aIndex, bIndex = People.index(a), People.index(b)
    aScore = P[aIndex, bIndex]
    bScore = P[bIndex, aIndex]
    return abs(aScore - bScore)


def Score(A: nx.Graph) -> int:
    score = 0
    for edge in A.edges(data="weight"):
        score += edge[2]

    return score


def ForestScore(A: Iterable[nx.DiGraph]) -> int:
    return sum([Score(g) for g in A])


def RandomOptimisation(G: nx.DiGraph,
                       minGroupSize: int,
                       maxGroupSize: int) -> Iterable[nx.DiGraph]:
    nodes = list(G.nodes)
    random.shuffle(nodes)
    forest = []
    while len(nodes) > 0:
        group = []
        while len(group) < minGroupSize or (len(nodes) < minGroupSize and len(nodes) > 0):
            group.append(nodes.pop())
        forest.append(G.subgraph(group))
    return forest


def Crossover(f1: Iterable[nx.DiGraph], f2: Iterable[nx.DiGraph]):
    crossovers = 5
    # i want to take an amount of


def GeneticOptimisation(G: nx.DiGraph,
                        minGroupSize: int,
                        maxGroupSize: int) -> Iterable[nx.DiGraph]:
    # Generate initial population
    maxPopulation = 20
    population = []
    for _ in range(maxPopulation):
        tmp = list(G.nodes)
        random.shuffle(tmp)
        population.append(tmp)
    # Start genetic loop
    candidatesToGrab = 4
    newMutations = 10  # How many new mutations to create each round
    switches = 3  # How many times to switch individual places
    maxIterations = 100
    iterations = 0
    while iterations <= maxIterations:
        # Select top candidates
        candidates = sorted(
            population,
            key=lambda string: ForestScore(
                StringToForest(string, G, minGroupSize)),
            reverse=True)[:candidatesToGrab]  # Pull top candidates
        population = candidates[:maxPopulation]
        print(
            f"""Reached iteration {iterations}, current top candidate: 
{candidates[0]} 
with score: {ForestScore(StringToForest(candidates[0], G, minGroupSize))} """)
        # Do shuffle
        for _ in range(newMutations):  # Create new mutations from top-candidates
            start = list(random.choice(candidates)).copy()
            # breakpoint()
            for i in range(switches):  # Switch x group members
                i = random.randint(0, len(start)-1)
                j = random.randint(0, len(start)-1)
                tmp = start[i]
                start[i] = start[j]
                start[j] = tmp
            population.append(start)

        iterations += 1

    candidates = [StringToForest(c, G, minGroupSize) for c in population]
    return sorted(candidates, key=lambda f: ForestScore(f), reverse=True)[0]


def StringToForest(s: AnyStr, G: nx.DiGraph, minGroupSize: int = 5,) -> Iterable[nx.DiGraph]:
    nodes = list(s)
    forest = []
    while len(nodes) > 0:
        group = []
        while len(group) < minGroupSize or (len(nodes) < minGroupSize and len(nodes) > 0):
            group.append(nodes.pop())
        forest.append(G.subgraph(group))
    return forest


def PrintForest(forest: Iterable[nx.DiGraph]):
    print(f"We made a forest with a score of {ForestScore(forest)}")
    print("Here is the forest:")
    for g in forest:
        print(f"Score: {Score(g)}", g.nodes)


def getAverages(G):
    randomTeams = 0
    geneticTeams = 0
    for _ in range(20):
        f = GeneticOptimisation(G, 5, 8)
        geneticTeams += ForestScore(f)
        r = RandomOptimisation(G, 5, 8)
        randomTeams += ForestScore(r)
    print("Random average:", randomTeams / 20)
    print("Genetic average:", geneticTeams / 20)


if __name__ == "__main__":
    # The above might suck
    # Get a list of connections from 1-5 for persons A-Z(28)
    minGroupSize = 5

    # random.seed(42)

    G = nx.DiGraph()
    # This adds every person to the graph, and adds an edge to every other
    for p in People:
        G.add_node(p)
        for p2 in People:
            G.add_edge(p, p2, weight=Weight(p, p2))

    # # First we do random optimisation
    # forest = RandomOptimisation(G, minGroupSize, 10)
    # PrintForest(forest)
    # otherforest = StringToForest("ABCDEFGHIJKLMNOPQRSTUVWXYZ", G)
    # PrintForest(otherforest)
    # optimalForest = GeneticOptimisation(G, 5, 8)
    # PrintForest(optimalForest)
    getAverages(G)
