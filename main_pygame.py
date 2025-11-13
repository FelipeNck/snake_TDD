import pygame
from snake import SnakeGame

# --- CONFIGURAÇÕES ---
BLOCK_SIZE = 40 # Tamanho de cada quadrado em pixels
GRID_W, GRID_H = 20, 15 # Dimensões do tabuleiro (colunas, linhas)
SCREEN_W, SCREEN_H = GRID_W * BLOCK_SIZE, GRID_H * BLOCK_SIZE

# --- CLASSE AUXILIAR DE INPUT ---
class PygameHandler:
    def __init__(self):
        # Precisamos dessas propriedades porque o SnakeGame as lê
        self.y_size = GRID_H
        self.x_size = GRID_W
        self.last_input = 'd'

# --- FUNÇÃO DE DESENHO SIMPLES (Correção do Erro) ---
def draw_snake_sprites(screen, snake_list):
    """Desenha a cobra como quadrados verdes (temporário até o Passo 4)."""
    for segment in snake_list:
        y, x = segment # O jogo usa (y, x)
        
        # O Pygame usa (x, y) para pixels
        rect_x = x * BLOCK_SIZE
        rect_y = y * BLOCK_SIZE
        
        rect = pygame.Rect(rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, (0, 255, 0), rect) # Cor Verde

# --- SETUP DO PYGAME ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake TDD com Pygame")
clock = pygame.time.Clock()

# Inicialização do Jogo
input_handler = PygameHandler()
game = SnakeGame(input_handler) 

running = True

# --- LOOP PRINCIPAL ---
while running:
    # 1. PROCESSAMENTO DE EVENTOS (INPUT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP: 
                input_handler.last_input = 'w'
            if event.key == pygame.K_s or event.key == pygame.K_DOWN: 
                input_handler.last_input = 's'
            if event.key == pygame.K_a or event.key == pygame.K_LEFT: 
                input_handler.last_input = 'a'
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT: 
                input_handler.last_input = 'd'
            if event.key == pygame.K_ESCAPE:
                input_handler.last_input = 'end'

    # 2. ATUALIZAÇÃO DO JOGO (UPDATE)
    game.update_game_state()

    if game.is_game_over:
        print("GAME OVER!")
        running = False

    # 3. DESENHO NA TELA (DRAW)
    screen.fill((0, 0, 0)) # Limpa a tela com preto
    
    # Desenha a Fruta (Vermelho)
    if game.fruit_position:
        fy, fx = game.fruit_position
        fruit_rect = pygame.Rect(fx * BLOCK_SIZE, fy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    # Desenha a Cobra (Verde)
    draw_snake_sprites(screen, game.snake) 

    pygame.display.flip() # Atualiza o display
    clock.tick(5) # Define a velocidade (5 frames por segundo)

pygame.quit()