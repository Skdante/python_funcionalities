from geopy.geocoders import Nominatim

'''Posibles Resultados'''
''' http://maps.googleapis.com | https://nominatim.openstreetmap.org | https://dev.virtualearth.net '''
geolocator = Nominatim(user_agent="http://maps.googleapis.com") 

location = geolocator.geocode("Chamula 327 Zirandaro")

print(location.address)
print((location.latitude, location.longitude))
(40.7410861, -73.9896297241625)
print(location.raw)