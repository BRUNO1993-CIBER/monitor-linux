#!/usr/bin/env python3
"""
CyberMonitor - Real-time System Monitor for Linux
Professional DevOps style monitoring tool
"""

import tkinter as tk
from tkinter import font as tkfont
import psutil
import subprocess
import os
from datetime import datetime
import time

class CyberMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        
        # Configuração inicial (antes de withdraw para evitar piscar)
        self.root.withdraw()
        
        # Configurações da janela
        self.width = 280
        self.height = 200
        self.setup_window()
        
        # Cores tema cyber
        self.bg_color = "#0a0e27"
        self.fg_primary = "#00ff41"
        self.fg_secondary = "#00d9ff"
        self.fg_warning = "#ffaa00"
        self.fg_danger = "#ff3366"
        self.fg_text = "#8892b0"
        
        self.root.config(bg=self.bg_color)
        
        # Fontes
        self.font_mono = tkfont.Font(family="JetBrains Mono", size=9, weight="bold")
        self.font_mono_small = tkfont.Font(family="JetBrains Mono", size=8)
        
        # Build UI
        self.create_widgets()
        
        # Variáveis de cache
        self.disk_cache = None
        self.disk_cache_time = 0
        
        # Mostrar janela após configuração completa
        self.root.deiconify()
        
        # Forçar janela para baixo após aparecer
        self.root.after(100, self.force_window_below)
        
        # Iniciar atualização
        self.update_stats()
        
    def setup_window(self):
        """Configura posicionamento e propriedades da janela"""
        # JANELA NORMAL - com bordas e botões
        # Remove o overrideredirect para ter comportamento normal
        # self.root.overrideredirect(True)  # DESABILITADO
        
        # Configurar como janela normal mas sticky
        self.root.attributes("-type", "utility")  # Janela utilitária pequena
        
        # Posicionar no canto superior direito
        screen_width = self.root.winfo_screenwidth()
        x_pos = screen_width - self.width - 20
        y_pos = 20
        
        self.root.geometry(f"{self.width}x{self.height}+{x_pos}+{y_pos}")
        
        # Não redimensionável
        self.root.resizable(False, False)
        
    def force_window_below(self):
        """Força a janela a ficar abaixo de todas as outras"""
        try:
            # Pegar o ID da janela
            window_id = self.root.wm_frame()
            
            # Tentar usar wmctrl
            subprocess.run(['wmctrl', '-i', '-r', window_id, '-b', 'add,below'], 
                         stderr=subprocess.DEVNULL, timeout=1)
        except:
            pass
        
        try:
            # Alternativa com xdotool
            subprocess.run(['xdotool', 'search', '--name', 'CyberMonitor', 
                          'windowraise', '%@'], 
                         stderr=subprocess.DEVNULL, timeout=1)
            subprocess.run(['xdotool', 'search', '--name', 'CyberMonitor', 
                          'set_window', '--role', 'desktop'], 
                         stderr=subprocess.DEVNULL, timeout=1)
        except:
            pass
        
    def create_widgets(self):
        """Cria a interface do monitor"""
        # Header simples (sem botão X já que agora tem borda)
        header = tk.Frame(self.root, bg="#141b33", height=25)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Título
        title_label = tk.Label(
            header, 
            text="⬢ MONITOR", 
            fg=self.fg_secondary,
            bg="#141b33",
            font=("JetBrains Mono", 9, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=8, pady=4)
        
        # Container principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        # Labels para métricas
        self.cpu_label = self.create_metric_label(main_frame, "CPU")
        self.cpu_temp_label = self.create_metric_label(main_frame, "TEMP")
        self.ram_label = self.create_metric_label(main_frame, "RAM")
        self.swap_label = self.create_metric_label(main_frame, "SWAP")
        self.gpu_label = self.create_metric_label(main_frame, "GPU")
        self.disk_label = self.create_metric_label(main_frame, "DISK")
        
    def create_metric_label(self, parent, name):
        """Cria um label formatado para métrica"""
        frame = tk.Frame(parent, bg=self.bg_color)
        frame.pack(fill=tk.X, pady=2)
        
        name_label = tk.Label(
            frame,
            text=f"{name}:",
            fg=self.fg_text,
            bg=self.bg_color,
            font=self.font_mono,
            width=6,
            anchor='w'
        )
        name_label.pack(side=tk.LEFT)
        
        value_label = tk.Label(
            frame,
            text="--",
            fg=self.fg_primary,
            bg=self.bg_color,
            font=self.font_mono,
            anchor='w'
        )
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        return value_label
    
    def get_color_by_percentage(self, value):
        """Retorna cor baseada no valor percentual"""
        if value < 50:
            return self.fg_primary
        elif value < 75:
            return self.fg_warning
        else:
            return self.fg_danger
    
    def get_cpu_temp(self):
        """Obtém temperatura da CPU"""
        try:
            # Tenta via psutil primeiro
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if 'coretemp' in name.lower() or 'k10temp' in name.lower() or 'cpu' in name.lower():
                        for entry in entries:
                            if 'tctl' in entry.label.lower() or 'package' in entry.label.lower():
                                return entry.current
                # Fallback para primeira temperatura disponível
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
        except:
            pass
        
        # Fallback para sensors command
        try:
            result = subprocess.run(['sensors'], stdout=subprocess.PIPE, text=True, timeout=1)
            for line in result.stdout.split('\n'):
                if 'Tctl' in line or 'Package id 0' in line:
                    temp_str = line.split()[1].replace('+', '').replace('°C', '')
                    return float(temp_str)
        except:
            pass
        
        return None
    
    def get_gpu_temp(self):
        """Obtém temperatura da GPU"""
        try:
            # Tenta via psutil
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if 'amdgpu' in name.lower() or 'nvidia' in name.lower():
                        for entry in entries:
                            if 'edge' in entry.label.lower() or 'temp' in entry.label.lower():
                                return entry.current
        except:
            pass
        
        # Tenta nvidia-smi para GPUs NVIDIA
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'],
                stdout=subprocess.PIPE, text=True, timeout=1
            )
            if result.returncode == 0:
                return float(result.stdout.strip())
        except:
            pass
        
        return None
    
    def get_disk_usage(self):
        """Obtém uso do disco (com cache)"""
        current_time = datetime.now().timestamp()
        
        # Cache de 5 segundos para operação de disco
        if self.disk_cache and (current_time - self.disk_cache_time) < 5:
            return self.disk_cache
        
        try:
            disk = psutil.disk_usage('/')
            self.disk_cache = disk.percent
            self.disk_cache_time = current_time
            return disk.percent
        except:
            return None
    
    def format_bytes(self, bytes_value):
        """Formata bytes para unidade legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}PB"
    
    def update_stats(self):
        """Atualiza todas as estatísticas"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0)
            cpu_color = self.get_color_by_percentage(cpu_percent)
            self.cpu_label.config(
                text=f"{cpu_percent:>5.1f}% [{self.get_bar(cpu_percent)}]",
                fg=cpu_color
            )
            
            # CPU Temperature
            cpu_temp = self.get_cpu_temp()
            if cpu_temp:
                temp_color = self.get_color_by_percentage((cpu_temp / 100) * 100)
                self.cpu_temp_label.config(
                    text=f"{cpu_temp:>5.1f}°C",
                    fg=temp_color
                )
            else:
                self.cpu_temp_label.config(text="N/A", fg=self.fg_text)
            
            # RAM
            ram = psutil.virtual_memory()
            ram_color = self.get_color_by_percentage(ram.percent)
            self.ram_label.config(
                text=f"{ram.percent:>5.1f}% [{self.get_bar(ram.percent)}] {self.format_bytes(ram.used)}",
                fg=ram_color
            )
            
            # SWAP
            swap = psutil.swap_memory()
            swap_color = self.get_color_by_percentage(swap.percent)
            self.swap_label.config(
                text=f"{swap.percent:>5.1f}% [{self.get_bar(swap.percent)}]",
                fg=swap_color
            )
            
            # GPU Temperature
            gpu_temp = self.get_gpu_temp()
            if gpu_temp:
                gpu_color = self.get_color_by_percentage((gpu_temp / 100) * 100)
                self.gpu_label.config(
                    text=f"{gpu_temp:>5.1f}°C",
                    fg=gpu_color
                )
            else:
                self.gpu_label.config(text="N/A", fg=self.fg_text)
            
            # DISK
            disk_percent = self.get_disk_usage()
            if disk_percent is not None:
                disk_color = self.get_color_by_percentage(disk_percent)
                self.disk_label.config(
                    text=f"{disk_percent:>5.1f}% [{self.get_bar(disk_percent)}]",
                    fg=disk_color
                )
            else:
                self.disk_label.config(text="N/A", fg=self.fg_text)
            
        except Exception as e:
            print(f"Error updating stats: {e}")
        
        # Agendar próxima atualização (1.5s para melhor performance)
        self.root.after(1500, self.update_stats)
    
    def get_bar(self, percent):
        """Cria barra de progresso ASCII"""
        filled = int(percent / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty
    
    def run(self):
        """Inicia o monitor"""
        self.root.mainloop()

if __name__ == "__main__":
    monitor = CyberMonitor()
    monitor.run()