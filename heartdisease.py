import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cross_validation import *
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

from itertools import cycle

import pymysql

from sklearn.linear_model import SGDClassifier


uname = ""

pymysql.install_as_MySQLdb()


def read_dataset():
    heart_df = pd.read_csv("heart_disease_data.csv",
                           names=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                                  'oldpeak', 'slope', 'ca', 'thal', 'hd'], sep=",")
    return heart_df

def pre_process_data(heart_df):

    chance_of_disease = heart_df.groupby('hd')
    #print(chance_of_disease.mean())


    #heart_df = heart_df.sort_values('hd')
    #heart_df.to_csv('sort_data.csv', encoding='utf-8', index=False)


    # to typecast float to integer
    # heart_df.sex = heart_df.sex.astype(int)
    # heart_df.cp = heart_df.cp.astype(int)
    indices = heart_df.columns

    # Typecasting float to integer
    heart_df.sex = heart_df.sex.astype(int)
    heart_df.cp = heart_df.cp.astype(int)
    heart_df.fbs = heart_df.fbs.astype(int)
    heart_df.restecg = heart_df.restecg.astype(int)
    heart_df.exang = heart_df.exang.astype(int)
    heart_df.slope = heart_df.slope.astype(int)


    # replacing number of major vessels(ca) missing data '?' with NaN(not a number)
    heart_df['ca'] = heart_df['ca'].replace('?', np.nan)

    heart_df['ca'] = pd.to_numeric(heart_df['ca'])  # Typecasting float to integer
    heart_df['ca'] = np.nan_to_num(heart_df['ca']).astype(int)

    # replacing thal missing data '?' with NaN(not a number)
    heart_df['thal'] = heart_df['thal'].replace('?', np.nan)

    heart_df['thal'] = pd.to_numeric(heart_df['thal'])  # Typecasting float to integer
    heart_df['thal'] = np.nan_to_num(heart_df['thal']).astype(int)


    thal_dummies = pd.get_dummies(heart_df['thal'])
    heart_df = heart_df.drop('thal',1)
    heart_df = pd.concat([heart_df,thal_dummies], axis = 1)

    heart_df = heart_df.drop(heart_df.columns[[13]], axis=1)
    meanCA = round(heart_df['ca'].mean())

    heart_df['ca'] = heart_df['ca'].fillna(meanCA)

def ruleset1():
    thal=3.0
    sex=1.0
    chol=286.0
    oldpeak=2.5
    thalach=124.0
    fbs=0.0
    exang=1.0
    cp=4.0
    ca=3.0
    trestbps=160.0

    pname = readPname()

    sql_attribute = "SELECT p_age,p_sex,p_cp,p_bp,p_chol,p_fsb,p_ecg,p_thalach,p_exang,p_oldpeak,p_slope,p_ca,p_thal from patient_attribute WHERE p_uname='%s'"
    try:
        conn = getConnection()
        cursor_ruleset1 = conn.cursor()
        cursor_ruleset1.execute("USE heartdisease")
        cursor_ruleset1.execute(sql_attribute % (pname))
        for row in cursor_ruleset1:
            age = row["p_age"]
            sex = row["p_sex"]
            cp = row["p_cp"]
            bp = row["p_bp"]
            chol = row["p_chol"]
            fsb = row["p_fsb"]
            ecg = row["p_ecg"]
            thalach = row["p_thalach"]
            exang = row["p_exang"]
            oldpeak = row["p_oldpeak"]
            slope = row["p_slope"]
            ca = row["p_ca"]
            thal = row["p_thal"]

    except pymysql.DatabaseError as e:
        print("Select error {0}".format(e))

    if sex == "Male":
        sex = 1
    else:
        sex = 0

    if cp == "Typical angina":
        cp = 1
    elif cp == "atypical angina":
        cp = 2
    elif cp == "Non-anginal pain":
        cp = 3
    else:
        cp = 4

    if fbs == "True":
        fbs = 1
    else:
        fbs = 0

    if exang == "Yes":
        exang = 1
    else:
        exang = 0

    if thal == "Normal":
        thal = 1
    elif thal == "Fixed defect":
        thal = 2
    else:
        thal = 3

    if slope == "unsloping":
        slope = 1
    elif slope == "flat":
        slope = 2
    else:
        slope = 3

    #ruleset1
    if (thal > 3.0 and sex <= 0.0 and chol <= 295.0):
        output = 3
    elif (sex > 0.0 and oldpeak > 2.4 and thalach <= 124.0):
        output = 3
    elif (oldpeak <= 2.4 and fbs > 0.0 and exang > 0.0):
        output = 2
    elif (thal > 3.0 and sex > 0.0 and oldpeak > 2.4 and exang <= 0.0):
        output = 4
    elif (thal <= 3.0 and oldpeak <= 2.1 and cp <= 3.0):
        output = 0
    elif (thal <= 3.0 and ca <= 0.0):
        output = 0
    elif (fbs > 0.0 and exang <= 0.0 and trestbps <= 156.0):
        output = 0
    elif (thal > 3.0 and chol > 295.0):
        output = 1
    else:
        output = 0

    #ruleset 2
    if (cp > 3.0 and fbs > 0.0 and oldpeak > 1.2):
        output2 = 2
    elif (fbs <= 0.0 and ca > 0.0 and thalach > 131.0 and trestbps>118.0 and exang>0.0):
        output2 = 4
    elif (fbs <= 0.0 and thal <= 6.0 and age > 58.0 and age<=63.0):
        output2 = 1
    elif (cp > 3.0 and ca > 0.0 and sex > 0.0 and thalach <= 131.0):
        output2 = 3
    elif (cp <= 3.0 and oldpeak <= 0.5):
        output2 = 0
    elif (fbs <= 0.0 and sex <= 0.0 and slope <= 1.0):
        output2 = 0
    elif (ca <= 0.0 and exang <= 0.0 and sex <= 0.0):
        output2 = 0
    elif (ca <= 0.0 and thal <= 6.0):
        output2 = 0
    else:
        output2 = 1


    result = max(output,output2)
    print('output ={0}'.format(result))


    if result == 0:
        result = "Normal"
    elif result == 1:
        result = "Class 1"
    elif result == 2:
        result = "Class 2"
    elif result == 3:
        result = "Class 3"
    else:
        result = "Class 4"

    return result


