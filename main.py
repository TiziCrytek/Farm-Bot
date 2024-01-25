from time import sleep
from farm_bot import FarmBot

with open('addr.txt', 'r') as file:
    device = file.readline()

def main():
    bot = FarmBot(device)
    print('Start Farm')
    bot.start()

main()