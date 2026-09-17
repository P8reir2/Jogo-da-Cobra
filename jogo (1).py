import tkinter as tk
from tkinter import simpledialog
import json
import os
import datetime
import pygame
from Cobra import Cobra
from Comida import Comida

class Jogo:
    def __init__(self):
        pygame.mixer.init()
        self.largura = 600
        self.altura = 400
        self.tamanho = 20

        self.tema = "claro"
        self.cor_cobra1 = "green"
        self.cor_cobra2 = "blue"
        self.velocidade_inicial = 100

        self.janela = tk.Tk()
        self.janela.title("Jogo da Cobra - Menu com Níveis")

        # Frames
        self.frame_menu = tk.Frame(self.janela, width=self.largura, height=self.altura)
        self.frame_niveis = tk.Frame(self.janela, width=self.largura, height=self.altura)
        self.frame_ranking = tk.Frame(self.janela, width=self.largura, height=self.altura)
        self.frame_config = tk.Frame(self.janela, width=self.largura, height=self.altura)
        self.frame_jogo = tk.Frame(self.janela, width=self.largura, height=self.altura)

        # Canvas do jogo
        self.canvas = tk.Canvas(self.frame_jogo, width=self.largura, height=self.altura, bg="lightgray")
        self.canvas.pack()

        # Arquivo de ranking
        self.ficheiro_ranking = "ranking.json"
        self.inicializar_ranking()

        self.modo_dois = False
        self.som_comer = None
        self.som_morte = None

        # MOSTRA O MENU APENAS UMA VEZ
        self.mostrar_menu()

        self.janela.mainloop()

    def inicializar_ranking(self):
        if not os.path.exists(self.ficheiro_ranking):
            with open(self.ficheiro_ranking, "w") as f:
                json.dump([], f)

    def guardar_ranking(self, nome, pontuacao):
        with open(self.ficheiro_ranking, "r") as f:
            lista = json.load(f)
        data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lista.append({"nome": nome, "pontuacao": pontuacao, "data": data})
        lista = sorted(lista, key=lambda x: x["pontuacao"], reverse=True)[:10]
        with open(self.ficheiro_ranking, "w") as f:
            json.dump(lista, f)

    def esconder_frames(self):
        self.frame_menu.pack_forget()
        self.frame_niveis.pack_forget()
        self.frame_ranking.pack_forget()
        self.frame_config.pack_forget()
        self.frame_jogo.pack_forget()

    def mostrar_menu(self):
        self.esconder_frames()
        self.canvas.delete("all")  # Limpa canvas do jogo
        self.frame_menu.pack()

        tk.Label(self.frame_menu, text="Jogo da Cobra", font=("Arial", 28)).pack(pady=40)
        tk.Button(self.frame_menu, text="1 Jogador", font=("Arial", 16), width=20, command=lambda: self.selecionar_nivel(False)).pack(pady=10)
        tk.Button(self.frame_menu, text="2 Jogadores", font=("Arial", 16), width=20, command=lambda: self.selecionar_nivel(True)).pack(pady=10)
        tk.Button(self.frame_menu, text="Ranking", font=("Arial", 16), width=20, command=self.mostrar_ranking).pack(pady=10)
        tk.Button(self.frame_menu, text="Configurações", font=("Arial", 16), width=20, command=self.mostrar_config).pack(pady=10)
        tk.Button(self.frame_menu, text="Sair", font=("Arial", 16), width=20, command=self.janela.quit).pack(pady=10)

    def selecionar_nivel(self, modo_dois):
        self.esconder_frames()
        self.frame_niveis.pack()
        self.modo_dois = modo_dois

        bg = "white" if self.tema == "claro" else "black"
        fg = "black" if self.tema == "claro" else "white"
        self.frame_niveis.configure(bg=bg)

        for widget in self.frame_niveis.winfo_children():
            widget.destroy()

        tk.Label(self.frame_niveis, text="Escolha o Nível", font=("Arial", 24), bg=bg, fg=fg).pack(pady=40)
        tk.Button(self.frame_niveis, text="Fácil", font=("Arial", 16), width=20, command=lambda: self.iniciar_com_nivel(150)).pack(pady=10)
        tk.Button(self.frame_niveis, text="Médio", font=("Arial", 16), width=20, command=lambda: self.iniciar_com_nivel(100)).pack(pady=10)
        tk.Button(self.frame_niveis, text="Difícil", font=("Arial", 16), width=20, command=lambda: self.iniciar_com_nivel(60)).pack(pady=10)
        tk.Button(self.frame_niveis, text="Voltar", font=("Arial", 16), width=20, command=self.mostrar_menu).pack(pady=20)

    def iniciar_com_nivel(self, velocidade):
        self.velocidade_inicial = velocidade
        self.iniciar_jogo(self.modo_dois)

    def mostrar_config(self):
        self.esconder_frames()
        self.frame_config.pack()

        bg = "white" if self.tema == "claro" else "black"
        fg = "black" if self.tema == "claro" else "white"
        self.frame_config.configure(bg=bg)

        for widget in self.frame_config.winfo_children():
            widget.destroy()

        tk.Label(self.frame_config, text="Configurações", font=("Arial", 24), bg=bg, fg=fg).pack(pady=40)

    def mostrar_ranking(self):
        self.esconder_frames()
        self.frame_ranking.pack()

        bg = "white" if self.tema == "claro" else "black"
        fg = "black" if self.tema == "claro" else "white"
        self.frame_ranking.configure(bg=bg)

        for widget in self.frame_ranking.winfo_children():
            widget.destroy()

        tk.Label(self.frame_ranking, text="Ranking Top 10", font=("Arial", 24), bg=bg, fg=fg).pack(pady=20)

        with open(self.ficheiro_ranking, "r") as f:
            ranking = json.load(f)

        for item in ranking:
            tk.Label(self.frame_ranking, text=f"{item['nome']} - {item['pontuacao']} ({item['data']})", font=("Arial", 16), bg=bg, fg=fg).pack()

        tk.Button(self.frame_ranking, text="Voltar", width=20, command=self.mostrar_menu).pack(pady=20)

    def iniciar_jogo(self, modo_dois):
        self.esconder_frames()  # Garante que frames antigos desapareçam
        self.frame_jogo.pack()
        self.canvas.delete("all")  # Limpa canvas antigo

        self.modo_dois = modo_dois
        self.pontuacao = 0
        self.velocidade = self.velocidade_inicial

        self.nome = simpledialog.askstring("Nome", "Digite seu nome:")

        self.cobra1 = Cobra(self.canvas, cor=self.cor_cobra1)
        self.comida = Comida(self.canvas, self.largura, self.altura)

        if self.modo_dois:
            self.cobra2 = Cobra(self.canvas, cor=self.cor_cobra2)
            self.cobra2.partes = [(300,100),(280,100),(260,100)]
            for i,(x,y) in enumerate(self.cobra2.partes):
                if i < len(self.cobra2.segmentos):
                    self.canvas.coords(self.cobra2.segmentos[i], x, y, x+self.tamanho, y+self.tamanho)
                else:
                    self.cobra2.segmentos.append(self.cobra2.desenhar_parte(x, y))

        self.janela.bind("<KeyPress>", self.teclas)

        # Loop do jogo
        self.atualizar_jogo()

    def teclas(self, evento):
        mapa = {"Up":"Cima","Down":"Baixo","Left":"Esquerda","Right":"Direita"}
        if evento.keysym in mapa:
            self.cobra1.mudar_direcao(mapa[evento.keysym])

        if self.modo_dois:
            mapa2 = {"w":"Cima","s":"Baixo","a":"Esquerda","d":"Direita"}
            if evento.keysym in mapa2:
                self.cobra2.mudar_direcao(mapa2[evento.keysym])

    def verificar_colisoes(self, cobra):
        x,y = cobra.partes[0]
        if x<0 or y<0 or x>=self.largura or y>=self.altura:
            return True
        if (x,y) in cobra.partes[1:]:
            return True
        return False

    def verificar_comida(self, cobra):
        if cobra.partes[0] == self.comida.posicao:
            cobra.crescer()
            self.comida.aparecer()
            self.pontuacao += 1
            self.velocidade = max(40, self.velocidade - 3)

    def fim(self):
        # Limpa o canvas
        self.canvas.delete("all")

        # Remove botões antigos do frame_jogo
        for widget in self.frame_jogo.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        # Guarda pontuação
        self.guardar_ranking(self.nome if self.nome else "Anônimo", self.pontuacao)

        # Mostra mensagem de fim de jogo
        self.canvas.create_text(self.largura/2, self.altura/2-40, text=f"Game Over! Pontuação: {self.pontuacao}", font=("Arial", 22))

        # Botão para voltar ao menu
        tk.Button(self.frame_jogo, text="Menu", width=20, command=self.mostrar_menu).place(x=200, y=self.altura/2+40)

    def atualizar_jogo(self):
        """Loop principal do jogo"""
        self.cobra1.mover()
        if self.verificar_colisoes(self.cobra1):
            return self.fim()
        self.verificar_comida(self.cobra1)

        if self.modo_dois:
            self.cobra2.mover()
            if self.verificar_colisoes(self.cobra2):
                return self.fim()
            self.verificar_comida(self.cobra2)

            if self.cobra1.partes[0] in self.cobra2.partes or self.cobra2.partes[0] in self.cobra1.partes:
                return self.fim()

        self.janela.after(self.velocidade, self.atualizar_jogo)


if __name__ == "__main__":
    Jogo()
