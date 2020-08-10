import time
import seabreeze
import seabreeze.spectrometers

class Spectrometer():
	def __init__(self):
		self.spec = self._setupSpectrometer()

	"""
	This should be the right way to check connection
	"""
	def test_connection(self):
		devices = seabreeze.spectrometers.list_devices()
		if devices == []:
			return 'No spectrometers listed'
		is_open = devices[0].is_open
		if is_open:
			return 'open'
		else:
			return 'closed'

	# """
	# Probably won't work
	# """
	# def test_connection2(self):
	# 	is_open = self.spec.is_open
	# 	print(is_open)

	"""
	Attempt to break connection and fix it by opening and closing it
	"""
	def break_connection1(self):
		self.spec = self._setupSpectrometer()
		self.spec = self._setupSpectrometer()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Closing connection...')
		self.spec.close()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Opening connection...')
		self.spec.open()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')

	"""
	Attempt to break connection and fix it by closing and reconnecting it
	"""
	def break_connection2(self):
		self.spec = self._setupSpectrometer()
		self.spec = self._setupSpectrometer()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Closing connection...')
		self.spec.close()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Reconnecting to spectrometer...')
		self.spec = _setupSpectrometer()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')

	"""
	Attempt to break connection and fix it by setting the variable to None and reconnecting it
	"""
	def break_connection3(self):
		self.spec = self._setupSpectrometer()
		self.spec = self._setupSpectrometer()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Setting Spectrometer to None to test if it disconnects spectrometer...')
		self.spec = None
		print(f'The spectrometer connection is now: {self.test_connection()}\n')
		print('Reconnecting to spectrometer...')
		self.spec = _setupSpectrometer()
		print(f'The spectrometer connection is now: {self.test_connection()}\n')

	def set_trigger(self, int=4):
		self.spec.trigger_mode(int)

	def integrate(self, test_time=20):
		self.spec.integration_time_micros(test_time*1000)
		wavelengths, intensities = self.spec.spectrum()
		print(intensities)
		return intensities

	"""
	Checks if the change from trigger mode 0 to trigger mode 4 was successful, otherwise switches to trigger mode 0
	"""
	def compare_data(self):
		data = []
		for _ in range(3):
			data.append(self.integrate())
			time.sleep(.5)
		for array in data[1:]:
			if data[0] != array:
				print("The data was not the same, need to use a different way to determine trigger mode")
				return
		print("The data is the same therefore there was no trigger, switching to normal trigger mode for gathering new data.")

	"""
	2 possibilities for when trigger mode is 4 and external triggering fails
	1. it hangs forever since it never receives the high signal so it'll never return a spectrum
	2. it returns the last spectrum taken so the method to solve it may be the same as compare_data() if it worked
	"""
	# def compare_data2(self):


	def _setupSpectrometer(self):
		"""
		Set up spectrometer connection
		"""
		devices = seabreeze.spectrometers.list_devices()
		if devices != []:
			spec = seabreeze.spectrometers.Spectrometer(devices[0])
			print("Spectrometer connected")
			return spec

		print("ERROR: No spectrometer listed by seabreeze!")
		return None

"""
initial test of is_open function
"""
def testing_is_open():
	devices = seabreeze.spectrometers.list_devices()
	if devices == []:
		print('No spectrometers listed')
		return
	is_open = devices[0].is_open
	if is_open:
		print('Spectrometer connection is currently open')
	else:
		print('Spectrometer connection is currently closed')

testing_is_open()
spec = Spectrometer()
print(f'The spectrometer connection is now: {spec.test_connection()}\n')

# is_open to check when the multiple connected spectrometer happens to see if it's actually open
# check if close or some other method will fix the multiple connected spectrometer error
# if close does, see if open multiple times causes the same error