from snake_screen import io_handler

class SnakeGame:
    def __init__(self, io_handler_instance: io_handler):
        self.io = io_handler_instance
        # A cobra será uma lista de tuplas (y, x), onde (y, x) é a coordenada da célula.
        # A primeira tupla é a cauda, a última é a cabeça.
        self.snake = [(0, 0), (0, 1)] # Posição inicial: corpo em (0,0), cabeça em (0,1)
        self.snake_head_position = self.snake[-1]
        self.current_direction = 'd' # Direção inicial para a direita

        self.update_matrix()

    def update_matrix(self):
        # Limpa a matriz do io_handler
        for y in range(self.io.y_size):
            for x in range(self.io.x_size):
                self.io.matrix[y][x] = 0

        # Desenha a cobra na matriz
        for i, segment in enumerate(self.snake):
            y, x = segment
            if i == len(self.snake) - 1: # É a cabeça
                self.io.matrix[y][x] = 2
            else: # É um segmento do corpo
                self.io.matrix[y][x] = 1

    def update_game_state(self):
        # Atualiza a direção com base no último input
        new_direction = self.io.last_input
        # Regras para não permitir virar 180 graus
        if (new_direction == 'w' and self.current_direction == 's') or \
           (new_direction == 's' and self.current_direction == 'w') or \
           (new_direction == 'a' and self.current_direction == 'd') or \
           (new_direction == 'd' and self.current_direction == 'a'):
            pass # Mantém a direção atual
        else:
            self.current_direction = new_direction

        head_y, head_x = self.snake_head_position
        new_head_y, new_head_x = head_y, head_x

        if self.current_direction == 'w':
            new_head_y = (head_y - 1 + self.io.y_size) % self.io.y_size
        elif self.current_direction == 's':
            new_head_y = (head_y + 1) % self.io.y_size
        elif self.current_direction == 'a':
            new_head_x = (head_x - 1 + self.io.x_size) % self.io.x_size
        elif self.current_direction == 'd':
            new_head_x = (head_x + 1) % self.io.x_size
        elif self.current_direction == 'end':
            return # O jogo termina, não move a cobra

        new_head_position = (new_head_y, new_head_x)
        self.snake.append(new_head_position)
        self.snake.pop(0) # Remove a cauda para simular o movimento
        self.snake_head_position = new_head_position

        self.update_matrix()

# Exemplo de como integrar ao game_loop fornecido:
# if __name__ == '__main__':
#     instance = io_handler((10, 15), 0.5)
#     game = SnakeGame(instance)
    
#     def game_loop():
#         instance.record_inputs()
#         while True:
#             instance.display()
#             print("mova com WASD, saia com esc. Ultimo botão:", end=' ')
#             game.update_game_state() # Adiciona esta linha
#             print(instance.last_input)
#             if(instance.last_input == 'end'):
#                 exit()
#             time.sleep(instance.game_speed)

#     # Remova ou comente as linhas de exemplo do io_handler no arquivo principal
#     # instance.matrix[0][0] = 1 #corpo
#     # instance.matrix[0][1] = 2 #cabeça
#     # instance.matrix[0][2] = 3 #fruta
#     game_loop()