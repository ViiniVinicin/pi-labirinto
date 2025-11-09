import pygame
import random
import sys
import time

# --- Configurações Iniciais ---
tamanho_celula = 25
cols = 20
rows = 15
INFO_BAR_HEIGHT = 30
largura_tela = cols * tamanho_celula + 40
altura_tela = rows * tamanho_celula + 40 + INFO_BAR_HEIGHT

# --- Paleta de Cores (Tema Escuro) ---
FUNDO = (20, 20, 30)
PAREDE = (100, 100, 120)
INFO_BAR_FUNDO = (40, 40, 50)
TEXTO_COR = (230, 230, 230)
BORDA_INFO_BAR = (80, 80, 90)
PRETO = (0, 0, 0) # ### CORREÇÃO: Cor PRETO adicionada de volta ###

# Cores dos elementos do jogo
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (50, 150, 255)
CINZA_CLARO = (45, 45, 60)
LARANJA = (255, 165, 0)
VIOLETA_CLARO = (55, 45, 70)

# --- Classe Celula ---
class Celula:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.paredes = [True, True, True, True]
        self.visitada = False
    
    def desenhar(self, tela, cor_parede=PAREDE):
        x_pixel, y_pixel = self.x * tamanho_celula + 20, self.y * tamanho_celula + 20
        if self.paredes[0]: pygame.draw.line(tela, cor_parede, (x_pixel, y_pixel), (x_pixel + tamanho_celula, y_pixel), 2)
        if self.paredes[1]: pygame.draw.line(tela, cor_parede, (x_pixel + tamanho_celula, y_pixel), (x_pixel + tamanho_celula, y_pixel + tamanho_celula), 2)
        if self.paredes[2]: pygame.draw.line(tela, cor_parede, (x_pixel + tamanho_celula, y_pixel + tamanho_celula), (x_pixel, y_pixel + tamanho_celula), 2)
        if self.paredes[3]: pygame.draw.line(tela, cor_parede, (x_pixel, y_pixel + tamanho_celula), (x_pixel, y_pixel), 2)

    def checar_vizinhos(self, grid):
        vizinhos = []
        if self.y > 0 and not grid[self.x][self.y - 1].visitada: vizinhos.append(grid[self.x][self.y - 1])
        if self.x < cols - 1 and not grid[self.x + 1][self.y].visitada: vizinhos.append(grid[self.x + 1][self.y])
        if self.y < rows - 1 and not grid[self.x][self.y + 1].visitada: vizinhos.append(grid[self.x][self.y + 1])
        if self.x > 0 and not grid[self.x - 1][self.y].visitada: vizinhos.append(grid[self.x - 1][self.y])
        return random.choice(vizinhos) if vizinhos else None

# --- Funções de Geração e Resolução (sem alterações lógicas) ---
def remover_paredes(atual, proxima):
    dx, dy = atual.x - proxima.x, atual.y - proxima.y
    if dx == 1: atual.paredes[3], proxima.paredes[1] = False, False
    elif dx == -1: atual.paredes[1], proxima.paredes[3] = False, False
    if dy == 1: atual.paredes[0], proxima.paredes[2] = False, False
    elif dy == -1: atual.paredes[2], proxima.paredes[0] = False, False

def gerar_labirinto(grid):
    for row in grid:
        for cell in row: cell.visitada = False
    pilha, celula_atual = [], grid[0][0]
    celula_atual.visitada = True
    pilha.append(celula_atual)
    while pilha:
        celula_atual = pilha.pop()
        vizinho = celula_atual.checar_vizinhos(grid)
        if vizinho:
            pilha.append(celula_atual)
            remover_paredes(celula_atual, vizinho)
            vizinho.visitada = True
            pilha.append(vizinho)

def criar_loops(grid, numero_de_loops):
    for _ in range(numero_de_loops):
        x, y = random.randint(0, cols - 2), random.randint(0, rows - 2)
        if random.choice([True, False]): remover_paredes(grid[x][y], grid[x+1][y])
        else: remover_paredes(grid[x][y], grid[x][y+1])

def resolver_com_bfs(grid, inicio, fim):
    fila, visitados = [(inicio, [inicio])], {inicio}
    while fila:
        (atual, caminho) = fila.pop(0)
        if atual == fim: return caminho, visitados
        x, y = atual.x, atual.y
        vizinhos_possiveis = []
        if y > 0 and not atual.paredes[0]: vizinhos_possiveis.append(grid[x][y-1])
        if x < cols - 1 and not atual.paredes[1]: vizinhos_possiveis.append(grid[x+1][y])
        if y < rows - 1 and not atual.paredes[2]: vizinhos_possiveis.append(grid[x][y+1])
        if x > 0 and not atual.paredes[3]: vizinhos_possiveis.append(grid[x-1][y])
        for vizinho in vizinhos_possiveis:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    return None, visitados

