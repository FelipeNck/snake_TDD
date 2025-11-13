import pytest
from snake import SnakeGame
from snake_screen import io_handler 

class TestSnakeGame:
    def setup_method(self):
        # Configura um tabuleiro 10x10 para os testes
        self.io = io_handler((10, 10), 0.5) 
        self.game = SnakeGame(self.io)

    def test_initial_snake_position(self):
        # Verifica se a cobra é inicializada corretamente olhando para a lista interna
        assert len(self.game.snake) == 2, "A cobra deve começar com tamanho 2."
        
        # A cabeça é o último elemento, a cauda o primeiro
        head = self.game.snake[-1]
        tail = self.game.snake[0]
        
        # Verifica posições específicas esperadas (baseado no seu __init__)
        assert head == (0, 1), "A cabeça deve começar em (0, 1)."
        assert tail == (0, 0), "A cauda deve começar em (0, 0)."

    def test_snake_moves_up(self):
        # Simula o input 'w' e verifica se a cobra se move para cima
        self.io.last_input = 'w'
        initial_head_pos = self.game.snake_head_position 
        
        self.game.update_game_state() 
        
        # A nova posição da cabeça deve ser uma unidade acima (y - 1)
        expected_new_head_y = (initial_head_pos[0] - 1 + self.io.y_size) % self.io.y_size
        
        # Verificação direta na variável de estado do jogo
        assert self.game.snake_head_position == (expected_new_head_y, initial_head_pos[1])
        assert self.game.snake[-1] == (expected_new_head_y, initial_head_pos[1])

    def test_snake_moves_down(self):
        # Configura cenário
        self.game.snake = [(1,1), (0,1)] 
        self.game.snake_head_position = (0,1)
        # Removido: self.game.update_matrix() -> Não é mais necessário para testar a lógica
        
        self.io.last_input = 's'
        initial_head_pos = self.game.snake_head_position
        
        self.game.update_game_state()
        
        expected_new_head_y = (initial_head_pos[0] + 1) % self.io.y_size
        assert self.game.snake_head_position == (expected_new_head_y, initial_head_pos[1])

    def test_snake_moves_left(self):
        self.game.snake = [(0,1), (0,2)] 
        self.game.snake_head_position = (0,2)
        
        self.game.current_direction = 'w' 
        self.io.last_input = 'a'
        initial_head_pos = self.game.snake_head_position
        
        self.game.update_game_state()
        
        expected_new_head_x = (initial_head_pos[1] - 1 + self.io.x_size) % self.io.x_size
        assert self.game.snake_head_position == (initial_head_pos[0], expected_new_head_x)

    def test_snake_moves_right(self):
        self.io.last_input = 'd'
        initial_head_pos = self.game.snake_head_position
        
        self.game.update_game_state()
        
        expected_new_head_x = (initial_head_pos[1] + 1) % self.io.x_size
        assert self.game.snake_head_position == (initial_head_pos[0], expected_new_head_x)

    def test_fruit_spawns_correctly(self):
        # Em vez de contar na matriz, verifica se a variável fruit_position não é None
        assert self.game.fruit_position is not None, "Deveria haver uma fruta definida no estado do jogo."
        
        # Verifica se a fruta está dentro dos limites do tabuleiro
        y, x = self.game.fruit_position
        assert 0 <= y < self.io.y_size
        assert 0 <= x < self.io.x_size

    def test_snake_eats_fruit_and_grows(self):
        self.game.snake = [(0, 0), (0, 1)]
        self.game.snake_head_position = (0, 1)
        self.game.current_direction = 'd' 
        self.io.last_input = 'd' 
        
        # Define a posição da fruta manualmente no estado
        fruit_position = (0, 2)
        self.game.fruit_position = fruit_position
        
        initial_length = len(self.game.snake)

        self.game.update_game_state()

        # Verifica crescimento
        assert len(self.game.snake) == initial_length + 1
        
        # Verifica posição
        assert self.game.snake_head_position == fruit_position
        assert self.game.snake[-1] == fruit_position

        # Verifica se uma NOVA fruta foi gerada (posição diferente de None)
        assert self.game.fruit_position is not None
        # Nota: Não podemos garantir que a posição mudou se o random escolher o mesmo lugar, 
        # mas garantimos que o objeto existe.

    def test_game_over_on_self_collision(self):
        self.game.snake = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.game.snake_head_position = (0, 1)
        self.game.current_direction = 's'
        self.io.last_input = 's' 

        self.game.update_game_state()

        # Verifica a variável booleana de estado
        assert self.game.is_game_over is True