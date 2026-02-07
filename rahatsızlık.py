import pyautogui
import time
time.sleep(5)  # 5 saniye bekle
for i in range(100):  # 100 kez mesaj gönder
    pyautogui.typewrite("damar gg!")  # Mesaj yaz
    pyautogui.press("enter")             # Enter tuşuna bas