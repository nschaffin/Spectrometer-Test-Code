"""
Manages communication with the spectrometer through the SeaBreeze library.
"""
import time as sleep_timers

import seabreeze
seabreeze.use('cseabreeze')
import seabreeze.spectrometers


class Spectrometer():
	"""Class for interacting with the spectrometer through seabreeze."""
	
	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()
		self.data = []
		self.data2 = []
		self.data3 = []
		self.data_external = []
	


	def _setupSpectrometer(self):
		devices = seabreeze.spectrometers.list_devices()
		print("\nSpectrometers Connected to USB: {}\n".format(devices))
		if devices != []:
			self.states_spectrometer = 0                                    # Standby state
			self.spec = seabreeze.spectrometers.Spectrometer(devices[0])
			print("You have connected {}\n".format(self.spec))
			return None
		else:
			print("No spectrometer available for connection...\n")
			self.states_spectrometer = 2                                    # Disconnected state
			return None

	def check_connection(self):
		listed = seabreeze.spectrometers.list_devices()
		if listed == [] or self.states_spectrometer == 2:
			responce = input("\nNo spectrometer connected, type 1 to reconnect or 2 to stay disconnected: ")
			while True:
				if responce == '1':
					self.spec_reestablish_connection()
					return None
				elif responce == '2':
					return None
				else:
					print("Invalid responce\n")
		return None


	def spec_reestablish_connection(self):
		listed = seabreeze.spectrometers.list_devices()
		if listed == []:
			self.states_spectrometer = 2
			for i in range(3):												# Giving the spectrometer 3 attempts to connect
				try:
					self.spec = self._setupSpectrometer()
					print("--------------------------")
					if i < 2:
						sleep_timers.sleep(1)
					if self.states_spectrometer != 2:
						break
				except:
					continue
		
		sleep_timers.sleep(.2)

		if self.states_spectrometer != 2:
			print("\nSpectrometer {} successfully connected!\n".format(self.spec))
			return None

		print("\nWARNING: No spectrometer connected, check connection...")
		return None


	def sample(self, microseconds, trigger):
		"""
		This function is used to signal the spectrometer to integrate for a set amount of time.

		Parameters
		----------
		milliseconds : int
			Inputted integration time for spectrometer
		"""
		self.spec.trigger_mode(trigger)								# Setting the trigger mode to normal
		self.spec.integration_time_micros(microseconds) 			# Set integration time for spectrometer

		try:
			wavelengths, intensities = self.spec.spectrum() 		# Returns wavelengths and intensities as a 2D array, and begins sampling
		except:
			print('\nAn error occurred while attempting to sample 1\n')
			return None 											# Command to sample didn't work properly
		
		self.data = wavelengths, intensities
		print("\nSpectrometer's collected data: {}\n".format(self.data))
		sleep_timers.sleep(3)

		try: 
			wavelengths2, intensities2 = self.spec.spectrum()		# Sample a second time
		except:
			print('\nAn error occurred while attempting to sample 2\n')
			return None 											# Command to sample didn't work properly

		self.data2 = wavelengths2, intensities2
		print("Spectrometer's collected data: {}\n".format(self.data2))
		sleep_timers.sleep(5)

		try: 
			wavelengths3, intensities3 = self.spec.spectrum()		# Sample a second time
		except:
			print('\nAn error occurred while attempting to sample 3\n')
			return None 											# Command to sample didn't work properly

		self.data3 = wavelengths3, intensities3
		print("Spectrometer's collected data: {}\n".format(self.data3))

		if data == []:
			print('No data entered\n')
			return None 											# Error handling for no data collected
		
		return None



	def sample_external(self, microseconds, trigger):
		"""
		This function is used to signal the spectrometer to integrate for a set amount of time.

		Parameters
		----------
		milliseconds : int
			Inputted integration time for spectrometer
		"""
		
		try:
			self.spec.trigger_mode(trigger)								# Setting the trigger mode to normal
			self.spec.integration_time_micros(microseconds) 			# Set integration time for spectrometer
		except:
			print('\nSpectrometer not set up properly\n')
			return None

		try:
			wavelengths, intensities = self.spec.spectrum() 		# Returns wavelengths and intensities as a 2D array, and begins sampling
		except:
			print('\nAn error occurred while attempting to sample\n')
			return None 											# Command to sample didn't work properly
		
		self.data_external = wavelengths, intensities
		print("\nSpectrometer's collected data: {}\n".format(self.data_external))

		if data == []:
			return 'No data entered\n' 								# Error handling for no data collected

		return None


spectrometer = Spectrometer()

time = 5000000		# 5 seconds

while True:
	t_mode = input("Input trigger mode (type q to quit): ")
	if t_mode == '0':
		spectrometer.check_connection()
		print("\nSpectrometer connected: {}".format(spectrometer.spec))
		spectrometer.sample(time, int(t_mode))				# Normal Trigger
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '1':
		spectrometer.check_connection()
		print("\nSpectrometer connected: {}".format(spectrometer.spec))
		spectrometer.sample_external(time, int(t_mode))		# External Hardware Level Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '3': 
		spectrometer.check_connection()
		print("\nSpectrometer connected: {}".format(spectrometer.spec))
		spectrometer.sample_external(time, int(t_mode))		# External Hardware Edge Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == "q":
		quit()
	else:
		print("\nYou have entered an invalid trigger mode\n")
