from webscraper import USPSTracking

response = USPSTracking().get("9374889715715058742161")
print(response)