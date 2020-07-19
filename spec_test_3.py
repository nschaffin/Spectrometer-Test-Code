import seabreeze
import seabreeze.spectrometers

spec1 = ''

"""
Connects the Spectrometer
"""
def connect():
	global spec1
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		spec1 = seabreeze.spectrometers.Spectrometer(spec_list[0])
		try:
			spec1.integration_time_micros(5000)
		except:
			spec1 = seabreeze.spectrometers.Spectrometer.from_first_available()
			print("Needed to reconnect...")
		print("Spectrometer successfully connected")
	except:
		print("Spectrometer failed to connect. Trying again...")
		try:
			spec1 = seabreeze.spectrometers.Spectrometer.from_first_available()
		except:
			print("Make sure the spectrometer is connected and try running connect() again")

"""
Tests disconnection during integration
"""
def integrate():
	global spec1
	try:
		print("\nStarting integration...\n")
		spec1.integration_time_micros(5000000)		# 5 seconds
		wavelengths = spec1.wavelengths()
		print(f"The wavelength is: {wavelengths}")
	except:
		print("Error during integration")

"""
Tests to see integration returns the same sized array
"""
def compare_size():
	global spec1
	size_array = set()
	for _ in range(4):
		try:
			spec1.integration_time_micros(5000)		# 5 milliseconds
			wavelengths = spec1.wavelengths()
			size_array.add(len(wavelengths))
			# print(f"The wavelength size is: {len(wavelengths)}")
		except:
			print("Error during integration. Check connection")
	try:
		if len(size_array) == 1:
			print(f"Test Successful... Size of arrays are the same. The size is {size_array[0]}")
		else:
			print("Unexpected Results... Size of arrays are not the same")
			print(f"Sizes of arrays are: {size_array}")
	except:
		print("The spectrometer failed to integrate.")

	print("\nStarting next test...\n")

	# new test due to unexpected short blink led during 5 second integration

	try:
		spec1.integration_time_micros(10000)		# 10 milliseconds
		wavelengths = spec1.wavelengths()
		size_array.add(len(wavelengths))
	except:
		print("Error during second integration")
	try:
		if len(size_array) == 1:
			print(f"Test Failed... Unexpected Results... Size of arrays are the same. The size is {size_array[0]}")
		else if (len(size_array)) == 2:
			print(f"Test Successful... Confirmed that size of arrays differ by integration time.")
			print(f"Sizes of arrays are: {size_array}")
		else:
			print("Test Successful... Size of arrays are not the same but there's an error with one of the tests")
			print(f"Sizes of arrays are: {size_array}")
	except:
		print("Error comparing wavelengths.")