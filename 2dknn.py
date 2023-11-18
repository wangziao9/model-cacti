# local linear regression?

import pickle
results = pickle.load(open("results.pkl",'rb'))
asso, cs, access, cycle, dynread, dynwrite, leak, gateleak = list(zip(*results))
cs_samps_per_asso = asso.index(2)

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import math

associativities = [1,2,4,8,16]
for i,asso in enumerate(associativities):
    result = []
    for tup in results:
        if tup[0] == asso:
            result.append(tup)
    data = np.array([[math.log(y, 2), z] for _, y, _, z, _, _, _, _  in result])
    train_data, test_data = train_test_split(data, test_size=0.5, random_state=42)
    
    X_train = train_data[:,0:1]
    y_train = train_data[:,1]

    X_test = test_data[:,0:1]
    y_test = test_data[:,1]
    
    # Create and train the KNN model
    knn_model = KNeighborsRegressor(n_neighbors=3)  # You can adjust the number of neighbors
    knn_model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = knn_model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Associativity: {asso}, Mean Squared Error: {mse}')

    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    fig = plt.figure()
    fig.set_size_inches(12, 8)
    ax = plt.axes()

    X_draw = np.linspace(12, 27, 1500)
    y_draw = knn_model.predict(X_draw.reshape(-1,1))
    #ax.scatter(X_test[:,0], y_pred, c='purple', marker='o', label="cycle time pred (ns)")
    ax.plot(X_draw, y_draw, c='purple')
    ax.scatter(X_test[:,0], y_test, c='green', marker='x', label="testing points")
    ax.scatter(X_train[:,0], y_train, c='purple', marker='x', label="training points")
    ax.set_xlabel("log cache size")
    ax.set_ylabel("cycle time (ns)")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(f"KNN model, associativity={asso}, {len(X_train)} training points, {len(X_test)} testing points, mse={'%.4f'%mse}")
    plt.legend()
    plt.savefig(f"plots/asso_{asso}.png")
    plt.close()