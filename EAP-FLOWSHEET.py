import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import tkinter.font as tkfont

class EAPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de EAP Visual - Interativo com Zoom")
        self.root.geometry("1600x900")
        
        self.root.withdraw()
        
        nome_projeto = simpledialog.askstring(
            "Bem-vindo", 
            "Digite o nome do Projeto :", 
            parent=self.root
        )
        
        if not nome_projeto or not nome_projeto.strip():
            nome_projeto = "Projeto"
            
        self.root.deiconify()
        
        # --- Configurações Base de Layout (Inalteráveis para referência do Zoom) ---
        self.base_pad_x = 40 
        self.base_pad_y = 70 
        self.base_min_width = 120 
        self.base_box_height = 60 
        
        # Variável de controle do Zoom (1.0 = 100%)
        self.zoom = 1.0 
        
        # Fonte base (será alterada dinamicamente pelo zoom)
        self.node_font = tkfont.Font(family='Arial', size=10, weight='bold')
        
        self.next_id = 2
        self.nodes = {
            1: {"text": nome_projeto.strip(), "children": [], "parent": None}
        }
        self.wbs_numbers = {} 
        self.node_dimensions = {} 
        
        self.setup_canvas()
        self.update_zoom(1.0) # Aplica o zoom inicial para calcular dimensões
        self.root.update() 
        self.draw_eap()

    def setup_canvas(self):
        frame_canvas = ttk.Frame(self.root)
        frame_canvas.pack(fill=tk.BOTH, expand=True)

        scroll_y = tk.Scrollbar(frame_canvas, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = tk.Scrollbar(frame_canvas, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(frame_canvas, bg="#f8f9fa", 
                                yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.canvas.yview)
        scroll_x.config(command=self.canvas.xview)

        # --- Binds de Teclado/Mouse para Zoom (Ctrl + Mouse Wheel) ---
        self.canvas.bind("<Control-MouseWheel>", self.on_mousewheel) # Windows/Mac
        self.canvas.bind("<Control-Button-4>", self.on_mousewheel)   # Linux Scroll Up
        self.canvas.bind("<Control-Button-5>", self.on_mousewheel)   # Linux Scroll Down

        # --- Botões Flutuantes de Zoom na Tela ---
        frame_zoom = tk.Frame(self.canvas, bg="#f8f9fa")
        self.canvas.create_window(10, 10, anchor="nw", window=frame_zoom) # Posiciona no canto superior esquerdo
        
        ttk.Button(frame_zoom, text="🔍 Zoom Out (-)", command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_zoom, text="🔍 Zoom In (+)", command=self.zoom_in).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_zoom, text="Resetar 100%", command=lambda: self.update_zoom(1.0)).pack(side=tk.LEFT, padx=2)

    # --- Funções de Zoom ---
    def zoom_in(self):
        self.update_zoom(self.zoom * 1.15) # Aumenta 15%

    def zoom_out(self):
        self.update_zoom(self.zoom / 1.15) # Diminui 15%

    def on_mousewheel(self, event):
        # Captura rodinha do mouse + Control
        if event.num == 5 or event.delta < 0:
            self.zoom_out()
        elif event.num == 4 or event.delta > 0:
            self.zoom_in()

    def update_zoom(self, novo_zoom):
        # Limita o zoom entre 30% e 300% para não quebrar a tela
        self.zoom = max(0.3, min(novo_zoom, 3.0))
        
        # Recalcula as variáveis de geometria aplicando o fator
        self.pad_x = self.base_pad_x * self.zoom
        self.pad_y = self.base_pad_y * self.zoom
        self.min_width = self.base_min_width * self.zoom
        self.box_height = self.base_box_height * self.zoom
        
        # Atualiza a fonte base (com limite mínimo para o texto não sumir)
        tamanho_fonte = max(5, int(10 * self.zoom))
        self.node_font.configure(size=tamanho_fonte)
        
        # Redesenha a árvore com os novos tamanhos
        self.draw_eap()

    # --- Funções de Interação (Sem alterações pesadas) ---
    def add_child(self, parent_id):
        nome = simpledialog.askstring("Nova Tarefa", "Digite o nome da Sub-tarefa (Filho):", parent=self.root)
        if nome and nome.strip():
            new_id = self.next_id
            self.next_id += 1
            self.nodes[new_id] = {"text": nome.strip(), "children": [], "parent": parent_id}
            self.nodes[parent_id]["children"].append(new_id)
            self.draw_eap()

    def add_sibling(self, node_id):
        parent_id = self.nodes[node_id]["parent"]
        if parent_id is None: return 

        nome = simpledialog.askstring("Nova Tarefa", "Digite o nome da Tarefa (Mesmo nível):", parent=self.root)
        if nome and nome.strip():
            new_id = self.next_id
            self.next_id += 1
            self.nodes[new_id] = {"text": nome.strip(), "children": [], "parent": parent_id}
            self.nodes[parent_id]["children"].append(new_id)
            self.draw_eap()

    def delete_node(self, node_id):
        if messagebox.askyesno("Excluir", f"Tem certeza que deseja excluir '{self.nodes[node_id]['text']}' e todas as suas sub-tarefas?"):
            parent_id = self.nodes[node_id]["parent"]
            if parent_id is not None:
                self.nodes[parent_id]["children"].remove(node_id)
            self._remove_recursively(node_id)
            self.draw_eap()

    def _remove_recursively(self, node_id):
        for child_id in self.nodes[node_id]["children"]:
            self._remove_recursively(child_id)
        del self.nodes[node_id]

    def calculate_wbs(self, node_id, current_wbs):
        self.wbs_numbers[node_id] = current_wbs
        for i, child_id in enumerate(self.nodes[node_id]["children"]):
            self.calculate_wbs(child_id, f"{current_wbs}.{i+1}")

    # --- Lógica de Medição e Desenho (Adaptada ao Zoom) ---
    def pre_calcular_dimensoes(self):
        self.node_dimensions.clear()
        for node_id, data in self.nodes.items():
            texto = data["text"]
            numero_wbs = self.wbs_numbers.get(node_id, "")
            
            largura_wbs = self.node_font.measure(numero_wbs)
            largura_texto = self.node_font.measure(texto)
            max_largura = max(largura_wbs, largura_texto)
            
            # Espaçamento interno (padding text) também aumenta com o zoom
            padding_interno = 30 * self.zoom
            largura_final = max(self.min_width, max_largura + padding_interno)
            self.node_dimensions[node_id] = (largura_final, self.box_height)

    def draw_eap(self):
        self.canvas.delete("all")
        if not hasattr(self, 'nodes') or not self.nodes: return # Previne erros na inicialização
        
        self.node_positions = {}
        self.wbs_numbers = {}
        
        self.calculate_wbs(1, "1")
        self.pre_calcular_dimensoes()
        
        self.current_leaf_x = 80 * self.zoom 
        self.calcular_posicoes(1, nivel=0)
        
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 100: canvas_width = 800 
            
        root_x = self.node_positions[1][0]
        offset_x = (canvas_width / 2) - root_x
        
        min_x = min(pos[0] - (self.node_dimensions[nid][0]/2) for nid, pos in self.node_positions.items())
        if min_x + offset_x < (80 * self.zoom):
            offset_x = (80 * self.zoom) - min_x 
            
        for node_id in self.node_positions:
            x, y = self.node_positions[node_id]
            self.node_positions[node_id] = (x + offset_x, y)
        
        self.desenhar_conexoes(1)
        self.desenhar_nos()
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def calcular_posicoes(self, node_id, nivel):
        filhos = self.nodes[node_id]["children"]
        node_width, node_height = self.node_dimensions[node_id]
        
        y = (80 * self.zoom) + nivel * (node_height + self.pad_y)

        if not filhos:
            x = self.current_leaf_x + (node_width / 2)
            self.current_leaf_x += node_width + self.pad_x
        else:
            xs_filhos = [self.calcular_posicoes(filho, nivel + 1) for filho in filhos]
            x = sum(xs_filhos) / len(xs_filhos)

        self.node_positions[node_id] = (x, y)
        return x

    def desenhar_conexoes(self, node_id):
        filhos = self.nodes[node_id]["children"]
        if not filhos: return

        px, py = self.node_positions[node_id]
        _, parent_height = self.node_dimensions[node_id]
        py_bottom = py + parent_height / 2
        
        # Espessura da linha se adapta ao zoom
        espessura_linha = max(1, int(2 * self.zoom))

        for filho_id in filhos:
            cx, cy = self.node_positions[filho_id]
            _, child_height = self.node_dimensions[filho_id]
            cy_top = cy - child_height / 2
            
            mid_y = py_bottom + self.pad_y / 2
            
            self.canvas.create_line(px, py_bottom, px, mid_y, fill="#6c757d", width=espessura_linha)
            self.canvas.create_line(px, mid_y, cx, mid_y, fill="#6c757d", width=espessura_linha)
            self.canvas.create_line(cx, mid_y, cx, cy_top, fill="#6c757d", width=espessura_linha)
            
            self.desenhar_conexoes(filho_id)

    def desenhar_nos(self):
        for node_id, (x, y) in self.node_positions.items():
            node_width, node_height = self.node_dimensions[node_id]
            
            x1 = x - node_width / 2
            y1 = y - node_height / 2
            x2 = x + node_width / 2
            y2 = y + node_height / 2
            
            espessura_borda = max(1, int(2 * self.zoom))
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ffffff", outline="#343a40", width=espessura_borda)
            
            texto_exibicao = f"{self.wbs_numbers[node_id]}\n{self.nodes[node_id]['text']}"
            self.canvas.create_text(x, y, text=texto_exibicao, fill="#212529", font=self.node_font, justify="center")

            # Adaptação dos botões interativos ao Zoom
            tamanho_btn = 12 * self.zoom
            tamanho_fonte_btn = max(6, int(12 * self.zoom))
            fonte_btn = ('Arial', tamanho_fonte_btn, 'bold')

            tag_child = f"add_child_{node_id}"
            self.canvas.create_rectangle(x - tamanho_btn, y2 - tamanho_btn, x + tamanho_btn, y2 + tamanho_btn, 
                                         fill="#28a745", outline="white", tags=tag_child)
            self.canvas.create_text(x, y2, text="+", fill="white", font=fonte_btn, tags=tag_child)
            self.canvas.tag_bind(tag_child, "<Button-1>", lambda e, nid=node_id: self.add_child(nid))

            if self.nodes[node_id]["parent"] is not None:
                tag_sib = f"add_sib_{node_id}"
                self.canvas.create_rectangle(x2 - tamanho_btn, y - tamanho_btn, x2 + tamanho_btn, y + tamanho_btn, 
                                             fill="#007bff", outline="white", tags=tag_sib)
                self.canvas.create_text(x2, y, text="+", fill="white", font=fonte_btn, tags=tag_sib)
                self.canvas.tag_bind(tag_sib, "<Button-1>", lambda e, nid=node_id: self.add_sibling(nid))

                tag_del = f"del_{node_id}"
                self.canvas.create_rectangle(x1 - tamanho_btn, y - tamanho_btn, x1 + tamanho_btn, y + tamanho_btn, 
                                             fill="#dc3545", outline="white", tags=tag_del)
                self.canvas.create_text(x1, y, text="-", fill="white", font=fonte_btn, tags=tag_del)
                self.canvas.tag_bind(tag_del, "<Button-1>", lambda e, nid=node_id: self.delete_node(nid))

if __name__ == "__main__":
    root = tk.Tk()
    app = EAPApp(root)
    root.mainloop()