from servicos.simulador import SimuladorIncendios
from utils.leitor_entrada import LeitorEntrada

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PATH
sys.path.append(str(Path(__file__).parent.parent))


def testar_simulacao(arquivo_teste: str):
    print(f"\n🔍 Testando com arquivo: {arquivo_teste}")
    
    dados = LeitorEntrada.ler_arquivo(arquivo_teste)
    if not dados:
        print("❌ Falha ao carregar arquivo")
        return
    
    simulador = SimuladorIncendios(max_dias=100)
    simulador.carregar_dados(*dados)
    resultados = simulador.simular()
    
    print("\n📊 Resultados:")
    print(f"- Sucesso: {'✅' if resultados['sucesso'] else '❌'}")
    print(f"- Dias totais: {resultados['dias_totais']}")
    print("- Focos extintos:")
    for foco, dia in resultados['dias_extincao'].items():
        print(f"  {foco}: Dia {dia}")


if __name__ == "__main__":
    testar_simulacao(os.path.join(os.path.dirname(__file__), "test_case2.txt"))