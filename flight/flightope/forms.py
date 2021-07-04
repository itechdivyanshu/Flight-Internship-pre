from django import forms
from .models import *

class visualizations(forms.Form):
    flights_no_choice = [
        ('A', 'ALL'),
        ('B', '0 - 5'),
        ('C', '6 - 13'),
    ]
    no_of_flights = forms.ChoiceField(choices = flights_no_choice)
    type_c=list(aircraft.objects.values('type'))
    type_choice=[
        ('ALL', 'ALL'),
    ]
    for i in type_c:
        type_choice.append((i['type'],i['type']))
    type = forms.ChoiceField(choices = type_choice,label='Aircraft Type')
    city_c=list(city.objects.values('name'))
    city_choice=[]
    for i in city_c:
        city_choice.append((i['name'],i['name']))
    city = forms.MultipleChoiceField(choices = city_choice,label='Cities covered')

    def save(self):
        return self.cleaned_data
