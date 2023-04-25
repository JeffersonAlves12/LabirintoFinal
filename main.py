import numpy as np
import time
import turtle
import random

def gerar_labirinto(linhas, colunas):
    linhas_internas = linhas - 2
    colunas_internas = colunas - 2
    grid_interno = np.zeros((linhas_internas, colunas_internas), dtype=int)

    def is_valid(linhas, colunas):
        return 0 <= linhas < linhas_internas and 0 <= colunas < colunas_internas

    def pegar_colunas_adjacente(linhas, colunas):
        paredes_adjacentes = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = linhas + dr * 2, colunas + dc * 2
            if is_valid(new_row, new_col) and grid_interno[new_row][new_col] == 0:
                paredes_adjacentes.append(((linhas + dr, colunas + dc), (new_row, new_col)))

        return paredes_adjacentes

    visited_cells = set()
    start_row, start_col = 1, colunas_internas - 2  # One unit diagonal from top right corner
    end_row, end_col = linhas_internas - 2, 1  # One unit diagonal from bottom left corner
    grid_interno[start_row][start_col] = 1
    visited_cells.add((start_row, start_col))
    walls = pegar_colunas_adjacente(start_row, start_col)

    while walls:
        (wall_row, wall_col), (cell_row, cell_col) = random.choice(walls)
        walls.remove(((wall_row, wall_col), (cell_row, cell_col)))

        if (cell_row, cell_col) not in visited_cells:
            grid_interno[wall_row][wall_col] = 1
            grid_interno[cell_row][cell_col] = 1
            visited_cells.add((cell_row, cell_col))
            walls.extend(pegar_colunas_adjacente(cell_row, cell_col))

    grid_interno[end_row][end_col] = 2
    grid_interno[start_row][start_col] = -1

    grid = np.ones((linhas, colunas), dtype=int)
    grid[1:-1, 1:-1] = grid_interno

# Fechamento das bordas superiores e laterais
    grid[0, :] = 0
    grid[-1, :] = 0
    grid[:, 0] = 0
    grid[:, -1] = 0

    return grid


def num_vizinhos_acessiveis(linhas, col, visited):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for dr, dc in directions:
        new_row, new_col = linhas + dr, col + dc
        if new_row >= 0 < grid_rows and 0 <= new_col < colunas_grid and not visitado(new_row, new_col, visited) and \
                grid_inicial[new_row][new_col] != 0:
            count += 1
    return count


def calcular_heuristica(linhas, col, linha_objetivo, coluna_objetivo, visited):
    distancia_manhattan = abs(linhas - linha_objetivo) + abs(col - coluna_objetivo)
    vizinhos_acessiveis = num_vizinhos_acessiveis(linhas, col, visited)

    alpha = 1
    beta = 1

    return alpha * distancia_manhattan + beta * vizinhos_acessiveis


class Node:

    def __init__(self, linha, column, parent, operator, moves, heuristic_cost=0):
        self.row = linha
        self.column = column
        self.parent = parent
        self.operator = operator
        self.moves = moves
        self.heuristic_cost = heuristic_cost
        self.total_cost = moves + heuristic_cost


def criar_no(linha, column, parent, operator, moves, heuristic_cost=0):
    return Node(linha, column, parent, operator, moves, heuristic_cost)


def expandir_no(node, visited):
    expanded_nodes = [
        criar_no(move_up(node.row, node.column, visited), node.column, node,
                    "Up", node.moves + 1),
        criar_no(node.row, move_left(node.row, node.column, visited), node,
                    "Left", node.moves + 1),
        criar_no(node.row, move_right(node.row, node.column, visited), node,
                    "Right", node.moves + 1),
        criar_no(move_down(node.row, node.column, visited), node.column, node,
                    "Down", node.moves + 1)
    ]
    expanded_nodes = [
        node for node in expanded_nodes
        if node.row is not None and node.column is not None
    ]
    return expanded_nodes


def visitado(linha, column, visited):
    for i in visited:  # checking if node is already visited or not
        if i.row == linha and i.column == column:
            return True
    return False


def move_left(linha, column, visited):
    if column != 0 and grid_inicial[linha][column - 1] in [
        1, 2
    ] and not visitado(linha, column - 1, visited):
        return column - 1
    return None


def move_right(linha, column, visited):
    if column != colunas_grid - 1 and grid_inicial[linha][column + 1] in [1, 2] \
            and not visitado(linha, column + 1, visited):
        return column + 1
    return None


def move_up(linha, column, visited):
    if linha != 0 and grid_inicial[linha - 1][column] in [
        1, 2
    ] and not visitado(linha - 1, column, visited):
        return linha - 1
    return None


def move_down(linha, column, visited):
    if linha != grid_rows - 1 and grid_inicial[linha + 1][column] in [
        1, 2
    ] and not visitado(linha + 1, column, visited):
        return linha + 1
    return None


