import seabreeze
import seabreeze.spectrometers
import time

'''
Meant to be run in interactive mode to catch errors.
'''

spec1 = ''

"""
Connects the Spectrometer
"""
def connect():
	global spec1
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		spec1 = seabreeze.spectrometers.Spectrometer(spec_list[0])
		spec1.integration_time_micros(5000)
		time.sleep(1)
	except:
		print("Spectrometer failed to connect. Trying again...")
		spec1 = seabreeze.spectrometers.Spectrometer.from_first_available()
		

"""
Tests disconnection during integration
"""
def integrate():
	global spec1
	print("\nStarting integration...\n")
	spec1.integration_time_micros(5000000)		# 5 seconds
	wavelengths = spec1.wavelengths()
	print(f"The wavelength is: {wavelengths}")


"""
Tests to see integration returns the same sized array.
It does return the same size array
"""
def compare_size():
	global spec1
	size_array = set()
	for _ in range(4):
		spec1.integration_time_micros(5000)		# 5 milliseconds
		wavelengths = spec1.wavelengths()
		size_array.add(len(wavelengths))
		# print(f"The wavelength size is: {len(wavelengths)}")

	if len(size_array) == 1:
		print(f"Test Successful... Size of arrays are the same. The size is {size_array[0]}")
	else:
		print("Unexpected Results... Size of arrays are not the same")
		print(f"Sizes of arrays are: {size_array}")

	print("\nStarting next test...\n")

	# new test due to unexpected short blink led during 5 second integration

	spec1.integration_time_micros(10000)		# 10 milliseconds
	wavelengths = spec1.wavelengths()
	size_array.add(len(wavelengths))

	if len(size_array) == 1:
		print(f"Test Failed... Unexpected Results... Size of arrays are the same. The size is {size_array[0]}")
	elif (len(size_array)) == 2:
		print(f"Test Successful... Confirmed that size of arrays differ by integration time.")
		print(f"Sizes of arrays are: {size_array}")
	else:
		print("Test Successful... Size of arrays are not the same but there's an error with one of the tests")
		print(f"Sizes of arrays are: {size_array}")
