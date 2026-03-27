<h1 align="center">📊 EAP

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/PyQt5-GUI-green.svg" alt="PyQt5">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  Um aplicativo educacional desenvolvido em Python e <b>PyQt5</b> para o estudo prático de algoritmos de renderização visual e estruturas de dados em formato de árvore (Tree Data Structures).
</p>

## 📖 Índice
- [Objetivo Educacional](#-objetivo-educacional)
- [Funcionalidades](#-funcionalidades)
- [Demonstração](#-demonstração)
- [Como a Estrutura Funciona?](#-como-a-estrutura-funciona)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Uso](#-instalação-e-uso)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Objetivo Educacional

Este projeto foi criado com o intuito de compreender os fundamentos por trás da construção de fluxogramas e organogramas, focando em:
* **Estruturas de Árvore (Trees):** Como armazenar relacionamentos de "Pai e Filho" (Nós) em um dicionário.
* **Algoritmos de Posicionamento:** Como calcular coordenadas (X, Y) dinamicamente para que os blocos de hierarquias diferentes não se sobreponham.
* **Renderização Gráfica Avançada:** Utilização da arquitetura `QGraphicsScene` e `QGraphicsView` do PyQt5 para gerenciar elementos visuais, eventos de clique e escala (zoom).
* **Numeração WBS:** Lógica recursiva para gerar códigos da Estrutura Analítica de Projeto como `1`, `1.1`, `1.1.1` automaticamente.

## ✨ Funcionalidades

* **Criação Interativa:** Adicione sub-tarefas e tarefas do mesmo nível com apenas um clique nos botões flutuantes dos nós.
* **Navegação e Zoom:** Amplie ou afaste a visualização usando os controles da barra de ferramentas (🔍+, 🔍-, ⟳ 100%) ou segurando `Ctrl + Scroll` do mouse.
* **Edição Fluida:** Renomeie blocos facilmente com um duplo clique (ou clicando no nó), que abre um editor de texto perfeitamente alinhado.
* **Exclusão Segura:** Remova nós e todas as suas sub-tarefas com um clique, protegido por um aviso de confirmação para evitar perdas acidentais.
* **Ajuste Dinâmico:** Os blocos se adaptam automaticamente à largura do texto ou da numeração WBS inserida.
* **Interface Moderna:** Paleta de cores *Dark Mode* cuidadosamente escolhida para reduzir o cansaço visual, com destaques em bordas e botões para facilitar a interação.

## 📸 Demonstração

**Exemplo 1 (Estrutura Básica)** <img width="1433" height="828" alt="Exemplo 1" src="https://github.com/user-attachments/assets/4be347d9-d6cd-4f7e-bff6-53aa6173588f" />

**Versão 2 (Nova Interface PyQt5)** <img width="1920" height="1042" alt="Demonstração PyQt5" src="https://github.com/user-attachments/assets/b0076182-2b3b-4909-a97f-8c8a3706d40f" />

**Versão 3 (Interface PyQt5 melhorada novas figuras)**  
<img width="1920" height="1080" alt="Novas figuras PyQt5"
src="https://github.com/user-attachments/assets/986c2304-a119-46a1-8c29-b5c56772f32b" />


## 🛠️ Como a Estrutura Funciona?

O projeto utiliza uma abordagem **Top-Down** para calcular as hierarquias e **Bottom-Up** para garantir o espaçamento correto no *canvas*:
1. **Mapeamento das Folhas:** O programa identifica as "folhas" (nós sem filhos) e reserva um espaço horizontal (eixo X) para cada uma delas no nível mais baixo.
2. **Cálculo dos Pais:** A posição X de um nó pai é calculada pela média matemática das posições X de seus filhos diretos. Isso garante que o pai fique perfeitamente centralizado acima da sua ramificação.
3. **Desenho Ortogonal:** As conexões (linhas) são desenhadas calculando pontos intermediários e fazendo quebras de 90 graus, criando a leitura visual clássica e limpa de organogramas profissionais.

## 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica:** PyQt5

## 📁 Estrutura do Projeto


  🏭 Flowsheet 
<h4 align="center">Uma ferramenta desktop open-source para desenhar Diagramas de Fluxo de Processos (PFD) com renderização 100% vetorial.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/PyQt5-GUI-green.svg?style=flat-square" alt="PyQt5">
  <img src="https://img.shields.io/badge/Engineering-Chemical-orange.svg?style=flat-square" alt="Chemical Engineering">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License MIT">
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-biblioteca-de-equipamentos">Equipamentos</a> •
  <a href="#-como-instalar-e-usar">Instalação e Uso</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-contribuir">Contribuir</a>
</p>

<img width="1920" height="1080" alt="2026-03-27_12-22-12" src="https://github.com/user-attachments/assets/c3235a82-b268-4b38-bfde-112e261bc80f" />

---

## 📖 Sobre o Projeto

O **PFD Flowsheet Maker Pro** é um simulador visual e criador de diagramas desenvolvido para a Engenharia Química e de Processos. Diferente de outras ferramentas, este software **não utiliza ficheiros de imagem externos (PNG, JPG)**. Cada equipamento é renderizado através de cálculos matemáticos puros (vetores) em tempo real, garantindo um executável ultraleve e um *zoom* infinito sem qualquer perda de resolução.

## ✨ Funcionalidades

* 🖱️ **Drag & Drop (Arrastar e Largar):** Paleta lateral de equipamentos em formato de grelha, totalmente retrátil para maximizar a área de trabalho.
* 🔀 **Tubagem Ortogonal (Manhattan Routing):** O algoritmo de roteamento desenha tubos com quebras estritas de 90 graus, mantendo o aspeto técnico e organizado.
* 🧲 **Conectores Magnéticos:** As tubagens calculam automaticamente as portas cardeais (Topo, Base, Esquerda, Direita) mais próximas de cada equipamento.
* 🔍 **Navegação de Alta Performance:** Zoom com a roda do rato (`Ctrl + Scroll`) ou através da barra de ferramentas, mantendo a nitidez vetorial.
* ⚙️ **Menu de Contexto Interativo:** Clica com o botão direito do rato sobre qualquer equipamento ou tubagem para redimensionar dinamicamente ou eliminar o elemento.
* 🌙 **UI Industrial (Dark Mode):** Interface desenhada para reduzir o cansaço visual, com alto contraste para as linhas de processo.

## 🏭 Biblioteca de Equipamentos

O software inclui **26 símbolos normalizados** organizados na paleta:

| Transferência de Calor | Movimentação de Fluidos | Separação & Operações | Reatores & Armazenamento |
| :--- | :--- | :--- | :--- |
| 🔹 Trocador de Calor<br>🔹 Permutador a Ar<br>🔹 Fornalha<br>🔹 Caldeira<br>🔹 Torre de Resfriamento | 🔹 Bomba Centrífuga<br>🔹 Compressor<br>🔹 Soprador<br>🔹 Turbina<br>🔹 Ejetor<br>🔹 Válvula | 🔹 Torre de Destilação<br>🔹 Coluna de Absorção<br>🔹 Separador Bifásico<br>🔹 Ciclone<br>🔹 Evaporador<br>🔹 Filtro / Filtro Prensa<br>🔹 Secador<br>🔹 Peneira | 🔹 Reator<br>🔹 Misturador<br>🔹 Moinho<br>🔹 Vaso<br>🔹 Tanque<br>🔹 Flare (Chaminé) |

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

# Executa a aplicação
$ python pfd_flowsheet.py
