from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from until.waits import *
from until.retries import *
import re
import subprocess

from until.waits import esperar_elemento_visivel


class WhatsAppPage:

    def __init__(self, driver):
        self.driver = driver


    def pegarNumero(self, udid):
        try:
            self.driver.press_keycode(3)
            # esperar_elemento_visivel(self.driver, (By.XPATH, '//android.widget.TextView[@content-desc="Telefone"]'))
            self.driver.activate_app('com.samsung.android.dialer')
            esperar_elemento_visivel(self.driver, (By.ID, "com.samsung.android.dialer:id/dialpad_spacer_view")).click()

            subprocess.run(f'adb -s {udid} shell am start -a android.intent.action.CALL -d tel:*846%23', shell=True)
            if verificar_elemento_visivel(self.driver,(By.XPATH, "//android.widget.TextView[contains(@text, 'Recarga Facil')]"), 20):
                campoNumero = esperar_elemento_visivel(self.driver, (By.ID, "android:id/message"))
                numeros = campoNumero.text
                print(numeros)
                numeros = re.findall(r"\[(\d+)]", campoNumero.text)
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                numero = int(numeros[0])
                print(numero)
                self.driver.terminate_app("com.samsung.android.dialer")
                return numero
            elif esperar_elemento_visivel(self.driver, (By.ID, "android:id/message")).text == 'Problema de conexão ou código MMI inválido.':
                    print('Numero Cancelado')
                    esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                    raise 'numero cancelado'
            elif esperar_elemento_visivel(self.driver, (By.ID, "android:id/message")).text == 'UNKNOWN APPLICATION':
                print('Chip da tim nao identificado')
                esperar_elemento_visivel(self.driver, (By.ID, 'android:id/button1')).click()
                raise 'numero cancelado'




        except Exception as e:

            print(f"Erro ao pegar numero: {e}")



    def abrirWhatsapp(self):
        time.sleep(2)
        self.driver.activate_app('com.whatsapp')

    def selecionar_linguagem(self):
        try:
            esperar_elemento_visivel(self.driver, (By.XPATH,
                                                   '//android.widget.CheckBox[@content-desc="Selecionar (idioma do dispositivo) como idioma do app"]')).click()
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao colocou a linguagem')
            pass

    def clicar_prosseguir(self):
        esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/eula_accept')).click()

    def inserir_numero(self, numero):

        campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/registration_phone"))
        campo.send_keys(numero)

        dd = self.driver.find_element(By.ID, 'com.whatsapp:id/registration_cc')
        if dd == " ":
            dd.send_keys('55')

        botao = self.driver.find_element(By.ID, "com.whatsapp:id/registration_submit")
        botao.click()

        print('colocou o numero')

    def confirmarNumero(self):

        try:
            confirmar = esperar_elemento_visivel(self.driver, (By.ID, "android:id/button1"))
            confirmar.click()
            time.sleep(0.5)


        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('Nao confirmou o numero')
            pass

    def verificarBanido(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == 'REGISTRAR NOVO NÚMERO DE TELEFONE':
                print('Número banido')
                raise ChipBanidoException("Número banido pelo WhatsApp")
        except TimeoutException:
            print("Não apareceu botão de banimento – ignorando.")

    def pedirAnalise(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == "PEDIR ANÁLISE":
                elemento.click()
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/submit_button')).click()
                time.sleep(0.5)
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/submit_button')).click()
                raise ChipEmAnaliseException("Chip em processo de análise")
        except TimeoutException:
            print("Não apareceu botão 'PEDIR ANÁLISE' – ignorando.")

    def verificarAnalise(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == 'VERIFICAR STATUS DA ANÁLISE':
                elemento.click()
                analise = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/appeal_submitted_heading'))
                print(analise.text)
                raise ChipEmAnaliseException("Chip já em análise")
        except TimeoutException:
            print("Não apareceu botão de status de análise – ignorando.")

    def verificarChip(self):
        try:
            tipoderecebimento = verificar_elemento_visivel(self.driver,
                                                         (By.ID, 'com.whatsapp:id/entire_content_holder'))
            if tipoderecebimento:
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/secondary_button')).click()
                try:
                    esperar_elemento_visivel(self.driver, (By.XPATH,
                                                           '(//android.widget.RadioButton[@resource-id="com.whatsapp:id/reg_method_checkbox"])[2]')).click()
                    esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/continue_button')).click()
                except Exception as e:
                    print(f"Erro ao selecionar linguagem: {e}")
                    print('nao foi possivel pedir sms')
                    pass

                try:
                    esperar_elemento_visivel(self.driver, (By.ID,
                                                           'com.android.permissioncontroller:id/permission_allow_button')).click()
                    esperar_elemento_visivel(self.driver, (By.ID,
                                                           'com.android.permissioncontroller:id/permission_allow_button')).click()
                except Exception as e:
                    print(f"Erro ao verificar chip: {e}")
                    print('nao aceitou as condicoes')
                    pass



        except Exception as e:

            print('Nao verificou o chip')
            pass


    def abrirAppMensagens(self):
        try:
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input"))
            self.driver.activate_app('com.samsung.android.messaging')
            print('abriu o app')
            return True
        except:
            print('nao abriu o app de mensagem')
            pass


    def pegarCodigoSms(self):
        try:
            # Localiza o elemento que contém a mensagem com o código de verificação
            esperar_elemento_visivel(self.driver, (By.XPATH,
                                                   '(//android.widget.LinearLayout[@resource-id="com.samsung.android.messaging:id/card_view_sub_layout"])[1]')).click()

            # Busca pela mensagem que contém o código de verificação
            esperar_elemento_visivel(self.driver,
                                     (By.XPATH, "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]"))
            mensagens = self.driver.find_elements(By.XPATH,
                                                  "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]")
            # Se houver mensagens que correspondem ao critério
            if mensagens:
                # Pegue a última mensagem que contém "Código do WhatsApp"
                ultima_mensagem = mensagens[-1]

                # Extraímos o texto ou o content-desc dessa última mensagem
                codigoCompleto = ultima_mensagem.get_attribute('content-desc')

                padrao = r'(\d+)-(\d+)'

                resultado = re.search(padrao, codigoCompleto)

                codigo = resultado.group(1) + resultado.group(2)

                self.driver.terminate_app("com.samsung.android.messaging")

            print('pegou o codigo')
            return codigo
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao precisou pegar o codigo')
            pass


    def voltarWhatsapp(self):
        try:
            self.driver.activate_app("com.whatsapp")
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input")).click()
            print('voltou')
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao precisou voltar')
            pass


    def inserir_codigo_sms(self, codigo):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input")).send_keys(codigo)
            print('colocou o codigo')
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao colocou o codigo')
            pass


    def concluir_perfil(self):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/submit")).click()
            print('clicou em aceitou')


        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao clicou ')
            pass

        try:
            permissao = verificar_elemento_visivel(self.driver, (By.ID,
                                                                 'com.android.permissioncontroller:id/permission_allow_button'))

            if permissao:
                esperar_elemento_visivel(self.driver,
                                         (By.ID, "com.android.permissioncontroller:id/permission_allow_button")).click()
                time.sleep(1)
                esperar_elemento_visivel(self.driver,
                                         (By.ID, "com.android.permissioncontroller:id/permission_allow_button")).click()
                time.sleep(1)
                esperar_elemento_visivel(self.driver,
                                         (By.ID, "com.android.permissioncontroller:id/permission_allow_button")).click()
            print('aceitou as permissoes')


        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao aceitou as notificações')
            pass


    def aceitarPermissao(self):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "android:id/button2")).click()
            print('negou o backup')
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('nao negou o backup')
            pass


    def colocarNome(self):
        try:
            campo_nome = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/registration_name"))
            campo_nome.send_keys("Call Center")
            print("colocou o nome")
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('colocou o nome')
            pass


    def finalizarPerfil(self):
        try:
            self.driver.find_element(By.ID, "com.whatsapp:id/register_name_accept").click()
            print('concluiu')
            if verificar_elemento_visivel(self.driver,(By.ID, 'com.whatsapp:id/secondary_button')):
                verificar_elemento_visivel(self.driver,(By.ID, 'com.whatsapp:id/secondary_button')).click()
            time.sleep(10)
        except Exception as e:
            print(f"Erro ao selecionar linguagem: {e}")
            print('parou no nome')
            pass
