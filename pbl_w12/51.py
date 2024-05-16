# -*- coding: utf-8 -*-
# Użycie
# ładowanie bibliotek

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ładowanie zbioru danych
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

# Wyświetlanie kształtu
print('Dataset dimensions')
print(dataset.shape)

# Wyświetlanie pierwszej części zbioru danych
print('Head of the data')
print(dataset.head(20))

# Wyświetlanie statystyk danych
print('Statistics')
print(dataset.describe())

# Wyświetlanie rozkładu klas
print('Class distribution')
print(dataset.groupby('class').size())

# Wyświetlanie danych na wykresach pudełkowych z wąsami
dataset.plot.box(layout=(2, 2), sharex=False, sharey=False)
plt.show()

# Wizualizacja danych na histogramach
dataset.hist()
plt.show()

# Wizualizacja danych na wykresach punktowych
scatter_matrix(dataset)
plt.show()

# Przygotowanie danych do klasyfikacji
array = dataset.values
X = array[:, 0:4]
y = array[:, 4]

# Podział danych na zestaw treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tworzenie modelu lasu losowego
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Dokonanie predykcji na zestawie testowym
predictions = model.predict(X_test)

print('Raport:')
print(classification_report(y_test, predictions))

print('Accuracy:')
print(accuracy_score(y_test, predictions))
