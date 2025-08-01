import subprocess
import re

def buscar_ips_dispositivos():
    """
    Busca os IPs dos dispositivos Android conectados via ADB e salva em um arquivo.
    """
    # Busca os dispositivos conectados
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')[1:]
    udids = [line.split('\t')[0] for line in lines if 'device' in line]
    ips = {}
    for udid in udids:
        # Executa comando para buscar IP
        cmd = f'adb -s {udid} shell ip route'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', res.stdout)
        ip = match.group(1) if match else None
        ips[udid] = ip
        print(f"Dispositivo: {udid} | IP: {ip}")
    # Salva no arquivo
    with open('ips_dispositivos.txt', 'w') as f:
        for udid, ip in ips.items():
            f.write(f"{udid}: {ip}\n")
    print("IPs salvos em ips_dispositivos.txt")

def conectar_dispositivos_por_ip(arquivo='ips_dispositivos.txt'):
    """
    Lê o arquivo de IPs e conecta cada dispositivo via adb connect.
    """
    with open(arquivo, 'r') as f:
        for linha in f:
            partes = linha.strip().split(':')
            if len(partes) == 2:
                udid, ip = partes
                if ip:
                    cmd = f'adb connect {ip}:5555'
                    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    print(f"Conectando {udid} ({ip}): {res.stdout.strip()}")

def wireless():
#if __name__ == "__main__":
    buscar_ips_dispositivos()
    conectar_dispositivos_por_ip()