def resolver_com_dfs(grid, inicio, fim):
    pilha, visitados = [(inicio, [inicio])], {inicio}
    while pilha:
        (atual, caminho) = pilha.pop()
        if atual == fim: return caminho, visitados
        x, y = atual.x, atual.y
        vizinhos_possiveis = []
        if y > 0 and not atual.paredes[0]: vizinhos_possiveis.append(grid[x][y-1])
        if x < cols - 1 and not atual.paredes[1]: vizinhos_possiveis.append(grid[x+1][y])
        if y < rows - 1 and not atual.paredes[2]: vizinhos_possiveis.append(grid[x][y+1])
        if x > 0 and not atual.paredes[3]: vizinhos_possiveis.append(grid[x-1][y])
        random.shuffle(vizinhos_possiveis)
        for vizinho in vizinhos_possiveis:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append((vizinho, caminho + [vizinho]))
    return None, visitados

# --- Função Principal do Jogo ---
def main():
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Jogo de Labirinto - Teoria dos Grafos")
    clock = pygame.time.Clock()
    
    largura_labirinto = largura_tela
    altura_labirinto = altura_tela - INFO_BAR_HEIGHT
    surface_labirinto = pygame.Surface((largura_labirinto, altura_labirinto))

    try:
        susto_imagem_original = pygame.image.load('susto.jpg')
        susto_som = pygame.mixer.Sound('grito.wav')
        susto_imagem = pygame.transform.scale(susto_imagem_original, (largura_tela, altura_tela))
        jump_scare_pronto = True
    except pygame.error as e:
        print(f"Erro ao carregar arquivos do jump scare: {e}")
        jump_scare_pronto = False

    grid = [[Celula(x, y) for y in range(rows)] for x in range(cols)]
    gerar_labirinto(grid)
    criar_loops(grid, 20)
    
    jogador_pos = grid[0][0]
    inicio, fim = grid[0][0], grid[cols - 1][rows - 1]
    
    caminho_solucao_bfs, visitados_bfs, tempo_bfs = None, set(), 0
    mostrar_solucao_bfs = False
    caminho_solucao_dfs, visitados_dfs, tempo_dfs = None, set(), 0
    mostrar_solucao_dfs = False
    fim_de_jogo = False
    
    try:
        fonte = pygame.font.SysFont('Consolas', 16, bold=True)
    except:
        fonte = pygame.font.Font(None, 22)

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: rodando = False
            if event.type == pygame.KEYDOWN and not fim_de_jogo:
                x, y = jogador_pos.x, jogador_pos.y
                if event.key == pygame.K_UP and not jogador_pos.paredes[0]: jogador_pos = grid[x][y - 1]
                elif event.key == pygame.K_RIGHT and not jogador_pos.paredes[1]: jogador_pos = grid[x + 1][y]
                elif event.key == pygame.K_DOWN and not jogador_pos.paredes[2]: jogador_pos = grid[x][y + 1]
                elif event.key == pygame.K_LEFT and not jogador_pos.paredes[3]: jogador_pos = grid[x - 1][y]
                elif event.key == pygame.K_s:
                    mostrar_solucao_bfs = not mostrar_solucao_bfs
                    mostrar_solucao_dfs = False
                    if mostrar_solucao_bfs and not caminho_solucao_bfs:
                        tempo_inicio = time.time()
                        caminho_solucao_bfs, visitados_bfs = resolver_com_bfs(grid, inicio, fim)
                        tempo_fim = time.time()
                        tempo_bfs = tempo_fim - tempo_inicio
                elif event.key == pygame.K_d:
                    mostrar_solucao_dfs = not mostrar_solucao_dfs
                    mostrar_solucao_bfs = False
                    if mostrar_solucao_dfs and not caminho_solucao_dfs:
                        tempo_inicio = time.time()
                        caminho_solucao_dfs, visitados_dfs = resolver_com_dfs(grid, inicio, fim)
                        tempo_fim = time.time()
                        tempo_dfs = tempo_fim - tempo_inicio

        # --- Desenho ---
        if not fim_de_jogo:
            surface_labirinto.fill(FUNDO)
            
            if mostrar_solucao_bfs and visitados_bfs:
                for celula in visitados_bfs: pygame.draw.rect(surface_labirinto, CINZA_CLARO, (celula.x * tamanho_celula + 20, celula.y * tamanho_celula + 20, tamanho_celula, tamanho_celula))
            if mostrar_solucao_dfs and visitados_dfs:
                for celula in visitados_dfs: pygame.draw.rect(surface_labirinto, VIOLETA_CLARO, (celula.x * tamanho_celula + 20, celula.y * tamanho_celula + 20, tamanho_celula, tamanho_celula))
            for x in range(cols):
                for y in range(rows): grid[x][y].desenhar(surface_labirinto)
            pygame.draw.rect(surface_labirinto, VERDE, (inicio.x*tamanho_celula+25, inicio.y*tamanho_celula+25, tamanho_celula-10, tamanho_celula-10))
            pygame.draw.rect(surface_labirinto, VERMELHO, (fim.x*tamanho_celula+25, fim.y*tamanho_celula+25, tamanho_celula-10, tamanho_celula-10))
            if mostrar_solucao_bfs and caminho_solucao_bfs:
                for i in range(len(caminho_solucao_bfs) - 1):
                    p1, p2 = (caminho_solucao_bfs[i].x * tamanho_celula + 32, caminho_solucao_bfs[i].y * tamanho_celula + 32), (caminho_solucao_bfs[i+1].x * tamanho_celula + 32, caminho_solucao_bfs[i+1].y * tamanho_celula + 32)
                    pygame.draw.line(surface_labirinto, AZUL, p1, p2, 4)
            if mostrar_solucao_dfs and caminho_solucao_dfs:
                for i in range(len(caminho_solucao_dfs) - 1):
                    p1, p2 = (caminho_solucao_dfs[i].x * tamanho_celula + 32, caminho_solucao_dfs[i].y * tamanho_celula + 32), (caminho_solucao_dfs[i+1].x * tamanho_celula + 32, caminho_solucao_dfs[i+1].y * tamanho_celula + 32)
                    pygame.draw.line(surface_labirinto, LARANJA, p1, p2, 4)
            pygame.draw.rect(surface_labirinto, AMARELO, (jogador_pos.x * tamanho_celula + 25, jogador_pos.y * tamanho_celula + 25, tamanho_celula - 10, tamanho_celula - 10))

            tela.fill(FUNDO)
            pygame.draw.rect(tela, INFO_BAR_FUNDO, (0, 0, largura_tela, INFO_BAR_HEIGHT))
            pygame.draw.line(tela, BORDA_INFO_BAR, (0, INFO_BAR_HEIGHT - 1), (largura_tela, INFO_BAR_HEIGHT - 1), 1)

            texto_ajuda = fonte.render("Pressione 'S' para BFS ou 'D' para DFS", True, TEXTO_COR)
            texto_ajuda_rect = texto_ajuda.get_rect(center=(largura_tela // 2, INFO_BAR_HEIGHT // 2))
            
            if mostrar_solucao_bfs and caminho_solucao_bfs:
                passos = len(caminho_solucao_bfs) - 1
                tempo_ms = tempo_bfs * 1000
                texto_algo = fonte.render("ALGORITMO: BFS", True, TEXTO_COR)
                texto_stats = fonte.render(f"TEMPO: {tempo_ms:.2f} ms | PASSOS: {passos}", True, TEXTO_COR)
                tela.blit(texto_algo, texto_algo.get_rect(midleft=(15, INFO_BAR_HEIGHT // 2)))
                tela.blit(texto_stats, texto_stats.get_rect(midright=(largura_tela - 15, INFO_BAR_HEIGHT // 2)))
            
            elif mostrar_solucao_dfs and caminho_solucao_dfs:
                passos = len(caminho_solucao_dfs) - 1
                tempo_ms = tempo_dfs * 1000
                texto_algo = fonte.render("ALGORITMO: DFS", True, TEXTO_COR)
                texto_stats = fonte.render(f"TEMPO: {tempo_ms:.2f} ms | PASSOS: {passos}", True, TEXTO_COR)
                tela.blit(texto_algo, texto_algo.get_rect(midleft=(15, INFO_BAR_HEIGHT // 2)))
                tela.blit(texto_stats, texto_stats.get_rect(midright=(largura_tela - 15, INFO_BAR_HEIGHT // 2)))
            else:
                 tela.blit(texto_ajuda, texto_ajuda_rect)

            tela.blit(surface_labirinto, (0, INFO_BAR_HEIGHT))

        if jogador_pos == fim and not fim_de_jogo:
            fim_de_jogo = True 
            if jump_scare_pronto:
                tela.fill(PRETO)
                tela.blit(susto_imagem, (0, 0))
                susto_som.play()
                pygame.display.flip()
                pygame.time.wait(2000)
                rodando = False
            else:
                print("Parabéns, você venceu!")
                pygame.time.wait(1000)
                rodando = False
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
