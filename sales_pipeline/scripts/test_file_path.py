import os

print("===== PATH DEBUG =====")

print("__file__ =", __file__)
print("abspath =", os.path.abspath(__file__))

level1 = os.path.dirname(os.path.abspath(__file__))
print("dirname level1 =", level1)

level2 = os.path.dirname(level1)
print("dirname level2 =", level2)

BASE_DIR = level2
print("BASE_DIR =", BASE_DIR)

UNPROCESSED_DIR = os.path.join(BASE_DIR, "data", "unprocessed")
print("UNPROCESSED_DIR =", UNPROCESSED_DIR)

print("======================")