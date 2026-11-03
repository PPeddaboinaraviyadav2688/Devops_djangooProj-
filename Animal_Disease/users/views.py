from ast import alias
from concurrent.futures import process
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages



from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import datetime as dt
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import classification_report


# Create your views here.

def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})
print("UserRegisterActions")
def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})
print("UserlogincheckActions")


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})

def DatasetView(request):
    path = settings.MEDIA_ROOT + "//" + 'animal_disease_dataset.csv'
    df = pd.read_csv(path)
    df = df.to_html
    return render(request, 'users/viewdataset.html', {'data': df})
print("dataset")
####################################################################################################################
from django.shortcuts import render

# Create your views here.
import pandas as pd
import os
from django.conf import settings
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np
from sklearn.ensemble import  RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from django.shortcuts import render
import joblib
# Load dataset
df = pd.read_csv(r'media\animal_disease_dataset.csv')
# Initialize individual LabelEncoders for each categorical column
le_animal = LabelEncoder()
le_age = LabelEncoder()
le_symptom1 = LabelEncoder()
le_symptom2 = LabelEncoder()
le_symptom3 = LabelEncoder()
le_disease = LabelEncoder()

# Fit and transform the categorical features
df['Animal'] = le_animal.fit_transform(df['Animal'])
df['Age'] = le_age.fit_transform(df['Age'])
df['Symptom 1'] = le_symptom1.fit_transform(df['Symptom 1'])
df['Symptom 2'] = le_symptom2.fit_transform(df['Symptom 2'])
df['Symptom 3'] = le_symptom3.fit_transform(df['Symptom 3'])
df['Disease'] = le_disease.fit_transform(df['Disease'])
# Train-test split
X = df.drop('Disease', axis=1)
y = df['Disease']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Initialize and train the RandomForest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
# Save the trained model and the encoders
joblib.dump(rf_model, 'rf_model.pkl')
joblib.dump(le_animal, 'le_animal.pkl')
joblib.dump(le_age, 'le_age.pkl')
joblib.dump(le_symptom1, 'le_symptom1.pkl')
joblib.dump(le_symptom2, 'le_symptom2.pkl')
joblib.dump(le_symptom3, 'le_symptom3.pkl')
joblib.dump(le_disease, 'le_disease.pkl')

def training(request):
    

    # Model evaluation
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    report = classification_report(y_test, y_pred)
    print(report)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Plot the confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()


    # Get user input from the request (POST method)
    # if request.method == 'POST':
        # animal = request.POST['animal_input']
        # age = request.POST['age_input']
        # temperature = float(request.POST['temperature_input'])  # assuming temperature is a number
        # symptom1 = request.POST['symptom1_input']
        # symptom2 = request.POST['symptom2_input']
        # symptom3 = request.POST['symptom3_input']

        # Load the trained model and encoders
        # rf_model = joblib.load('rf_model.pkl')
        # le_animal = joblib.load('le_animal.pkl')
        # le_age = joblib.load('le_age.pkl')
        # le_symptom1 = joblib.load('le_symptom1.pkl')
        # le_symptom2 = joblib.load('le_symptom2.pkl')
        # le_symptom3 = joblib.load('le_symptom3.pkl')
        # le_disease = joblib.load('le_disease.pkl')

        # # Transform user input using the label encoders
        # animal_encoded = le_animal.transform([animal])[0]
        # age_encoded = le_age.transform([age])[0]
        # symptom1_encoded = le_symptom1.transform([symptom1])[0]
        # symptom2_encoded = le_symptom2.transform([symptom2])[0]
        # symptom3_encoded = le_symptom3.transform([symptom3])[0]

        # # Create input array for the prediction
        # user_input = np.array([[animal_encoded, age_encoded, temperature, symptom1_encoded, symptom2_encoded, symptom3_encoded]])

        # # Predict the disease based on user input
        # predicted_disease = rf_model.predict(user_input)
        # predicted_disease_label = le_disease.inverse_transform(predicted_disease)

        # Return the prediction to the template
    context = {
        'acc': accuracy,
        'report': report,
        # 'predicted_disease': predicted_disease_label[0]
    }
    return render(request, 'users/training.html', context)
    # else:
    #     return render(request,'ml.html')

    
def prediction(request):
    import joblib
    import numpy as np

    if request.method == 'POST':
        # Retrieve input values from the form (replace 'animal_input', etc. with your form field names)
        animal = request.POST['animal_input']
        age = request.POST['age_input']
        temperature = float(request.POST['temperature_input'])  # assuming temperature is a number
        symptom1 = request.POST['symptom1_input']
        symptom2 = request.POST['symptom2_input']
        symptom3 = request.POST['symptom3_input']

        # Load the trained model and encoders
        rf_model = joblib.load('rf_model.pkl')
        le_animal = joblib.load('le_animal.pkl')
        le_age = joblib.load('le_age.pkl')
        le_symptom1 = joblib.load('le_symptom1.pkl')
        le_symptom2 = joblib.load('le_symptom2.pkl')
        le_symptom3 = joblib.load('le_symptom3.pkl')
        le_disease = joblib.load('le_disease.pkl')

        # Transform user input using the label encoders
        animal_encoded = le_animal.transform([animal])[0]
        age_encoded = le_age.transform([age])[0]
        symptom1_encoded = le_symptom1.transform([symptom1])[0]
        symptom2_encoded = le_symptom2.transform([symptom2])[0]
        symptom3_encoded = le_symptom3.transform([symptom3])[0]

        # Create input array for the prediction
        user_input = np.array([[animal_encoded, age_encoded, temperature, symptom1_encoded, symptom2_encoded, symptom3_encoded]])

        # Predict the disease based on user input
        predicted_disease = rf_model.predict(user_input)
        predicted_disease_label = le_disease.inverse_transform(predicted_disease)
        print('predicted label',predicted_disease_label)

        return render(request,'users/predictForm.html', {'output': predicted_disease_label})

    return render(request,'users/predictForm.html')
    ####

