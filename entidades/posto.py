class Posto:
    """Representa um posto de brigadistas com capacidade de operação."""
     
    def __init__(self, id_posto: str, capacidade_total_ph: float):
        self.id = id_posto
        self.capacidade_total_ph = float(capacidade_total_ph)
        self.tempo_trabalho_diario = 12.0
        self.capacidade_alocada = 0.0

    def reset_alocacao_diaria(self) -> None:
        """Reseta a capacidade alocada no início de cada dia."""
        self.capacidade_alocada = 0.0

    def capacidade_disponivel(self) -> float:
        """Retorna a capacidade ainda disponível para alocação."""
        return max(0, self.capacidade_total_ph - self.capacidade_alocada)

    def alocar_capacidade(self, capacidade: float) -> bool:
        """
        Tenta alocar capacidade do posto.
        Retorna True se a alocação foi bem-sucedida, False caso contrário.
        """
        if capacidade <= self.capacidade_disponivel():
            self.capacidade_alocada += capacidade
            return True
        return False

    def __repr__(self) -> str:
        return (f"Posto(id='{self.id}', cap={self.capacidade_total_ph:.2f} km²/h, "
                f"disponível={self.capacidade_disponivel():.2f})")