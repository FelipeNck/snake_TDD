import pytest
from snake import SnakeGame
from snake_screen import io_handler 

class TestSnakeGame:
    def setup_method(self):
        # Configura um tabuleiro 10x10 para os testes
        self.io = io_handler((10, 10), 0.5) 
        self.game = SnakeGame(self.io)

    def test_initial_snake_position(self):
        # Verifica se a cobra é inicializada com um corpo e uma cabeça
        # Vamos assumir que a cabeça é 2 e o corpo é 1
        assert any(2 in row for row in self.io.matrix), "A cabeça da cobra deve estar presente."
        assert sum(row.count(1) for row in self.io.matrix) >= 1, "Pelo menos um segmento do corpo da cobra deve estar presente."
        
        # Teste mais específico: vamos esperar que a cabeça esteja em (0,1) e o corpo em (0,0) inicialmente
        assert self.io.matrix[0][1] == 2
        assert self.io.matrix[0][0] == 1

    def test_snake_moves_up(self):
        # Simula o input 'w' e verifica se a cobra se move para cima
        self.io.last_input = 'w'
        initial_head_pos = self.game.snake_head_position 
        self.game.update_game_state() 
        
        # A nova posição da cabeça deve ser uma unidade acima da posição inicial (y - 1)
        expected_new_head_y = (initial_head_pos[0] - 1 + self.io.y_size) % self.io.y_size
        assert self.game.snake_head_position == (expected_new_head_y, initial_head_pos[1]), "A cobra deve se mover para cima."

    def test_snake_moves_down(self):
        # Simula o input 's' e verifica se a cobra se move para baixo
        self.game.snake = [(1,1), (0,1)] # Ex: corpo em (1,1), cabeça em (0,1)
        self.game.snake_head_position = (0,1)
        self.game.update_matrix() 
        
        self.io.last_input = 's'
        initial_head_pos = self.game.snake_head_position
        self.game.update_game_state()
        
        expected_new_head_y = (initial_head_pos[0] + 1) % self.io.y_size
        assert self.game.snake_head_position == (expected_new_head_y, initial_head_pos[1]), "A cobra deve se mover para baixo."

    def test_snake_moves_left(self):
        # Simula o input 'a' e verifica se a cobra se move para a esquerda
        self.game.snake = [(0,1), (0,2)] # Ex: corpo em (0,1), cabeça em (0,2)
        self.game.snake_head_position = (0,2)
        self.game.update_matrix()

        self.game.current_direction = 'w' # Força cobra a começar indo pra cima
        
        self.io.last_input = 'a'
        initial_head_pos = self.game.snake_head_position
        self.game.update_game_state()
        
        expected_new_head_x = (initial_head_pos[1] - 1 + self.io.x_size) % self.io.x_size
        assert self.game.snake_head_position == (initial_head_pos[0], expected_new_head_x), "A cobra deve se mover para a esquerda."

    def test_snake_moves_right(self):
        # Simula o input 'd' e verifica se a cobra se move para a direita
        self.io.last_input = 'd'
        initial_head_pos = self.game.snake_head_position
        self.game.update_game_state()
        
        expected_new_head_x = (initial_head_pos[1] + 1) % self.io.x_size
        assert self.game.snake_head_position == (initial_head_pos[0], expected_new_head_x), "A cobra deve se mover para a direita."
