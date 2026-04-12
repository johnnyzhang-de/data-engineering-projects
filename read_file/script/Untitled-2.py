arr = [1,1,2,2,3,3,3]

from collections import Counter

count = Counter(arr)
print(count.most_common(1))
