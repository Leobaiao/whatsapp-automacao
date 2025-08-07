from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from until.utilitys import *


class SmartphonePage:

    def __init__(self, driver):
        self.driver = driver

    def abrirDiscador(self):
        self.driver.press_keycode(3)
        self.driver.activate_app('com.samsung.android.dialer')
        dialpad = esperar_elemento_visivel(self.driver, (By.ID, "com.samsung.android.dialer:id/dialpad_spacer_view"))
        if dialpad:
            dialpad.click()



    def fecharDiscador(self):
        self.driver.terminate_app("com.samsung.android.dialer")

