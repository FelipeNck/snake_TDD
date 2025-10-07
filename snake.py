import random
from snake_screen import io_handler

class SnakeGame:
    COLLISION_TYPE_NONE = 0
    COLLISION_TYPE_FRUIT = 1
    COLLISION_TYPE_SELF = 2

    def __init__(self, io_handler_instance: io_handler):
        self.io = io_handler_instance
        self.snake = [(0, 0), (0, 1)] 
        self.snake_head_position = self.snake[-1]
        self.current_direction = 'd'
        self.fruit_position = None
        self.is_game_over = False 

        self._spawn_fruit()
        self.update_matrix()

    def _spawn_fruit(self):
        occupied_cells = set(self.snake)
        empty_cells = []
        for y in range(self.io.y_size):
            for x in range(self.io.x_size):
                if (y, x) not in occupied_cells:
                    empty_cells.append((y, x))
        if empty_cells:
            self.fruit_position = random.choice(empty_cells)
    
    def _calculate_next_head_position(self, current_head_y, current_head_x, direction):
        next_y, next_x = current_head_y, current_head_x
        if direction == 'w':
            next_y = (current_head_y - 1 + self.io.y_size) % self.io.y_size
        elif direction == 's':
            next_y = (current_head_y + 1) % self.io.y_size
        elif direction == 'a':
            next_x = (current_head_x - 1 + self.io.x_size) % self.io.x_size
        elif direction == 'd':
            next_x = (current_head_x + 1) % self.io.x_size
        return (next_y, next_x)

    def _process_input(self):
        """Lê o input do usuário e atualiza a direção da cobra."""
        new_direction = self.io.last_input
        if new_direction == 'end':
            self.is_game_over = True
            return

        # Regra dos 180 graus
        is_opposite_direction = (new_direction == 'w' and self.current_direction == 's') or \
                                (new_direction == 's' and self.current_direction == 'w') or \
                                (new_direction == 'a' and self.current_direction == 'd') or \
                                (new_direction == 'd' and self.current_direction == 'a')
        
        if not is_opposite_direction:
            self.current_direction = new_direction

    def _get_collision_type(self, position):
        """Verifica uma posição e retorna o tipo de colisão."""
        if position in self.snake[1:]:
            return self.COLLISION_TYPE_SELF
        if position == self.fruit_position:
            return self.COLLISION_TYPE_FRUIT
        return self.COLLISION_TYPE_NONE

    def _move_snake(self, new_head_position):
        """Move a cobra para a frente (sem crescer)."""
        self.snake.append(new_head_position)
        self.snake.pop(0)
        self.snake_head_position = new_head_position

    def _grow_snake(self, new_head_position):
        """Faz a cobra crescer, adicionando a nova cabeça."""
        self.snake.append(new_head_position)
        self.snake_head_position = new_head_position
    
    def update_matrix(self):
        for y in range(self.io.y_size):
            for x in range(self.io.x_size):
                self.io.matrix[y][x] = 0
        for i, segment in enumerate(self.snake):
            y, x = segment
            if i == len(self.snake) - 1:
                self.io.matrix[y][x] = 2
            else:
                self.io.matrix[y][x] = 1
        if self.fruit_position:
            y, x = self.fruit_position
            self.io.matrix[y][x] = 3

    def update_game_state(self):
        """Coordena todas as ações de um passo do jogo."""
        if self.is_game_over:
            return

        # 1. Processa o input do jogador
        self._process_input()
        if self.is_game_over:
            return

        # 2. Calcula a próxima posição
        head_y, head_x = self.snake_head_position
        next_pos = self._calculate_next_head_position(head_y, head_x, self.current_direction)

        # 3. Verifica o que tem na próxima casa
        collision_type = self._get_collision_type(next_pos)

        # 4. Age com base na resposta
        if collision_type == self.COLLISION_TYPE_SELF:
            self.is_game_over = True
        elif collision_type == self.COLLISION_TYPE_FRUIT:
            self._grow_snake(next_pos)
            self._spawn_fruit()
        else: # COLLISION_TYPE_NONE
            self._move_snake(next_pos)

        # 5. Atualiza a tela
        self.update_matrix()