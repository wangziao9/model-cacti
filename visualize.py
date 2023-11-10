import matplotlib.pyplot as plt
fig = plt.figure()
ax = plt.axes(projection ='3d')

import pickle
results = pickle.load(open("results.pkl",'rb'))
x, y, access, cycle, dynread, dynwrite, leak, gateleak = list(zip(*results))

ax.scatter(x, y, access, c='red', label="access time (ns)")
ax.scatter(x, y, cycle, c='yellow', label="cycle time (ns)")
ax.scatter(x, y, dynread, c='green', label="dynamic read (nJ)")
ax.scatter(x, y, dynwrite, c='blue', label="dynamic write (nJ)")
ax.set_xlabel("log associativity")
ax.set_ylabel("log cache size")
ax.set_zlabel("value")
plt.legend()
plt.show()