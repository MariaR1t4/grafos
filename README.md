# Estrutura de dados
## Estrutura do projeto 

### 📄 `main.py` *(arquivo principal)*

### 📂 `entidades/`
- 📄 `__init__.py` *(torna a pasta um pacote Python)*
- 📄 `foco.py` *(classe Foco de incêndio)*
- 📄 `posto.py` *(classe Posto de brigadistas)*

### 📂 `servicos/`
- 📄 `__init__.py`
- 📄 `alocador_recursos.py` *(lógica de alocação)*
- 📄 `simulador.py` *(núcleo da simulação)*
- 📄 `visualizacao.py` *(geração de gráficos)*

### 📂 `utils/`
- 📄 `__init__.py`
- 📄 `leitor_entrada.py` *(leitura de arquivos de teste)*
- 📄 `relatorio.py` *(geração de relatórios)*

### 📂 `testes/`
- 📄 `__init__.py`
- 📄 `test_simulador.py` *(testes automatizados)*

## Como utilizar
### 🛠️ Configuração do Ambiente
  - Clone o repositório:
  - git clone https://github.com/MariaR1t4/grafos
  - cd ED
### Instale as bibliotecas necessárias em `requirements.txt`

### Executar teste:
  python main.py testes/nome_arquivo.txt

## Features:
- Rodar testes `in batch`, no presente modelo os testes devem ser chamados de forma unitária.
