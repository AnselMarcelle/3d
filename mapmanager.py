class Mapmanager:
    def __init__(self):
        self.model = "block.egg"
        self.texture = "block.png"
        self.colors = [
            (0.5, 0.3, 0.0, 1),
            (0.2, 0.2, 0.3, 1),
            (0.5, 0.5, 0.2, 1),
            (0.0, 0.6, 0.0, 1)
        ]
        self.start_new()

    def start_new(self):
        self.land = render.attach_new_node("Land")

    def get_color(self, z):
        return self.colors[min(z, len(self.colors) - 1)]

    def addBlock(self, position):
        block = loader.load_model(self.model)
        block.set_texture(loader.load_texture(self.texture))
        block.set_pos(position)
        color = self.get_color(int(position[2]))
        block.set_color(color)
        block.set_tag("at", str(position))
        block.reparent_to(self.land)

    def clear(self):
        self.land.remove_node()
        self.start_new()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def find_blocks(self, pos):
        return self.land.find_all_matches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.find_blocks(pos)
        return not bool(blocks)

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.add_block(new)

    def delBlock(self, position):
        for block in self.find_blocks(position):
            block.remove_node()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.find_blocks(pos):
            block.remove_node()
