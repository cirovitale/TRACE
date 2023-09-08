from geopy.geocoders import Nominatim
from flask import jsonify

geolocator = Nominatim(user_agent="TRACE")

def predictFromLocation(location, username):    
    # Retrieve Location object from location github info

    if (location is not None and not isinstance(location, dict)):
        print('Search location ISO of  ', username + '...')
    else:
        return None

    try:
        locationCoded = geolocator.geocode(location, addressdetails=True)
        
        if locationCoded:
            # Extract ISO Code
            countryCode = locationCoded.raw.get("address", {}).get("country_code", "").upper()

            if countryCode:
                return countryCode
    except Exception as e:
        # If an error occured during the call
        print(f"[LOCATION PREDICT] Error geopy: {e}")
        return jsonify({
            "error": str(e),
            "status": "403"
        })
    
    
    return None