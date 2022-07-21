#!/usr/bin/python3
# -*- coding: utf-8 -*-

from modules.color_log import color_log, purple, green, red, yellow, normal
from modules.get_proxy import get_good_proxy
from modules.selenium.webdriver.common.keys import Keys
from modules.selenium.webdriver.common.by import By
from modules.selenium import webdriver
import modules.requests
from multiprocessing import Pool
from typing import List
import time
import random
import sys
import os

directory_script = os.path.abspath('')

sys.path.insert(1, directory_script + '/modules')


global index_i
index_i = 0


def main() -> None:
    try:
        global index_i
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
        options.add_argument("--start-maximized")

        # Отключаем сохранение паролей, webrtc и устанавливаем англ язык
        options.add_experimental_option(
            'prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                },
                'intl.accept_languages': 'en,en_US',
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False
            })

        options.headless = True

        rand_proxy = random.choice(get_good_proxy())
        options.add_argument(f'--proxy-server={rand_proxy}')
        driver = webdriver.Chrome(
            #executable_path = directory_script + '/data/chromedriver',
            options=options)
        driver.set_window_size(1920, 1080)
        # Список блокируемых форматов изображений
        img_format_list = [
            '*.svg*', '*.png*', '*.jpg*', '*.jpeg*', '*.bmp*', '*.gif*',
            '*.tif*', '*.ico*', '*adpresenter.de*'
        ]
        driver.execute_cdp_cmd('Network.setBlockedURLs',
                               {'urls': img_format_list})
        driver.execute_cdp_cmd('Network.enable', {})

        # -------------------------------- Регистрация -------------------------------- #
        try:
            modules.requests.head('https://skibbel-1.bmsjava.repl.co')
        except:
            pass
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
                if driver.find_element(
                        By.XPATH,
                        '//button[@id="btnStartText" and @disabled="disabled"]'
                ).is_displayed():
                    time.sleep(1)
                    cicle += 1
            elif len(
                    driver.find_elements(
                        By.XPATH,
                        '//button[@id="btnStartText" and @disabled="disabled"]'
                    )) == 0:
                visible = True
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
            try:
                modules.requests.head('https://skibbel-1.bmsjava.repl.co')
            except:
                pass
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
            # Пишем первое сообщение
            probel = '​'
            text = f'F{probel * random.randint(1,9)}uc{probel * random.randint(1,9)}k m{probel * random.randint(1,9)}e pl{probel * random.randint(1,9)}ea{probel * random.randint(1,9)}se ❤️{probel * random.randint(1,9)}❤️{probel * random.randint(1,9)}❤️ 👉 https://bit.ly/3Pk9bc0 {probel * random.randint(1,9)}'
            javaScript = f'document.getElementById("ownMessage").value="{text}"'
            driver.execute_script(javaScript)
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
            text = f'Программа SKIBBEL Сервер № 1. Отправили сообщений - {str(index_i)}'
            modules.requests.get(
                f'https://api.telegram.org/bot5130975486:AAF4z76SYX1GrzsbLOPp5UWOPGB90VKcBzw/sendMessage?chat_id=-1001500342257&text={text}'
            )
        # ----------------------------------------------------------------------------- #

    except Exception as ex:
        text = f'Программа SKIBBEL Сервер № 1. Ошибка\n{ex}'
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
