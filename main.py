import sys
from servicos.simulador import SimuladorIncendios
from utils.leitor_entrada import LeitorEntrada
from utils.relatorio import GeradorRelatorio
from servicos.visualizacao import visualizar_grafo

from pathlib import Path

'''
ANTONIO AUGUSTO NUNES DE SOUZA 15440698
ASHTON APEBIO MERGULHÃO SEGNIBO 15441765
CESAR MÂNCIO SILVA 15635890 
MARIA RITA SOUSA BORGES 15656239
'''
def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        sys.exit(1)
    
    # Carrega dados
    dados = LeitorEntrada.ler_arquivo(sys.argv[1])
    if not dados:
        sys.exit(1)
        
    num_focos, num_postos, capacidades, areas_iniciais, fatores, matriz = dados
    
    nome_base = Path('test_case1').stem

    # Visualização
    visualizar_grafo(num_focos, num_postos, matriz)
    
    # Simulação
    simulador = SimuladorIncendios(max_dias=100)
    simulador.carregar_dados(*dados)
    resultados = simulador.simular()
    
    # Relatório
    relatorio = GeradorRelatorio.gerar_relatorio(
        resultados,
        simulador.mapa_focos,
        simulador.mapa_postos,
        simulador.historico_alocacoes,
    )

    print("\n"+relatorio)


if __name__ == '__main__':
    main()