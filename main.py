#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
directory_script = os.path.abspath('')
import sys
sys.path.insert(1, directory_script + '/modules')

import random
import time
from typing import List
import json
import re
import urllib3


import modules.requests
from modules.selenium import webdriver
from modules.selenium.webdriver.common.by import By
from modules.selenium.webdriver.common.keys import Keys

from modules.get_proxy import get_good_proxy
from modules.color_log import color_log, purple, green, red, yellow, normal


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global index_i
index_i = 0
global text, url
text = f'Fuck me please ❤️❤️❤️ 👉'
url_creative = 'https://bit.ly/3PMrIhi'


def _replace_platform(platform_name: str) -> str:
    platform_mathches = {
        'Windows NT 10.0'    :  'Windows 10',
        'Windows NT 6.3'     :  'Windows 8.1',
        'Windows NT 6.2'     :  'Windows 8',
        'Windows NT 6.1'     :  'Windows 7',
        'Windows NT 6.0'     :  'Windows Vista',
        'Windows NT 5.2'     :  'Windows Server 2003/XP x64',
        'Windows NT 5.1'     :  'Windows XP',
        'Windows xp'         :  'Windows XP',
        'Windows NT 5.0'     :  'Windows 2000',
        'Windows me'         :  'Windows ME',
        'Win98'              :  'Windows 98',
        'Win95'              :  'Windows 95',
        'Win16'              :  'Windows 3.11',
    }
    if platform_name not in platform_mathches:
        return 'Windows 10'
    return platform_mathches[platform_name]


