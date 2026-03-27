<h1 align="center">
  <br>
  ⚙️ Flowsheet & EAP 
  <br>
</h1>

<h4 align="center">Uma ferramenta desktop unificada (All-in-One) para desenhar Diagramas de Fluxo de Processos (PFD) e Estruturas Analíticas de Projeto (EAP) com renderização 100% vetorial.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/PyQt5-GUI-green.svg?style=flat-square" alt="PyQt5">
  <img src="https://img.shields.io/badge/Engineering-Chemical-orange.svg?style=flat-square" alt="Chemical Engineering">
  <img src="https://img.shields.io/badge/Management-WBS-purple.svg?style=flat-square" alt="Project Management">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License MIT">
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-módulos-e-funcionalidades">Funcionalidades</a> •
  <a href="#-biblioteca-de-equipamentos-pfd">Equipamentos</a> •
  <a href="#-como-instalar-e-usar">Instalação e Uso</a> •
  <a href="#-arquitetura-vetorial">Arquitetura</a> •
  <a href="#-contribuir">Contribuir</a>
</p>

<img width="1920" height="1080" alt="Tela inicial" src="https://github.com/user-attachments/assets/b92a0a96-4d33-473f-b7bb-0a5e1c5daa24" />


<img width="1920" height="1080" alt="EAP" src="https://github.com/user-attachments/assets/f159c1f7-40d8-4dbf-ba84-1d12dd32df87" />

<img width="1920" height="1080" alt="FLOWSHEET" src="https://github.com/user-attachments/assets/f159c1f7-40d8-4dbf-ba84-1d12dd32df87" />


---

## 📖 Sobre o Projeto

O **Flowsheet & EAP * é uma suíte de software desenvolvida para unir duas áreas fundamentais da Engenharia: a conceção de processos (Chemical Engineering) e a gestão de projetos (Project Management). 

O grande diferencial tecnológico deste projeto é a sua **renderização matemática**. A aplicação **não utiliza ficheiros de imagem externos (PNG, JPG)**. Todos os 26 equipamentos industriais e as hierarquias de projeto são desenhados através de cálculos vetoriais em tempo real, garantindo um executável ultraleve e um *zoom* infinito sem qualquer perda de qualidade visual.

---

## ✨ Módulos e Funcionalidades

A aplicação está dividida em dois motores gráficos independentes acessíveis por separadores (Tabs):

### 📊 Módulo 1: EAP (Estrutura Analítica de Projeto)
* 🖱️ **Criação 1-Click:** Adiciona subtarefas e tarefas paralelas através de botões flutuantes integrados em cada nó.
* 🔢 **WBS Nativo:** Cálculo e propagação automática de numeração hierárquica (ex: 1, 1.1, 1.1.2) em tempo real.
* 📐 **Auto-Posicionamento:** Algoritmo *Top-Down / Bottom-Up* que centraliza nós pais com base na média espacial dos filhos diretos, evitando sobreposições.
* ✏️ **Edição In-line:** Caixas de texto flutuantes e responsivas que redimensionam a árvore inteira consoante o tamanho da palavra digitada.

### 🏭 Módulo 2: Flowsheet (Diagrama de Fluxo de Processos)
* 🏗️ **Drag & Drop Retrátil:** Paleta lateral com 26 símbolos normalizados que pode ser recolhida (botão `☰ Equipamentos`) para maximizar o Canvas.
* 🔀 **Tubagem Ortogonal (Manhattan Routing):** Desenha ligações entre equipamentos com quebras estritas de 90 graus, mantendo o aspeto técnico.
* 🧲 **Portas Magnéticas:** O algoritmo deteta automaticamente o porto cardeal ideal (Topo, Base, Esquerda, Direita) para ancorar a tubagem.
* ⚙️ **Menu de Contexto Intuitivo:** Clica com o `Botão Direito` sobre qualquer máquina ou tubo para redimensionar ou apagar sem necessidade de barras de ferramentas confusas.

---

## 🔧 Biblioteca de Equipamentos 

A grelha de ícones gera matematicamente 26 símbolos essenciais da indústria química:

| Movimentação de Fluidos | Transferência de Calor | Separação & Operações | Reatores & Armazenamento |
| :--- | :--- | :--- | :--- |
| 🔹 Bomba Centrífuga<br>🔹 Compressor<br>🔹 Soprador<br>🔹 Turbina<br>🔹 Ejetor<br>🔹 Válvula | 🔹 Trocador de Calor<br>🔹 Permutador a Ar<br>🔹 Fornalha<br>🔹 Caldeira<br>🔹 Torre de Resfriamento | 🔹 Torre de Destilação<br>🔹 Coluna de Absorção<br>🔹 Separador Bifásico<br>🔹 Ciclone<br>🔹 Evaporador<br>🔹 Filtro / Filtro Prensa<br>🔹 Secador<br>🔹 Peneira | 🔹 Reator<br>🔹 Misturador<br>🔹 Moinho<br>🔹 Vaso<br>🔹 Tanque<br>🔹 Flare (Chaminé) |

---

## 🚀 Como Instalar e Usar

Para clonar e correr esta aplicação vais precisar do [Git](https://git-scm.com) e do [Python](https://www.python.org/downloads/) instalados no teu computador.

No teu terminal (linha de comandos):

```bash
# Clona este repositório
$ git clone [https://github.com/TEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/TEU-USUARIO/NOME-DO-REPOSITORIO.git)

# Acede à pasta do projeto
$ cd NOME-DO-REPOSITORIO

# Instala as dependências necessárias (PyQt5)
$ pip install PyQt5

# Executa a aplicação integrada
$ python main_app.py
