import seabreeze
import seabreeze.spectrometers
from seabreeze.spectrometers import Spectrometer

# Step 1 and step 4
def test_spectrometer():
	# Test list_devices
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		if spec_list == []:
			print("ERROR: No spectrometers listed.")
		else:
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
		spec1.integration_time_micros(5000)		# insert shortest integration time here
		wavelengths = spec1.wavelengths()
		print(f"Wavelengths: {wavelengths}")
	except:
		print("Failed to get wavelengths")
	print("\n")

# Step 2 and 3
def check_spectrometer():
	# Test list_devices
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		if spec_list == []:
			print("No spectrometers listed.")
		else:
			print(f"The devices listed are: {spec_list}.")
	except:
		print("Error with list_devices function")

	# Test integrating when it's disconnected but the spectrometers are still listed
	try:
		spec1.integration_time_micros(5000)		# insert shortest integration time here
		wavelengths = spec1.wavelengths()
		print(f"Wavelengths: {wavelengths}")
	except:
		print("Failed to get wavelengths as expected")
	print("\n")
"""
Connect:
check devices
connect to spec
check if both specs are the same thing
run a command

Disconnected:
check devices
run a command

Reconnect:
check devices
run a command

Reconnect retry:
check devices
connect to spec
check if both specs are the same thing
run a command
"""
