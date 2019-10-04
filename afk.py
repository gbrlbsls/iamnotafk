import os
import time
import psutil
import re

import win32gui
import pyautogui

LEAGUE_WINDOW_TITLE = 'League of Legends'
LEAGUE_PROCESS_NAME = 'LeagueClient.exe'
LEAGUE_PHASES = ['Lobby', 'Matchmaking', 'ReadyCheck', 'ChampSelect', 'GameStart', 'PostGame', 'ReadyCheckAccepted']

class LeagueClient(object):
    def __init__(self):
        self.hwnd = None #Window handle
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        self.phase = None #Cliente gameflow phase

        self.process = None #Process object
        self.logname = None #Log filename

        # log attrs
        self._last_size = 0 # Last log size
        self._last_str = '' # Last log update
        self._file_index = 0 # Current file position

        self.update()

    def focus(self):
        try:
            if win32gui.IsIconic(self.hwnd): # Check if client window is minimized
                win32gui.ShowWindow(self.hwnd, 9) # If yes, then restore it
                return False

            win32gui.SetForegroundWindow(self.hwnd) # Bring window to front
            win32gui.SetActiveWindow(self.hwnd) # Active it
        except:
            pass
        
        return self._is_focused() # Return if the window is focused

    def _is_focused(self):
        return (win32gui.GetForegroundWindow() == self.hwnd) and (win32gui.IsWindowVisible(self.hwnd) == 1) # Check if window is visible

    def _get_window(self):
        self.hwnd = win32gui.FindWindow(None, LEAGUE_WINDOW_TITLE) # Find league client window
        if self.hwnd <= 0: # If not found, set it to None
            self.hwnd = None

    def _get_window_info(self):
        if self.hwnd == None:
            return
        
        rect = win32gui.GetWindowRect(self.hwnd) # Get window position and dimensions
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2] - self.x
        self.h = rect[3] - self.y

    def _get_process(self):
        self.process = None # Set process to None, so it won't pretend to exist when don't
        for p in psutil.process_iter(attrs=['exe']): # Search process
            if p.info['exe'] != None and p.info['exe'].endswith(LEAGUE_PROCESS_NAME): # Check if process exe matches league exe
                self.process = p # Set it

    def _get_logname(self):
        if self.process == None:
            self.logname = None
            return None

        try:
            # this returns the list of opened files by the current process
            flist = self.process.open_files() # Get process open files
            if flist:
                for nt in flist:
                    if nt.path.endswith('LeagueClient.log'): # Check if the filename matches our log
                        self.logname = nt.path

        # This catches a race condition where a process ends
        # before we can examine its files
        except psutil.NoSuchProcess:
            self.logname = None

    def _update_log(self):
        if self.process == None:
            return False

        with open(self.logname) as f:
            f.seek(self._file_index) # Seek to last position
            self._last_str = f.read(self._last_size - self._file_index) # Get the changes
            self._file_index = self._last_size # Update the last position
        
        return True

    def _log_has_changed(self):
        if self.logname == None:
            return False

        fsize = os.stat(self.logname).st_size # Get the current log size in bytes
        if fsize != self._last_size: # If the size is different to the stored size, the update things
            self._last_size = fsize
            self._update_log()
            return True

        return False

    def _parse_log(self):
        lines = self._last_str.splitlines() # Split string of log changes into lines(list)

        for lineNumber in reversed(range(len(lines))): # Let's iterate over the lines from end to start
            line = lines[lineNumber]
            phase = re.search(r'Gameflow: entering state \'(\w+)\'', line) # Find the gameflow changes
            if phase != None: # Check if something was found
                phase = phase.group(1) # Store it
                if (self.phase != phase) and LEAGUE_PHASES.count(phase) > 0: # If the phase differs from the previous, then update the object
                    self.phase = phase
                    break
            elif 'READY_CHECK_USER_ACCEPTED' in line: # Check if the match was accepted
                self.phase = 'ReadyCheckAccepted'
                break

    def _accept_match(self):
        button_x = self.x + (self.w * 0.511) # Calc the accept button position
        button_y = self.y + (self.h * 0.765)

        pyautogui.click(x=button_x, y=button_y) 

    def try_accept_match(self):
        if(self.focus()):# If the window was focused
            self._accept_match() # Accept the match

    def log(self, p_phase): # Prettify the output, or not...
        #['Lobby', 'Matchmaking', 'ReadyCheck', 'ChampSelect', 'GameStart', 'PostGame', 'ReadyCheckAccepted']
        if p_phase != self.phase:
            if self.phase == 'Matchmaking':
                print('>', 'Queue started')
            elif self.phase == 'ReadyCheck':
                print('>', 'Match found')
            elif self.phase == 'ReadyCheckAccepted':
                print('>', 'Match accepted')
            elif self.phase == 'ChampSelect':
                print('>', 'Picks and bans')
            elif self.phase == 'GameStart':
                print('>', 'Game started')
            elif self.phase == 'PostGame':
                print('>', 'Game finished')
            else:
                print('>', self.phase)
        
    def update(self):
        self._get_process() # Get the pid
        self._get_logname() # Get the filename

        p_phase = self.phase # Store previous phase
        if self._log_has_changed(): # Check if the log has changed
            self._parse_log() # Parse the changed log
        
        if self.phase == 'ReadyCheck': # If a match has found
            self._get_window() # Get window pid
            self._get_window_info() # Get window dimensions
            self.try_accept_match() # Accept the match
        
        self.log(p_phase) # Print things

def main():
    league_client = LeagueClient()
    if league_client.process == None:
        print("LeagueClient not running")
        return None

    print("I am not afk")
    while league_client.process != None:
        league_client.update()
        time.sleep(0.5)

main()

