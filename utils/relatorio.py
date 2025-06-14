from typing import Dict, List
from entidades.foco import Foco
from entidades.posto import Posto
from servicos.simulador import SimuladorIncendios


class GeradorRelatorio:
    """Gera relatórios detalhados sobre a simulação."""
    
    @staticmethod
    def gerar_relatorio(resultados: Dict, mapa_focos: Dict[str, Foco], 
                        mapa_postos: Dict[str, Posto],
                        historico_alocacoes: List[List[dict]]) -> str:
        """Gera um relatório simulação."""
        partes = []
        
        # Cabeçalho com resultado geral
        partes.append(GeradorRelatorio._cabecalho_relatorio(resultados))
        
        partes.append("\n📊 DETALHES POR FOCO:")
        partes.extend(GeradorRelatorio._detalhes_focos(mapa_focos))
        
        partes.append("\n🏗️ RECURSOS DOS POSTOS:")
        partes.extend(GeradorRelatorio._detalhes_postos(mapa_postos))
        
        partes.append("\n⏳ HISTÓRICO DE ALOCAÇÕES DIÁRIAS:")
        partes.extend(GeradorRelatorio._historico_alocacoes(historico_alocacoes))
        
        return "\n".join(partes)

    @staticmethod
    def _cabecalho_relatorio(resultados: Dict) -> str:
        """Gera o cabeçalho do relatório com o resultado geral."""
        if resultados['sucesso']:
            return f"✅ TODOS OS FOCOS FORAM EXTINTOS EM {resultados['dias_totais']} DIAS."
        elif resultados['limite_atingido']:
            return f"⏰ LIMITE DE {resultados['dias_totais']} DIAS ATINGIDO SEM EXTINÇÃO TOTAL."
        else:
            return "❌ NÃO FOI POSSÍVEL EXTINGUIR TODOS OS FOCOS COM OS RECURSOS DISPONÍVEIS."

    @staticmethod
    def _detalhes_focos(mapa_focos: Dict[str, Foco]) -> List[str]:
        """Gera os detalhes de cada foco."""
        detalhes = []
        for foco_id, foco in mapa_focos.items():
            status = "EXTINTO" if foco.status == 'extinto' else f"ATIVO ({foco.area_atual:.2f} km²)"
            dia_ext = foco.dia_extincao if foco.dia_extincao != -1 else "N/A"
            detalhes.append(
                f"  - {foco_id}: {status} | Dia extinção: {dia_ext} | "
                f"Área inicial: {foco.area_inicial:.2f} km² | Crescimento: {foco.taxa_alpha}x/dia"
            )
        return detalhes

    @staticmethod
    def _detalhes_postos(mapa_postos: Dict[str, Posto]) -> List[str]:
        """Gera os detalhes de cada posto."""
        return [
            f"  - {posto.id}: Capacidade total {posto.capacidade_total_ph:.2f} km²/h"
            for posto in mapa_postos.values()
        ]

    @staticmethod
    def _historico_alocacoes(historico: List[List[dict]]) -> List[str]:
        """Gera o histórico de alocações."""
        historico_str = []
        for dia, alocacoes in enumerate(historico, 1):
            historico_str.append(f"\n  Dia {dia}:")
            if not alocacoes:
                historico_str.append("    Nenhum recurso alocado")
            for aloc in alocacoes:
                historico_str.append(
                    f"    {aloc['posto'].id} → {aloc['foco'].id}: "
                    f"{aloc['capacidade_alocada']:.2f} km²/h por {aloc['tempo_combate']:.1f}h "
                    f"(Total: {aloc['area_reduzida']:.2f} km²)"
                )
        return historico_str