import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List

def visualizar_grafo(num_focos: int, num_postos: int, 
                     matriz_distancias: List[List[float]], 
                     nome_arquivo: str = "case3"):
    """
    Gera uma visualização do grafo com estilo robusto e nome personalizado
    
    Args:
        num_focos: Número de focos de incêndio
        num_postos: Número de postos de brigadistas
        matriz_distancias: Matriz de distâncias entre os nós
        nome_arquivo: Nome base do arquivo de teste (sem extensão)
    """
    try:
        # Configuração de estilo mais robusta
        if 'seaborn' in plt.style.available:
            plt.style.use('seaborn')
        else:
            plt.style.use('default')  # Fallback seguro
            plt.rcParams.update({
                'figure.facecolor': 'white',
                'axes.edgecolor': '0.3',
                'axes.labelcolor': '0.3',
                'text.color': '0.3'
            })

        G = nx.Graph()
        
        # Adiciona nós com cores acessíveis
        for i in range(1, num_focos + 1):
            G.add_node(f'f{i}', tipo='foco', color='#e74c3c')  # Vermelho
        for i in range(1, num_postos + 1):
            G.add_node(f'b{i}', tipo='posto', color='#3498db')  # Azul
        
        # Conecta arestas
        todos_nos = [f'f{i}' for i in range(1, num_focos+1)] + [f'b{i}' for i in range(1, num_postos+1)]
        for i in range(len(todos_nos)):
            for j in range(len(todos_nos)):
                if matriz_distancias[i][j] > 0:
                    G.add_edge(todos_nos[i], todos_nos[j], weight=matriz_distancias[i][j])
        
        # Layout otimizado
        pos = nx.spring_layout(G, seed=42, k=0.8)
        
        # Figura com tamanho responsivo
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Desenho do grafo com fallbacks
        nx.draw_networkx_nodes(G, pos, ax=ax,
                               node_color=[G.nodes[n]['color'] for n in G.nodes()],
                               node_size=800,
                               edgecolors='#2c3e50',
                               linewidths=1.5)
        
        nx.draw_networkx_labels(G, pos, ax=ax,
                                labels={n: n.upper() for n in G.nodes()},
                                font_size=12,
                                font_weight='bold',
                                font_family='sans-serif')
        
        nx.draw_networkx_edges(G, pos, ax=ax,
                               width=2,
                               alpha=0.8,
                               edge_color='#7f8c8d')
        
        nx.draw_networkx_edge_labels(G, pos, ax=ax,
                                     edge_labels=nx.get_edge_attributes(G, 'weight'),
                                     font_size=10,
                                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        # Título e legenda resilientes
        ax.set_title(f"Rede de Combate - {nome_arquivo}", pad=20, fontsize=14)
        fig.text(0.5, 0.02, 
                 "FOCOS (vermelho) | POSTOS (azul)", 
                 ha='center',
                 bbox=dict(facecolor='#ecf0f1', alpha=0.7, boxstyle='round,pad=0.5'))
        
        # Salva com tratamento de erros
        nome_saida = f"grafo_incendio_{nome_arquivo}.png"
        try:
            plt.savefig(nome_saida, dpi=150, bbox_inches='tight')
            print(f"✓ Gráfico salvo como {nome_saida}")
        except Exception as e:
            print(f"⚠ Erro ao salvar gráfico: {str(e)}")
            nome_saida = None
        
        plt.close()
        return nome_saida
        
    except Exception as e:
        print(f"⚠ Erro na geração do gráfico: {str(e)}")
        return None