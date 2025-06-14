import networkx as nx
from typing import Dict, List, Optional
# REMOVA os imports relativos (com ..) e use:
from entidades.foco import Foco
from entidades.posto import Posto
from servicos.alocador_recursos import AlocadorRecursos


class SimuladorIncendios:
    """Classe principal que gerencia a simulação do combate a incêndios."""
    
    def __init__(self, max_dias: int = 100):
        """
        Inicializa o simulador com configurações padrão.
        
        Args:
            max_dias: Número máximo de dias para a simulação (padrão: 100)
        """
        self.mapa_focos: Dict[str, Foco] = {}
        self.mapa_postos: Dict[str, Posto] = {}
        self.grafo = nx.Graph()
        self.alocador: Optional[AlocadorRecursos] = None
        self.dia_atual = 0
        self.max_dias = max_dias
        self.historico_alocacoes: List[List[dict]] = []

    def carregar_dados(self, num_focos: int, num_postos: int, capacidades: List[float],
                       areas_iniciais: List[float], fatores_crescimento: List[float],
                       matriz_distancias: List[List[float]]) -> None:
        """
        Carrega todos os dados iniciais da simulação.
        
        Args:
            num_focos: Número de focos de incêndio
            num_postos: Número de postos de brigadistas
            capacidades: Lista de capacidades dos postos (km²/hora)
            areas_iniciais: Lista de áreas iniciais dos focos (km²)
            fatores_crescimento: Lista de fatores de crescimento diário dos focos
            matriz_distancias: Matriz de distâncias entre todos os nós
        """
        self._criar_entidades(num_focos, num_postos, capacidades, areas_iniciais, fatores_crescimento)
        self._construir_grafo(matriz_distancias)
        self.alocador = AlocadorRecursos(self.mapa_focos, self.mapa_postos, self.grafo)

    def _criar_entidades(self, num_focos: int, num_postos: int, capacidades: List[float],
                        areas_iniciais: List[float], fatores_crescimento: List[float]) -> None:
        """Cria as entidades (focos e postos) a partir dos dados iniciais."""
        self.mapa_focos = {
            f"f{i}": Foco(f"f{i}", areas_iniciais[i], fatores_crescimento[i]) 
            for i in range(num_focos)
        }
        self.mapa_postos = {
            f"b{i}": Posto(f"b{i}", capacidades[i]) 
            for i in range(num_postos)
        }

    def _construir_grafo(self, matriz_distancias: List[List[float]]) -> None:
        """Constrói o grafo de conexões a partir da matriz de distâncias."""
        node_names = list(self.mapa_focos.keys()) + list(self.mapa_postos.keys())
        for i in range(len(node_names)):
            for j in range(len(node_names)):
                distancia = matriz_distancias[i][j]
                if distancia > 0:  # Ignora conexões com distância zero
                    self.grafo.add_edge(node_names[i], node_names[j], weight=distancia)

    def executar_dia(self) -> bool:
        """
        Executa um dia completo de simulação.
        
        Returns:
            True se a simulação pode continuar, False se não foi possível alocar recursos
        """
        self.dia_atual += 1
        
        if not self.alocador:
            raise RuntimeError("Alocador de recursos não foi inicializado")
            
        alocacoes = self.alocador.alocar_recursos_dia()
        self.historico_alocacoes.append(alocacoes)
        
        # Verifica se há focos ativos sem alocação
        if not alocacoes and any(f.status == 'ativo' for f in self.mapa_focos.values()):
            return False
        
        # Aplica o combate aos focos
        for aloc in alocacoes:
            aloc['foco'].combater(aloc['area_reduzida'], self.dia_atual)
        
        # Aplica crescimento aos focos ativos
        for foco in self.mapa_focos.values():
            if foco.status == 'ativo':
                foco.crescer()
        
        return True

    def simular(self) -> Dict:
        """
        Executa a simulação completa até extinguir todos os focos ou atingir o limite de dias.
        
        Returns:
            Dicionário com os resultados da simulação:
            {
                'sucesso': bool,
                'dias_totais': int,
                'dias_extincao': Dict[str, int],
                'limite_atingido': bool,
                'focos_ativos': Dict[str, float]
            }
        """
        while self.dia_atual < self.max_dias:
            if not any(f.status == 'ativo' for f in self.mapa_focos.values()):
                break  # Todos os focos extintos
                
            if not self.executar_dia():
                break  # Falha na alocação
        
        return self._gerar_resultados()

    def _gerar_resultados(self) -> Dict:
        """Compila os resultados finais da simulação."""
        return {
            'sucesso': not any(f.status == 'ativo' for f in self.mapa_focos.values()),
            'dias_totais': self.dia_atual,
            'dias_extincao': {f.id: f.dia_extincao for f in self.mapa_focos.values() 
                              if f.status == 'extinto'},
            'limite_atingido': self.dia_atual >= self.max_dias,
            'focos_ativos': {f.id: f.area_atual for f in self.mapa_focos.values() 
                             if f.status == 'ativo'}
        }

    def obter_estado_atual(self) -> Dict:
        """Retorna um snapshot do estado atual da simulação."""
        return {
            'dia': self.dia_atual,
            'focos': {f.id: {'area': f.area_atual, 'status': f.status} 
                      for f in self.mapa_focos.values()},
            'postos': {p.id: {'capacidade_total': p.capacidade_total_ph,
                              'capacidade_alocada': p.capacidade_alocada}
                       for p in self.mapa_postos.values()}
        }