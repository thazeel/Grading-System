import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

ml_data = pd.read_csv("ML.csv")
print(ml_data.head())

x = ml_data[["Debt", "Deficit", "Inflation", "Unemployment"]]
y = ml_data["GDP"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=100)

mlr = LinearRegression()
mlr.fit(x_train, y_train)

print("GDP = ", mlr.intercept_, " + (", mlr.coef_[0], "* Debt ) + (", mlr.coef_[1], "* Deficit ) + (", mlr.coef_[2], " * Inflation ) + (", mlr.coef_[3], " * Unemployment ) + e")

y_pred_mlr = mlr.predict(x_test)
mlr_diff = pd.DataFrame({"Actual Value": y_test, "Predicted Value": y_pred_mlr})
print(mlr_diff.head())

meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
RootmeanSqErr = np.sqrt(meanSqErr)

print("R Squared Value = {:.2f}".format(mlr.score(x, y)*100))
print("Mean Absolute Error = ", meanAbErr)
print("Mean Squared Error = ", meanSqErr)
print("Root Mean Squared Error = ", RootmeanSqErr)
