from django.shortcuts import render
from .models import *
from .forms import visualizations
from geopy.geocoders import Nominatim
import folium

# Create your views here.
def home(request):
    dict1 = {'title':'Flight Operations'}
    flight = flights.objects.all()
    dict1['flight'] = flight
    form = visualizations(request.POST or None)
    geolocator = Nominatim(user_agent="Flight_Operations")
    dict1['form'] = form
    if form.is_valid():
        data = form.save()
        location = data.get('city')
        geolocation=[]
        for i in location:
            geolocation.append(geolocator.geocode(i))
        fromlocation = geolocator.geocode("175 5th Avenue NYC")
        m = folium.Map(width=855,height=500)
        for loc in geolocation:
            folium.Marker([loc.latitude,loc.longitude], tooltip='click here for more', popup=loc.address,
                icon=folium.Icon(color='blue', icon='plane'),
            ).add_to(m)
        type_id = ['ALL','Airbus','Jets','Narrow Body Aircraft']
        if data.get('type') != 'ALL':            
            flight=flight.filter(airtype=type_id.index(data.get('type')))
        flight=flight.filter(fromlocation__name__in=location,tolocation__name__in=location)
        if data.get('no_of_flights') == 'A':
            for fl in flight:
                loc_ind_l=location.index(fl.fromlocation.first().name)
                loc_ind_d=location.index(fl.tolocation.first().name)
                pointA=(geolocation[loc_ind_l].latitude,geolocation[loc_ind_l].longitude)
                pointB=(geolocation[loc_ind_d].latitude,geolocation[loc_ind_d].longitude)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color='blue',
                    )
                )
        elif data.get('no_of_flights') == 'B':
            for fl in flight[:5]:
                loc_ind_l=location.index(fl.fromlocation.first().name)
                loc_ind_d=location.index(fl.tolocation.first().name)
                pointA=(geolocation[loc_ind_l].latitude,geolocation[loc_ind_l].longitude)
                pointB=(geolocation[loc_ind_d].latitude,geolocation[loc_ind_d].longitude)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color='blue',
                    )
                )
        elif data.get('no_of_flights') == 'C':
            for fl in flight[5:]:
                loc_ind_l=location.index(fl.fromlocation.first().name)
                loc_ind_d=location.index(fl.tolocation.first().name)
                pointA=(geolocation[loc_ind_l].latitude,geolocation[loc_ind_l].longitude)
                pointB=(geolocation[loc_ind_d].latitude,geolocation[loc_ind_d].longitude)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color='blue',
                    )
                )
        m=m._repr_html_()
        dict1['map'] = m
    return render(request, 'home.html', dict1)