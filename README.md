#  Maze Game - Teoria dos Grafos

> Um jogo de labirinto desenvolvido em Python e Pygame como projeto para a disciplina de Teoria dos Grafos. O objetivo principal é aplicar e visualizar algoritmos de grafos, como DFS e BFS, em um ambiente interativo.

![Prévia do Jogo](https://i.imgur.com/3d3c2c.png)

---

## 🧠 Conceitos Chave Demonstrados

Este projeto serve como uma demonstração prática da aplicação de algoritmos de busca em grafos para resolver problemas do mundo real.

### Geração do Labirinto: Depth-First Search (DFS)
O labirinto é gerado proceduralmente utilizando o algoritmo **DFS**. Ele começa com uma grade sólida e "cava" um caminho, garantindo que todas as células sejam acessíveis. Após a geração de um "labirinto perfeito" (com caminho único), paredes extras são derrubadas aleatoriamente para criar **loops**, tornando o desafio de encontrar o caminho mais curto mais interessante e significativo.

### Resolução de Caminho: Breadth-First Search (BFS) vs. DFS
O jogo permite uma comparação visual e numérica em tempo real entre dois algoritmos de busca:

* **BFS (Busca em Largura):** É o algoritmo ideal para encontrar a solução ótima. Ele explora o labirinto em camadas, garantindo encontrar o **caminho com o menor número de passos**. No jogo, é representado pelo caminho **azul**.
* **DFS (Busca em Profundidade):** Este algoritmo explora um caminho até o fim antes de tentar outro. Ele encontra *um* caminho, mas raramente o mais curto. Frequentemente, seu tempo de execução é menor por "tropeçar" na solução por sorte. No jogo, é representado pelo caminho **laranja**.

---

## ✨ Features

* **Geração Procedural:** Cada labirinto é único a cada execução.
* **Visualização de Algoritmos:** Compare em tempo real a área explorada e o caminho encontrado pelos algoritmos BFS e DFS.
* **Painel de Informações:** Uma interface limpa que exibe o algoritmo ativo, o tempo de execução em milissegundos e o número de passos do caminho encontrado.
* **Tema Escuro:** Uma interface moderna e esteticamente agradável.
* **Player Controlável:** Navegue pelo labirinto com as setas do teclado.
* **Jump Scare:** Uma surpresa aguarda quem conseguir chegar ao final do labirinto!

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Biblioteca Gráfica:** Pygame

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o jogo em sua máquina local.

### Pré-requisitos
* [Python 3](https://www.python.org/downloads/) instalado.
* [Git](https://git-scm.com/downloads/) instalado.

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/ViniVincin/pi-labirinto.git](https://github.com/ViniVincin/pi-labirinto.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd pi-labirinto
    ```

3.  **Instale as dependências (Pygame):**
    ```bash
    pip install pygame
    ```

### Rodando o Jogo

Certifique-se de que os arquivos `susto.jpg` e `grito.wav` estão na mesma pasta do script. Em seguida, execute o comando:

```bash
python labirinto.py
