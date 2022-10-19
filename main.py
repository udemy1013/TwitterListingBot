#programm in
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import configparser
from webdriver_manager.chrome import ChromeDriverManager
import sys
import tkinter as tk


driver = webdriver.Chrome(ChromeDriverManager().install())

# ConfigParserのインスタンスを取得
config = configparser.ConfigParser()

# リストした数をカウントする変数
# driver = webdriver.Chrome()
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

def start_listing(listing_num):

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


# jump_to_page(target_id)
# login(user_name, pass_word)
# jump_to_page(target_id)
# start_listing()

# PySimpleGUIの記述
# sg.theme("DarkAmber")
#
# # ウィンドウに配置するコンポーネント
# layout = [[sg.Text('Twitter Listing Bot')],
#             [sg.Text('TwitterID'), sg.InputText(key="twitterid")],
#             [sg.Text('Twitterパスワード'), sg.InputText(key="password")],
#             [sg.Text('対象のTwitterID'), sg.InputText(key="targetid")],
#             [sg.Text('リストに追加する人数'), sg.InputText(default_text="1500", key="listingNum")],
#             [sg.Button('スタート'), sg.Button('終了')]]
#
# # ウィンドウの生成
# window = sg.Window('TwitterListingBot', layout)
#
# # イベントループ
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == '終了':
#         break
#     elif event == 'スタート':
#         jump_to_page(values["targetid"])
#         login(values["twitterid"], values["password"])
#         jump_to_page(values["targetid"])
#         start_listing(values["listingNum"])

# window.close()

# tkinter初期設定
root = tk.Tk()
root.title("Twitter listing Bot")
root.geometry("400x300")


def click1():
    jump_to_page(textbox3.get())
    login(textbox1.get(), textbox2.get())
    jump_to_page(textbox3.get())
    start_listing(textbox4.get())


# ユーザー名
label1 = tk.Label(root, text="Twitterユーザー名")
label1.pack()
textbox1 = tk.Entry(master=root)
textbox1.pack()

# パスワード
label2 = tk.Label(root, text="Twitterパスワード")
label2.pack()
textbox2 = tk.Entry(master=root)
textbox2.pack()

# 対象のTwitterID
label3 = tk.Label(root, text="対象のTwitterID")
label3.pack()
textbox3 = tk.Entry(master=root)
textbox3.pack()

# リストする人数
label4 = tk.Label(root, text="リスティングする人数")
label4.pack()
textbox4 = tk.Entry(master=root)
textbox4.pack()
textbox4.insert(0, "1500")

button1 = tk.Button(root, text='開始', command=click1)
button1.pack(pady=30)

root.mainloop()

