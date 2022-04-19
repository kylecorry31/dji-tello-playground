class LinearCombinationFilter:
    def __init__(self, weights: [float]):
        self.weights = weights

    def calculate(self, values):
        return sum([self.weights[i] * values[i] for i in range(len(values))])
