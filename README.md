# discord-bot-logger
Use discord as a logger

Thanks for this guide: https://realpython.com/how-to-make-a-discord-bot-python/#creating-an-application

Follow this to create bot and copy bot's TOKEN
Pre-defineed configuration of the bot is at /var/log/bots/discord.cfg
Log is at: /var/log/bots/discord-bot.log
Run the bot:
```
export TOKEN=<bot_token>
python src/bot.py
```

At config channel on discord app. you can change the config on the fly.

```
DucPhamTV
 — 
02/11/2021
!cfg load_config
rasp3-monitorBOT
 — 
02/11/2021
Load config from storage{'cameras_list': [], 'interval': 10, 'cloud_nodes': ['https://duc-blogs.herokuapp.com/posts/', 'https://duc-blogs.herokuapp.com/%27]%7D
DucPhamTV
 — 
02/11/2021
!cfg load_config
rasp3-monitorBOT
 — 
02/11/2021
Load config from storage{'cameras_list': [], 'interval': 10, 'cloud_nodes': ['https://duc-blogs.herokuapp.com/posts/', 'https://duc-blogs.herokuapp.com/%27]%7D
DucPhamTV
 — 
02/11/2021
!cfg add_cloud_nodes http://192.168.1.2/
rasp3-monitorBOT
 — 
02/11/2021
Updated cloud_nodes: ['http://192.168.1.2/']
DucPhamTV
 — 
02/11/2021
!cfg set_interval 10
rasp3-monitorBOT
 — 
02/11/2021
interval has been updated to 10 seconds
DucPhamTV
 — 
02/11/2021
!cfg add_cloud_nodes http://192.168.1.2/
rasp3-monitorBOT
 — 
02/11/2021
Updated cloud_nodes: ['http://192.168.1.2/']
DucPhamTV
 — 
02/11/2021
!cfg set_interval 10
rasp3-monitorBOT
 — 
02/11/2021
interval has been updated to 10 seconds
DucPhamTV
 — 
02/11/2021
!cfg add_cloud_nodes https://duc-blogs.herokuapp.com/posts/
Duc Pham's blog
rasp3-monitorBOT
 — 
02/11/2021
Updated cloud_nodes: ['https://duc-blogs.herokuapp.com/posts/']
DucPhamTV
 — 
02/11/2021
!cfg set_interval 120
rasp3-monitorBOT
 — 
02/11/2021
interval has been updated to 120 seconds
```
