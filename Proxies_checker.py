#!/bin/python3

import os, time
from concurrent.futures import ThreadPoolExecutor

# auto module install if module not found
try:
    import requests
except:
    os.system("pip install requests")
    import requests

# get terminal width size
tsize=os.get_terminal_size()[0]
linex=lambda:print("="*tsize)


def main():
    # clear terminate screen
    os.system("clear")
    print(f"""\x1b[38;5;123m
██╗  ██╗██╗   ██╗██████╗ 
██║  ██║██║   ██║██╔══██╗
███████║██║   ██║██████╔╝
██╔══██║██║   ██║██╔══██╗
██║  ██║╚██████╔╝██████╔╝
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ """)
    linex()
    print("\x1b[96m [1] ♲︎︎︎𝐂𝐡𝐞𝐜𝐤 𝐅𝐫𝐨𝐦 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 ")
    print("\x1b[38;5;118m [2] ♲︎︎𝐆𝐞𝐭 𝐅𝐫𝐞𝐞 𝐀𝐜𝐭𝐢𝐯𝐞 𝐏𝐫𝐨𝐱𝐢𝐞𝐬 ")
    linex()
    optz = input("\x1b[96m𝐄𝐧𝐭𝐞𝐫 𝐲𝐨𝐮𝐫 𝐜𝐡𝐨𝐢𝐜𝐞 ➻ ")
    if optz == "1":
        proxies_checker_1()
    elif optz == "2":
        proxies_checker_2()
    else:
        print("Option number", optz, "not found")
        time.sleep(0.2)
        main()

proxies_list = []
def getpx(type):
    global proxies_list
    try:
        data = requests.get(f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={type}&timeout=100000&country=all&ssl=all&anonymity=all").text
        proxies_list += data.splitlines()
    except:
        print("Connection Error")
        time.sleep(1)
        getpx(type)

def proxies_checker_2():
    global proxies_list
    # free http proxies ယူတဲ့အဆင့်
    getpx("http")
    # free socks4 proxies ယူတဲ့အဆင့်
    getpx("socks4")
    # free socks5 proxies ယူတဲ့အဆင့်
    getpx("socks5")
    with ThreadPoolExecutor(max_workers=50) as trd:
        for ip in proxies_list:
            trd.submit(proxy_check, ip)

def proxies_checker_1():
    global proxies_list
    file_name = input("Enter file name : ")
    # file မရှိရင် not found ပြမည့်နေရာ
    if not os.path.isfile(file_name):
        exit("File : " + file_name + " not found")
    # proxies file ကို read လုပ်ပီး list အနေနဲ့ data dictionary ထဲထည့်လိုက်သည်
    data = open(file_name, "r").read().splitlines()
    with ThreadPoolExecutor(max_workers=50) as trd:
        for ip in data:
            trd.submit(proxy_check, ip)




def proxy_check(ip):
    type = ["http","socks4","socks5"] # proxies type
    # proxy နဲ့ http requests တွေတွဲသုံးချင်ရင် dictionary အနေနဲ့သတ်မှတ်ပေးရမှာပါ
    for _type_ in type:
        proxy = {"http":f"{_type_}://{ip}"}
        #print("\x1b[1;97m",proxy)
        try:
            # တကယ်လို့ proxy ကမှားနေရင်တော့ requests လို့ရမှာမဟုတ်ပါဘူး။ error တက်မှာပါ
            data = requests.get("http://ip-api.com/json/", proxies=proxy, timeout=5)
            if data.status_code == 200:
                if proxy["http"].startswith(("http")):
                    color = "\x1b[1;92m"
                elif proxy["http"].startswith(("socks4")):
                    color = "\x1b[1;96m"
                elif proxy["http"].startswith(("socks5")):
                    color = "\x1b[1;93m"
                print(color+"Active    :", proxy["http"])
                
                with open("/sdcard/Download/Telegram/Hub_active_proxies.txt", "a")   as file:
                    file.write(ip + "\n")
                break # active proxy ရလာပီဖြစ်တဲ့အတွက် http proxy လား sock proxy လားထပ်မစစ်တော့ပဲ loop ကို break တာပါ။
        except Exception as Error:
            # requests တဲ့အခါ proxy အလုပ်မလုပ်လို့ error တက်ရင် ဒီပို့ပေးမှာပါ။
            if _type_ == "socks5":
                print("\x1b[1;31mWas Proxy :", ip)
            else:continue



main()
