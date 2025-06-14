from typing import List


class Foco:
    """Representa um foco de incêndio"""

    def __init__(self, id_foco: str, area_inicial: float, taxa_alpha: float):
        self.id = id_foco
        self.area_inicial = float(area_inicial)
        self.taxa_alpha = float(taxa_alpha)
        self.area_atual = float(area_inicial)
        self.status = 'ativo'  # 'ativo' ou 'extinto'
        self.dia_extincao = -1
        self.historico_areas: List[float] = [float(area_inicial)]

    def crescer(self) -> None:
        """Aplica o fator de crescimento diário se o foco estiver ativo."""
        if self.status == 'ativo':
            self.area_atual = round(self.area_atual * self.taxa_alpha, 4)
            self.historico_areas.append(self.area_atual)

    def combater(self, area_reduzida: float, dia_atual: int) -> bool:
        """
        Reduz a área do foco e verifica se foi extinto.
        Retorna True se o foco foi extinto, False caso contrário.
        """
        if self.status == 'ativo':
            self.area_atual = max(0, round(self.area_atual - area_reduzida, 4))
            if self.area_atual <= 0.001:
                self.area_atual = 0
                self.status = 'extinto'
                self.dia_extincao = dia_atual
                return True
        return False

    def __repr__(self) -> str:
        return (f"Foco(id='{self.id}', area={self.area_atual:.2f} km², "
                f"status='{self.status}', crescimento={self.taxa_alpha})")