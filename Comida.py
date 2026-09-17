import random

class Comida:
    def __init__(self, canvas, largura, altura):
        self.canvas = canvas
        self.largura = largura
        self.altura = altura
        self.tamanho = 20
        self.id = None     # <- nome padronizado para o item no canvas

        self.aparecer()

    def aparecer(self):
        """Cria a comida em posição aleatória."""

        # Remove comida antiga
        if self.id:
            self.canvas.delete(self.id)

        # Gera coordenadas alinhadas à grade
        x = random.randrange(0, self.largura, self.tamanho)
        y = random.randrange(0, self.altura, self.tamanho)

        # posição lógica
        self.posicao = (x, y)

        # Desenha a comida e guarda o ID
        self.id = self.canvas.create_oval(
            x, y,
            x + self.tamanho,
            y + self.tamanho,
            fill="red"
        )
