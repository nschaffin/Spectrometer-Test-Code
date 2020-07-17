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
		print(listed)
		if listed == []:
			self.states_spectrometer = 2
			for _ in range(3):												# Giving the spectrometer 3 attempts to connect
				tyme.sleep(1.5)
				#import seabreeze
				#import seabreeze.spectrometers
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

	def spec_reestablish_connection_without_import(self):
		listed = seabreeze.spectrometers.list_devices()
		if listed == []:
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

	def __init__(self):
		# 0 = standby, 1 = integrating, 2 = disconnected
		self.states_spectrometer = 2
		self.spec = self._setupSpectrometer()

subtest = input("Please enter which subtest you would like to perform (1, 2, or 3): ")

if subtest == '1':
	spectrometer = Spectrometer()
	print("Spectrometers listed: {}\n".format(spectrometer.spec))
	print("Spectrometer's current state: {}".format(spectrometer.states_spectrometer))
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}".format(spectrometer.states_spectrometer))
elif subtest == '2':
	spectrometer = Spectrometer()
	print("Spectrometers listed: {}\n".format(spectrometer.spec))
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Please unplug spectrometer before proceeding.\nOnce unplugged, please enter in any character to confirm: ")
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Now, please plug spectrometer back in before proceeding.\nOnce plugged in, please enter in any character to confirm: ")
	spectrometer.spec_reestablish_connection()
	print("Spectrometer's current state: {}".format(spectrometer.states_spectrometer))
elif subtest == '3':
	spectrometer = Spectrometer()
	print("Spectrometers listed: {}\n".format(spectrometer.spec))
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Please unplug spectrometer before proceeding.\nOnce unplugged, please enter in any character to confirm: ")
	spectrometer.spec_reestablish_connection_without_import()
	print("Spectrometer's current state: {}\n".format(spectrometer.states_spectrometer))
	input("Now, please plug spectrometer back in before proceeding.\nOnce plugged in, please enter in any character to confirm: ")
	spectrometer.spec_reestablish_connection_without_import()
	print("Spectrometer's current state: {}".format(spectrometer.states_spectrometer))
else:
	print("\nInvalid subtest, please run this program again")
