"""
~ This program holds various functions that attempt to check the functionality of our spectrometer. This can be used as a playground to test different things on the Flame-T. ~
~ The program also comes pre-initialized with a 'spectrometer' object, you may add more object calls to this class if you would like though.

    connect()
        * This function is used to setup a class variable that calls an object of the spectrometer we want to interface with

    multiple_connect(attempts)
        * This function repeats connect over and over for the amount of times the user has requested
        * Included is a sleep timer that is changeable
            * This can be used to test unplugging and replugging in our spectrometer while this command is ongoing

    initialize()
        * This resets all usb devices on load
        * Can be used to possibly re-enumerate our spectrometer devices

    min_max()
        * This tests the minimum and maximum integration times our spectrometer can handle

    quick_integrate(trigger, microseconds)
        * This will make the spectrometer integrate just once
        * It will also print out spectrum, wavelengths, and intensities (this will also include the length of each of these lists)

    wavelengths_integrate(trigger, microseconds)
        * This will make the spectrometer integrate and only return wavelengths

    intensities_integrate(trigger, microseconds)
        * This will make the spectrometer integrate and only return intensities

    multiple_integrate(trigger, microseconds, integrations, type)
        * This will allow for the spectrometer to integrate multiple times (also this will be dependent on the type of parameters)

Test Stuff:
    * None of these classes reimport seabreeze, since this will lead to failure. If needed, either use initialize() or use unbind/rebind console commands to reset spectrometer drivers
    * Cseabreeze has precedence over pyseabreeze, using the 'seabreeze.use('pyseabreeze')' command will force your program to use pyseabreeze (though this is rather buggy)
    * Use wavelengths_integrate() and intensities_integrate() to see if we can figure out why they don't integrate for the proper duration
    * All integration functions also feature length outputs for each list of values
    * Spec_test_4.py is fixed, but this program incorporates mostly if not all features from previous tests
    * We are using list_devices() to setup spectrometer instead of from_first_available(), this can be swapped out if needed
    * Also, we should see if the spectrometer only blinks once for everytime the spectrometer integrates in especially in multiple_integrate()
    * As a final side note, this program is also rather flexible, so you can just straight up use seabreeze commands instead of using the given functions
"""
import time as sleep_timers

import seabreeze
#seabreeze.use('pyseabreeze')               # This may work, this may not (incase if errors, just comment it out). This is also used in initialize().
import seabreeze.spectrometers

class Spectrometer():
    
    def __init__(self):
        self.spec = self.connect()
        self.states_spectrometer = 2
    
    def connect(self):
        """
            This function is meant to connect our spectrometer and allow for us to send it commands
        """
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

    def multiple_connect(self, attempts):                                   # attempts(int) - number of reconnection attempts
        """
            This function is meant to connect our spectrometer repeatedly
        """
        print("")
        for a in range(attempts):
            print("-----------------------\n")
            print("Attempt number: {}".format(a+1))
            connection = self.connect()
            print("-----------------------\n")
            
            if a != attempts-1:
                sleep_timers.sleep(1)
        return None


    def initialize(self):
        """
            This function is meant to reenumerate all spectrometers connected to a system
        """
        if self.states_spectrometer == 0:
            seabreeze.pyseabreeze.SeaBreezeAPI.initialize()
            print("\nDevices now present: {}\n".format(seabreeze.spectrometers.list_devices()))
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None

    def min_max(self):
        """
            This function is meant to obtain a spectrometer's minimum and maximum integration times
        """
        if self.states_spectrometer == 0:
            minMax = self.spec.get_integration_time_micros_limits()
            print("\n{}\n".format(minMax))
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None
    
    def quick_integrate(self, trigger, microseconds):                   # trigger(int) - trigger mode | microseconds(int) - integration time
        """
            This function is meant to integrate only once
        """
        if trigger < 0 or trigger > 3 or trigger == 2:
            print("\nInvalid trigger mode\n")
            return None

        if self.states_spectrometer == 0:
            self.spec.trigger_mode(trigger)
            self.spec.integration_time_micros(microseconds)

            wavelengths, intensities = self.spec.spectrum()
            spectrum = wavelengths, intensities

            print("\nSpectrum: {}".format(spectrum))
            print("Spectrum length: {}\n".format(len(spectrum)))
            print("Wavelengths only: {}".format(wavelengths))
            print("Wavelengths length: {}\n".format(len(wavelengths)))
            print("Intensities only: {}".format(intensities))
            print("Intensities length: {}\n".format(len(intensities)))
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None

    def wavelengths_integrate(self, trigger, microseconds):              # trigger(int) - trigger mode | microseconds(int) - integration time
        """
            This function is meant to grab only wavelengths from an integration
        """
        if trigger < 0 or trigger > 3 or trigger == 2:
            print("\nInvalid trigger mode\n")
            return None

        if self.states_spectrometer == 0:
            self.spec.trigger_mode(trigger)
            self.spec.integration_time_micros(microseconds)

            wavelengths = self.spec.get_wavelengths()

            print("\nWavelengths: {}".format(wavelengths))
            print("Wavelengths length: {}\n".format(len(wavelengths)))
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None

    def intensities_integrate(self, trigger, microseconds):             # trigger(int) - trigger mode | microseconds(int) - integration time
        """
            This function is meant to grab only intesities from an integration
        """
        if trigger < 0 or trigger > 3 or trigger == 2:
            print("\nInvalid trigger mode\n")
            return None

        if self.states_spectrometer == 0:
            self.spec.trigger_mode(trigger)
            self.spec.integration_time_micros(microseconds)

            intensities = self.spec.get_intensities()

            print("\nIntensities: {}".format(intensities))
            print("Intensities length: {}\n".format(len(intensities)))
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None

    def multiple_integrate(self, trigger, microseconds, integrations, integration_type):    # trigger(int) - trigger mode(0, 1, or 3)
                                                                                            # microseconds(int) - integration time
                                                                                            # integrations(int) - num. of integrations
                                                                                            # integration_type(int): 0 - spectrum, 1 - wavelengths only, 2 - intensities only
        """                                                                     
            This function is meant to request multiple integrations one after the other
        """
        if self.states_spectrometer == 0:
            if integration_type == 0 or integration_type == 1 or integration_type == 2:
                if trigger <= 3 and trigger >= 0 and trigger != 2:
                    self.spec.trigger_mode(trigger)
                    self.spec.integration_time_micros(microseconds)

                    for n in range(integrations):
                        if integration_type == 0:
                            wavelengths, intensities = self.spec.spectrum()
                            spectrum = wavelengths, intensities
                        elif integration_type == 1:
                            wavelengths = self.spec.get_wavelengths()
                        elif integration_type == 2:
                            intensities = self.spec.get_intensities()
                        
                        print("\n-----------------------\n")
                        print("Integration number: {}\n".format(n+1))
                        
                        if integration_type == 0:
                            print("Spectrum: {}".format(spectrum))
                            print("Spectrum length: {}\n".format(len(spectrum)))
                        elif integration_type == 1:
                            print("Wavelengths: {}".format(wavelengths))
                            print("Wavelengths length: {}\n".format(len(wavelengths)))
                        elif integration_type == 2:
                            print("Intensities: {}".format(intensities))
                            print("Intensities length: {}\n".format(len(intensities)))

                        print("-----------------------\n")
                        sleep_timers.sleep(1)
                        
                    return None
                else:
                    print("\nInvalid trigger mode\n")
            else: 
                print("\nInvalid integration type\n")
        else:
            print("\nPlease set up your spectrometer and retry...\n")
        return None


spectrometer = Spectrometer()
# Make a second object and see if that messes up 