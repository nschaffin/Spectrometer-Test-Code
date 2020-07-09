import seabreeze
import seabreeze.spectrometers
from seabreeze.spectrometers import Spectrometer

"""
Series of try except statements testing each function
"""
def try_commands():
	# Test list_devices
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		spec1 = spec_list[0]
		print(f"The devices listed are: {spec_list}. The spectrometer selected is: {spec1}")
	except:
		print("Error with list_devices function")

	# Test from_first_available
	try:
		first_spec = seabreeze.spectrometers.Spectrometer.from_first_available
		print(f"The first available device is: {first_spec}")
	except:
		print("Error with from_first_available function")

	# Compare the results of both spectrometers
	try:
		if first_spec == spec1:
			print("list_devices and from_first_available give the same spectrometer")
		else:
			print("list_devices and from_first_available give different spectrometers")
	except:
		print("Error comparing spectrometers")

	# Test integrating when it's disconnected but the spectrometers are still listed
	try:
		spec1.integration_time_micros(1000)		# insert shortest integration time here
		wavelengths = spec1.wavelengths()
		print(f"Wavelengths: {wavelengths}")
	except:
		print("Failed to get wavelengths")
	print("\n")
# test for shortest integration time
# test for trigger modes
