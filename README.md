# iamnotafk
  A python script that accepts league of legends matchs automatically and notifies with beeps, messages on the screen and discord messages!

# Requirements
  Python==3.8.6 
  PyAutoGUI==0.9.47
  PyGetWindow==0.0.9
  requests==2.24.0 

# Installing
  git clone git://github.com/gbrlbsls/iamnotafk.git

# Configuring
  There is a config.ini file that contains some configurations:
  
  GAME_START_CLOSE
    Close program when the game starts (can be better on potatos computers like mine)
    
  GAME_START_ALERT_BEEP
    Alert game start with some beeps (the value is the number of beeps)
    
  GAME_START_ALERT_TEXT
    Show a message box alerting that the game was started (useful if you want to watch something while the game is loading)
   
  DISCORD_WEBHOOK
    Set the webhook url ( [How to create one](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) )
    
  GAME_PHASES_ALERT_DISCORD
    Send a message on discord with the game phase(like picks and bans, pick turn, ban turn, game start) | Needs webhook
   
  DISCORD_MENTION
    Use a different name on discord messages (like "Sir, the game was started!" instead of "Hey, the game was started!")
  
  DISCORD_WEBHOOK_PARAMS
    Set some webhook params ( [See more here](https://discord.com/developers/docs/resources/webhook) )
  
# How i use?
  1. I created a discord server
  2. I created a webhook
  3. I put the webhook and my nick in the config.ini
  4. I start the script and walk to my kitchen to get some snacks
  
# How the program works?
  The program reads the league client logs and game logs to see if some match was found, the game was started or where we are in the phases(picks and bans, queue, out of queue, accepting match, in game). When some match is found, click on the 'Accept match' button. (The program doesn't find the button on screen, just click on it by a relative position multiplier, if that exists).
  
  I've tested only in windows 7 32 bits.
  
# Running
    python afk.py
