""" Tyler Zheng
    ITP-449
    Final Project - 1
    Description: This program will predict the quality of wine given the other attributes.
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def wine_quality():
    pd.set_option('display.width', None)
    file_path = "winequality.csv"
    df_wines = pd.read_csv(file_path)
    print('1. The data is loaded\n')

    x = df_wines.drop(['Quality'], axis=1)
    y = df_wines['Quality']

    norm = StandardScaler()
    X = pd.DataFrame(norm.fit_transform(x), columns=x.columns)
    # print(X.head())
    print('2. All variables other than Quality are standardized\n')

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=0.6, random_state=42, stratify=y)
    X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, train_size=0.5, random_state=42,
                                                        stratify=y_temp)
    print('3. The dataset is partitioned:\n\ta. random_state=42\n\tb. Partitions 60/20/20\n\tc. Stratify\n')

    score_train_list = []
    score_valid_list = []
    ks = []
    for i in range(1, 31):
        k = i
        ks.append(k)
        # import and instantiate algorithm
        model_knn = KNeighborsClassifier(n_neighbors=k)
        model_knn.fit(X_train, y_train)
        # y_pred = model_knn.predict(X_valid)
        score_train = model_knn.score(X_train, y_train)
        score_valid = model_knn.score(X_valid, y_valid)

        score_train_list.append(score_train)
        score_valid_list.append(score_valid)

    plt.plot(ks, score_train_list)
    plt.plot(ks, score_valid_list)
    plt.xlabel('Number of K Nerghbors')
    plt.ylabel('Accuracy Score')
    plt.legend(['Training Partition', 'Validation Partition'])
    plt.title('Accuracy Score vs K\'s')
    plt.tight_layout()
    plt.savefig('Accuracy Score.png')
    print(
        '5. The plot for the accuracy scores for both the training and validation datasets is shown in Accuracy Score.png\n')

    print('6. From the plot produced in 5, when k=15, it produces the best accuracy\n')
    model_knn_new = KNeighborsClassifier(n_neighbors=15)
    model_knn_new.fit(X_train, y_train)
    y_pred_test = model_knn.predict(X_test)

    cm = confusion_matrix(y_test, y_pred_test, labels=model_knn_new.classes_)
    print('7. The confusion matrix for the test partition is:\n', cm)
    cm_disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model_knn_new.classes_)
    fig, ax1 = plt.subplots()  # figsize=(10,10))
    cm_disp.plot(ax=ax1)
    plt.savefig('wine_cm.png')
    print(
        '   The confusion matrix for the test partition of the actual vs predcited wine quality is shown in wine_cm.png\n')

    score_test = model_knn_new.score(X_test, y_test)
    print('8. The accuracy score of the model on the test dataset is', score_test, '\n')

    wine_train, wine_temp, y_train, y_temp = train_test_split(df_wines, y, train_size=0.6, random_state=42, stratify=y)
    wine_valid, wine_test, y_valid, y_test = train_test_split(wine_temp, y_temp, train_size=0.5, random_state=42,
                                                              stratify=y_temp)
    wine_test['Predicted Quality'] = y_pred_test
    print('9. The test dataframe with the added columns is:\n', wine_test)


if __name__ == '__main__':
    wine_quality()