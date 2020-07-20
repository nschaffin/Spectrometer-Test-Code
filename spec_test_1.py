"""
Manages communication with the spectrometer through the SeaBreeze library.
"""
import time as sleep_timers

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
		return None



	def spec_reestablish_connection(self):
		listed = seabreeze.spectrometers.list_devices()
		if listed == []:
			self.states_spectrometer = 2
			for i in range(3):												# Giving the spectrometer 3 attempts to connect
				#import seabreeze
				#import seabreeze.spectrometers
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

		print("\nWARNING: No spectrometer connected, check connection...\n")
		return None

	def spec_reestablish_connection_without_import(self):
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

		print("\nWARNING: No spectrometer connected, check connection...\n")
		return None

	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()

subtest = input("Please enter which subtest you would like to perform (1, 2, or 3): ")

if subtest == '1':
	spectrometer = Spectrometer()
	print("Spectrometer's current state: {}".format(spectrometer.states_spectrometer))
	print("-------------------------------")
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
elif subtest == '2':
	spectrometer = Spectrometer()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Unplug spectrometer before proceeding, once done type any character then hit enter: ")
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Now, plug spectrometer back in before proceeding, once done type any character then hit enter: ")
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
elif subtest == '3':
	spectrometer = Spectrometer()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Unplug spectrometer before proceeding, once done type any character then hit enter: ")
	spectrometer.spec_reestablish_connection_without_import()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Now, plug spectrometer back in before proceeding, once done type any character then hit enter: ")
	spectrometer.spec_reestablish_connection_without_import()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
else:
	print("\nInvalid subtest, please run this program again")
