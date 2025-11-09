# 🧩 RunLab - Teoria dos Grafos | Versão Web (Flask)

> Visualização interativa dos algoritmos de busca **BFS** e **DFS** aplicados em um labirinto gerado proceduralmente.  
> Projeto desenvolvido para a disciplina de **Teoria dos Grafos**.

<img width="480" alt="preview" src="https://github.com/user-attachments/assets/82b0b2a1-4807-4f84-8e09-1ab2ab89d1c7" />

---

## 🧠 Conceitos Demonstrados

Este projeto utiliza a representação de labirintos como **grafos**, onde cada célula é um **nó** conectado a seus vizinhos.

| Algoritmo | Funcionamento | Resultado na Visualização | Uso no Projeto |
|----------|----------------|--------------------------|----------------|
| **DFS (Depth-First Search)** | Explora profundamente um caminho antes de retornar | *Laranja* | Usado para **gerar o labirinto** |
| **BFS (Breadth-First Search)** | Explora em camadas até encontrar o destino | *Azul* | Usado para encontrar o **caminho mais curto** |

O labirinto é primeiro gerado como um **labirinto perfeito** via DFS e, em seguida, passa por suavização para criar caminhos alternativos, tornando a solução menos trivial.

---

## 🛠️ Tecnologias Utilizadas

- Python 3
- Flask (API e servidor)
- HTML + CSS + JavaScript (Canvas para renderização)

---

## 📁 Estrutura de Pastas

Uma visão rápida da organização do projeto:

```bash
.
├── server/ # Backend (Flask) + motor do labirinto/algoritmos
│ ├── app.py # Ponto de entrada do servidor Web
│ ├── engine/ # Lógica de geração e busca no labirinto
│ └── ...
├── templates/ # Páginas HTML servidas pelo Flask
│ └── index.html # Interface principal da versão Web
├── static/ # Arquivos estáticos (JS, CSS, imagens, mídia)
│ ├── js/
│ ├── css/
│ └── media/ # Coloque aqui imagens, sons, etc.
├── desktop/ # Versão Pygame (modo Desktop)
│ ├── labirinto.py
│ └── resources/ # Sons, imagens, eventuais assets
├── Dockerfile # Build da imagem Docker
├── docker-compose.yml # Execução da aplicação com Docker
└── .gitignore # Regras para ignorar arquivos locais
```

---

## 🚀 Execução Recomendada (via Docker)

> Este é o método **principal e mais simples** para rodar o projeto.  
> Não precisa instalar Python, dependências ou configurar ambiente.

### 1. Clone o repositório

```bash
git clone https://github.com/ViniVincin/pi-labirinto.git
cd pi-labirinto
```
### 2. Execute o projeto com Docker Compose
```bash
sudo docker compose up --build -d
```

### 3. Acesse no navegador:
```bash
http://localhost:5000
```

### ✅ Pronto! A aplicação estará rodando na sua máquina.

### 4. Para parar o servidor
```bash
sudo docker compose down
```

## 🟠 Alternativa (Somente se não puder usar Docker)
Use apenas se estiver sem suporte ao Docker ou se desejar rodar o código diretamente.

### 1. Crie um ambiente Python (opcional, recomendado)
```bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o servidor Flask

```bash
python app.py
```

### 4. Acesse:

```bash
http://localhost:5000
```

## 🎮 Funcionalidades da Interface Web
- Visualização interativa do labirinto
- Botões para executar BFS e DFS
- Comparação visual entre caminhos
- Indicação clara da solução otimizada vs solução exploratória

---

📄 Licença
Projeto desenvolvido com foco educacional e demonstrativo para fins acadêmicos.
