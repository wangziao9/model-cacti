import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
fig = plt.figure()
ax = plt.axes(projection ='3d')

import pickle
results = pickle.load(open("results.pkl",'rb'))
asso, cs, access, cycle, dynread, dynwrite, leak, gateleak = list(zip(*results))

cs = [math.log(item,2) for item in cs]
ax.scatter(asso, cs, access, c='red', label="access time (ns)")
ax.scatter(asso, cs, cycle, c='purple', label="cycle time (ns)")
ax.scatter(asso, cs, dynread, c='green', label="dynamic read (nJ)")
ax.scatter(asso, cs, dynwrite, c='blue', label="dynamic write (nJ)")
ax.scatter(asso, cs, leak, c='green', label="leakage (nJ)")
ax.scatter(asso, cs, gateleak, c='blue', label="leakage (nJ)")
ax.set_xlabel("associativity")
ax.set_ylabel("log cache size")
ax.set_zlabel("value")
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.legend()
plt.show()