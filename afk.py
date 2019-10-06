import os
import time
import psutil
import re

import win32gui
import pyautogui

LEAGUE_WINDOW_TITLE = 'League of Legends'
LEAGUE_PROCESS_NAME = 'LeagueClient.exe'
LEAGUE_GAME_NAME = 'League of Legends.exe'
LEAGUE_PHASES = ['Lobby', 'Matchmaking', 'ReadyCheck', 'ChampSelect', 'GameStart', 'PostGame', 'ReadyCheckAccepted']

class LeagueClient(object):
    def __init__(self):
        self.hwnd = None
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

        self.phase = None

        self.process = None
        self.logname = None

        # log attrs
        self._last_size = 0
        self._last_str = ''
        self._file_index = 0

        self.update()

    def focus(self):
        try:
            if win32gui.IsIconic(self.hwnd):
                win32gui.ShowWindow(self.hwnd, 9)
                return False

            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.SetActiveWindow(self.hwnd)
        except:
            pass
        
        return self._is_focused()

    def _is_focused(self):
        return (win32gui.GetForegroundWindow() == self.hwnd) and (win32gui.IsWindowVisible(self.hwnd) == 1)

    def _get_window(self):
        self.hwnd = win32gui.FindWindow(None, LEAGUE_WINDOW_TITLE)
        if self.hwnd <= 0:
            self.hwnd = None

    def _get_window_info(self):
        if self.hwnd == None:
            return
        
        rect = win32gui.GetWindowRect(self.hwnd)
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2] - self.x
        self.h = rect[3] - self.y

    def _get_process(self):
        self.process = None
        for p in psutil.process_iter(attrs=['exe']):
            if p.info['exe'] != None and p.info['exe'].endswith(LEAGUE_PROCESS_NAME):
                self.process = p

    def _get_logname(self):
        if self.process == None:
            self.logname = None
            return None

        try:
            # this returns the list of opened files by the current process
            flist = self.process.open_files()
            if flist:
                for nt in flist:
                    if nt.path.endswith('LeagueClient.log'):
                        self.logname = nt.path

        # This catches a race condition where a process ends
        # before we can examine its files
        except psutil.NoSuchProcess:
            self.logname = None

    def _update_log(self):
        if self.process == None:
            return False

        with open(self.logname) as f:
            f.seek(self._file_index)
            self._last_str = f.read(self._last_size - self._file_index)
            self._file_index = self._last_size
        
        return True

    def _log_has_changed(self):
        if self.logname == None:
            return False

        fsize = os.stat(self.logname).st_size
        if fsize != self._last_size:
            self._last_size = fsize
            self._update_log()
            return True

        return False

    def _parse_log(self):
        lines = self._last_str.splitlines()

        for lineNumber in reversed(range(len(lines))):
            line = lines[lineNumber]
            phase = re.search(r'Gameflow: entering state \'(\w+)\'', line)
            if phase != None:
                phase = phase.group(1)
                if (self.phase != phase) and LEAGUE_PHASES.count(phase) > 0:
                    self.phase = phase
                    break
            elif 'READY_CHECK_USER_ACCEPTED' in line:
                self.phase = 'ReadyCheckAccepted'
                break

    def _accept_match(self):
        button_x = self.x + (self.w * 0.511)
        button_y = self.y + (self.h * 0.765)

        pyautogui.click(x=button_x, y=button_y) 

    def try_accept_match(self):
        if(self.focus()):
            self._accept_match()

    def log(self, p_phase):
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

    def wait_game(self):
        while True:
		    has_game_process = False # League game process found
            for p in psutil.process_iter(attrs=['exe']):
			    pname = p.info['exe']
                if pname != None and pname.endswith(LEAGUE_GAME_NAME): # Find the game process, if it exists, we can continue the program
                    has_game_process = True
			
		    if not has_game_process:
		        break

            time.sleep(5)
            
                

    def update(self):
        self._get_process()
        self._get_logname()

        p_phase = self.phase
        if self._log_has_changed():
            self._parse_log()
        
        if self.phase == 'ReadyCheck':
            self._get_window()
            self._get_window_info()
            self.try_accept_match()
        
        self.log(p_phase)

def main():
    sleep_time = 1
    print(":> I am not afk!")
    league_client = LeagueClient()
    if league_client.process == None:
        print(":< Because the client isn't running...")
        return None
    while league_client.process != None: # Keep running until the client is closed
        league_client.update()
        if league_client.phase == 'GameStart': # Check if the game was started
            print('>', 'Waiting game end...')
            league_client.wait_game() # Wait it finishes, reducing cpu consumption
        elif league_client.phase == 'Matchmaking':
            sleep_time = 0.5 # When in the queue, check faster for changes
        else:
            sleep_time = 1 # else, we can slow down

        time.sleep(sleep_time)

main()

