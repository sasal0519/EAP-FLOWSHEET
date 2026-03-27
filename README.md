
📊 Gerador Interativo de EAP (Estrutura Analítica de Projeto)
Um aplicativo educacional desenvolvido em Python e PyQt5 para o estudo prático de algoritmos de renderização visual e estruturas de dados em formato de árvore (Tree Data Structures).

🎯 Objetivo Educacional
Este projeto foi criado com o intuito de compreender os fundamentos por trás da construção de fluxogramas e organogramas, focando em:

Estruturas de Árvore (Trees): Como armazenar relacionamentos de "Pai e Filho" (Nós) em um dicionário.

Algoritmos de Posicionamento: Como calcular coordenadas (X, Y) dinamicamente para que os blocos de hierarquias diferentes não se sobreponham.

Renderização Gráfica Avançada: Utilização da arquitetura QGraphicsScene e QGraphicsView do PyQt5 para gerenciar elementos visuais, eventos de clique e escala (zoom).

Numeração WBS: Lógica recursiva para gerar códigos da Estrutura Analítica de Projeto como 1, 1.1, 1.1.1 automaticamente.

✨ Funcionalidades
Criação Interativa: Adicione sub-tarefas e tarefas do mesmo nível com apenas um clique nos botões flutuantes dos nós.

Navegação e Zoom: Amplie ou afaste a visualização usando os controles da barra de ferramentas (🔍+, 🔍-, ⟳ 100%) ou segurando Ctrl + Scroll do mouse.

Edição Fluida: Renomeie blocos facilmente com um duplo clique (ou clicando no nó), que abre um editor de texto perfeitamente alinhado.

Exclusão Segura: Remova nós e todas as suas sub-tarefas com um clique, protegido por um aviso de confirmação para evitar perdas acidentais.

Ajuste Dinâmico: Os blocos se adaptam automaticamente à largura do texto ou da numeração WBS inserida.

Interface Moderna (Dark Mode): Paleta de cores escuras cuidadosamente escolhida para reduzir o cansaço visual, com destaques em bordas e botões para facilitar a interação.

Exemplo 1
<img width="1433" height="828" alt="Exemplo 1" src="https://github.com/user-attachments/assets/4be347d9-d6cd-4f7e-bff6-53aa6173588f" />
Versão 2 (PyQt5)
<img width="1920" height="1042" alt="2026-03-27_08-50-45" src="https://github.com/user-attachments/assets/b0076182-2b3b-4909-a97f-8c8a3706d40f" />

🛠️ Como a Estrutura do Fluxograma Funciona?
O projeto utiliza uma abordagem Top-Down para calcular as hierarquias e Bottom-Up para garantir o espaçamento correto no canvas:

Mapeamento das Folhas: O programa identifica as "folhas" (nós sem filhos) e reserva um espaço horizontal X para cada uma delas no nível mais baixo.

Cálculo dos Pais: A posição X de um nó pai é calculada pela média matemática das posições X de seus filhos diretos. Isso garante que o pai fique perfeitamente centralizado acima da sua ramificação.

Desenho Ortogonal: As conexões (linhas) são desenhadas calculando pontos intermediários e fazendo quebras de 90 graus, criando a leitura visual clássica e limpa de organogramas profissionais.

🚀 Como Executar o Projeto
Pré-requisitos
Python 3.x instalado.

Biblioteca PyQt5.

Passos
Clone este repositório:

Bash
git clone https://github.com/sarududu/NOME-DO-REPOSITORIO.git
Navegue até o diretório do projeto:

Bash
cd NOME-DO-REPOSITORIO
Instale as dependências necessárias (recomenda-se o uso de um ambiente virtual):

Bash
pip install PyQt5
Execute o arquivo principal do aplicativo:

Bash
python eap_flowsheet.py
