import ipinfo 
import ipaddress 


def validate_ip(client_ip):
    try:
        ipaddress.ip_address(client_ip)
        return True 
    except ValueError:
        return False

def get_client_country_from_ip(client_ip, access_token):
    # Create IPInfo Handler
    handler = ipinfo.getHandler(access_token)

    # Handle IP if run in local
    if client_ip == "127.0.0.1":
        details = handler.getDetails()
    else:
        details = handler.getDetails(client_ip)
    
    # Return country
    return details.country