import time
import pygetwindow as gw
import ctypes  
from discord import DiscordBot

from league_game import LeagueGame
from league_client import LeagueClient
from config import Config
from util import pretty_print, pretty_log
from const import *

WINDOW_TITLE = 'iamnotafk (' + str(time.time()) + ')'

def focus_program():
    w = gw.getWindowsWithTitle(WINDOW_TITLE)
    if len(w) < 1:
        return
    
    w = w[0]
    if not w.isMinimized:
        w.minimize()

    w.restore()
    w.activate()   

def main():
    sleep_time = 1

    ctypes.windll.kernel32.SetConsoleTitleW(WINDOW_TITLE)  
    pretty_log("I Am Not Afk!")

    config = Config()
    
    print(('\t' + '\n\t'.join(config.printable(True).split('\n'))).expandtabs(11))
   
    discord_bot = DiscordBot(config.get_str_value('DISCORD_WEBHOOK') + config.get_str_value('DISCORD_WEBHOOK_PARAMS'))
    
    league_client = LeagueClient()
    league_game = LeagueGame()

    first_loop = True
    while True: # Keep running until the client is closed
        league_client.update()
        league_game.update()
        if league_client.exists():
            if league_client.in_phase(LEAGUE_PHASE.QUEUE):
                sleep_time = 0.5 # When in the queue, check faster for changes
            else:
                sleep_time = 1 # else, we can slow down

                if league_client.in_phase(LEAGUE_PHASE.MATCHFOUND):
                    league_client.try_accept_match() 

                if league_client.isnt_same_phase():
                    if config.get_bool_value('GAME_PHASES_ALERT_DISCORD') and discord_bot.ok:
                        message = None
                        if league_client.in_phase(LEAGUE_PHASE.PICKSANDBANS):
                            message = ', estamos na seleção de campeões!'
                        elif league_client.in_phase(LEAGUE_PHASE.BAN_TURN):
                            message = ', é sua vez de banir um campeão!'
                        elif league_client.in_phase(LEAGUE_PHASE.PICK_TURN):
                            message = ', selecione seu campeão!'
                        
                        if message:
                            message = (config.get_mention_value('DISCORD_MENTION') or 'Hey') + message
                            discord_bot.send_message(
                                message=message
                            )
        
        if league_game.exists():
            if league_game.has_started():

                if config.get_bool_value('GAME_PHASES_ALERT_DISCORD') and discord_bot.ok:
                    discord_bot.send_message(
                        message=(config.get_mention_value('DISCORD_MENTION') or 'Hey') + ', a partida iniciou!',
                    )
                    
                if config.get_value('GAME_START_ALERT_BEEP') > 0:
                    print('\a' * config.get_value('GAME_START_ALERT_BEEP'), end='')
                if config.get_value('GAME_START_ALERT_TEXT') == 1:
                    if not league_game.is_focused():
                        focus_program()
                    ctypes.windll.user32.MessageBoxW(0, "The game was started!", "I Am Not Afk", 48)
                
                if config.get_value('GAME_START_CLOSE') == 1:
                    break
                else:
                    pretty_log('Waiting game end...')
                    league_game.wait_game_end() # Wait it finishes, reducing cpu consumption
        
        if first_loop:
            if not league_client.exists() and not league_game.exists():
                pretty_log('League Client not found. Searching...')
            first_loop = False
        time.sleep(sleep_time)

try:
    main()
except KeyboardInterrupt:
    pretty_log('Tchau!')

