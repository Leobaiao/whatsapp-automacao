import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # ✅ correto
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import TimeoutException


# ...existing code...
def clicar_elemento(self, by, value, timeout=10):
    try:
        esperar_elemento_visivel(self.driver, (by, value), timeout).click()
        return True
    except Exception as e:
        print(f"Erro ao clicar elemento {value}: {e}")
        return False

def texto_elemento(self, by, value, timeout=10):
    try:
        elem = esperar_elemento_visivel(self.driver, (by, value), timeout)
        return elem.text if elem else ""
    except Exception as e:
        print(f"Erro ao obter texto do elemento {value}: {e}")
        return ""
# ...existing code...

def esperar_elemento_visivel(driver: object, locator: object, timeout: object = 10):
    try:
        return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    except WebDriverException as e:
        print(f"🛑 Erro de comunicação com Appium: {e}")
        raise  # propaga para o executor capturar
def verificar_elemento_visivel(driver: object, locator: object, timeout: object = 10) ->  Any:
    try:
        esperar_elemento_visivel(driver, locator, timeout)
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    except TimeoutException:
        print(f"Elemento {locator} não apareceu após {timeout} segundos.")
        return None
        pass

def executar_paralelo_arg(*funcoes):
    threads = []
    for func, *args in funcoes:
        thread = threading.Thread(target=func, args=tuple(args))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

def executar_paralelo_normal(*funcoes):
    with ThreadPoolExecutor(max_workers=len(funcoes)) as executor:
        # Envia cada função (sem argumentos) para execução
        futures = [executor.submit(func) for func in funcoes]

        for future in as_completed(futures):
            exc = future.exception()
            if exc:
                raise exc  # Propaga a exceção original corretamente


def executar_paralelo(*funcoes):
    """
    Executa funções em paralelo e interrompe se alguma retornar True.
    """
    with ThreadPoolExecutor() as executor:
        futuros = {executor.submit(func): func for func in funcoes}
        for future in as_completed(futuros):
            try:
                resultado = future.result()
                if resultado is True:
                    # Cancela os outros
                    for f in futuros:
                        if not f.done():
                            f.cancel()
                    print("⚠️ Uma das funções retornou True. Interrompendo automação.")
                    return True
            except Exception as e:
                print(f"❌ Erro ao executar função paralela: {e}")
    return False


class WebDriverException(Exception):
    pass


class ChipBanidoException(Exception):
    pass


class ChipEmAnaliseException(Exception):
    pass
