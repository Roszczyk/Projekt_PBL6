# -*- coding: utf-8 -*-
# Użycie
# Ładowanie bibliotek

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

from sklearn.svm import SVC

# Ładowanie zbioru danych
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

# Tworzenie zbiorów danych uczącego i walidacyjnego
array = dataset.values
X = array[:, 0:4]
Y = array[:, 4]

validation_size = 0.20
seed = 42
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y,
                                                                                test_size=validation_size, random_state=seed)

# Określanie kryterium oceny
scoring = 'accuracy'

# Budowanie wszystkich modeli
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
models.append(('RF', RandomForestClassifier(n_estimators=100)))
models.append(('MLP', MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)))

# Szacowanie każdego modelu
results = []
names = []
best = (0, '')

for name, model in models:
    kfold = model_selection.KFold(n_splits=10, random_state=seed, shuffle=True)
    cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold,
                                                 scoring=scoring)
    results.append(cv_results)
    names.append(name)
    if cv_results.mean() > best[0]:
        best = (cv_results.mean(), name)

    msg = "%s: %f(%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)

print(f'\nNajlepszy model to: {best[1]}, z dokładnością: {best[0].mean()}')

# Kreślenie wyników modeli
figure = plt.figure()
figure.suptitle('Algorithm Comparison')
algPlot = figure.add_subplot(1, 1, 1)
plt.boxplot(results)
algPlot.set_xticklabels(names)
plt.show()


best_model = None
for name, model in models:
    if name == best[1]:
        best_model = model

# Predykcja najlepszego modelu
m = best_model
m.fit(X_train, Y_train)
predictions = m.predict(X_validation)

print(accuracy_score(Y_validation, predictions))
print(confusion_matrix(Y_validation, predictions))
print(classification_report(Y_validation, predictions))
