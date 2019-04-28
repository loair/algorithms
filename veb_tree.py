import math


# basic veb tree
class T:
    def __init__(self, u):
        self.min = None
        self.max = None
        self.cluster = []
        self.summary = None
        # print(u)
        if u <= 2:
            self.u = 2

        else:
            self.u = self.get_u(u)
            high = self.high(self.u)
            print(high)
            for i in range(high):
                self.cluster.append(T(high))
            self.summary = T(high)

    @staticmethod
    def get_u(n):
        return 2 ** (math.ceil(math.log(n, 2)))

    def low(self, x):
        u = 2 ** (math.floor(math.log(self.u, 2) / 2))
        return x % u

    # define the cluster index
    def high(self, x):
        u = 2 ** (math.floor(math.log(self.u, 2) / 2))
        return math.floor(x / u)

    def index(self, x, y):
        u = 2 ** (math.floor(math.log(self.u, 2) / 2))
        return x * u + y

    def empty_insert(self, x):
        self.min = x
        self.max = x

    def insert(self, x):
        if self.min is None:
            self.empty_insert(x)
        elif x < self.min:
            temp = self.min
            self.min = x
            x = temp

        elif self.u > 2:
            high = self.high(x)
            low = self.low(x)
            # print("high = " + str(high))
            # print("low = " + str(low))
            # print("index = " + str(self.index(high, low)))

            if self.cluster[high].minimum() is None:
                self.summary.insert(high)
                self.cluster[high].empty_insert(low)
            else:
                self.cluster[high].insert(low)
        if x > self.max:
            self.max = x

    def minimum(self):
        return self.min

    def maximum(self):
        return self.max

    def successor(self, x):
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            else:
                return None

        elif self.min is not None and x < self.min:
            return self.min

        else:
            high = self.high(x)
            low = self.low(x)
            max_low = self.cluster[high].maximum()
            if max_low is not None and low < max_low:
                offset = self.cluster[high].successor(low)
                return self.index(high, offset)
            else:
                succ_cluster = self.summary.successor(high)
                if succ_cluster is None:
                    return None
                else:
                    succ_cluster = int(succ_cluster)
                    offset = self.cluster[succ_cluster].minimum()
                    return self.index(succ_cluster, offset)

    def predecessor(self, x):
        if self.u == 2:
            if x == 1 and self.min == 0:
                return 0
            else:
                return None

        elif self.max is not None and x > self.max:
            return self.max

        else:
            high = self.high(x)
            low = self.low(x)
            min_low = self.cluster[high].minimum()
            if min_low is not None and low > min_low:
                offset = self.cluster[high].predecessor(low)
                return self.index(high, offset)
            else:
                pred_cluster = self.summary.predecessor(high)
                if pred_cluster is None:
                    if self.min is not None and x > self.min:
                        return self.min
                    else:
                        return None
                else:
                    offset = self.cluster[pred_cluster].maximum()
                    return self.index(pred_cluster, offset)

    def delete(self, x):
        # print("delete " + str(x))
        if self.min == self.max:
            self.min = None
            self.max = None
        elif self.u == 2:
            if x == 0:
                self.min = 1
            else:
                self.min = 0
            self.max = self.min
        else:
            high = self.high(x)
            low = self.low(x)
            if x == self.min:
                first_cluster = self.summary.minimum()
                x = self.index(first_cluster, self.cluster[first_cluster].minimum())
                self.min = x

            self.cluster[high].delete(low)
            if self.cluster[high].minimum() is None:
                self.summary.delete(high)
                if x == self.max:
                    summary_max = self.summary.maximum()
                    if summary_max is None:
                        self.max = self.min
                    else:
                        self.max = self.index(summary_max, self.cluster[summary_max].maximum())

            elif x == self.max:
                self.max = self.index(high, self.cluster[high].maximum())

    def __str__(self):
        a = [self.min]
        successor = self.successor(self.min)
        while successor:
            a.append(successor)
            successor = self.successor(successor)
        return str(a)

    def extract_max(self):
        m = self.maximum()
        self.delete(m)
        return m


# veb tree values with keys
class VebTree:
    def __init__(self, u):
        self.keys = T(u)
        self.values = [None] * u

    def insert(self, value, key):
        self.values[key] = value
        self.keys.insert(key)

    def extract_max(self):
        key = self.keys.extract_max()
        m = self.values[key]
        self.values[key] = None
        return m

    def increase_key(self, value, key):
        if self.values[key] is not None:
            raise ValueError("key = " + str(key) + " already exists")

        key_0 = self.values.index(value)

        self.values[key_0] = None
        self.values[key] = value

        self.keys.delete(key_0)
        self.keys.insert(key)


# Test

arr = [2, 3, 4, 5, 7, 10]


t = T(10)

for a in arr:
    print("insert " + str(a))
    t.insert(a)

print("..................")
print(t.u)
print(t)
print(t.successor(4))
print(t.predecessor(4))
print(t.extract_max())
print(t)
