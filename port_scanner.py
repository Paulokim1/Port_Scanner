import argparse
import socket
from tqdm import tqdm
import pyfiglet
from rich.console import Console
from rich.table import Table

console = Console()

# Definindo as portas conhecidas e seus respectivos serviços
WELL_KNOWN_PORTS = {
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    587: "SMTP (TLS)",
    993: "IMAP (TLS)",
    995: "POP3 (TLS)"
}


def scan_port(ip, port):
    """
    Verifica se uma determinada porta está aberta em um endereço IP
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
    except:
        return False


def scan_ports(ip, start_port, end_port):
    """
    Escaneia um intervalo de portas em um endereço IP
    """
    open_ports = []
    port_range = range(start_port, end_port + 1)
    for port in tqdm(port_range, desc="Scanning Ports", unit="ports"):
        if scan_port(ip, port):
            open_ports.append(port)
    return open_ports


def get_service(port):
    """
    Retorna o nome do serviço associado a uma determinada porta
    """
    if port in WELL_KNOWN_PORTS:
        return WELL_KNOWN_PORTS[port]
    else:
        return "Desconhecido"


def main():
    # Definindo argumentos de linha de comando
    parser = argparse.ArgumentParser(description='Port scanner tool')
    parser.add_argument('ip', metavar='target-ip', type=str, help='Target host IP address')
    parser.add_argument('--port-start', dest='port_start', type=int, default=1, help='Starting port number')
    parser.add_argument('--port-end', dest='port_end', type=int, default=65535, help='Ending port number')
    args = parser.parse_args()

    # Imprimindo o banner do programa
    console.print(pyfiglet.figlet_format("Port Scanner", font="slant"))

    # Escaneando as portas do endereço IP especificado
    open_ports = scan_ports(args.ip, args.port_start, args.port_end)

    # Imprimindo os resultados
    console.print(f"[bold green]Portas abertas em {args.ip}:[/bold green]")
    if len(open_ports) == 0:
        console.print("[bold yellow]Nenhuma porta aberta foi encontrada[/bold yellow]")
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Porta", style="cyan")
        table.add_column("Serviço", style="green")
        for port in open_ports:
            table.add_row(str(port), get_service(port))
        console.print(table)


if __name__ == "__main__":
    main()