# K Means Clustering Algorithm

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

data = pd.read_csv("Country.csv")
print(data)
# Shows the data set

plt.scatter(data["Longitude"], data["Latitude"])
plt.xlim(-180, 180)
plt.ylim(-90, 90)
plt.show()

x = data.iloc[:, 2:4].values

# Finding optimum value of K for Clustering using "Within Cluster Sum of Squares" Method
wcss_list = []

for i in range(1, 7):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    wcss_list.append(kmeans.inertia_)

plt.plot(range(1, 7), wcss_list)
plt.show()
# As seen in graph, sharp turning occurs at k = 3. Hence, that is the desired value of K

# Now Clustering the data
kmeans = KMeans(3)
kmeans.fit(x)

# Displaying Results
identified_clusters = kmeans.fit_predict(x)
print(identified_clusters)

data_with_clusters = data.copy()
data_with_clusters["Clusters"] = identified_clusters
plt.scatter(data_with_clusters["Longitude"], data_with_clusters["Latitude"], c=data_with_clusters["Clusters"], cmap="rainbow")
plt.show()
