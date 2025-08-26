import serial
import serial.tools.list_ports
import time

# -------------------
# Funções de comunicação com o modem
# -------------------

def listar_portas():
    """Retorna lista de portas seriais disponíveis."""
    return [porta.device for porta in serial.tools.list_ports.comports()]

def testar_sms_porta(porta, log_callback=print):
    """Testa se uma porta suporta SMS e retorna o objeto Serial ou None."""
    try:
        ser = serial.Serial(porta, 115200, timeout=2)
        time.sleep(1)

        # Teste básico de comunicação
        ser.write(b'AT\r')
        time.sleep(0.5)
        resposta = ser.read_all().decode(errors='ignore')
        if "OK" not in resposta:
            ser.close()
            return None

        # Configura modo texto e notificações de SMS
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        ser.write(b'AT+CNMI=2,1,0,0,0\r')
        time.sleep(0.5)
        ser.write(b'AT+CMGL="ALL"\r')
        time.sleep(1)
        resposta_sms = ser.read_all().decode(errors='ignore')

        if "+CMGL:" in resposta_sms or "OK" in resposta_sms:
            log_callback(f"[OK] Porta SMS encontrada: {porta}")
            return ser
        else:
            ser.close()
            return None

    except Exception as e:
        log_callback(f"[ERRO] {porta}: {e}")
        return None

def consultar_operadora(ser):
    """Consulta a operadora do SIM conectado."""
    try:
        if ser and ser.is_open:
            ser.write(b'AT+COPS?\r')
            time.sleep(0.5)
            resposta = ser.read_all().decode(errors='ignore').upper()
            if "CLARO" in resposta:
                return "CLARO"
            elif "TIM" in resposta:
                return "TIM"
            elif "VIVO" in resposta:
                return "VIVO"
            elif "OI" in resposta:
                return "OI"
            else:
                return "DESCONHECIDA"
        else:
            return "Porta fechada ou inválida"
    except Exception as e:
        return f"ERRO: {e}"

def consultar_numero(ser):
    """Consulta o número do SIM conectado."""
    try:
        if ser and ser.is_open:
            ser.write(b'AT+CNUM\r')
            time.sleep(0.5)
            resposta = ser.read_all().decode(errors='ignore')
            return resposta.strip()
        else:
            return "Porta fechada ou inválida"
    except Exception as e:
        return f"ERRO: {e}"

def monitorar_sms(ser, log_callback=print, intervalo=0.2):
    """Monitora SMS em tempo real, chamando log_callback para cada mensagem recebida."""
    try:
        while True:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode(errors='ignore').strip()
                if data:
                    log_callback("Nova mensagem recebida:\n" + data + "\n")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        log_callback("\n🛑 Monitoramento encerrado.")
    finally:
        if ser.is_open:
            ser.close()
