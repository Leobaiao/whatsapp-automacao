from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from until.waits import *
from until.retries import *
import re
import subprocess

class WhatsAppPage:
    
    def __init__(self, driver):
        self.driver = driver

    @retry(max_tentativas=3, delay=1)
    def pegarNumeroChip1(self, udid):
        """
        Tenta obter o número do chip via discador Samsung.
        Retorna o número ou lança exceção em caso de erro.

        Nota: Este método utiliza o decorador @retry para tentar novamente até 3 vezes em caso de falha, com 1 segundos de espera entre as tentativas.
        """

        try:
            subprocess.run(f'adb -s {udid} shell am start -a android.intent.action.CALL -d tel:*846%23', shell=True)
            try:
                escolherChip = esperar_elemento_visivel(self.driver, (By.ID, "com.samsung.android.incallui:id/title"), 10)
                if escolherChip:
                    chip1 = esperar_elemento_visivel(self.driver, (By.XPATH, '//android.widget.TextView[@resource-id="com.samsung.android.incallui:id/account_label" and @text="SIM 1"]'), 10)
                    chip1.click()
            except:
                pass
            mensagem_elem = esperar_elemento_visivel(self.driver, (By.ID, "android:id/message"), 10)
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

    def abrirWhatsapp(self):
        try:
            time.sleep(2)
            self.driver.activate_app('com.whatsapp')
            return True
        except Exception as e:
            print(f"[abrirWhatsapp] Erro: {e}")
            return False

    def selecionar_linguagem(self):
        try:
            esperar_elemento_visivel(self.driver, (By.XPATH,
                '//android.widget.CheckBox[@content-desc="Selecionar (idioma do dispositivo) como idioma do app"]')).click()
            return True
        except Exception as e:
            print(f"[selecionar_linguagem] Erro: {e}")
            return False

    def clicar_prosseguir(self):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/eula_accept')).click()
            return True
        except Exception as e:
            print(f"[clicar_prosseguir] Erro: {e}")
            return False

    def inserir_numero(self, numero):
        try:
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/registration_phone"))
            campo.send_keys(numero)
            dd = self.driver.find_element(By.ID, 'com.whatsapp:id/registration_cc')
            if dd.text == " ":
                dd.send_keys('55')
            botao = self.driver.find_element(By.ID, "com.whatsapp:id/registration_submit")
            botao.click()
            print('colocou o numero')
            return True
        except Exception as e:
            print(f"[inserir_numero] Erro: {e}")
            return False

    def confirmarNumero(self):
        try:
            confirmar = esperar_elemento_visivel(self.driver, (By.ID, "android:id/button1"))
            confirmar.click()
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[confirmarNumero] Erro: Não Precisou Confirmar o Numero")
            return False

    def verificarBanido(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == 'REGISTRAR NOVO NÚMERO DE TELEFONE':

                raise ChipBanidoException("❌ Número banido pelo WhatsApp")
            return True
        except TimeoutException:
            print("[verificarBanido] Não apareceu botão de banimento – ignorando.")
            return False
        except Exception as e:
            print(f"[verificarBanido] Erro: {e}")
            return False

    def pedirAnalise(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == "PEDIR ANÁLISE":
                elemento.click()
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/submit_button')).click()
                time.sleep(0.5)
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/submit_button')).click()

                raise ChipEmAnaliseException("❌ Chip em processo de análise")
            return True
        except TimeoutException:
            print("[pedirAnalise] Não apareceu botão 'PEDIR ANÁLISE' – ignorando.")
            return False
        except Exception as e:
            print(f"[pedirAnalise] Erro: {e}")
            return False

    def verificarAnalise(self):
        try:
            elemento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/action_button'))
            if elemento and elemento.text == 'VERIFICAR STATUS DA ANÁLISE':
                elemento.click()
                analise = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/appeal_submitted_heading'))
                print(analise.text)

                raise ChipEmAnaliseException("❌ Chip já em análise")
            return True
        except TimeoutException:
            print("[verificarAnalise] Não apareceu botão de status de análise – ignorando.")
            return False
        except Exception as e:
            print(f"[verificarAnalise] Erro: {e}")
            return False

    def verificarChip(self):
        try:

            tipoderecebimento = esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/entire_content_holder'))

            if tipoderecebimento:
                esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/secondary_button')).click()
                try:
                    esperar_elemento_visivel(self.driver, (By.XPATH,
                        '(//android.widget.RadioButton[@resource-id="com.whatsapp:id/reg_method_checkbox"])[2]')).click()
                    esperar_elemento_visivel(self.driver, (By.ID, 'com.whatsapp:id/continue_button')).click()
                except Exception as e:
                    print(f"[verificarChip] Erro ao pedir SMS: {e}")
                try:
                    esperar_elemento_visivel(self.driver, (By.ID,
                        'com.android.permissioncontroller:id/permission_allow_button')).click()
                    esperar_elemento_visivel(self.driver, (By.ID,
                        'com.android.permissioncontroller:id/permission_allow_button')).click()
                except Exception as e:

                    print(f"[verificarChip] Erro ao aceitar condições: Não verificou o Chip")

        except Exception as e:
            print(f"[verificarChip] Erro: Não verificou o Chip")

            return False

    def abrirAppMensagens(self):
        try:
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input"))
            self.driver.activate_app('com.samsung.android.messaging')
            print('abriu o app')
            return True
        except Exception as e:
            print(f"[abrirAppMensagens] Erro: Não Abriu o App De Mensagem ")
            return False

    def pegarCodigoSms(self):
        try:
            esperar_elemento_visivel(self.driver, (By.XPATH,
                '(//android.widget.LinearLayout[@resource-id="com.samsung.android.messaging:id/card_view_sub_layout"])[1]')).click()
            esperar_elemento_visivel(self.driver,
                (By.XPATH, "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]"))
            mensagens = self.driver.find_elements(By.XPATH,
                "//android.widget.LinearLayout[contains(@content-desc, 'WhatsApp')]")
            if mensagens:
                ultima_mensagem = mensagens[-1]
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
            self.driver.activate_app("com.whatsapp")
            campo = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input")).click()
            print('voltou')
            return True
        except Exception as e:
            print(f"[voltarWhatsapp] Erro: {e}")
            return False

    def inserir_codigo_sms(self, codigo):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/verify_sms_code_input")).send_keys(codigo)
            print('colocou o codigo')
            return True
        except Exception as e:
            print(f"[inserir_codigo_sms] Erro: {e}")
            return False

    def concluir_perfil(self):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/submit")).click()
            print('clicou em aceitou')
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
                print(f"[concluir_perfil] Erro ao aceitar notificações: {e}")
            return True
        except Exception as e:

            print(f"[concluir_perfil] Erro: Erro ao Concluir perfil")

            return False

    def aceitarPermissao(self):
        try:
            esperar_elemento_visivel(self.driver, (By.ID, "android:id/button2")).click()
            print('negou o backup')
            return True
        except Exception as e:
            print(f"[aceitarPermissao] Erro: Não Aceitou as Permissoes")
            return False

    def colocarNome(self):
        try:
            campo_nome = esperar_elemento_visivel(self.driver, (By.ID, "com.whatsapp:id/registration_name"))
            campo_nome.send_keys("Call Center")
            print("colocou o nome")
            return True
        except:
            print(f"[colocarNome] Erro: Não Colocou o Nome")
            return False

    def finalizarPerfil(self):
        try:
            self.driver.find_element(By.ID, "com.whatsapp:id/register_name_accept").click()
            print('concluiu')
            if esperar_elemento_visivel(self.driver,(By.ID, 'com.whatsapp:id/secondary_button')):
                verificar_elemento_visivel(self.driver,(By.ID, 'com.whatsapp:id/secondary_button')).click()
            time.sleep(10)
            return True
        except Exception as e:
            print(f"[finalizarPerfil] Erro: Não Finalizou o Perfil")
            return False
