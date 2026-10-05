# Configuração do ambiente de desenvolvimento

Este guia explica como criar e ativar um ambiente virtual Python para o backend do projeto.

## Pré-requisitos

Instale o Python 3. No Windows, confirme que o Python está disponível pelo comando `py`; no Linux e macOS, use `python3`.

Execute os comandos a partir da pasta `apps/backend`.

## Criar o ambiente virtual

### Windows

```powershell
py -m venv .venv
```

### Linux e macOS

```bash
python3 -m venv .venv
```

## Ativar o ambiente virtual

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução do script, permita scripts para o utilizador atual e tente novamente:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows (Prompt de Comando)

```bat
.venv\Scripts\activate.bat
```

### Linux

```bash
source .venv/bin/activate
```

### macOS

```bash
source .venv/bin/activate
```

Quando estiver ativo, o nome do ambiente, normalmente `(.venv)`, aparece no início da linha de comandos.

## Instalar dependências

Com o ambiente virtual ativo, instale as dependências do backend:

```bash
pip install -r requirements.txt
```

## Desativar o ambiente virtual

Para sair do ambiente virtual, execute:

```bash
deactivate
```
