from time import sleep
from farm_bot import FarmBot

def main():
    ip = input('IP and PORT:' )
    bot = FarmBot(ip)
    bot.start()