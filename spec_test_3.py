import seabreeze
import seabreeze.spectrometers

"""
Connects the Spectrometer
"""
def connect():
	try:
		spec_list = seabreeze.spectrometers.list_devices()
		spec1 = spec_list[0]
		print("Spectrometer successfully connected")
	except:
		print("Spectrometer failed to connect. Try again")

"""
Tests disconnection during integration
"""
def integrate():
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
	size_array = set()
	for _ in range(3):
		try:
			spec1.integration_time_micros(5000)		# 5 milliseconds
			wavelengths = spec1.wavelengths()
			size_array.add(len(wavelengths))
			# print(f"The wavelength size is: {len(wavelengths)}")
		except:
			print("Error during integration")
	try:
		if size_array == 1:
			print(f"Test Successful... Size of arrays are the same. The size is {size_array[0]}")
		else:
			print("Test Failed... Size of arrays are not the same")
			print(f"Sizes of arrays are: {size_array}")
	except:
		print("The spectrometer failed to integrate.")
