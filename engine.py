"""
Módulo de engine do labirinto sem dependências do Pygame.
Fornece classes e funções puras para gerar, resolver e manipular o labirinto
em memória (serializável para JSON) usado pelo backend web.
"""
import random
import time
from typing import List, Tuple, Optional


class Celula:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        # paredes: [top, right, bottom, left]
        self.paredes = [True, True, True, True]
        self.visitada = False

    def checar_vizinhos(self, grid: List[List['Celula']]) -> Optional['Celula']:
        cols = len(grid)
        rows = len(grid[0]) if cols else 0
        vizinhos = []
        if self.y > 0 and not grid[self.x][self.y - 1].visitada:
            vizinhos.append(grid[self.x][self.y - 1])
        if self.x < cols - 1 and not grid[self.x + 1][self.y].visitada:
            vizinhos.append(grid[self.x + 1][self.y])
        if self.y < rows - 1 and not grid[self.x][self.y + 1].visitada:
            vizinhos.append(grid[self.x][self.y + 1])
        if self.x > 0 and not grid[self.x - 1][self.y].visitada:
            vizinhos.append(grid[self.x - 1][self.y])
        return random.choice(vizinhos) if vizinhos else None


def remover_paredes(atual: Celula, proxima: Celula):
    dx, dy = atual.x - proxima.x, atual.y - proxima.y
    if dx == 1:
        atual.paredes[3], proxima.paredes[1] = False, False
    elif dx == -1:
        atual.paredes[1], proxima.paredes[3] = False, False
    if dy == 1:
        atual.paredes[0], proxima.paredes[2] = False, False
    elif dy == -1:
        atual.paredes[2], proxima.paredes[0] = False, False


def gerar_labirinto(grid: List[List[Celula]]):
    for row in grid:
        for cell in row:
            cell.visitada = False
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


def criar_loops(grid: List[List[Celula]], numero_de_loops: int):
    cols = len(grid)
    rows = len(grid[0]) if cols else 0
    for _ in range(numero_de_loops):
        x, y = random.randint(0, cols - 2), random.randint(0, rows - 2)
        if random.choice([True, False]):
            remover_paredes(grid[x][y], grid[x+1][y])
        else:
            remover_paredes(grid[x][y], grid[x][y+1])


def resolver_com_bfs(grid: List[List[Celula]], inicio: Celula, fim: Celula):
    fila, visitados = [(inicio, [inicio])], {inicio}
    while fila:
        (atual, caminho) = fila.pop(0)
        if atual == fim:
            return caminho, visitados
        x, y = atual.x, atual.y
        vizinhos_possiveis = []
        if y > 0 and not atual.paredes[0]: vizinhos_possiveis.append(grid[x][y-1])
        if x < len(grid) - 1 and not atual.paredes[1]: vizinhos_possiveis.append(grid[x+1][y])
        if y < len(grid[0]) - 1 and not atual.paredes[2]: vizinhos_possiveis.append(grid[x][y+1])
        if x > 0 and not atual.paredes[3]: vizinhos_possiveis.append(grid[x-1][y])
        for vizinho in vizinhos_possiveis:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    return None, visitados


def resolver_com_dfs(grid: List[List[Celula]], inicio: Celula, fim: Celula):
    pilha, visitados = [(inicio, [inicio])], {inicio}
    while pilha:
        (atual, caminho) = pilha.pop()
        if atual == fim:
            return caminho, visitados
        x, y = atual.x, atual.y
        vizinhos_possiveis = []
        if y > 0 and not atual.paredes[0]: vizinhos_possiveis.append(grid[x][y-1])
        if x < len(grid) - 1 and not atual.paredes[1]: vizinhos_possiveis.append(grid[x+1][y])
        if y < len(grid[0]) - 1 and not atual.paredes[2]: vizinhos_possiveis.append(grid[x][y+1])
        if x > 0 and not atual.paredes[3]: vizinhos_possiveis.append(grid[x-1][y])
        random.shuffle(vizinhos_possiveis)
        for vizinho in vizinhos_possiveis:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append((vizinho, caminho + [vizinho]))
    return None, visitados


class Game:
    def __init__(self, cols: int = 20, rows: int = 15, loops: int = 20):
        self.cols = cols
        self.rows = rows
        self.grid = [[Celula(x, y) for y in range(rows)] for x in range(cols)]
        gerar_labirinto(self.grid)
        criar_loops(self.grid, loops)
        self.jogador = self.grid[0][0]
        self.inicio = self.grid[0][0]
        self.fim = self.grid[cols - 1][rows - 1]
        self.fim_de_jogo = False
        # armazenar soluções calculadas para este labirinto (não regenerar o labirinto ao resolver)
        # cada chave será 'bfs' ou 'dfs' mapeando para o resultado {'path':..., 'visited':..., 'time_ms':...}
        self.solutions = {}

    def to_dict(self):
        # Serializa o estado do jogo para JSON
        grid_serial = []
        for x in range(self.cols):
            col = []
            for y in range(self.rows):
                c = self.grid[x][y]
                col.append({'x': c.x, 'y': c.y, 'paredes': [int(p) for p in c.paredes]})
            grid_serial.append(col)
        return {
            'cols': self.cols,
            'rows': self.rows,
            'jogador': {'x': self.jogador.x, 'y': self.jogador.y},
            'inicio': {'x': self.inicio.x, 'y': self.inicio.y},
            'fim': {'x': self.fim.x, 'y': self.fim.y},
            'fim_de_jogo': self.fim_de_jogo,
            'grid': grid_serial,
            'solutions': self.solutions
        }

    def move(self, direction: str) -> bool:
        x, y = self.jogador.x, self.jogador.y
        moved = False
        if direction == 'up' and not self.jogador.paredes[0]:
            self.jogador = self.grid[x][y - 1]
            moved = True
        elif direction == 'right' and not self.jogador.paredes[1]:
            self.jogador = self.grid[x + 1][y]
            moved = True
        elif direction == 'down' and not self.jogador.paredes[2]:
            self.jogador = self.grid[x][y + 1]
            moved = True
        elif direction == 'left' and not self.jogador.paredes[3]:
            self.jogador = self.grid[x - 1][y]
            moved = True

        if moved and self.jogador == self.fim:
            self.fim_de_jogo = True
        return moved

    def solve(self, algorithm: str = 'bfs'):
        inicio, fim = self.inicio, self.fim
        t0 = time.time()
        if algorithm == 'bfs':
            caminho, visitados = resolver_com_bfs(self.grid, inicio, fim)
        else:
            caminho, visitados = resolver_com_dfs(self.grid, inicio, fim)
        t1 = time.time()
        caminho_coords = [{'x': c.x, 'y': c.y} for c in caminho] if caminho else []
        visitados_coords = [{'x': c.x, 'y': c.y} for c in visitados] if visitados else []
        result = {'path': caminho_coords, 'visited': visitados_coords, 'time_ms': (t1 - t0) * 1000}
        # armazenar a solução para que o frontend possa recuperá-la ao pedir o estado
        self.solutions[algorithm] = result
        return result