def main() -> None:
    try:
        global index_i
        global text, url_creative
        rand = random.uniform(0.1, 0.9)
        url = f'https://fingerprints.bablosoft.com/preview?rand={str(rand)}&tags=Chrome,Desktop,Microsoft Windows'
        r = modules.requests.get(url, verify = False)
        json_text = json.loads(r.text)
        ua = json_text['ua']
        platform = re.search(r'\((Win[^;]+);', ua).group(1)
        width = json_text['availWidth']
        height = json_text['availHeight']
        webgl_vendor = json_text['vendor']
        renderer = json_text['renderer']

        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches",
                                        ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--enable-webgl-draft-extensions")
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument('disable-infobars')
        options.add_argument('--start-maximized')


        # Отключаем сохранение паролей
        options.add_experimental_option(
            'prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                },
            })

        options.headless = False

        # Получаем все прокси
        all_proxy = get_good_proxy()

        # Получаем данные о timezone
        good_proxy = False
        cicle = 0
        while good_proxy == False:
            if cicle >= len(all_proxy):
                raise Exception('Не удалось найти рабочий прокси... Переподключаемся')
            try:
                # Получаем случайный прокси
                rand_proxy = random.choice(all_proxy)
                ip = re.search(r'socks\d:\/\/(\d+\.\d+\.\d+\.\d+):\d+', rand_proxy).group(1)
                url = f'http://worldtimeapi.org/api/ip/{ip}.json'
                r = modules.requests.get(url, verify = False, timeout = 3)
                json_text = json.loads(r.text)
                timezone = json_text['timezone']
                good_proxy = True
            except:
                cicle += 1
            

        #utc = json_text['utc_offset']
        driver = webdriver.Chrome(
            executable_path = directory_script + '/data/chromedriver',
            options = options)


        # Установка User Agent и платформы
        override = {"userAgent": ua, "platform": platform}
        driver.execute_cdp_cmd('Network.setUserAgentOverride', override)

        # Список блокируемых форматов изображений
        img_format_list = [
            '*.svg*', '*.png*', '*.jpg*', '*.jpeg*', '*.bmp*', '*.gif*',
            '*.tif*', '*.ico*', '*adpresenter.de*'
        ]
        # Запрет загрузки изображений или сайтов
        driver.execute_cdp_cmd('Network.setBlockedURLs',
                                {'urls': img_format_list})
        driver.execute_cdp_cmd('Network.enable', {})

        # Установка времени системы
        driver.execute_cdp_cmd('Emulation.setTimezoneOverride',{'timezoneId': f'{timezone}'})

        # Установка данных о браузере
        screenOrientation = dict(angle=0, type='portraitPrimary')
        driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
            'mobile': False,
            'width': width,
            'height': height,
            'deviceScaleFactor': 1,
            'screenOrientation': screenOrientation,
            'vendor':'Google Inc.',
            'platform':platform,
            'webgl_vendor':webgl_vendor,
            'renderer':renderer,
            'fix_hairline':True,
            'languages':["en-US", "en"]
        })
        # Отключаем отслеживание webrtc
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                const newProto = navigator.__proto__
                delete newProto.webdriver
                navigator.__proto__ = newProto
                """
            })

        # Исправляем hearlines modernizr
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
                Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
                ...elementDescriptor,
                get: function() {
                    if (this.id === 'modernizr') {
                        return 1;
                    }
                    return elementDescriptor.get.apply(this);
                    },
                });   
                '''
            })
        

        # -------------------------------- Регистрация -------------------------------- #
        driver.set_page_load_timeout(30)
        driver.get('https://www.skibbel.com/')

        # Ждем загрузки всей страницы
        cicle = 0
        while len(driver.find_elements(By.CSS_SELECTOR, '#gender_text')) == 0:
            if cicle >= 30:
                raise Exception('Не дождались загрузки начальной страницы')
            time.sleep(1)
            cicle += 1
        time.sleep(0.5)

        # Ставим фото
        rand_photo = directory_script + '/photos/' + random.choice(
            os.listdir(directory_script + '/photos'))
        file_oldname = os.path.join(rand_photo)
        name_photo_list = ['may', 'april', 'oktober', 'december', 'september']
        file_newname_newfile = os.path.join(
            directory_script + '/photos',
            f'{random.choice(name_photo_list)}{random.randint(100, 5000)}.jpg')
        os.rename(file_oldname, file_newname_newfile)
        if len(driver.find_elements(By.CSS_SELECTOR, '#galleryPicture')) != 0:
            driver.find_element(
                By.CSS_SELECTOR,
                '#galleryPicture').send_keys(file_newname_newfile)
        time.sleep(1)

        # Выбираем свой пол
        while len(driver.find_elements(By.CSS_SELECTOR, '#gender_text')) == 0:
            time.sleep(1)
        driver.find_element(By.XPATH,
                            '(//div[@class="select-wrapper"])[1]').click()
        time.sleep(0.5)
        driver.find_element(
            By.XPATH, '(//div[@class="select-wrapper"])[1]/ul/li[3]').click()
        time.sleep(0.5)

        # Выбираем свой возраст
        while len(driver.find_elements(By.CSS_SELECTOR, '#my_age_text')) == 0:
            time.sleep(1)
        driver.find_element(By.XPATH,
                            '(//div[@class="select-wrapper"])[2]').click()
        time.sleep(0.5)
        driver.find_element(
            By.XPATH,
            f'(//div[@class="select-wrapper"])[2]/ul/li[{random.randint(2, 12)}]'
        ).click()
        time.sleep(0.5)

        # Выбираем пол собеседника
        while len(driver.find_elements(By.CSS_SELECTOR,
                                       '#s_gender_text')) == 0:
            time.sleep(1)
        driver.find_element(By.XPATH,
                            '(//div[@class="select-wrapper"])[3]').click()
        time.sleep(0.5)
        driver.find_element(
            By.XPATH, '(//div[@class="select-wrapper"])[3]/ul/li[2]').click()
        time.sleep(0.5)

        # Ждем и нажимаем кнопку начать чат
        cicle = 0
        visible = False
        while visible == False:
            if cicle >= 30:
                raise Exception('Не дождались появления кнопки НАЧАТЬ ЧАТ')
            if len(
                    driver.find_elements(
                        By.XPATH,
                        '//button[@id="btnStartText" and @disabled="disabled"]'
                    )) != 0:
                time.sleep(1)
                cicle += 1
            elif len(
                    driver.find_elements(
                        By.XPATH,
                        '//button[@id="btnStartText" and @disabled="disabled"]'
                    )) == 0:
                visible = True
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#btnStartText').click()
        time.sleep(2)

        # Закрываем лишние окна
        if len(driver.window_handles) > 1:
            for _ in range(len(driver.window_handles) - 1):
                main_page = driver.window_handles[0]
                driver.switch_to.window(main_page)
                driver.close()
                time.sleep(0.5)
            main_page = driver.window_handles[0]
            driver.switch_to.window(main_page)
        time.sleep(0.5)
        # Список блокируемых форматов изображений
        img_format_list = [
            '*.svg*', '*.png*', '*.jpg*', '*.jpeg*', '*.bmp*', '*.gif*',
            '*.tif*', '*.ico*', '*adpresenter.de*'
        ]
        driver.execute_cdp_cmd('Network.setBlockedURLs',
                               {'urls': img_format_list})
        driver.execute_cdp_cmd('Network.enable', {})
        color_log(f'Прошли регистрацию', green)
        # ----------------------------------------------------------------------------- #

        # --------------------------------- Рассылка ---------------------------------- #
        for _ in range(random.randint(200, 250)):
            # Проверяем подключился ли партнер
            index = 0
            visible = True
            while visible == True:
                if index >= 10:
                    raise Exception('Меняем IP')
                if len(driver.find_elements(By.XPATH,
                                            '//p[@class="info"]')) != 0:
                    if driver.find_element(
                            By.XPATH, '//p[@class="info"]').is_displayed():
                        color_log('Ждём подключения партнёра', yellow)
                        time.sleep(3)
                        index += 1
                    else:
                        visible = False
                        time.sleep(1)
                else:
                    visible = False
                    time.sleep(1)
            time.sleep(random.randint(3, 6))
            # Проверяем есть ли видео звонок
            if len(
                    driver.find_elements(
                        By.XPATH,
                        '//*[@id="video_call"]/div/div/a[2]/i')) != 0:
                if driver.find_element(
                        By.XPATH,
                        '//*[@id="video_call"]/div/div/a[2]/i').is_displayed():
                    element = driver.find_element(
                        By.XPATH, '//*[@id="video_call"]/div/div/a[2]/i')
                    driver.execute_script("arguments[0].click();", element)
            # Проверяем рекламу
            if len(
                    driver.find_elements(
                        By.XPATH,
                        '//button[@class="swal2-cancel swal2-styled"]')) != 0:
                if driver.find_element(
                        By.XPATH,
                        '//button[@class="swal2-cancel swal2-styled"]'
                ).is_displayed():
                    element = driver.find_element(
                        By.XPATH,
                        '//button[@class="swal2-cancel swal2-styled"]')
                    driver.execute_script("arguments[0].click();", element)
            # Проверяем не ушел ли из чата партнер
            if len(
                    driver.find_elements(
                        By.XPATH,
                        '//div[@class="text-message red offline"]')) != 0:
                if driver.find_element(
                        By.XPATH, '//div[@class="text-message red offline"]'
                ).is_displayed():
                    element = driver.find_element(
                        By.XPATH, '//div[@class="text-message red offline"]')
                    color_log(f'Партнер отключился', yellow)
                    driver.execute_script("arguments[0].click();", element)
                    continue
            time.sleep(1)

            def _a(one: int, two: int) -> str:
                probel = '​'
                return probel * random.randint(one, two)

            
            # Уникализируем крео
            if type(text) == list:
                text = random.choice(text)
            text_list = list(text)  
            c = [i + _a(1, 9) if  i != ' ' else ' ' for i in text_list ]
            rand_text = ''.join(c) + f' {url_creative} {_a(1, 9)}'
            # Пишем первое сообщение
            javaScript = f'document.getElementById("ownMessage").value="{str(rand_text)}"'
            driver.execute_script(javaScript)
            time.sleep(1)
            driver.find_element(By.XPATH,
                                '//*[@id="ownMessage"]').send_keys(' ')
            time.sleep(1)
            driver.find_element(By.XPATH,
                                '//*[@id="ownMessage"]').send_keys(Keys.ENTER)
            time.sleep(random.randint(2, 5))

            element = driver.find_element(By.XPATH,
                                          '//i[@class="fa fa-user-times"]')
            driver.execute_script("arguments[0].click();", element)
            index_i += 1
            color_log(f'Отправили сообщений - {str(index_i)}', green)
            text = f'Программа SKIBBEL Сервер zomro № 1. Отправили сообщений - {str(index_i)}'
            modules.requests.get(
                f'https://api.telegram.org/bot5130975486:AAF4z76SYX1GrzsbLOPp5UWOPGB90VKcBzw/sendMessage?chat_id=-1001500342257&text={text}'
            )
        # ----------------------------------------------------------------------------- #

    except Exception as ex:
        text = f'Программа SKIBBEL Сервер zomro № 1. Ошибка\n{ex}'
        modules.requests.get(
            f'https://api.telegram.org/bot5130975486:AAF4z76SYX1GrzsbLOPp5UWOPGB90VKcBzw/sendMessage?chat_id=-1001656173344&text={text}'
        )
        color_log(ex, red)

    finally:
        try:
            driver.close()
            driver.quit()
        except:
            color_log(f'НЕ УДАЛОСЬ ЗАПУСТИТЬ WEBDRIVER', red)


while True:
    main()
