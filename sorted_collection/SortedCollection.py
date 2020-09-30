from bisect import bisect_left, bisect_right


# (bisect usa la ricerca binaria)
# key: funzione usata per stabilire l'ordinamento, idea presa da https://docs.python.org/3.3/howto/sorting.html
class SortedCollection:
    def __init__(self, key):
        self.key = key
        self.keys = []
        self.items = []

    def get_item(self, i):
        return self.items[i]

    def index(self, item):
        k = self.key(item)
        i = bisect_left(self.keys, k)
        j = bisect_right(self.keys, k)
        return self.items[i:j].index(item) + i

    def insert(self, item):
        k = self.key(item)
        i = bisect_left(self.keys, k)
        self.keys.insert(i, k)
        self.items.insert(i, item)

    def remove(self, item):
        i = self.index(item)
        del self.keys[i]
        del self.items[i]

    def find(self, k):
        i = bisect_left(self.keys, k)
        if i != len(self.keys) and self.keys[i] == k:
            return self.items[i]
        raise ValueError('Oggetto non trovato.')

    # Trova l'ultimo elemento con chiave < k
    def find_lesser(self, k):
        i = bisect_left(self.keys, k)
        if i:
            return self.items[i - 1]
        raise ValueError('Oggetto non trovato')

    # Trova il primo elemento con chiave >= k
    def find_greater_equal(self, k):
        i = bisect_left(self.keys, k)
        if i != len(self.keys):
            return self.items[i]
        raise ValueError('Oggetto non trovato')

    # Trova il primo elemento con chiave >=k
    def find_greater(self, k):
        i = bisect_right(self.keys, k)
        if i != len(self.keys):
            return self.items[i]
        raise ValueError('Oggetto non trovato')

    # Faccio due ricerche binarie -> O(log(n))
    def find_between_range(self, lower_bound, upper_bound):
        lower_bound_i = bisect_left(self.keys, lower_bound)
        upper_bound_i = bisect_right(self.keys, upper_bound, lo=lower_bound_i)
        return self.items[lower_bound_i: upper_bound_i]
