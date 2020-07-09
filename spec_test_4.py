import seabreeze
import seabreeze.spectrometers

"""
Tests to see if other USB devices will appear
"""
def check_spectrometer_list():
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		print(f"List of Spectrometers include: {spec_list}")
	except:
		print("Error with list_devices.")