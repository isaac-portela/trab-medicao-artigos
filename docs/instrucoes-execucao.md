# Instruções de Execução do Pipeline de Classificação

Este documento explica o passo a passo necessário para preparar o ambiente Python e executar o pipeline de classificação e análise dos 88 artigos.

---

## 📋 Pré-requisitos
1. **Python 3.10 ou superior** instalado.
2. **Chave de API do DeepSeek (API Key)** obtida em [platform.deepseek.com](https://platform.deepseek.com/).

---

## 🛠️ Passo a Passo para Execução

### 1. Criar o Ambiente Virtual (venv)
Caso ainda não tenha criado, abra o terminal na pasta raiz do projeto (`trab-medicao-artigos`) e execute:
```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual
Ative o ambiente virtual de acordo com o seu terminal/sistema operacional:

* **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (Prompt de Comando - cmd)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **Linux / macOS (Bash/Zsh)**:
  ```bash
  source .venv/bin/activate
  ```

*Quando ativado, você verá `(.venv)` no início da linha de comando.*

### 3. Instalar as Dependências
Com o ambiente ativado, instale as bibliotecas Python necessárias declaradas no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar a Chave da API do DeepSeek
Defina a sua API Key como uma variável de ambiente para que o script possa consumi-la:

* **Windows (PowerShell)**:
  ```powershell
  $env:DEEPSEEK_API_KEY="SUA_CHAVE_AQUI"
  ```
* **Windows (cmd)**:
  ```cmd
  set DEEPSEEK_API_KEY=SUA_CHAVE_AQUI
  ```
* **Linux / macOS**:
  ```bash
  export DEEPSEEK_API_KEY="SUA_CHAVE_AQUI"
  ```

---

## 🚀 Executando o Pipeline

O script `scripts/run_pipeline.py` possui parâmetros para ajudar na execução segura:

### Opção A: Executar um Teste Rápido (Recomendado)
Antes de rodar para todos os 88 arquivos, execute o modo de teste seco (dry run). Isso processará **apenas o primeiro artigo** para validar a integração:
```bash
python scripts/run_pipeline.py --dry-run
```
* **Resultado esperado**: Um arquivo chamado `classificacao_artigos.xlsx` será gerado na raiz com apenas 1 linha de dados. Abra-o e verifique se as notas, resumo e justificativas foram criados com sucesso.

### Opção B: Executar a Análise Completa
Para analisar todos os 88 artigos, execute:
```bash
python scripts/run_pipeline.py
```
* **Tratamento de Rate Limits**: Por padrão, o script espera **4.0 segundos** entre cada requisição para não estourar a cota de chamadas gratuitas da API. 
* **Ajustar Delay**: Se você possuir uma chave com maior limite e quiser acelerar o processo, pode diminuir a pausa (ex: pausa de 2 segundos):
  ```bash
  python scripts/run_pipeline.py --delay 2.0
  ```

---

## 📊 Arquivo de Saída
O resultado será salvo na raiz do projeto como **`classificacao_artigos.xlsx`**. 

A planilha virá pré-estilizada com:
* Ajuste automático de largura de colunas.
* Congelamento da primeira linha de cabeçalhos.
* Destaque em cores (Verde para artigos altamente relevantes, Amarelo para intermediários e Vermelho para artigos com baixo alinhamento/aprendizado).
