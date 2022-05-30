def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value