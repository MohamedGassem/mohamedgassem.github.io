import numpy as np
import pprint
import copy

class GeneticAlgorithmParameters:
    """
        Class that encapsulates all parameters for genetic algorithm
    """

    def __init__(self, **kwargs):
        """
            Ctor

            Parameters
            ----------
                kwargs: dict
                    -seed: int
                        The seed for the random number generator
                    -genes_count: int
                        The number of genes for each member of population
                        A vector of genes_count genes is then called a genome
                    -population_size: int
                        The number of genome in each population
                    -elitism: int
                        The number of best genome that will pass to the
                        next generation
                    -reproduction: int 
                        The number of genome that comes from crossovers.
                        reproduction - reproduction_elitism crossovers are 
                        made between random genomes of the current population. 
                    -reproduction_elitism: int
                        The number of genomes that comes from crossovers 
                        between the best genomes of the population
                    -mutation_rate: float
                        The mutation rate
                    -fitness: function
                        Takes as parameter a genome and return a float value 
                        that needs to be maximized
        """
        self.seed = kwargs.get("seed", None)
        self.random = np.random.RandomState(self.seed)

        self.genes_count = kwargs.get("genes_count", 4)
        self.population_size = kwargs.get("population_size", 20)
        
        self.elitism      = kwargs.get("elitism", 5)
        self.reproduction = kwargs.get("reproduction", 0)
        self.reproduction_elitist = kwargs.get("reproduction_elitist", 5)

        self.mutation_rate = kwargs.get("mutation_rate", 0.2)
        self.fitness = kwargs.get("fitness", lambda x, y: 0.0)

class GeneticAlgorithmStatistics:
    """
        Statistics for Genetic Algorithm

        The statistics computed are :
            -mean fitness of each generation
            -sd fitness of each generation
            -min (and argmin) of each generation
            -max (and argmax) of each generation

        Those are available in the data attribute

        All times statistics are also availaible (tough mean and sd both
        to be computed by the user using "sum", "sum_squared" and "count" keys)

        Those are available in the allTime attribute
    """
    def __init__(self):
        """
            Ctor
        """
        self.data = []
        self.allTime = {
            "count": 0, 
            "sum": 0, 
            "sum_squared": 0,
            "min":  np.inf, 
            "max": -np.inf,
            "min_genome": [], 
            "max_genome": []
        }

    def aggregate(self, population, fitnesses):
        """
            Aggregate statistcs

            Parameters
            ----------
                population: 2d array_like
                    The population of the generation
                fitnesses: 1d array_like
                    The fitnesses for each member of the
                    popumation
        """
        self.data.append({
            "sd": np.std(fitnesses),
            "mean": np.mean(fitnesses), 
            "min": np.min(fitnesses), 
            "max": np.max(fitnesses), 
            "min_genome": population[np.argmin(fitnesses)], 
            "max_genome": population[np.argmax(fitnesses)]
        })

        self.allTime["count"] += 1
        self.allTime["sum"] += np.sum(fitnesses)
        self.allTime["sum_squared"] += np.sum(fitnesses ** 2)

        if self.data[-1]["min"] < self.allTime["min"]:
            self.allTime["min"] = self.data[-1]["min"]
            self.allTime["min_genome"] = self.data[-1]["min_genome"]

        if self.data[-1]["max"] > self.allTime["max"]:
            self.allTime["max"] = self.data[-1]["max"]
            self.allTime["max_genome"] = self.data[-1]["max_genome"]

class GeneticAlgorithm:
    """
        Simple implementation of genetic algorithm
    """
    def __init__(self, params):
        """
            Ctor

            Parameters
            ----------
                params: GeneticAlgorithmParameters
                    The parameters for the algorithm
        """
        self._params = params
        self.stats = GeneticAlgorithmStatistics()
        self._population = self._params.random.normal(
            size = (self._params.population_size, self._params.genes_count)
        )

    def _crossover(self, genome1, genome2):
        """
            Perform crossover between two genomes

            The crossover is performed at the midpoint of the genomes

            Parameters
            ----------
                genome1: 1d array_like
                    The first parent
                genome2: 1d array_like
                    The second parent     
        
            Returns
            -------
                tuple
                    The two possible crossover
        """
        assert(genome1.shape == genome2.shape)
        crossover_point = int(genome1.shape[0] / 2)

        new_gene1 = copy.deepcopy(genome2)
        new_gene2 = copy.deepcopy(genome2)

        for i in range(0, crossover_point):
            new_gene1[i] = genome2[i]

        for i in range(crossover_point, genome1.shape[0]):
            new_gene2[i] = genome2[i]

        return new_gene1, new_gene2

    def train(self, generations, population = None):
        """
            Runs the population for a given amount of generation

            Parameters
            ----------
                generations: int
                    The number of generation to run
                population: 2d array_like
                    Default is None (which means use the previous
                    population, random no training is done). The starting 
                    population. Make sure it meets the given parameters

            Returns
            -------
                GeneticAlgorithm
                    The statistics for the ran generations. Note that they
                    are not reset between subsequent calls to this function
        """
        pp = pprint.PrettyPrinter(indent = 4)
            
        if not (population is None):
            self._population = population

        for i in range(0, generations):
            new_population = []        

            # Compute fitnesses    
            fitnesses = np.asarray([
                self._params.fitness(i * self._params.population_size + j, self._population[j, :]) 
                for j in range(0, self._params.population_size)
            ])
            
            self.stats.aggregate(self._population, fitnesses)

            # Choose best
            max_fitnesses = fitnesses.argsort()[-self._params.elitism:][::-1]
        
            # Add them to new population
            for mf in max_fitnesses:
                new_population.append(self._population[mf])

            # Crossover only between best genes
            crossover_elitist = self._params.random.randint(
                0, self._params.elitism - 1, 
                size = (self._params.reproduction_elitist, 2)
            )

            for parents in crossover_elitist:
                children = self._crossover(
                    self._population[max_fitnesses[parents[0]]], 
                    self._population[max_fitnesses[parents[1]]]
                )

                new_population.append(children[0])
            
            # Random crossover of population
            crossover_count = self._params.reproduction - \
                              self._params.reproduction_elitist

            to_crossover    = self._params.random.randint(
                0, self._params.population_size - 1, 
                size = (crossover_count, 2)
            )

            # Perform crossovers
            for parents in to_crossover:
                children = self._crossover(
                    self._population[parents[0]], 
                    self._population[parents[1]]
                )

                new_population.append(children[0])
                # new_population.append(children[1])
                
            # Perform mutations
            for i in range(len(new_population)):
                for j in range(new_population[i].shape[0]):
                    mutate = self._params.random.uniform()

                    if mutate < self._params.mutation_rate:
                        new_population[i][j] += self._params.random.normal(0, 0.1)

            # Add new random genes
            random_genes_count = self._params.population_size - len(new_population)
            random_population = self._params.random.normal(
                size = (random_genes_count, self._params.genes_count)
            )

            for i in range(0, random_genes_count):
                new_population.append(random_population[i].tolist())

            self._population = np.array(new_population)

            print("****************")
            print("Generation : ")
            pp.pprint(self.stats.data[-1])
            print("All time : ")
            pp.pprint(self.stats.allTime)
            print("****************")

        pp.pprint(self.stats.allTime)
        return self.stats