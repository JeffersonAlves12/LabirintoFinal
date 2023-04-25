# Labirinto

## Descrição

O programa consiste em um labirinto de tamanho N x M, onde N e M são números inteiros positivos. O labirinto é representado por uma matriz de nós, onde cada nó representa um tipo de terreno (parede ou caminho). O programa deve encontrar o caminho mais curto entre a posição inicial e a posição final do labirinto.

## Como executar

### Windows
```ps
python -m venv venv
```

```ps
venv\Scripts\activate
```
    
```ps
pip install -r requirements.txt
```

```ps
python main.py
```

### Linux
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```
    
```bash
pip install -r requirements.txt
```

```bash
python3 main.py
```

---

Ao executar o script será solicitado o número de linhas e colunas do labirinto, em seguida será exibido um menu de escolha entre o algoritmo de busca em profundidade e o algoritmo de busca gulosa.
