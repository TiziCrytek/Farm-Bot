from time import sleep
from farm_bot import FarmBot

def main():
    input('Enter to Start')
    bot = FarmBot('5.tcp.eu.ngrok.io:12905')
    bot.start()

main()
