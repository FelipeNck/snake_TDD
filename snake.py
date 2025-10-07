from snake_screen import io_handler

class SnakeGame:
    def __init__(self, io_handler_instance: io_handler):
        self.io = io_handler_instance
        self.snake = [(0, 0), (0, 1)] 
        self.snake_head_position = self.snake[-1]
        self.current_direction = 'd'

        self.update_matrix()

    def _calculate_next_head_position(self, current_head_y, current_head_x, direction):
        # Calcula a próxima posição da cabeça com base na direção e limites da tela
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

    def update_game_state(self):
        new_direction = self.io.last_input
        
        # Não permite virar 180 graus
        if not ((new_direction == 'w' and self.current_direction == 's') or \
                (new_direction == 's' and self.current_direction == 'w') or \
                (new_direction == 'a' and self.current_direction == 'd') or \
                (new_direction == 'd' and self.current_direction == 'a')):
            self.current_direction = new_direction

        if self.current_direction == 'end':
            return 

        head_y, head_x = self.snake_head_position
        new_head_position = self._calculate_next_head_position(head_y, head_x, self.current_direction)
        
        self.snake.append(new_head_position)
        self.snake.pop(0)
        self.snake_head_position = new_head_position

        self.update_matrix()