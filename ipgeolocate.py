import geocoder
import reverse_geocoder as rg
import folium
import argparse

banner = r"""
---------------------------------------------------------------------
|-|---------------------------------------------------------------|-|
(~|   ___ ____        ____            _                 _         |~)       
|~)  |_ _|  _ \      / ___| ___  ___ | | ___   ___ __ _| |_ ___   (~|
(~|   | || |_) |____| |  _ / _ \/ _ \| |/ _ \ / __/ _` | __/ _ \  |~)
|~)   | ||  __/_____| |_| |  __/ (_) | | (_) | (_| (_| | ||  __/  (~|
(~|  |___|_|         \____|\___|\___/|_|\___/ \___\__,_|\__\___|  |~)                                              
|-|---------------------------------------------------------------|-| 
(~|  Geographical location/address finder using ip address        |~)
|-|---------------------------------------------------------------|-|
|~)     Created by: Ibrahim-Ajimati                               (~|
|-|---------------------------------------------------------------|-|
[~|                 A.K.A f3ar_0f_th3_unkn0wn @github             |~]
---------------------------------------------------------------------
                            +---------+         -----
                           +-----------+        |   |
                          +-------------+       -----
=====================================================================
=====================================================================                
"""
# arguments
parser = argparse.ArgumentParser(prog="IP Geolocate", description="A program to get geographical location/find location information from an ip address ")
parser.add_argument("-t", "--target", help="specify IP address to geo-locate", required=True)
parser.add_argument("-m", "--map", help="specify map name to generate location map ")
args = parser.parse_args()

target = args.target


def get_latlng(ip_addr=target):
    g = geocoder.ip(ip_addr)
    latitude, longitude = g.latlng
    return latitude, longitude


# geolocate engine
def locate():
    city = ""
    region1 = ""
    region2 = ""
    country = ""
    lat, lng = get_latlng(target)
    ip_info = rg.search((lat, lng), verbose=False)
    for item in ip_info:
        city = item["name"]
        region1 = item["admin1"]
        region2 = item["admin2"]
        country = item["cc"]

    return str(f"""++++++++++++++++++++++++++++++++++
    City: {city}
    State: {region1}
    Region: {region2}
    Country: {country}
+++++++++++++++++++++++++++++++++++++++++++++++++""")


print(banner)
if __name__ == "__main__":
    try:
        print(f"++++++++++++++++++++++++++++++++++\n Locating target: {target}")
        print(locate())
        # map
        if args.map:
            map_name = args.map + ".html"
            print(f"""|| Creating and saving Map ({map_name})
+++++++++++++++++++++++++++++++++++++++++++++++++""")
            latlng = get_latlng()
            save_map = folium.Map(location=latlng, zoom_start=10)
            folium.CircleMarker(location=latlng, radius=100, popup="Found Location").add_to(save_map)
            save_map.save(map_name)
    # except TypeError:
    #     print(f"Error, check network connectivity")
    #
    except KeyboardInterrupt:
        print(f"""
----------------------------------
|| program Aborting... (Ctrl+c) ||
----------------------------------""")
        quit()
