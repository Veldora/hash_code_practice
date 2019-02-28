import copy

class Pizza:

    def __init__(self, struct, rows, cols, p_min, p_max, slices=None, portion=None):
        self.struct = struct
        self.rows = rows
        self.cols = cols
        self.p_min = p_min
        self.p_max = p_max
        if slices is None:
            self.slices = []
        else:
            self.slices = slices
        if portion is None:
            self.portion = 0
        else: self.portion = portion

    def cut(self, start, end):
        area = (end[0] - start[0] + 1) * (end[1] - start[1] + 1)
        if area < 2 * self.p_min or area > self.p_max:
            return False
        t_m = 0
        t_t = 0
        t_portion = 0
        t_struct = copy.deepcopy(self.struct)
        for y in range(start[0], end[0] + 1):
            for x in range(start[1], end[1] + 1):
                if t_struct[y][x] is None:
                    return False
                if t_struct[y][x] == 'T':
                    t_t += 1
                else:
                    t_m += 1
                t_struct[y][x] = None
                t_portion += 1
        if t_t < self.p_min or t_m < self.p_min:
            return False
        self.struct = copy.deepcopy(t_struct)
        self.slices.append((start, end))
        self.portion += t_portion
        return True
    
    def check_not_valid(self, point):
        if point[0] < 0 or point[1] < 0 or point[0] >= self.rows or point[1] >= self.cols:
            return True
        return False

def process(pizzas, rows, cols, p_min, p_max):
    t_pizzas = []
    change = False
    for pizza in pizzas:
        gal = False
        t_pizza = copy.deepcopy(pizza)
        for y in range(rows):
            if gal:
                break
            for x in range(cols):
                if gal:
                    break
                if t_pizza.struct[y][x] is not None:
                    end = [rows - 1, cols - 1]
                    if p_max <= cols - x - 1:
                        end[1] = x + p_max
                    if p_max <= rows - y - 1:
                        end[0] = y + p_max
                        
                    for y1 in range(y, end[0] + 1):
                        for x1 in range(x, end[1] + 1):
                            if t_pizza.cut((y, x),(y1, x1)):
                                t_pizzas.append(copy.deepcopy(t_pizza))
                                t_pizza = copy.deepcopy(pizza)
                                change = True
                                gal = True
    if change:
        return process(t_pizzas, rows, cols, p_min, p_max)
    return pizzas

def load(path):
    with open(path, 'r') as f:
        datas = f.readlines()
        struct = []
        rows, cols, L, H = [int(num) for num in datas[0].strip("\n").split()]
        for i in range(1, len(datas)):
            struct.append(list(datas[i].strip("\n")))
    return struct, rows, cols, L, H

def save(path, pizza):
    with open(path, 'w') as f:
        f.write(str(len(pizza.slices)) + "\n")
        for each in pizza.slices:
            f.write("{0} {1} {2} {3}\n".format(each[0][0], each[0][1], each[1][0], each[1][1]))

def main():
    path_in = "b_small.in"
    path_out = "example.out"
    struct, rows, cols, L, H = load(path_in)
    proto = Pizza(struct, rows, cols, L, H)
    all_pz = process([proto], rows, cols, L, H)
    portions = 0
    ans = None
    for pz in all_pz:
        if pz.portion == rows * cols:
            ans = pz
            break
        if pz.portion > portions:
            portions = pz.portion
            ans = pz
    save(path_out, ans)

if __name__ == "__main__":
    main()
