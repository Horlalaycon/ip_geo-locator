import geocoder
import reverse_geocoder as rg
import folium
import argparse
import socket
import re


# domain name option processing
def convert_domain_name(domain):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1)
		ip = socket.gethostbyname(domain)
		pattern= r"(\d+\.\d+\.\d+\.\d+)"
		match = re.search(pattern, ip)
		match_result = match.group(1)
		return match_result

	except socket.gaierror:
		print(r"""
========================================
 Error!:
    Incorrect domain name 
            or
    No internet connection
========================================
""")
		quit()


# arguments
parser = argparse.ArgumentParser(description="A program to get geographical location/find location information from an ip address ")

# One of the two options must be selected
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-ip", "--ip_addr", help="specify Target's IP address to geolocate", )
group.add_argument("-d", "--domain", help="Specify Target's Domain name to geolocate")

parser.add_argument("-m", "--map", help="specify map name to generate location map ")
args = parser.parse_args()

# Target
if args.domain:
	target = convert_domain_name(args.domain)
else:
	target = args.ip_addr


def get_latlng(ip_addr=target):
	g = geocoder.ip(ip_addr)
	latitude, longitude = g.latlng
	return latitude, longitude


# geolocator engine
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

	return str(f"""----------------------------------------
	City: {city}
	State: {region1}
	Region: {region2}
	Country: {country}
	Lat, Lng: {lat, lng}
========================================
""")


if __name__ == "__main__":
	# banner
	print("=" * 40)
	print("	 *****(IP GEOLOCATOR)*****")
	print("-" * 40)

	print("   By: sys_br3ach3r")
	print("=" * 40)

	try:
		print(f"\n  Locating target: {target}")
		print(locate())

		# map
		if args.map:
			map_name = args.map + ".html"
			print(f""" Generating Map...
	Map Saved: ({map_name})
========================================""")
			latlng = get_latlng()
			save_map = folium.Map(location=latlng, zoom_start=10)
			folium.CircleMarker(location=latlng, radius=100, popup="Found Location").add_to(save_map)
			save_map.save(map_name)

	except TypeError:
		print(f"Error, check network connectivity")


	except KeyboardInterrupt:
		print(f"""
----------------------------------
|| program Aborting... (Ctrl+c) ||
----------------------------------""")
		quit()
