"""
Manages communication with the spectrometer through the SeaBreeze library.
"""
import time

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
				import seabreeze
				import seabreeze.spectrometers
				try:
					self.spec = self._setupSpectrometer()
					print("--------------------------------------")
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
