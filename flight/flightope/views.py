from django.shortcuts import render
from .models import *
from .forms import visualizations
from geopy.geocoders import Nominatim
import folium

# Create your views here.
def change_line_c(type):
    if type=='Indigo':
        line_c = 'blue'
    else:
        line_c = 'yellow'
    return line_c

def home(request):
    dict1 = {'title':'Flight Operations'}
    flight = flights.objects.all()
    citys = city.objects.all()
    dict1['flight'] = flight
    form = visualizations(request.POST or None)
    geolocator = Nominatim(user_agent="flight")
    dict1['form'] = form
    m = folium.Map(zoom_start=2)
    geolocation=[]
    fit_bounds_list=[]
    for i in citys:
        gcode=geolocator.geocode(i.name)
        geolocation.append(gcode)
        fit_bounds_list.append([gcode.latitude,gcode.longitude])
    for loc in geolocation:
        folium.Marker([loc.latitude,loc.longitude], tooltip='click here for more', popup=loc.address,
            icon=folium.DivIcon(html=f"""
                <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="15" cy="15" r="15" fill="#3186CC" fill-opacity="0.27"/>
                <circle cx="15" cy="15" r="9" fill="#3186CC"/>
                </svg>
                </div>"""),
        ).add_to(m)
    if form.is_valid():
        data = form.save()
        location = data.get('city')
        geolocation=[]
        for i in location:
            geolocation.append(geolocator.geocode(i))
        m = folium.Map(zoom_start=2)
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
                folium.Marker(pointA, tooltip='click here for more', popup=geolocation[loc_ind_l].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#31CC37" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#31CC37"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                folium.Marker(pointB, tooltip='click here for more', popup=geolocation[loc_ind_d].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#D32727" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#D32727"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color=change_line_c(fl.airlinename.first().name),
                    )
                )
        elif data.get('no_of_flights') == 'B':
            for fl in flight[:5]:
                loc_ind_l=location.index(fl.fromlocation.first().name)
                loc_ind_d=location.index(fl.tolocation.first().name)
                pointA=(geolocation[loc_ind_l].latitude,geolocation[loc_ind_l].longitude)
                pointB=(geolocation[loc_ind_d].latitude,geolocation[loc_ind_d].longitude)
                folium.Marker(pointA, tooltip='click here for more', popup=geolocation[loc_ind_l].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#31CC37" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#31CC37"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                folium.Marker(pointB, tooltip='click here for more', popup=geolocation[loc_ind_d].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#D32727" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#D32727"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color=change_line_c(fl.airlinename.first().name),
                    )
                )
        elif data.get('no_of_flights') == 'C':
            for fl in flight[5:]:
                loc_ind_l=location.index(fl.fromlocation.first().name)
                loc_ind_d=location.index(fl.tolocation.first().name)
                pointA=(geolocation[loc_ind_l].latitude,geolocation[loc_ind_l].longitude)
                pointB=(geolocation[loc_ind_d].latitude,geolocation[loc_ind_d].longitude)
                folium.Marker(pointA, tooltip='click here for more', popup=geolocation[loc_ind_l].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#31CC37" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#31CC37"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                folium.Marker(pointB, tooltip='click here for more', popup=geolocation[loc_ind_d].address,
                    icon=folium.DivIcon(html=f"""
                        <div style="position: relative;right: 10px;bottom: 10px;"><svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="15" cy="15" r="15" fill="#D32727" fill-opacity="0.27"/>
                        <circle cx="15" cy="15" r="9" fill="#D32727"/>
                        </svg>
                        </div>"""),
                ).add_to(m)
                m.add_child(
                    folium.PolyLine(
                        locations=[pointA,pointB],
                        weight=2,
                        color=change_line_c(fl.airlinename.first().name),
                    )
                )
    m.fit_bounds(fit_bounds_list)
    m=m._repr_html_()
    dict1['map'] = m
    return render(request, 'home.html', dict1)

'''
<svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="5" cy="5" r="5" fill="#3186CC" fill-opacity="0.27"/>
<circle cx="5" cy="5" r="3" fill="#3186CC"/>
</svg>

folium.CircleMarker([loc.latitude,loc.longitude], tooltip='click here for more', popup=loc.address,
            icon=folium.Icon(color='blue', icon='plane'),color='#3186cc57',fill=True,fill_color="#3186cc",fill_opacity = 0.9,
        ).add_to(m)


if form.is_valid():
        data = form.save()
        location = data.get('city')
        geolocation=[]
        for i in location:
            geolocation.append(geolocator.geocode(i))
        fromlocation = geolocator.geocode("175 5th Avenue NYC")
        m = folium.Map()
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
'''