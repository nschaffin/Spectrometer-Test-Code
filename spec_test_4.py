"""
Manages communication with the spectrometer through the SeaBreeze library.
"""
import time as tyme

import seabreeze
import seabreeze.spectrometers


class Spectrometer():
	"""Class for interacting with the spectrometer through seabreeze."""

	def _setupSpectrometer(self):
		devices = seabreeze.spectrometers.list_devices()
		print("\nSpectrometers Detected: {}\n".format(devices))				# This will print out all devices listed by seabreeze library
		if devices != []:
			self.states_spectrometer = 0
			spec = seabreeze.spectrometers.Spectrometer(devices[0])
			return spec

		self.states_spectrometer = 2
		print("No spectrometer listed by seabreeze...\n")
		return None



	def spec_reestablish_connection(self):
		listed = seabreeze.spectrometers.list_devices()
		if listed == []:
			self.states_spectrometer = 2
			for i in range(3):												# Giving the spectrometer 3 attempts to connect
				try:
					self.spec = self._setupSpectrometer()
					print("--------------------------------------")
					if i < 2:
						sleep_timers.sleep(1.5)
					if self.states_spectrometer != 2:
						break
				except:
					continue
		
		if self.states_spectrometer != 2:
			return "\nSpectrometer {} successfully connected!\n".format(self.spec)

		print("\nWARNING: No spectrometer connected, check connection...\n")
		return None

	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()


	def sample(self, microseconds, trigger):
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
			try:
				wavelengths, intensities = self.spec.spectrum() 		# Returns wavelengths and intensities as a 2D array, and begins sampling
			except:
				return 'An error occurred while attempting to sample' 	# Command to sample didn't work properly
			
			self.data = wavelengths, intensities
			print("Spectrometer's collected data: {}".format(self.data))
			tyme.sleep(3)

			try: 
				wavelengths2, intensities2 = self.spec.spectrum()		# Sample a second time
			except:
				return 'An error occurred while attempting to sample' 	# Command to sample didn't work properly

			self.data2 = wavelengths2, intensities2
			print("Spectrometer's collected data: {}".format(self.data2))
			tyme.sleep(5)

			try: 
				wavelengths3, intensities3 = self.spec.spectrum()		# Sample a second time
			except:
				return 'An error occurred while attempting to sample' 	# Command to sample didn't work properly

			self.data3 = wavelengths3, intensities3
			print("Spectrometer's collected data: {}".format(self.data3))

			if data == []:
				return 'No data entered' 								# Error handling for no data collected

		except:
			self.spec_reestablish_connection()
			return 'Attempting to Reconnect Spectrometer'
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
			try:
				wavelengths, intensities = self.spec.spectrum() 		# Returns wavelengths and intensities as a 2D array, and begins sampling
			except:
				
				return 'An error occurred while attempting to sample' 	# Command to sample didn't work properly
			
			self.data_external = wavelengths, intensities
			print("Spectrometer's collected data: {}".format(self.data_external))

			if data == []:
				return 'No data entered' 								# Error handling for no data collected

		except:
			self.spec_reestablish_connection()
			return 'Attempting to Reconnect Spectrometer'
		return None





	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()
		self.data = []
		self.data2 = []
		self.data3 = []
		self.data_external = []


spectrometer = Spectrometer()

time = 5000000		# 5 seconds

while True:
	t_mode = input("Input trigger mode (type q to quit): ")
	if t_mode == '0':
		spectrometer.sample(time, int(t_mode))				# Normal Trigger
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '1':
		spectrometer.sample_external(time, int(t_mode))		# External Hardware Level Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '3': 
		spectrometer.sample_external(time, int(t_mode))		# External Hardware Edge Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == "q":
		quit()
	else:
		print("\nYou have entered an invalid trigger mode\n")
