from django import forms


class PredictionForm(forms.Form):
    total_bill = forms.FloatField(label='Total Bill', min_value=0.0, widget=forms.NumberInput(attrs={'step': '0.01'}))
    sex = forms.ChoiceField(label='Sex', choices=[('Male', 'Male'), ('Female', 'Female')])
    smoker = forms.ChoiceField(label='Smoker', choices=[('Yes', 'Yes'), ('No', 'No')])
    day = forms.ChoiceField(label='Day', choices=[('Thur', 'Thur'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun')])
    time = forms.ChoiceField(label='Time', choices=[('Lunch', 'Lunch'), ('Dinner', 'Dinner')])
    size = forms.IntegerField(label='Party Size', min_value=1, max_value=20)

