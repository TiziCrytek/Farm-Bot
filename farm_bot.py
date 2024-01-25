import uiautomator2 as u2
import json, random
from time import sleep

class FarmBot:
    def __init__(self, addres):
        self.connect_deviec(addres)
        self.alive = True

        self.home_btn = self.d(description="Главная")
        self.games_btn = self.d(description="Игры")
        self.bonus_btn = self.d(className='android.widget.Button', index=1, description='Забрать', enabled='true')
        self.quiz_btn = self.d(className='android.widget.Button', index=5, description='Забрать', enabled='true')

        self.package = 'com.skinsfarm.farm'
        self.activity = '.MainActivity'

    def main(self):
        while True:
            if self.alive:
                if not self.check_app():
                    self.app_start()
                    sleep(2)
                    self.games_btn.click()

                if self.quiz_btn.click_exists():
                    sleep(2)
                    # self.quiz()
                    self.d.app_stop(self.package)
                    self.d.screen_off()
                    sleep(60*60*3 + random.randint(1, 20))
                    self.d.screen_on()
                    self.d.swipe(500, 1000, 500, 500, 400)

                # if self.bonus_btn.click_exists():
                #     self.get_bonus()

    def quiz(self):
        while self.alive:
            if self.d(description="Далее").click_exists():
                sleep(0.8)
                if self.d(description="Закрыть").click_exists():
                    return

            with open('db.json', 'r', encoding='utf-8') as file:
                data = json.load(file)

            sleep(3)

            title = self.d(className='android.view.View', index='7').info.get('contentDescription')
            btns = self.d(className='android.widget.Button')

            if title not in data:
                data[title] = {"q": "", "w": []}

            buttons_list = list(btns)

            random.shuffle(buttons_list)
            bl = []
            b = False
            print()
            print(title)

            for btn in buttons_list:
                if btn.info['contentDescription'] == data[title]['q']:
                    b = False
                    print(f'DB SUCCESS {btn.info["contentDescription"]}')
                    btn.click()
                    break
                
                if data[title]['w'] != [] and btn.info['contentDescription'] in data[title]['w']:
                    print(f'SKIP: {btn.info["contentDescription"]}')
                    continue

                bl.append(btn)
                b = True

            if b:
                for btn in bl:

                    test_btn = btn.info['contentDescription']
                    sleep(0.5)
                    btn.click()
                        
                    sleep(2)

                    if self.d(description="Выйти").exists:
                        print(f'DARK: {test_btn}')
                        data[title]["w"].append(test_btn)
                        with open('db.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4, ensure_ascii=False)
                        self.d(description="Выйти").click()
                        # d(description="Посмотреть рекламу").click()
                        
                        # while True:
                        #     if d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.widget.ImageView[2]').exists:
                        #         print('OK')
                        #         break

                        #     # if d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]').exists:
                        #     #     d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]').click()
                            
                        #     sleep(1)
                        break
                    else:
                        print(f'SUCCESS: {test_btn}')
                        data[title]["q"] = test_btn
                        with open('db.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4, ensure_ascii=False)
                        break

                sleep(2)
                self.quiz_btn.click()

    def get_bonus(self):
        sleep(1)
        self.d(description="Забрать бонус").click_exists()
        sleep(31)

    def start(self):
        self.d.screen_on()
        self.d.swipe(500, 1000, 500, 500, 400)
        sleep(2)
        self.app_start()

        self.games_btn.click()
        self.main()

    def app_start(self):
        if not self.check_app():
            self.d.app_start(self.package, self.activity)
            while True:
                if self.home_btn.exists:
                    break
                sleep(0.5)

    def check_app(self):
        if self.d.app_current()['package'] != self.package:
            return False
        
        return True

    def get_balance(self):
        pass

    #!!!!!!!!!!EDIT!!!!!!!!!!!!!!
    def connect_deviec(self, addres):
        while True:
            try:
                self.d = u2.connect_adb_wifi(addres)
                return
            except:
                sleep(10)