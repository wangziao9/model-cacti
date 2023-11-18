import pickle
results = pickle.load(open("results3.pkl",'rb'))
asso, cs, access, cycle, dynread, dynwrite, leak, gateleak = list(zip(*results))

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import math

# Assuming your data is stored in a list of tuples (x, y, z)
data = []
for x, y, _, z, _, _, _, _ in results:
    try:
        data.append((math.log(x, 2), math.log(y, 2), z))
    except ValueError:
        print(x,y,z)

# Split the data into training and testing sets
train_data, test_data = train_test_split(data, test_size=0.5, random_state=42)

# Separate features (log(x) and log(y)) and target variable (z)
X_train = np.array([(x, y) for x, y, z in train_data])
y_train = np.array([z for x, y, z in train_data])

X_test = np.array([(x, y) for x, y, z in test_data])
y_test = np.array([z for x, y, z in test_data])

# Create and train the KNN model
knn_model = KNeighborsRegressor(n_neighbors=5)  # You can adjust the number of neighbors
knn_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = knn_model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
fig = plt.figure()
ax = plt.axes(projection ='3d')

ax.scatter(X_test[:,0], X_test[:,1], y_pred, c='purple', label="cycle time pred (ns)")
ax.scatter(X_test[:,0], X_test[:,1], y_test, c='green', label="cycle time real (ns)")
ax.set_xlabel("log associativity")
ax.set_ylabel("log cache size")
ax.set_zlabel("value")
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.legend()
plt.show()