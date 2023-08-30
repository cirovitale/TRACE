from geopy.geocoders import Nominatim
from flask import jsonify

geolocator = Nominatim(user_agent="TRACE")

def predictFromLocation(location):    
    # Retrieve Location object from location github info
    try:
        locationCoded = geolocator.geocode(location, addressdetails=True)
        
        if locationCoded:
            # Extract ISO Code
            countryCode = locationCoded.raw.get("address", {}).get("country_code", "").upper()

            if countryCode:
                return countryCode
    except Exception as e:
        # If an error occured during the call
        print(f"Error geopy: {e}")
        return jsonify({
            "error": str(e),
            "status": "403"
        })
    
    
    return None