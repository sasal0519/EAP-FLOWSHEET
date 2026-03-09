# 📊 Gerador Interativo de EAP (Estrutura Analítica de Projeto)

Um aplicativo educacional desenvolvido em Python e Tkinter para o estudo prático de algoritmos de renderização visual e estruturas de dados em formato de árvore (Tree Data Structures).

## 🎯 Objetivo Educacional

Este projeto foi criado com o intuito de compreender os fundamentos por trás da construção de um fluxograma e organogramas, focando em:
* **Estruturas de Árvore (Trees):** Como armazenar relacionamentos de "Pai e Filho" (Nós) em um dicionário.
* **Algoritmos de Posicionamento:** Como calcular coordenadas (X, Y) dinamicamente para que os blocos de hierarquias diferentes não se sobreponham.
* **Renderização Dinâmica:** Como medir a largura de textos em tempo de execução para adaptar os retângulos de forma fluida.
* **Numeração WBS:** Lógica recursiva para gerar códigos como `1`, `1.1`, `1.1.1` automaticamente.

## ✨ Funcionalidades

* **Criação Interativa:** Adicione sub-tarefas e tarefas do mesmo nível com apenas um clique.
* **Ajuste Dinâmico:** Os blocos se adaptam automaticamente ao tamanho do texto inserido.
* **Centralização Automática:** A raiz do projeto está sempre no centro da tela.
* **Numeração Automática:** A numeração da Estrutura Analítica de Projeto (WBS) é gerada e atualizada dinamicamente.

Exemplo 1
<img width="1433" height="828" alt="Exemplo 1" src="https://github.com/user-attachments/assets/4be347d9-d6cd-4f7e-bff6-53aa6173588f" />

## 🛠️ Como a Estrutura do Fluxograma Funciona?

O projeto utiliza uma abordagem **Top-Down** para calcular as hierarquias e **Bottom-Up** para garantir o espaçamento:
1.  **Mapeamento das Folhas:** O programa identifica as "folhas" (nós sem filhos) e reserva um espaço horizontal X para cada uma delas.
2.  **Cálculo dos Pais:** A posição X de um nó pai é sempre a média matemática das posições de seus filhos, garantindo que ele fique perfeitamente centralizado acima deles.
3.  **Desenho Ortogonal:** As conexões são desenhadas com quebras de 90 graus para criar a leitura visual clássica de organogramas.

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.x instalado.
* (A biblioteca `tkinter` já é nativa na maioria das instalações do Python).

### Passos
1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
