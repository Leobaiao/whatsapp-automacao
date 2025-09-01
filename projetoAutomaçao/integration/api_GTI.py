import os
import base64
from io import BytesIO
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import pyodbc
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://api.gtiapi.workers.dev"


class AgenteGTI:
    def __init__(self, token, nome=None, timeout=10, debug=False):
        self.token = token
        self.nome = nome or "Agente GTI"
        self.numero = None
        self.conectado = False
        self.qrcode = ""
        self.status_data = {}
        self.timeout = timeout
        self.debug = debug

        # Sessão persistente para reduzir latência
        self.session = requests.Session()
        self.session.headers.update({
            "token": self.token,
            "Content-Type": "application/json"
        })

        self.atualizar_status()

    def atualizar_status(self):
        """Atualiza status da instância usando sessão persistente"""
        try:
            resp = self.session.get(f"{BASE_URL}/instance/status", timeout=self.timeout)
            data = resp.json()
            self.numero = data.get("instance", {}).get("owner")
            self.conectado = data.get("status", {}).get("connected", False)
            self.qrcode = data.get("instance", {}).get("qrcode", "")
            self.status_data = data
        except Exception as e:
            print(f"[{self.nome}] Erro ao atualizar status: {e}")
            self.conectado = False

    def enviar_mensagem(self, numero, mensagem, mentions=""):
        """Envia mensagem via API GTI"""
        if not mensagem:
            print(f"[{self.nome}] Mensagem vazia. Abortando envio.")
            return None

        payload = {
            "number": str(numero),
            "text": str(mensagem),
            "linkPreview": False,
            "replyid": "",
            "mentions": str(mentions),
            "readchat": True,
            "delay": 0
        }

        try:
            resp = self.session.post(f"{BASE_URL}/send/text", json=payload, timeout=self.timeout)
            resp.raise_for_status()
            print(f"[{self.nome}] Mensagem enviada para {numero}")
            return resp.json()
        except requests.RequestException as e:
            print(f"[{self.nome}] Erro ao enviar mensagem: {e}")
            return None

    def exibir_qr(self):
        """Exibe QR code como imagem"""
        if not self.qrcode:
            print(f"[{self.nome}] Nenhum QR code disponível")
            return
        try:
            img_bytes = base64.b64decode(self.qrcode)
            img = Image.open(BytesIO(img_bytes))
            img.show()
        except Exception as e:
            print(f"[{self.nome}] Erro ao abrir QR code: {e}")

    def gerar_qr_terminal(self, qr_string=None):
        """Exibe QR code no terminal"""
        qr_string = qr_string or self.qrcode
        if not qr_string:
            return
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(qr_string)
        qr.make(fit=True)
        for linha in qr.get_matrix():
            print("".join(["██" if celula else "  " for celula in linha]))

    def gerar_qr(self, modo="img"):
        """Solicita geração de QR code"""
        try:
            resp = self.session.post(f"{BASE_URL}/instance/connect", timeout=self.timeout)

            if resp.status_code == 409:
                print(f"[{self.nome}] Já conectado, atualizando status.")
                self.atualizar_status()
            else:
                resp.raise_for_status()
                data = resp.json()
                qr_base64 = data.get("instance", {}).get("qrcode", "")
                if qr_base64.startswith("data:image/png;base64,"):
                    qr_base64 = qr_base64.split(",")[1]
                self.qrcode = qr_base64

            if self.qrcode:
                print(f"\n[{self.nome}] QR Code disponível")
                if modo == "terminal":
                    self.gerar_qr_terminal(self.qrcode)
                else:
                    self.exibir_qr()
        except requests.RequestException as e:
            print(f"[{self.nome}] Erro ao gerar QR code: {e}")

    def dados(self):
        """Mostra dados básicos"""
        print(f"{self.nome} | Número: {self.numero} | Conectado: {self.conectado}")


# ======================
# Funções auxiliares
# ======================

def carregar_agentes_do_banco(conn_str):
    """
    Carrega agentes direto do banco e retorna lista de AgenteGTI
    """
    query = """
        SELECT TELEFONE, SENHA
        FROM [NEWWORK].[dbo].[ROTA]
        WHERE SERVICO = 'MATURACAO' AND TELEFONE LIKE 'GTI%'
    """
    agentes = []
    try:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                for nome_instancia, token in cursor.fetchall():
                    agentes.append(AgenteGTI(token=token, nome=nome_instancia))
        return agentes
    except Exception as e:
        print(f"❌ Erro ao carregar agentes: {e}")
        return []


def atualizar_status_parallel(agentes, max_workers=10):
    """Atualiza status em paralelo"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_agente = {executor.submit(ag.atualizar_status): ag for ag in agentes}
        for future in as_completed(future_to_agente):
            ag = future_to_agente[future]
            try:
                future.result()
            except Exception as e:
                print(f"[{ag.nome}] Erro inesperado ao atualizar: {e}")


def enviar_mensagens_parallel(agentes, numero, mensagem, max_workers=10):
    """Envia mensagens em paralelo para todos os agentes"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_agente = {executor.submit(ag.enviar_mensagem, numero, mensagem): ag for ag in agentes}
        for future in as_completed(future_to_agente):
            ag = future_to_agente[future]
            try:
                future.result()
            except Exception as e:
                print(f"[{ag.nome}] Erro inesperado no envio: {e}")


# ======================
# Execução
# ======================

# Conexão com o banco via .env
server = os.getenv('SERVER')
database = os.getenv('DATABASE')
username = os.getenv('USERNAMEDB')
password = os.getenv('PASSWORD')
DB = (f"DRIVER={{ODBC Driver 18 for SQL Server}};"
      f"SERVER={server};"
      f"DATABASE={database};"
      f"UID={username};"
      f"PWD={password};"
      f"TrustServerCertificate=yes;")

# Carrega agentes direto do banco
agentes_gti = carregar_agentes_do_banco(DB)

# Atualiza status de todos em paralelo
atualizar_status_parallel(agentes_gti, max_workers=25)

# Mostra status de cada agente
for ag in agentes_gti:
    ag.dados()

# Exemplo de envio paralelo de mensagens (opcional)
enviar_mensagens_parallel(agentes_gti, "5511954510423", "Mensagem teste 🚀", max_workers=15)
