import time
import pyautogui

time.sleep(5)
# Esses 5 segundos são o tempo para posicionar o mouse no campo do email. 
# Como a resolução dos computadores é diferente, isso é importante para selecionar o campo de email no navegador e colocar no código
print(pyautogui.position()) # Dá a posição de onde o mouse está

pyautogui.scroll(200)