from django.shortcuts import render
from django.http import HttpResponse
from pickle import load
import pandas as pd
# Create your views here.
def index(request):
    return render(request,'churn/index.html')
def result(request):
    post_data = dict(request.POST.lists())
    vals=pd.DataFrame.from_dict(post_data)
    
    #vals=vals.apply(lambda x :x[0])
    X=pd.get_dummies(vals)
    X = X.reindex(labels = ['Zip Code', 'Tenure Months', 'Monthly Charges', 'Total Charges',
       'Gender_Male', 'Senior Citizen_Yes', 'Partner_Yes', 'Dependents_Yes',
       'Phone Service_Yes', 'Multiple Lines_No phone service',
       'Multiple Lines_Yes', 'Internet Service_Fiber optic',
       'Internet Service_No', 'Online Security_No internet service',
       'Online Security_Yes', 'Online Backup_No internet service',
       'Online Backup_Yes', 'Device Protection_No internet service',
       'Device Protection_Yes', 'Tech Support_No internet service',
       'Tech Support_Yes', 'Streaming TV_No internet service',
       'Streaming TV_Yes', 'Streaming Movies_No internet service',
       'Streaming Movies_Yes', 'Contract_One year', 'Contract_Two year',
       'Paperless Billing_Yes', 'Payment Method_Credit card (automatic)',
       'Payment Method_Electronic check', 'Payment Method_Mailed check'], axis = 1, fill_value = 0)
    print(X.shape)
    # load the model
    model = load(open('churn/model.pkl', 'rb'))   
    # load the scaler
    scaler = load(open('churn/scaler.pkl', 'rb'))
    
    X=scaler.transform(X)
    print(model.predict_proba(X))
    return render(request,'churn/result.html',{'prediction':model.predict_proba(X)[0][1]*100})