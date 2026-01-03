#!/bin/bash
# Script para iniciar o CyberMonitor com venv

# Navegar para o diretório
cd "/home/bhm/Documents/mini conky"

# Ativar o ambiente virtual e executar
source .venv/bin/activate
python3 mini_conky.py &

# Desativar venv (não é necessário mas mantém limpo)
deactivate
