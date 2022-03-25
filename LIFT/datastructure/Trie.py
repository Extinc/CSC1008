from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.isEnd = False
        self.child = {}


class Trie:
    __slots__ = ('children', 'freq', 'name', 'top5')

    def __init__(self):
        self.children = defaultdict(Trie)
        self.freq = 0
        self.name = None
        self.top5 = []

    def __getitem__(self, suffix):
        node = self
        for letter in suffix:
            node = node.children[letter]
        return node

    def computetop5(self):
        candidates = []
        for letter, child in self.children.items():
            child.computetop5()
            candidates.extend(child.top5)
        if self.name is not None:
            candidates.append((self.freq, self.name))
        candidates.sort(reverse=True)
        self.top5 = candidates[:5]

    def insert(self, freq, name):
        node = self[name]
        node.freq += freq
        node.name = name
