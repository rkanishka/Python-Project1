class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        return f"{self.feet} feet, {self.inches} inches"

    def to_inches(self):
        return self.feet * 12 + self.inches

    def __lt__(self, other):
        return self.to_inches() < other.to_inches()

    def __le__(self, other):
        return self.to_inches() <= other.to_inches()

    def __eq__(self, other):
        return self.to_inches() == other.to_inches()

    def __gt__(self, other):
        return self.to_inches() > other.to_inches()

    def __ge__(self, other):
        return self.to_inches() >= other.to_inches()

    def __ne__(self, other):
        return self.to_inches() != other.to_inches()

# Test cases
h1 = Height(5, 10)
h2 = Height(5, 11)
h3 = Height(5, 10)

print(f"{h1} < {h2}:", h1 < h2)  # Should be True
print(f"{h1} <= {h2}:", h1 <= h2)  # Should be True
print(f"{h1} == {h3}:", h1 == h3)  # Should be True
print(f"{h2} > {h1}:", h2 > h1)  # Should be True
print(f"{h2} >= {h1}:", h2 >= h1)  # Should be True
print(f"{h1} != {h2}:", h1 != h2)  # Should be True
print(f"{h1} != {h3}:", h1 != h3)  # Should be False