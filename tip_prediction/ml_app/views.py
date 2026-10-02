import joblib
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.shortcuts import render

from .forms import PredictionForm

BASE_DIR = Path(settings.BASE_DIR).resolve().parent
MODEL_CANDIDATES = [
    BASE_DIR / 'ml_project' / 'models' / 'linear_regression_model.pkl',
    BASE_DIR / 'ml_project' / 'model' / 'tip_model.pkl',
]

MODEL = None
for model_path in MODEL_CANDIDATES:
    if model_path.exists():
        MODEL = joblib.load(model_path)
        break

if MODEL is None:
    raise FileNotFoundError('No trained model file found in ml_project/models or ml_project/model.')


def _encode_input(data):
    feature_names = MODEL.feature_names_in_
    encoded = {
        'total_bill': float(data['total_bill']),
        'size': int(data['size']),
        'sex_Male': 1 if data['sex'] == 'Male' else 0,
        'sex_Female': 1 if data['sex'] == 'Female' else 0,
        'smoker_Yes': 1 if data['smoker'] == 'Yes' else 0,
        'smoker_No': 1 if data['smoker'] == 'No' else 0,
        'day_Thur': 1 if data['day'] == 'Thur' else 0,
        'day_Fri': 1 if data['day'] == 'Fri' else 0,
        'day_Sat': 1 if data['day'] == 'Sat' else 0,
        'day_Sun': 1 if data['day'] == 'Sun' else 0,
        'time_Lunch': 1 if data['time'] == 'Lunch' else 0,
        'time_Dinner': 1 if data['time'] == 'Dinner' else 0,
    }
    return pd.DataFrame([encoded], columns=feature_names)


def landing_page(request):
    return render(request, 'ml_app/landing.html')


def home(request):
    result = None
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            features = _encode_input(form.cleaned_data)
            prediction = MODEL.predict(features)[0]
            result = round(float(prediction), 2)
    else:
        form = PredictionForm()

    return render(request, 'ml_app/home.html', {'form': form, 'result': result})
