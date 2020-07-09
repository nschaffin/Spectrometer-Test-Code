import seabreeze
import seabreeze.spectrometers

"""
Tests disconnection during integration
"""
spec_list = seabreeze.spectrometers.list_devices()
spec1 = spec_list[0]

def integrate():
	try:
		print("\nStarting integration...\n")
		spec1.integration_time_micros(5000)		# insert shortest integration time here
		wavelengths = spec1.wavelengths()
		print(f"The wavelength is: {wavelengths}")
	except:
		print("Error during integration")
