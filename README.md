# iamnotafk
&nbsp;A python script that accepts league of legends matchs automatically and notifies with beeps, messages on the screen and discord messages!

# Requirements
&nbsp;Python==3.8.6 
&nbsp;PyAutoGUI==0.9.47
&nbsp;PyGetWindow==0.0.9
&nbsp;requests==2.24.0 

# Installing
&nbsp;git clone git://github.com/gbrlbsls/iamnotafk.git

# Configuring
&nbsp;There is a config.ini file that contains some configurations:
  
&nbsp;GAME_START_CLOSE
&nbsp;&nbsp;Close program when the game starts (can be better on potatos computers like mine)
    
&nbsp;GAME_START_ALERT_BEEP
&nbsp;&nbsp;Alert game start with some beeps (the value is the number of beeps)
    
&nbsp;GAME_START_ALERT_TEXT
&nbsp;&nbsp;Show a message box alerting that the game was started (useful if you want to watch something while the game is loading)
   
&nbsp;DISCORD_WEBHOOK
&nbsp;&nbsp;Set the webhook url ( [How to create one](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) )
    
&nbsp;GAME_PHASES_ALERT_DISCORD
&nbsp;&nbsp;Send a message on discord with the game phase(like picks and bans, pick turn, ban turn, game start) | Needs webhook
   
&nbsp;DISCORD_MENTION
&nbsp;&nbsp;Use a different name on discord messages (like "Sir, the game was started!" instead of "Hey, the game was started!")
  
&nbsp;DISCORD_WEBHOOK_PARAMS
&nbsp;&nbsp;Set some webhook params ( [See more here](https://discord.com/developers/docs/resources/webhook) )
  
# How i use?
&nbsp;1. I created a discord server
&nbsp;2. I created a webhook
&nbsp;3. I put the webhook and my nick in the config.ini
&nbsp;4. I start the script and walk to my kitchen to get some snacks
  
# How the program works?
&nbsp;The program reads the league client logs and game logs to see if some match was found, the game was started or where we are in the phases(picks and bans, queue, out of queue, accepting match, in game). When some match is found, click on the 'Accept match' button. (The program doesn't find the button on screen, just click on it by a relative position multiplier, if that exists).
  
&nbsp;I've tested only in windows 7 32 bits.
  
# Running
&nbsp;python afk.py
