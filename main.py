from time import sleep
from farm_bot import FarmBot

def main():
    bot = FarmBot('5.tcp.eu.ngrok.io:12905')
    input('Enter to Start')
    bot.start()

main()