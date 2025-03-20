# meta_algebra.py

from julia import Main

# Load the sets32.jl file
Main.include("HllSets/src/HllSets.jl")

Main.using(".HllSets")

class HllSet:
    def __init__(self, P=10):
        """
        Initialize an HllSet with a given precision P.
        """
        self.P = P
        self.hll = Main.HllSet(P)  # Create a new HllSet in Julia

    def add(self, element):
        """
        Add an element to the HllSet.
        """
        # Use getattr to call the Julia function with '!'
        add_func = getattr(Main, "add!")
        add_func(self.hll, element)

    def count(self):
        """
        Estimate the cardinality of the HllSet.
        """
        return Main.count(self.hll)

    def union(self, other):
        """
        Perform a union with another HllSet.
        """
        result = Main.union(self.hll, other.hll)
        return HllSet.from_julia(result)

    def intersection(self, other):
        """
        Perform an intersection with another HllSet.
        """
        result = Main.intersect(self.hll, other.hll)
        return HllSet.from_julia(result)

    def difference(self, other):
        """
        Perform a difference with another HllSet.
        """
        result = Main.diff(self.hll, other.hll)
        return HllSet.from_julia(result)

    def complement(self, other):
        """
        Perform a complement operation with another HllSet.
        """
        result = Main.set_comp(self.hll, other.hll)
        return HllSet.from_julia(result)

    @classmethod
    def from_julia(cls, julia_hll):
        """
        Create a Python HllSet from a Julia HllSet.
        """
        hll = cls()
        hll.hll = julia_hll
        return hll

    def __repr__(self):
        return f"HllSet(P={self.P}, count={self.count()})"