def busca_profundidade(linha_inicio, coluna_incial, linha_objetivo, coluna_objetivo):
    startNode = criar_no(linha_inicio, coluna_incial, None, None, 0)
    nodes = [startNode]
    visitado = []
    custo = 0

    turtle.tracer(0, 0)
    desenhar_labirinto(grid_inicial)

    while nodes:
        node = nodes.pop(0)
        if node.row == linha_objetivo and node.column == coluna_objetivo:
            turtle.done()
            return custo, node
        visitado.append(node)
        desenhar_agente(node)
        time.sleep(0.1)  # Tempo de Movimentação do Agente
        turtle.update()
        expanded_nodes = expandir_no(node, visitado)
        custo += len(expanded_nodes)
        expanded_nodes.extend(nodes)
        nodes = expanded_nodes

    turtle.done()
    return -1, None


def busca_gulosa(linha_inicio, coluna_incial, linha_objetivo, coluna_objetivo):
    nodes = [criar_no(linha_inicio, coluna_incial, None, None, 0)]
    visitado = []
    custo = 0

    turtle.tracer(0, 0)
    desenhar_labirinto(grid_inicial)

    while nodes:
        node = min(nodes, key=lambda n: calcular_heuristica(n.row, n.column, linha_objetivo, coluna_objetivo, visitado))
        nodes.remove(node)
        visitado.append(node)
        desenhar_agente(node)
        time.sleep(0.1)  # Tempo de Movimentação do Agente
        turtle.update()
        if node.row == linha_objetivo and node.column == coluna_objetivo:
            turtle.done()
            return custo, node
        custo += len(expandir_no(node, visitado))
        nodes.extend(expandir_no(node, visitado))

    turtle.done()
    return -1, None



def desenhar_labirinto(grid):
    turtle.clear()
    turtle.speed(0)
    turtle.penup()
    start_x, start_y = -colunas_grid * 20 / 2, grid_rows * 20 / 2
    turtle.goto(start_x, start_y)

    for linha in range(grid_rows):
        for col in range(colunas_grid):
            x = start_x + col * 20
            y = start_y - linha * 20
            if grid[linha][col] == 0:
                draw_square(x, y, 20)
            elif grid[linha][col] == -1:  # Definindo O Inicio do Labirinto
                turtle.color("green")
                draw_square(x, y, 20)
                turtle.color("black")
            elif grid[linha][col] == 2:  # Definindo o Fim do Labirinto
                turtle.color("red")
                draw_square(x, y, 20)
                turtle.color("black")

    turtle.update()


def draw_square(x, y, size):
    turtle.penup()
    turtle.goto(x, y)

    turtle.pendown()
    turtle.begin_fill()

    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)

    turtle.end_fill()
    turtle.penup()


def desenhar_agente(node):
    x_offset = - colunas_grid * 20 / 2
    y_offset = grid_rows * 20 / 2
    x_position = x_offset + node.column * 20 + 10
    y_position = y_offset - node.row * 20 - 10

    turtle.goto(x_position, y_position)
    turtle.color("red")
    turtle.dot(10)
    turtle.color("black")


def main():
    # Inicializando o inicio e o fim do labirinto
    linha_inicio, coluna_incial = np.where(grid_inicial == -1)  # Posição Inicial do Labirinto
    linha_inicio, coluna_incial = int(linha_inicio), int(coluna_incial)
    linha_objetivo, coluna_objetivo = np.where(grid_inicial == 2)   # Posição Final do Labirinto
    linha_objetivo, coluna_objetivo = int(linha_objetivo), int(coluna_objetivo)

    print("\nEscolha um algoritmo de busca:")
    print("1. Busca em Profundidade")
    print("2. Busca Gulosa")
    print("3. Sair")
    op = int(input("Digite uma opção: "))

    if op == 1:
        cost1, result1 = busca_profundidade(linha_inicio, coluna_incial, linha_objetivo, coluna_objetivo)
        if result1 is None:
            print("Nenhuma solução encontrada")
        else:
            print(
                'Algoritmo usado = "DFS"\nMenor quantidade de passos para solução = {}'
                '\nQuantidade de passos do agente = {}'.format(
                    result1.moves, cost1))
    elif op == 2:
        cost2, result2 = busca_gulosa(linha_inicio, coluna_incial, linha_objetivo, coluna_objetivo)
        if result2 is None:
            print("Nenhuma solução encontrada")
        else:
            print(
                'Algoritmo usado = "Busca Gulosa"\nMenor quantidade de passos para resolução = {}\n'
                'No de etapas de busca = {}'.format(
                    result2.moves, cost2))

if __name__ == "__main__":
    print("Bem Vindo ao Labirinto")
    linhas = int(input("Digite o número de linhas: "))
    colunas = int(input("Digite o número de colunas: "))

    while linhas < 4 or colunas < 4:
        print("O número de linhas e colunas deve ser maior ou igual a 4.")
        linhas = int(input("Digite o número de linhas: "))
        colunas = int(input("Digite o número de colunas: "))

    grid_inicial = gerar_labirinto(linhas, colunas)
    grid_rows, colunas_grid = grid_inicial.shape
    main()
