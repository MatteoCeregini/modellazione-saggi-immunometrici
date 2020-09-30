class Model:
    def __init__(self, count, mode, group, verteces, color):
        self.count = count
        self.mode = mode
        self.group = group
        self.verteces = ('v3f', verteces)
        self.color = ('c3f', color)



