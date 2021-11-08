from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
import pickle
import numpy as np


app = Flask(__name__)
cors=CORS(app)
df = pd.read_csv('cleaned_car.csv')
model = pickle.load(open("LR_MODEL.pkl", "rb"))


@app.route('/', methods=['GET', 'POST'])
def index():
    companies = sorted(df['company'].unique())
    companies.insert(0, "select company")
    car_models = sorted(df['name'].unique())
    year = sorted(df['year'].unique())
    fuel_type = sorted(df['fuel_type'].unique())
    return render_template('index.html', companies=companies, car_models=car_models,
                            years=year, fuel_types=fuel_type)



@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    company = request.form.get('company')
    car_model = request.form.get('car_models')
    year = int(request.form.get('year'))
    fuel_type = request.form.get('fuel_type')
    kms_driven = int(request.form.get('kilo_driven'))
    predicion = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]],
                                           columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))
    # print(predicion)
    # print(company, car_model, year, fuel_type, kms_driven)
    return str(np.round(predicion[0], 2))



if __name__ == "__main__":
    app.run()
