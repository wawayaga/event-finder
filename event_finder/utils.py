from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="event_finder")

def get_coordinates(address):
    location = geolocator.geocode(address, country_codes="", addressdetails=True) #addressdetails include relevant details like 'city'
    if location == None:
        return None
    else:
        return [location.raw['lat'], location.raw['lon'], location.raw['address']['city']]