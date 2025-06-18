from typing import Dict, List, Optional
import networkx as nx
# Altere para:
from entidades.foco import Foco
from entidades.posto import Posto


class AlocadorRecursos:
    """Responsável por alocar recursos dos postos para os focos de forma otimizada."""
    
    def __init__(self, mapa_focos: Dict[str, Foco], mapa_postos: Dict[str, Posto], grafo: nx.Graph):
        self.mapa_focos = mapa_focos
        self.mapa_postos = mapa_postos
        self.grafo = grafo
        self.precomputar_tempos_deslocamento()

    def precomputar_tempos_deslocamento(self) -> None:
        """Pré-computa os tempos de deslocamento entre todos os nós."""
        self.tempos_deslocamento = dict(nx.all_pairs_dijkstra_path_length(self.grafo, weight='weight'))

    def obter_tempo_deslocamento(self, posto_id: str, foco_id: str) -> float:
        """Retorna o tempo de deslocamento entre um posto e um foco."""
        return self.tempos_deslocamento.get(posto_id, {}).get(foco_id, float('inf'))

    def alocar_recursos_dia(self) -> List[dict]:
        """Realiza a alocação de recursos para o dia atual."""
        alocacoes = []
        
        # Resetar alocações dos postos
        for posto in self.mapa_postos.values():
            posto.reset_alocacao_diaria()
        
        # Processar focos por prioridade (maiores primeiro)
        for foco in sorted(
            [f for f in self.mapa_focos.values() if f.status == 'ativo'],
            key=lambda f: (-f.area_atual, f.id)
        ):
            if foco.area_atual <= 0:
                continue
            # Encontrar postos candidatos para este foco
            postos_candidatos = self.encontrar_postos_candidatos(foco)
            
            # Alocar recursos dos postos para este foco
            for candidato in postos_candidatos:
                alocacao = self.alocar_recurso_foco(candidato, foco)
                if alocacao:
                    alocacoes.append(alocacao)
                    if foco.area_atual <= 0:
                        break
        
        return alocacoes

    def encontrar_postos_candidatos(self, foco: Foco) -> List[dict]:
        """Encontra postos que podem atender ao foco."""
        candidatos = []
        
        for posto in self.mapa_postos.values():
            tempo_desloc = self.obter_tempo_deslocamento(posto.id, foco.id)
            tempo_combate = posto.tempo_trabalho_diario - tempo_desloc
            
            if tempo_combate > 0 and posto.capacidade_disponivel() > 0:
                candidatos.append({
                    'posto': posto,
                    'tempo_desloc': tempo_desloc,
                    'tempo_combate': tempo_combate
                })
        
        # Ordenar por maior capacidade disponível e menor tempo de deslocamento
        return sorted(candidatos, key=lambda x: (-x['posto'].capacidade_disponivel(), x['tempo_desloc']))

    def alocar_recurso_foco(self, candidato: dict, foco: Foco) -> Optional[dict]:
        """Tenta alocar recurso de um posto para um foco."""
        posto = candidato['posto']
        tempo_combate = candidato['tempo_combate']
        cap_necessaria = foco.area_atual / tempo_combate
        cap_alocar = min(cap_necessaria, posto.capacidade_disponivel())
        
        if cap_alocar > 0.001 and posto.alocar_capacidade(cap_alocar):
            area_reduzida = cap_alocar * tempo_combate
            foco.combater(area_reduzida, 0)  # O dia atual será definido depois
            return {
                'posto': posto,
                'foco': foco,
                'capacidade_alocada': cap_alocar,
                'tempo_combate': tempo_combate,
                'area_reduzida': area_reduzida
            }
        return None