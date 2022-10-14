from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import configparser

CHROMEDRIVER = "chromedriver.exe"

# ConfigParserのインスタンスを取得
config = configparser.ConfigParser()

# configを読みだし
config.read("config.ini", 'UTF-8')

user_name = config["BASE"]["user_id"]
pass_word = config["BASE"]["password"]
target_id = config["BASE"]["target_id"]
listing_num = config["BASE"]["listing_num"]

# リストした数をカウントする変数


chrome_service = fs.Service(executable_path=CHROMEDRIVER)
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


def login(username, password):
    # ログインページを開く
    driver.get("https://twitter.com/i/flow/login")
    time.sleep(2)

    # account入力
    element_account = driver.find_element(By.NAME, "text")
    element_account.send_keys(username)

    # デバッグ1
    # driver.save_screenshot("①ログインID入力画面.png")

    # 次へボタンをクリック
    element_login_next = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    element_login_next.click()
    time.sleep(3)

    # パスワード入力
    element_pass = driver.find_element(By.NAME, "password")
    element_pass.send_keys(password)

    # デバッグ2
    # driver.save_screenshot('②ログインPW入力画面.png')

    # ログインボタンクリック
    element_login = driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    element_login.click()

    time.sleep(5)

    # デバッグ3
    # driver.save_screenshot('③ログイン後の画面.png')


def jump_to_page(username):

    # ユーザーのページに飛ぶ
    driver.get("https://twitter.com/" + username)
    time.sleep(3)

def start_listing():

    # リスティングしたユーザー名を保管する変数の初期化
    listed_user = []
    # リストした数をカウントする変数
    listed_number = 0

    # フォロワーをクリック
    element_follower = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]')
    element_follower.click()
    time.sleep(3)

    # フォロワーを配列に格納
    element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
    print(element_follower)

    for i in range(0, int(listing_num)):
        element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
        print("start another loop")
        for index, item in enumerate(element_follower):

            if listed_number > int(listing_num):
                quit()

            element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
            time.sleep(1)

            # フォロワーズがout of rangeの場合リセット
            try:
                user_name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[' +str(index + 1) + ']/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span').text
            except NoSuchElementException:

                scroll_by_offset(element_follower[index], 500)
                break

            if user_name not in listed_user:
                time.sleep(1)
                # リストしたユーザーネームを格納
                listed_user.append(user_name)
                print(listed_user)
                # フォロワーをクリック
                element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
                driver.execute_script("arguments[0].scrollIntoView();", element_follower[index])
                driver.execute_script("window.scrollBy(0, -100)", "")
                element_follower[index].click()
                print(index)
                # ちょぼマークをクリック
                time.sleep(3)
                # ちょぼマーク要素が存在する時にだけ以下のスクリプトを実行する
                is_present = driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div[1]/div')
                if len(is_present) > 0:
                    driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div[1]/div').click()
                    # リストに追加をクリック
                    time.sleep(2)
                    is_present2 = driver.find_elements(By.XPATH,
                                                      '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/a[2]/div[2]')
                    if len(is_present2) > 0:
                        driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/a[2]/div[2]').click()
                        # 一番上のリストをクリック
                        time.sleep(2)
                        driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/section/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div').click()
                        # 保存をクリック
                        time.sleep(2)
                        driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[3]/div/div').click()

                        # リストに加えた人数を増やす
                        listed_number += 1
                        print("listed " + str(listed_number) + " people.")
                # 一個戻る
                driver.back()
                time.sleep(1)

            else:
                print(user_name + ' is already listed')

            # # フォロワーを配列に格納
            # element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
            # if index >= 25:
            #     driver.execute_script('arguments[0].scrollIntoView(true)',  element_follower[index])
            #
            #     element_followers = driver.find_element(By.XPATH,
            #                                             '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div')
            #
            #     # フォロワーを配列に格納
            #     element_follower = driver.find_elements(By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]')
            #     print(len(element_follower))


def scroll_by_offset(element, offset=0):

    driver.execute_script("arguments[0].scrollIntoView();", element)

    if offset != 0:
        script = "window.scrollTo(0, document.body.scrollHeight);"
        driver.execute_script(script)


jump_to_page(target_id)
login(user_name, pass_word)
jump_to_page(target_id)
start_listing()

