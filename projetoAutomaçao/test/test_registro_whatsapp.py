import unittest
from until.waits import *
from drivers.drivers_factory import *
from pages.whatsapp_page import *
from drivers.mult_drivers import *

class TestWhatsAppRegistro(unittest.TestCase):


    def test_registrar_novo_numero(self):
        try:
            appium_server()
            udid = pegar_udid()
            driver = criar_driver(4723, udid[0])

            whatsapp = WhatsAppPage(driver)

            numero = whatsapp.pegarNumero(udid[0])
            whatsapp.abrirWhatsapp()
            whatsapp.selecionar_linguagem()
            whatsapp.clicar_prosseguir()
            whatsapp.inserir_numero(numero)
            whatsapp.confirmarNumero()
            executar_paralelo(
                whatsapp.verificarBanido,
                whatsapp.verificarAnalise,
                whatsapp.pedirAnalise,
                whatsapp.verificarChip
            )
            if whatsapp.abrirAppMensagens():
                codigo = whatsapp.pegarCodigoSms()
                whatsapp.voltarWhatsapp()
                whatsapp.inserir_codigo_sms(codigo)
                whatsapp.concluir_perfil()
            whatsapp.aceitarPermissao()
            whatsapp.colocarNome()
            whatsapp.finalizarPerfil()




        except ChipBanidoException as e:
            print(f"⚠️ Teste encerrado: {e}")
            self.skipTest("Número banido – teste ignorado.")

        except ChipEmAnaliseException as e:
            print(f"⚠️ Teste encerrado: {e}")
            self.skipTest("Número em análise – teste ignorado.")

        except Exception as e:

            self.fail(f"❌ Erro inesperado: {e}")

    def test_registrar_mult(self):
        try:
            #appium_server()
            udid = pegar_udids()
            porta_livre()
            #iniciar_appium()

            driver = criar_driver(4723, udid[0])

            whatsapp = WhatsAppPage(driver)

            numero = whatsapp.pegarNumero(udid[0])
            whatsapp.abrirWhatsapp()
            whatsapp.selecionar_linguagem()
            whatsapp.clicar_prosseguir()
            whatsapp.inserir_numero(numero)
            whatsapp.confirmarNumero()
            executar_paralelo(
                whatsapp.verificarBanido,
                whatsapp.verificarAnalise,
                whatsapp.pedirAnalise,
                whatsapp.verificarChip
            )
            if whatsapp.abrirAppMensagens():
                codigo = whatsapp.pegarCodigoSms()
                whatsapp.voltarWhatsapp()
                whatsapp.inserir_codigo_sms(codigo)
                whatsapp.concluir_perfil()
            whatsapp.aceitarPermissao()
            whatsapp.colocarNome()
            whatsapp.finalizarPerfil()




        except ChipBanidoException as e:
            print(f"⚠️ Teste encerrado: {e}")
            self.skipTest("Número banido – teste ignorado.")

        except ChipEmAnaliseException as e:
            print(f"⚠️ Teste encerrado: {e}")
            self.skipTest("Número em análise – teste ignorado.")

        except Exception as e:

            self.fail(f"❌ Erro inesperado: {e}")

if __name__ == '__main__':
    unittest.main()

