import re
import subprocess
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from until.retries import *
from until.waits import *


class WaBussinesPage:

    def __init__(self, driver):
        self.driver = driver

    # Nota: Este mét0do utiliza o decorador @retry para tentar novamente até 3 vezes em caso de falha, com 1 segundos de espera entre as tentativas.
    @retry(max_tentativas=3, delay=1)
    def pegar_numero_chip2(self, udid):
        """
        Tenta obter o número do chip via discador Samsung.
        Retorna o número ou lança exceção em caso de erro.
        """

        try:
            subprocess.run(f'adb -s {udid} shell am start -a android.intent.action.CALL -d tel:*846%23', shell=True)
            try:
                escolherChip = esperar_elemento_visivel(self.driver, (By.ID, "com.samsung.android.incallui:id/title"), 10)
                if escolherChip:
                    chip2 = esperar_elemento_visivel(self.driver, (By.XPATH,
                                                                   '//android.widget.TextView[@resource-id="com.samsung.android.incallui:id/account_label" and @text="SIM 2"]'))
                    chip2.click()
            except:
                pass

            mensagem_elem = esperar_elemento_visivel(self.driver, (By.ID, "android:id/message"), 10)
            mensagem_texto = mensagem_elem.text if mensagem_elem else ""
            if verificar_elemento_visivel(self.driver,
                                          (By.XPATH, "//android.widget.TextView[contains(@text, 'Recarga Facil')]"),
                                          20):
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

    def aceitar_termos(self):
        try:
            termos = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/eula_accept'))
            termos.click()
        except Exception as e:
            print("[aceitar_termos] Erro: Não aceitou os termos")
            return False

    def registrar_numero(self, numero):
        try:
            registrar_phone = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp.w4b:id/registration_phone"))
            registrar_phone.send_keys(numero)
            ddd = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp.w4b:id/registration_phone"))
            if ddd.text == "":
                ddd.send_keys("55")
            submit = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/registration_submit'))
            submit.click()
        except Exception as e:
            print("[registrar_numero] Erro: Não registrou o número")
            return False

    def verificar_banido(self):
        try:
            banido = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp.w4b:id/action_button"))
            if banido.text == "REGISTRAR NOVO NÚMERO DE TELEFONE":
                print("❌ Numero Banido ❌")
                return True
        except:
            pass

    def verificar_analise(self):
        try:
            analise = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/action_button'))
            print(analise.text)
            if analise.text == 'VERIFICAR STATUS DA ANÁLISE':
                print('⛔ Em Analise ⛔')
                return True
        except:
            pass

    def colocar_em_analise(self):
        try:
            pedirAnalise = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/action_button'))
            if pedirAnalise.text == "PEDIR ANÁLISE":
                pedirAnalise.click()
                enviar = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/submit_button'))
                enviar.click()
                analise = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/appeal_submitted_heading'))
                print(analise.text)
                return True
        except:
            pass

    def confirmar_chip(self):
        try:
            confirmar = esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1'))
            confirmar.click()
        except Exception as e:
            print("[confirmar_chip] Erro: Não confirmou o chip")
            return False

    def abrir_app_mensagens(self):
        try:
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp.w4b:id/verify_sms_code_input"))
            time.sleep(1)
            self.driver.activate_app('com.samsung.android.messaging')
            print('abriu o app')
            return True
        except Exception as e:
            print(f"[abrir_app_mensagens] Erro: Não abriu o app de mensagem")
            return False

    def pegarCodigoSms(self):
        try:
            appMensagem = esperar_elemento_visivel(self.driver, (By.XPATH,
                                                                 '//android.widget.TextView[@content-desc="2 9 7 4 4 "]'))
            appMensagem.click()
            mensagens = esperar_elemento_visivel(self.driver,
                                                 (By.XPATH,
                                                  "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]"))
            mensagem = self.driver.find_elements(By.XPATH,
                                                 "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]")
            if mensagem:
                ultima_mensagem = mensagem[-1]
                codigoCompleto = ultima_mensagem.get_attribute('content-desc')
                padrao = r'(\d+)-(\d+)'
                resultado = re.search(padrao, codigoCompleto)
                codigo = resultado.group(1) + resultado.group(2)
                self.driver.terminate_app("com.samsung.android.messaging")
                print('pegou o codigo')
                return codigo
            print('[pegarCodigoSms] Nenhuma mensagem encontrada.')
            return None
        except Exception as e:
            print(f"[pegarCodigoSms] Erro: {e}")
            return None

    def voltarWhatsapp(self):
        try:
            self.driver.activate_app("com.whatsapp.w4b")
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp.w4b:id/action_button"))
            campo.click()
            print('voltou')
            return True
        except Exception as e:
            print(f"[voltarWhatsapp] Erro: Não voltou para o whatsapp")
            pass

    def colocar_codigo(self, codigo):
        try:
            print(codigo)
            input_codigo = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp.w4b:id/verify_sms_code_input'))
            input_codigo.send_keys(codigo)
        except Exception as e:
            print("[colocar_codigo] Erro: Não inseriu o código")
            return False

    def negar_backup(self):
        try:
            negar = esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button2'), 20)
            negar.click()
        except Exception as e:
            print("[negar_backup] Erro: Não clicou em negar backup")
            return False

    def colocar_nome(self):
        try:
            nome = esperar_elemento_visivel(self.driver, (By.XPATH, '//android.widget.EditText'))
            nome.send_keys("Call Center")
            continuar = esperar_elemento_visivel(self.driver, (By.XPATH, '//android.widget.Button'))
            continuar.click()
        except Exception as e:
            print(f"[colocar_nome] Erro: Não colocou o nome")
            return False

    def selecionar_empresa(self):
        try:
            categoria = esperar_elemento_visivel(self.driver, (By.ID, '//android.widget.TextView[@text="Outras empresas"]'))
            categoria.click()
            avancar = esperar_elemento_visivel(self.driver, (By.ID, '//android.widget.TextView[@text="Avançar"]'))
            avancar.click()
        except Exception as e:
            print(f"[selecionar_empresa] Erro: Não selecionou a empresa")
            return False

    def horario_de_atendimento(self):
        try:
            horario = esperar_elemento_visivel(self.driver, (By.ID, '//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View[1]/android.view.View[2]/android.widget.RadioButton'))
            horario.click()
            avancar = esperar_elemento_visivel(self.driver, (By.ID, '//android.widget.TextView[@text="Avançar"]'))
            avancar.click()
            time.sleep(1)
            avancar.click()
            time.sleep(1)
        except Exception as e:
            print("[horario_de_atendimento] Erro: Não concluiu o horário")
            return False

    def foto_perfil(self):
        try:
            avancar = esperar_elemento_visivel(self.driver, (By.ID, '//android.widget.TextView[@text="Avançar"]'))
            avancar.click()
        except Exception as e:
            print("[foto_perfil] Erro: Não avançou na foto de perfil")
            return False

    def formas_encontrar_empresa(self):
        try:
            pular = esperar_elemento_visivel(self.driver, (By.ID, '//android.widget.TextView[@text="Pular"]'))
            pular.click()
            time.sleep(1)
            pular.click()
        except Exception as e:
            print('[formas_encontrar_empresa] Erro: Não concluiu o pulo')
            return False
