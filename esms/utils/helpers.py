# esms/utils/helpers.py
import pycountry

def get_country_code(country_name):
    """Convert country name to its 2-letter ISO code for flag display"""
    try:
        # Try to find the country by name
        country = pycountry.countries.get(name=country_name)
        if not country:
            # Try to find by common name if not found by official name
            for c in pycountry.countries:
                if hasattr(c, 'common_name') and c.common_name == country_name:
                    country = c
                    break
            
            # Try partial matches if still not found
            if not country:
                matches = [c for c in pycountry.countries if country_name in c.name]
                if matches:
                    country = matches[0]
        
        if country:
            # Return lowercase ISO code for flag-icon-css
            return country.alpha_2.lower()
    except Exception as e:
        print(f"Error finding country code for {country_name}: {str(e)}")
    
    # Return xx as placeholder for unknown
    return 'xx'