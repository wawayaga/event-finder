from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="event_finder")

def get_coordinates(address):
    location = geolocator.geocode(address)
    lat = location.latitude
    lon = location.longitude
    return [lat, lon]

#location = geolocator.reverse("52.509669, 13.376294")

#print(location.address) #address
#print((location.latitude, location.longitude)) #coordinates
#print(location.raw) #location object?
