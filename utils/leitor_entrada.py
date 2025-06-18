from typing import Tuple, Optional, List
import sys


class LeitorEntrada:
    """Responsável por ler e validar os dados de entrada do simulador."""
    
    def ler_arquivo(nome_arquivo: str) -> Optional[Tuple]:
        """Lê e valida um arquivo de entrada."""
        try:
            with open(nome_arquivo, 'r') as f:
                linhas = [linha.strip() for linha in f if linha.strip()]
                
                # Validação formato pedido edisciplinas
                if len(linhas) < 4:
                    raise ValueError("Arquivo de entrada incorreto")
                
                # Linha 1: Números de focos e postos
                try:
                    num_focos, num_postos = map(int, linhas[0].split())
                except ValueError:
                    raise ValueError("Formato inválido na linha 1 "
                                     "esperado dois números inteiros")
                
                linhas_necessarias = 4 + num_focos + num_postos
                if len(linhas) < linhas_necessarias:
                    raise ValueError(f"Arquivo deve ter pelo menos {linhas_necessarias} linhas")
                
                # Linhas seguintes: capacidades, áreas, fatores de crescimento
                capacidades = LeitorEntrada.ler_lista_float(linhas[1], num_postos, "capacidades dos postos")
                areas_iniciais = LeitorEntrada.ler_lista_float(linhas[2], num_focos, "áreas iniciais")
                fatores_crescimento = LeitorEntrada.ler_lista_float(linhas[3], num_focos, "fatores de crescimento")
                
                # matriz de distância (edisciplinas)
                matriz_distancias = []
                for i in range(4, 4 + num_focos + num_postos):
                    linha = LeitorEntrada.ler_lista_float(linhas[i], num_focos + num_postos, f"linha {i+1} da matriz")
                    matriz_distancias.append(linha)
                
                return (num_focos, num_postos, capacidades, areas_iniciais, 
                        fatores_crescimento, matriz_distancias)
                        
        except FileNotFoundError:
            print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.", file=sys.stderr)
            return None
        except ValueError as e:
            print(f"Erro no arquivo '{nome_arquivo}': {str(e)}", file=sys.stderr)
            return None
        
    def validar_matriz_distancias(matriz: List[List[float]], num_nos: int) -> None:
        """Valida a matriz de distâncias."""
        if len(matriz) != num_nos:
            raise ValueError(f"Matriz deve ter {num_nos} linhas")
        for linha in matriz:
            if len(linha) != num_nos:
                raise ValueError("Matriz deve ser quadrada")
            if any(x < 0 for x in linha):
                raise ValueError("Distancias não podem ser negativas")

    def ler_lista_float(linha: str, tamanho_esperado: int, descricao: str) -> List[float]:
        """Lê e valida uma lista de valores float."""
        try:
            valores = list(map(float, linha.split()))
            if len(valores) != tamanho_esperado:
                raise ValueError(f"Quantidade inválida de {descricao}-esperado {tamanho_esperado}, obtido {len(valores)}")
            return valores
        except ValueError:
            raise ValueError(f"Formato inválido para {descricao} - todos os valores devem ser números")