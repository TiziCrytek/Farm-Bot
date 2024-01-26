import uiautomator2 as u2
import json, random, subprocess
from time import sleep

class FarmBot:
    def __init__(self, addres):
        self.alive = True
        self.d = u2.connect(addres)
        self.home_btn = self.d(description="Главная")
        self.games_btn = self.d(description="Игры")
        self.bonus_btn = self.d(className='android.widget.Button', index=1, description='Забрать', enabled='true')
        self.quiz_btn = self.d(className='android.widget.Button', index=5, description='Забрать', enabled='true')
        self.aim_game = self.d(className='android.widget.Button', index=6, description='Забрать', enabled='true')

        self.back_btn = self.d(resourceId="com.android.systemui:id/back")

        self.package = 'com.skinsfarm.farm'
        self.activity = '.MainActivity'

        self.pm_avtivity = 'com.google.android.finsky.activities.MainActivity'
        self.ads_activity = 'com.applovin.adview.AppLovinFullscreenThemedActivity'

    def main(self):
        while self.alive:
            if self.alive:
                if not self.check_app():
                    self.app_start()
                    sleep(2)
                    self.games_btn.click()
            
                # if self.bonus_btn.click_exists():
                #     self.get_bonus()

                sleep(1.5)
                if self.quiz_btn.click_exists():
                    sleep(2)
                    self.quiz()
                    if self.alive:
                        self.d.app_stop(self.package)
                        self.d.screen_off()
                        sleep(60*60*3 + random.randint(1, 20))
                        self.d.screen_on()
                        self.d.swipe(500, 1300, 500, 200, duration=0.1)
                else:
                    self.d.app_stop(self.package)
                    sleep(2)
                    self.d.screen_off()
                    sleep(30*1 + random.randint(1, 10))
                    self.d.screen_on()
                    self.d.swipe(500, 1300, 500, 200, duration=0.1)

    def quiz(self):
        while self.alive:
            try:
                sleep(1.6)
                if self.d(description="Далее").click_exists():
                    sleep(0.8)
                    if self.d(description="Закрыть").click_exists():
                        return
                    
                with open('db.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)

                title = self.d(className='android.view.View', index='7').info.get('contentDescription')
                btns = self.d(className='android.widget.Button')

                print(title)

                if title not in data:
                    data[title] = {"q": "", "w": []}

                n = 0
                for btn in btns:
                    if not self.alive:
                        return
                    n += 1
                    btn_desc = btn.info['contentDescription']

                    if btn_desc == data[title]['q']:
                        print(f'SUCCESS {btn_desc}')
                        btn.click()
                        break

                    if n == 4:
                        btn.click()
                        sleep(2)
                        if self.d(description="Выйти").click_exists():
                            print(f'DARK: {btn_desc}')
                            data[title]["w"].append(btn_desc)
                            with open('db.json', 'w', encoding='utf-8') as file:
                                json.dump(data, file, indent=4, ensure_ascii=False)
                            self.quiz_btn.click()
                            break
                        else:
                            print(f'DB: {btn_desc}')
                            data[title]["q"] = btn_desc
                            with open('db.json', 'w', encoding='utf-8') as file:
                                json.dump(data, file, indent=4, ensure_ascii=False)
                            break

                    if data[title]['w'] != [] and btn_desc in data[title]['w']:
                        print(f'SKIP: {btn_desc}')
                        continue
            except:
                return

    def get_bonus(self):
        sleep(2)
        if self.d(description="Забрать бонус").click_exists():
            while self.alive:
                if not self.check_ads():
                    continue

                sleep(45)

                if self.d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]').click_exists():
                    break
                
                self.d.click()

                sleep(10)

                sleep(10)
        else:
            self.games_btn.click()

    def start(self):
        # self.d.screen_on()
        # sleep(0.5)
        # self.d.swipe(500, 1300, 500, 200, duration=0.1)
        # sleep(0.5)
        self.app_start()

        self.games_btn.click()
        self.main()

    def stop(self):
        self.d.app_stop(self.package)
        sleep(3)
        self.d.screen_off()

    def app_start(self):
        self.d.app_stop(self.package)
        sleep(0.5)
        if not self.check_app():
            self.d.app_start(self.package, self.activity)
            while self.alive:
                if self.home_btn.exists:
                    break
                sleep(2)

    def check_app(self):
        if self.d.app_current()['package'] != self.package:
            return False
        
        return True

    def check_ads(self):
        if self.d.app_current()['activity'] != self.ads_activity:
            return False
        
        return True

    def check_pm(self):
        if self.d.app_current()['activity'] != self.pm_avtivity:
            return False
        
        return True

    def check_connect(self):
        try:
            if self.d.app_current():
                return True
        except:
            return False
        
        return False

    def get_balance(self):
        pass

    #!!!!!!!!!!EDIT!!!!!!!!!!!!!!
    def connect_deviec(self, addres):
        pass

    def t(self):
        return True