import pygame
import os
from snake import SnakeGame

# --- CONFIGURAÇÕES ---
BLOCK_SIZE = 40 
GRID_W, GRID_H = 20, 15
SCREEN_W, SCREEN_H = GRID_W * BLOCK_SIZE, GRID_H * BLOCK_SIZE

# --- CLASSE AUXILIAR DE INPUT ---
class PygameHandler:
    def __init__(self):
        self.y_size = GRID_H
        self.x_size = GRID_W
        self.last_input = 'd'

# --- GERENCIADOR DE GRÁFICOS ---
class Graphics:
    def __init__(self):
        self.images = {}
        self.load_images()

    def load_images(self):
        # Helper para carregar e escalar
        def load(name):
            path = os.path.join("Graphics", name + ".png")
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
            except FileNotFoundError:
                print(f"ERRO CRÍTICO: Imagem não encontrada: {path}")
                print("Verifique se a pasta 'Graphics' está junto com o main_pygame.py e se os nomes estão corretos.")
                exit()

        # Carrega as imagens usando os nomes que você mostrou
        self.images['apple'] = load("apple")

        # Cabeças
        self.images['head_w'] = load("head_up")
        self.images['head_s'] = load("head_down")
        self.images['head_a'] = load("head_left")
        self.images['head_d'] = load("head_right")

        # Caudas
        self.images['tail_w'] = load("tail_up")
        self.images['tail_s'] = load("tail_down")
        self.images['tail_a'] = load("tail_left")
        self.images['tail_d'] = load("tail_right")

        # Corpos Retos
        self.images['body_vert'] = load("body_vertical")
        self.images['body_horiz'] = load("body_horizontal")

        # Curvas (Corrigido para os nomes do seu print)
        self.images['curve_top_left'] = load("body_topleft") 
        self.images['curve_top_right'] = load("body_topright")
        self.images['curve_bottom_left'] = load("body_bottomleft")
        self.images['curve_bottom_right'] = load("body_bottomright")

    def get_vector(self, start, end, limit):
        """Calcula a direção de start para end, considerando o wrap-around (teleporte)."""
        dx = end[1] - start[1]
        dy = end[0] - start[0] 

        if dx > 1: dx = -1
        if dx < -1: dx = 1
        if dy > 1: dy = -1
        if dy < -1: dy = 1
        
        return dy, dx 

    def draw_snake(self, screen, snake_list):
        for i, segment in enumerate(snake_list):
            y, x = segment
            screen_pos = (x * BLOCK_SIZE, y * BLOCK_SIZE)
            
            # 1. CABEÇA
            if i == len(snake_list) - 1:
                prev = snake_list[i-1]
                dy, dx = self.get_vector(prev, segment, (GRID_H, GRID_W))
                
                if dx == 1: img = self.images['head_d']
                elif dx == -1: img = self.images['head_a']
                elif dy == 1: img = self.images['head_s']
                else: img = self.images['head_w']
                
                screen.blit(img, screen_pos)

            # 2. CAUDA
            elif i == 0:
                next_seg = snake_list[i+1]
                dy, dx = self.get_vector(segment, next_seg, (GRID_H, GRID_W))
                
                if dx == 1: img = self.images['tail_a']
                elif dx == -1: img = self.images['tail_d']
                elif dy == 1: img = self.images['tail_w']
                else: img = self.images['tail_s']
                
                screen.blit(img, screen_pos)

            # 3. CORPO (Reto ou Curva)
            else:
                prev = snake_list[i-1]
                next_seg = snake_list[i+1]
                
                py, px = self.get_vector(segment, prev, (GRID_H, GRID_W))
                ny, nx = self.get_vector(segment, next_seg, (GRID_H, GRID_W))
                
                if px == nx: # Vertical
                    screen.blit(self.images['body_vert'], screen_pos)
                elif py == ny: # Horizontal
                    screen.blit(self.images['body_horiz'], screen_pos)
                else:
                    # Lógica para curvas
                    if (py == 1 and nx == 1) or (px == 1 and ny == 1):
                        screen.blit(self.images['curve_bottom_right'], screen_pos)
                    elif (py == 1 and nx == -1) or (px == -1 and ny == 1):
                        screen.blit(self.images['curve_bottom_left'], screen_pos)
                    elif (py == -1 and nx == 1) or (px == 1 and ny == -1):
                        screen.blit(self.images['curve_top_right'], screen_pos)
                    elif (py == -1 and nx == -1) or (px == -1 and ny == -1):
                        screen.blit(self.images['curve_top_left'], screen_pos)
                    else:
                        screen.blit(self.images['body_horiz'], screen_pos)

# --- SETUP GERAL ---
pygame.init()
# AQUI ESTÁ A DEFINIÇÃO QUE FALTAVA NO SEU ERRO:
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake Game TDD")
clock = pygame.time.Clock()

graphics = Graphics() # Carrega os assets
input_handler = PygameHandler()
game = SnakeGame(input_handler) 

running = True
while running:
    # 1. INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP: input_handler.last_input = 'w'
            if event.key == pygame.K_s or event.key == pygame.K_DOWN: input_handler.last_input = 's'
            if event.key == pygame.K_a or event.key == pygame.K_LEFT: input_handler.last_input = 'a'
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT: input_handler.last_input = 'd'
            if event.key == pygame.K_ESCAPE: input_handler.last_input = 'end'

    # 2. UPDATE
    game.update_game_state()

    if game.is_game_over:
        print("GAME OVER!")
        game = SnakeGame(input_handler) # Reinicia

    # 3. DRAW
    screen.fill((34, 139, 34)) # Fundo Verde
    
    if game.fruit_position:
        fy, fx = game.fruit_position
        screen.blit(graphics.images['apple'], (fx * BLOCK_SIZE, fy * BLOCK_SIZE))

    graphics.draw_snake(screen, game.snake)

    pygame.display.flip()
    clock.tick(8) # 8 FPS

pygame.quit()