def getData():
    return heart_df.drop['hd',1]

def getTarget():
    return heart_df['hd']

def processHD(heart_df):
    for i in range(0, len(heart_df)):
        if heart_df['hd'].ix[i] > 1:
            heart_df['hd'].ix[i] = 1

#Training model and Testing model

def training_testing_set(heart_df):
    data = heart_df.drop('hd',1)
    target = heart_df['hd']
    X_train, X_test, Y_train, Y_test = train_test_split(data, target,test_size=0.33, random_state=0)
    return X_train , X_test, Y_train, Y_test, data , target


def SupportVectorMachine(X_train, X_test, Y_train, Y_test, data, target):

    model = SVC(kernel = 'linear', C = 2)
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)
    print(metrics.accuracy_score(Y_test,predictions))
    scores = cross_val_score(model,data,target, cv=10)
    acc = scores.mean() * 100
    acc = acc.tolist()
    global SVM_accuracy
    SVM_accuracy = acc


def RandomForest(X_train, X_test, Y_train, Y_test, data, target):

    rfc = RandomForestClassifier(n_estimators = 10)
    rfc.fit(X_train, Y_train)
    predictions = rfc.predict(X_test)
    print(metrics.accuracy_score(Y_test, predictions))
    scores = cross_val_score(rfc,data,target,cv = 15)
    acc = scores.mean() * 100
    acc = acc.tolist()
    global RF_accuracy
    RF_accuracy = acc


def readPname():
    f = open('u', 'r')
    pname = f.read()
    f.close()
    return pname

def getConnection():
    try:
        conn = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='root',
                                    db='heartdisease',
                                    cursorclass=pymysql.cursors.DictCursor)  # connect to database
        print("connection to Database ok")
        return conn

    except pymysql.DatabaseError as e:
        print("Connection to database Error {0}".format(e))


def getAccuracy():
    result =ruleset1()
    Accuracy_SVM = SVM_accuracy
    Accuracy_RF = RF_accuracy
    pname = readPname()


    sql = "UPDATE patient_attribute SET p_result='%s', p_svm=%s ,p_rf=%s WHERE p_uname='%s'"
    try:
        conn = getConnection()
        cursor_acc = conn.cursor()
        cursor_acc.execute("USE heartdisease")
        cursor_acc.execute(sql % (result, Accuracy_SVM, Accuracy_RF, pname))
        conn.commit()

    except pymysql.DatabaseError as e:
        print("Update Database {0}".format(e))



def main():
    heart_df=read_dataset()
    pre_process_data(heart_df)
    processHD(heart_df)
    X_train, X_test, Y_train, Y_test, data, target = training_testing_set(heart_df)
    SupportVectorMachine(X_train, X_test, Y_train, Y_test, data, target)
    RandomForest(X_train, X_test, Y_train, Y_test, data, target)
    getAccuracy()


if __name__=="__main__":
    main()