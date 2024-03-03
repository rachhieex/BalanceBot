import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials
import os  # Adding the import statement for the os module

# Discord bot token
TOKEN = 'MTIxMzQyOTg0MzE4MjQ4NTU0NQ.Gbl0Qm.YzFPMSshyT1LwYOqDm1CuT9brEUAsY4v4i1CD8'

# Google Sheets credentials
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
CREDS_FILE = os.path.join(os.path.expanduser('~'), 'Downloads', 'balance-bot-415723-890e6a72ca18.json')

# Google Sheet details
SPREADSHEET_KEY = '1eb6eZ3_ntefvULsbkdw_0Wk3hSzVczaQODk1fH1tUUo'
SHEET_NAME = 'From Discord'

# Discord channels to monitor
CHANNEL_IDS = ['1212104092076343429', '1212050634216448050']

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Authenticate with Google Sheets
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_KEY).worksheet(SHEET_NAME)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def syncsheet(ctx):
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(int(channel_id))
        print(f"Syncing messages from channel: {channel.name}")
        async for message in channel.history(limit=None):
            print(f"Message content: {message.content}")
            if message.content.startswith('Name:'):
                # Extracting data from the message
                data = {}
                for line in message.content.split('\n'):
                    if ':' in line:
                        key, value = map(str.strip, line.split(':', 1))
                        data[key] = value
                
                print(f"Extracted data: {data}")
                
                # Updating Google Sheet
                sheet.append_row([data.get('Name', ''),
                                  data.get('Price', ''),
                                  data.get('Booster Name', ''),
                                  data.get('Date', ''),
                                  data.get('Service', ''),
                                  data.get('Advertiser', '')])
    await ctx.send('Google Sheet has been updated with messages from specified channels!')

bot.run(TOKEN)