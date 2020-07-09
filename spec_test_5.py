import seabreeze
import seabreeze.spectrometers

"""
Tests to see integration returns the same sized array
"""
def check_size():
	size_array = set()
	for _ in range(3):
		try:
			spec1.integration_time_micros(5000)		# insert shortest integration time here
			wavelengths = spec1.wavelengths()
			size_array.add(len(wavelengths))
			print(f"The wavelength size is: {len(wavelengths)}")
		except:
			print("Error during integration")
	if size_array == 1:
		print("Test Successful... Size of arrays are the same")
	else:
		print("Test Failed... Size of arrays are not the same")
		print(f"Sizes of arrays are: {size_array}")
check_size()