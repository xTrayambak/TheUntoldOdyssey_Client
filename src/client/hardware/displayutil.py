#!/usr/bin/python3

import sys
import subprocess
import enum

class DisplayServer(enum.IntEnum):
    XORG = 0
    WAYLAND = 1

class DisplayUtil:
    def __init__(self):
        if sys.platform in ('win32', 'win64'):
            self.collect_windows()
        elif sys.platform == 'darwin':
            self.collect_mac()
        elif sys.platform == 'linux':
            self.collect_linux()
        else:
            self.collect_null()

        self.refresh_rate = int(self.refresh_rate)
        self.refresh_rate_str = str(self.refresh_rate) + 'Hz'


    def collect_windows(self):
        """
        Collect data for a Windows/NT implementation using the win32api module.
        """
        import win32api

        monitor = win32api.EnumDisplayDevices()
        monitor_settings = win32api.EnumDisplaySettings()

        self.refresh_rate = monitor_settings.DisplayFrequency
        self.monitor = monitor


    def collect_mac(self):
        """
        Collect data for a MacOS/Darwin implementation using the PyOBJC wrapper.
        """
        from AppKit import NSScreen

        # Let's prioritize screen 0.
        monitor = NSScreen.get_screens()[0]

        self.refresh_rate = monitor.maximumFramesPerSecond()
        self.monitor = monitor


    def collect_linux(self):
        """
        Collect data for a Linux implementation
        """
        # This is a bit tricky. Thank you, StackOverflow. :-)
        # I hate this Wayland-Xorg tomfoolery. I hope I never have to see it again.

        if self.get_display_server() == DisplayServer.XORG:
            from Xlib import display
            from Xlib.ext import randr

            monitor = display.Display()
            settings = monitor.screen(monitor.get_default_screen())

            resources = randr.get_screen_resources(settings.root)
            active_modes = set()

            for crtc in resources.crtcs:
                crtc_info = randr.get_crtc_info(settings.root, crtc, resources.config_timestamp)
                if crtc_info.mode:
                    active_modes.add(crtc_info.mode)

            for mode in resources.modes:
                if mode.id in active_modes:
                    self.refresh_rate = (mode.dot_clock / (mode.h_total * mode.v_total))

            self.monitor = monitor
        else:
            # I have no clue how to do a Wayland implementation.
            self.collect_null()


    def collect_null(self):
        """
        Get data for when no compatible implementations are found.
        """
        self.refresh_rate = 60.0
        self.monitor = None

    def get_display_server(self):
        """
        *LINUX ONLY*
        Get the currently running display server.
        """
        assert sys.platform == 'linux', f'DisplayServer.get_display_server(): You must be running the Linux kernel, not {sys.platform}!'
        try:
            pidof_xorg_server = subprocess.check_output(['pidof', 'Xorg'])
            return DisplayServer.XORG
        except subprocess.CalledProcessError:
            return DisplayServer.WAYLAND
