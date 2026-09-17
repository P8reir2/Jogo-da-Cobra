class Cobra:
    def __init__(self, canvas, cor="green"):
        self.canvas = canvas
        self.tamanho_quadrado = 20
        self.cor = cor
        self.direcao = "Direita"

        # Posições iniciais da cobra
        self.partes = [(100, 100), (80, 100), (60, 100)]

        # Desenha os segmentos iniciais
        self.segmentos = [
            self.desenhar_parte(x, y) for x, y in self.partes
        ]

    def desenhar_parte(self, x, y):
        """Desenha um segmento da cobra."""
        return self.canvas.create_rectangle(
            x,
            y,
            x + self.tamanho_quadrado,
            y + self.tamanho_quadrado,
            fill=self.cor,
            outline="black"
        )

    def mover(self):
        """Atualiza a posição da cobra."""

        # Guarda a cauda antes de mover (necessário para crescer corretamente)
        self.cauda_anterior = self.partes[-1]

        x, y = self.partes[0]

        # Atualiza posição da cabeça conforme direção
        if self.direcao == "Cima":
            y -= self.tamanho_quadrado
        elif self.direcao == "Baixo":
            y += self.tamanho_quadrado
        elif self.direcao == "Esquerda":
            x -= self.tamanho_quadrado
        elif self.direcao == "Direita":
            x += self.tamanho_quadrado

        nova_cabeca = (x, y)

        # Move a cobra (insere nova cabeça e remove a cauda)
        self.partes = [nova_cabeca] + self.partes[:-1]

        # Atualiza graficamente os segmentos
        for i, (x, y) in enumerate(self.partes):
            self.canvas.coords(
                self.segmentos[i],
                x,
                y,
                x + self.tamanho_quadrado,
                y + self.tamanho_quadrado
            )

    def crescer(self):
        """Adiciona um segmento na cauda corretamente."""
        x_ultimo, y_ultimo = self.partes[-1]

        # Cria um novo segmento exatamente na posição da cauda
        self.partes.append((x_ultimo, y_ultimo))

        # Desenha o novo segmento
        self.segmentos.append(
            self.desenhar_parte(x_ultimo, y_ultimo)
        )

    def mudar_direcao(self, nova_direcao):
        """Evita que a cobra dê a volta nela mesma."""
        opostos = {
            "Cima": "Baixo",
            "Baixo": "Cima",
            "Esquerda": "Direita",
            "Direita": "Esquerda"
        }

        if opostos.get(self.direcao) != nova_direcao:
            self.direcao = nova_direcao
