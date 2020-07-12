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
		if self.spec == None:
			self.states_spectrometer = 2
			for _ in range(3):												# Giving the spectrometer 3 attempts to connect
				tyme.sleep(1.5)
				try:
					self.spec = self._setupSpectrometer()
					print("--------------------------------------")
					if self.states_spectrometer != 2:
						break
				except:
					continue
		tyme.sleep(1)
		if self.states_spectrometer != 2:
			return "\nSpectrometer {} successfully connected!\n".format(self.spec)
		print("\nWARNING: No spectrometer connected, check connection...\n")
		return None


	def sample(self, milliseconds, trigger):
		"""
		This function is used to signal the spectrometer to integrate for a set amount of time.

		Parameters
		----------
		milliseconds : int
			Inputted integration time for spectrometer
		"""
		
		try:
			self.spec.trigger_mode = trigger 							# Setting the trigger mode to normal
			self.spec.integration_time_micros(milliseconds) 			# Set integration time for spectrometer
			self.spectrometer_state.integrate()
			self.oasis_serial.sendBytes(b'\x01') 						# Sending nominal responce
			try:
				wavelengths, intensities = self.spec.spectrum() 		# Returns wavelengths and intensities as a 2D array, and begins sampling
			except:
				
				return 'An error occurred while attempting to sample' 	# Command to sample didn't work properly

			data = wavelengths, intensities 							# Saving 2D array to variable data
			if data == []:
				return 'No data entered' 								# Error handling for no data collected
			self.oasis_serial.sendBytes(b'\x30') 						# Code sent to spectrometer signaling sampling has successfully finished

			timestamp = time.time() 									# Returns # of seconds since Jan 1, 1970 (since epoch)
			self.fm.save_sample(timestamp, data) 						# Function call to create spectrometer file
			self.spectrometer_state.on_standby()
		except:
			self.spec_reestablish_connection()
			return 'Attempting to Reconnect Spectrometer'
		return None



	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()


spectrometer = Spectrometer()

time = 10000		# 10 seconds

while True:
	t_mode = input("Input trigger mode (type q to quit): ")
	if t_mode == '0':
		spectrometer.sample(time, t_mode)		# Normal Trigger
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '1':
		spectrometer.sample(time, t_mode)		# External Hardware Level Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == '3': 
		spectrometer.sample(time, t_mode)		# External Hardware Edge Trigger Mode
		print("Spectrometer's Current Status: {}\n".format(spectrometer.states_spectrometer))
	elif t_mode == "q":
		quit()
	else:
		print("\nYou have entered an invalid trigger mode\n")
