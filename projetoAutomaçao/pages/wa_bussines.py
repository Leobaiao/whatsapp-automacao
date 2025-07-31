from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from until.waits import *
from until.retries import *
import re
import subprocess

class WaBussinesPage:

    def __init__(self, driver):
        self.driver = driver
#Nota: Este mét0do utiliza o decorador @retry para tentar novamente até 3 vezes em caso de falha, com 1 segundos de espera entre as tentativas.
    @retry(max_tentativas=3, delay=1)
    def pegarNumeroChip2(self, udid):
        """
        Tenta obter o número do chip via discador Samsung.
        Retorna o número ou lança exceção em caso de erro.


        """

        try:
            subprocess.run(f'adb -s {udid} shell am start -a android.intent.action.CALL -d tel:*846%23', shell=True)
            try:
                escolherChip = esperar_elemento_visivel(self.driver, (By.ID, "com.samsung.android.incallui:id/title"))
                if escolherChip:
                    chip1 = esperar_elemento_visivel(self.driver, (By.XPATH, '//android.widget.TextView[@resource-id="com.samsung.android.incallui:id/account_label" and @text="SIM 1"]'))
                    chip1.click()
            except:
                pass
            mensagem_elem = esperar_elemento_visivel(self.driver, (By.ID, "android:id/message"))
            mensagem_texto = mensagem_elem.text if mensagem_elem else ""
            if verificar_elemento_visivel(self.driver, (By.XPATH, "//android.widget.TextView[contains(@text, 'Recarga Facil')]"), 20):
                numeros = re.findall(r"\[(\d+)]", mensagem_texto)
                time.sleep(0.5)
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                if numeros:
                    numero = int(numeros[0])
                    print(f"Número encontrado: {numero}")
                    return numero
                else:
                    raise ValueError("Número não encontrado na mensagem.")
            elif mensagem_texto == 'Problema de conexão ou código MMI inválido.':
                print('Número cancelado')
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                raise RuntimeError('Número cancelado')
            elif mensagem_texto == 'UNKNOWN APPLICATION':
                print('Chip da TIM não identificado')
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                raise RuntimeError('Chip da TIM não identificado')
            else:
                print(f"Mensagem inesperada: {mensagem_texto}")
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                print(f"[pegarNumero] Erro: {mensagem_texto}")


        except Exception as e:
            raise {e}
            return None

