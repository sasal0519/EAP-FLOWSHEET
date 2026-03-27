import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGraphicsView, QGraphicsScene,
    QGraphicsItem, QLineEdit, QLabel
)
from PyQt5.QtGui import (
    QFont, QFontMetrics, QPen, QBrush, QColor,
    QPainter, QPalette, QCursor
)
from PyQt5.QtCore import Qt, QRectF, QTimer, pyqtSignal, QObject

C_BG_APP       = "#0D0D0D"
C_BG_NODE      = "#1A0A0A"
C_BG_ROOT      = "#2A0F0F"
C_BORDER       = "#CC2222"
C_BORDER_ROOT  = "#E03535"
C_BORDER_EMPTY = "#8B2020"
C_TEXT_WBS     = "#CC2222"
C_TEXT_MAIN    = "#FAE8E8"
C_PLACEHOLDER  = "#8B2020"
C_BTN_ADD      = "#1A5C1A"
C_BTN_SIB      = "#1A3A6B"
C_BTN_DEL      = "#8B1515"
C_LINE         = "#8B2020"


class NodeSignals(QObject):
    commit_text = pyqtSignal(int, str)
    add_child   = pyqtSignal(int)
    add_sibling = pyqtSignal(int)
    delete_node = pyqtSignal(int)
    edit_start  = pyqtSignal(int)


class NodeItem(QGraphicsItem):

    def __init__(self, node_id, wbs, text, is_root, signals, zoom):
        super().__init__()
        self.node_id  = node_id
        self.wbs      = wbs
        self.text     = text
        self.is_root  = is_root
        self.signals  = signals
        self.zoom     = zoom
        self._hovered = False

        self._font_wbs  = QFont("Consolas", max(5, int(8  * zoom)), QFont.Bold)
        self._font_text = QFont("Segoe UI",  max(5, int(10 * zoom)),
                                QFont.Bold if is_root else QFont.Normal)
        self._font_ph   = QFont("Segoe UI",  max(5, int(9  * zoom)))
        self._font_ph.setItalic(True)
        self._font_btn  = QFont("Consolas",  max(6, int(9  * zoom)), QFont.Bold)

        self._calc_size()
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def _get_text_width(self, fm, text):
        # Fallback seguro para compatibilidade com versões antigas e novas do PyQt5
        if hasattr(fm, 'horizontalAdvance'):
            return fm.horizontalAdvance(text)
        return fm.width(text)

    def _calc_size(self):
        fm  = QFontMetrics(self._font_text)
        fmw = QFontMetrics(self._font_wbs)
        sample = self.text if self.text.strip() else "Clique para nomear"
        pad    = 40 * self.zoom
        
        text_w = self._get_text_width(fm, sample)
        wbs_w  = self._get_text_width(fmw, self.wbs)
        
        self._w = max(150 * self.zoom, max(text_w, wbs_w) + pad)
        self._h = max(60  * self.zoom, fm.height() + fmw.height() + 24 * self.zoom)

    def width(self):  return self._w
    def height(self): return self._h

    def boundingRect(self):
        m = 14 * self.zoom
        return QRectF(-m, -m, self._w + m * 2, self._h + m * 2)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        empty = not self.text.strip()
        r     = QRectF(0, 0, self._w, self._h)
        bs    = 14 * self.zoom
        hbs   = bs / 2

        bg = C_BG_ROOT if self.is_root else C_BG_NODE
        if self._hovered:
            bg = QColor(bg).lighter(130).name()
        painter.setBrush(QBrush(QColor(bg)))

        border = C_BORDER_ROOT if self.is_root else (C_BORDER if not empty else C_BORDER_EMPTY)
        style  = Qt.SolidLine if not empty else Qt.DashLine
        painter.setPen(QPen(QColor(border), 2.0 if self.is_root else 1.5, style))
        painter.drawRoundedRect(r, 7, 7)

        if self.is_root and not empty:
            painter.setBrush(QBrush(QColor(C_BORDER_ROOT)))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(0, 0, self._w, 4), 2, 2)

        if empty:
            painter.setFont(self._font_ph)
            painter.setPen(QColor(C_BORDER if self._hovered else C_PLACEHOLDER))
            painter.drawText(r, Qt.AlignCenter, "✎  Clique para nomear")
        else:
            fmw = QFontMetrics(self._font_wbs)
            painter.setFont(self._font_wbs)
            painter.setPen(QColor(C_TEXT_WBS))
            painter.drawText(QRectF(10 * self.zoom, 6 * self.zoom,
                                    self._w - 20 * self.zoom, fmw.height()),
                             Qt.AlignLeft | Qt.AlignVCenter, self.wbs)
            painter.setFont(self._font_text)
            painter.setPen(QColor(C_TEXT_MAIN))
            painter.drawText(QRectF(8 * self.zoom,
                                    6 * self.zoom + fmw.height() + 2 * self.zoom,
                                    self._w - 16 * self.zoom,
                                    QFontMetrics(self._font_text).height()),
                             Qt.AlignCenter, self.text)

        if self._hovered:
            painter.setFont(self._font_btn)
            self._draw_btn(painter,
                           QRectF(self._w / 2 - hbs, self._h - hbs, bs, bs),
                           "+", C_BTN_ADD)
            if not self.is_root:
                self._draw_btn(painter,
                               QRectF(self._w - hbs, self._h / 2 - hbs, bs, bs),
                               "+", C_BTN_SIB)
                self._draw_btn(painter,
                               QRectF(-hbs, self._h / 2 - hbs, bs, bs),
                               "−", C_BTN_DEL)

    def _draw_btn(self, painter, rect, label, color):
        painter.setBrush(QBrush(QColor(color)))
        painter.setPen(QPen(QColor("#FF6666"), 1))
        painter.drawRoundedRect(rect, 4, 4)
        painter.setPen(QColor("#FAE8E8"))
        painter.drawText(rect, Qt.AlignCenter, label)

    def _btn_rects(self):
        bs  = 14 * self.zoom
        hbs = bs / 2
        rects = {"child": QRectF(self._w / 2 - hbs, self._h - hbs, bs, bs)}
        if not self.is_root:
            rects["sibling"] = QRectF(self._w - hbs, self._h / 2 - hbs, bs, bs)
            rects["delete"]  = QRectF(-hbs,           self._h / 2 - hbs, bs, bs)
        return rects

    def hoverEnterEvent(self, event):
        self._hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self._hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        event.accept()
        sinais = self.signals
        nid    = self.node_id
        if self._hovered:
            for action, rect in self._btn_rects().items():
                if rect.contains(event.pos()):
                    if   action == "child":
                        QTimer.singleShot(0, lambda s=sinais, n=nid: s.add_child.emit(n))
                    elif action == "sibling":
                        QTimer.singleShot(0, lambda s=sinais, n=nid: s.add_sibling.emit(n))
                    elif action == "delete":
                        QTimer.singleShot(0, lambda s=sinais, n=nid: s.delete_node.emit(n))
                    return
        QTimer.singleShot(0, lambda s=sinais, n=nid: s.edit_start.emit(n))

    def mouseDoubleClickEvent(self, event):
        event.accept()
        sinais = self.signals
        nid    = self.node_id
        QTimer.singleShot(0, lambda s=sinais, n=nid: s.edit_start.emit(n))


class FloatingEditor(QLineEdit):
    committed = pyqtSignal(int, str)

    def __init__(self, parent_view):
        super().__init__(parent_view)
        self._node_id  = -1
        self._original = ""
        self._done     = False
        self.setStyleSheet("""
            QLineEdit {
                background  : #2A0F0F;
                color       : #FAE8E8;
                border      : 2px solid #CC2222;
                border-radius: 5px;
                font-family : 'Segoe UI';
                font-size   : 11pt;
                padding     : 4px 10px;
            }
        """)
        self.hide()

    def open(self, node_id, current_text, scene_rect, view):
        self._node_id  = node_id
        self._original = current_text
        self._done     = False
        tl = view.mapFromScene(scene_rect.topLeft())
        w  = max(180, int(scene_rect.width()))
        h  = 36
        self.setGeometry(tl.x(),
                         tl.y() + int(scene_rect.height() / 2) - h // 2,
                         w, h)
        self.setText(current_text)
        self.selectAll()
        self.show()
        self.raise_()
        self.setFocus()

    def _commit(self, text=None):
        if self._done:
            return
        self._done = True
        result = (text if text is not None else self.text()).strip()
        self.hide()
        self.committed.emit(self._node_id, result)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._commit()
        elif event.key() == Qt.Key_Escape:
            self._commit(self._original)
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self._commit()
        super().focusOutEvent(event)


class EAPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EAP-FLOWSHEET")
        self.setGeometry(100, 100, 1600, 900)

        self.base_pad_x      = 40
        self.base_pad_y      = 70
        self.base_min_width  = 120
        self.base_box_height = 60
        self.zoom            = 1.0

        self.next_id         = 2
        self.wbs_numbers     = {}
        self.node_dimensions = {}
        self.node_positions  = {}
        self._scene_items    = []

        self.nodes = {1: {"text": "", "children": [], "parent": None}}

        self.signals = NodeSignals()
        self.signals.commit_text.connect(self._on_commit)
        self.signals.add_child.connect(self._on_add_child)
        self.signals.add_sibling.connect(self._on_add_sibling)
        self.signals.delete_node.connect(self._on_delete)
        self.signals.edit_start.connect(self._on_edit_start)

        self._setup_palette()
        self._setup_ui()

        self._float_editor = FloatingEditor(self.view)
        self._float_editor.committed.connect(self._on_commit)

        self.update_zoom(1.0)

    def _setup_palette(self):
        p = QPalette()
        p.setColor(QPalette.Window,          QColor("#0D0D0D"))
        p.setColor(QPalette.WindowText,      QColor("#FAE8E8"))
        p.setColor(QPalette.Base,            QColor("#1A0A0A"))
        p.setColor(QPalette.AlternateBase,   QColor("#2A0F0F"))
        p.setColor(QPalette.Text,            QColor("#FAE8E8"))
        p.setColor(QPalette.Button,          QColor("#1A0A0A"))
        p.setColor(QPalette.ButtonText,      QColor("#FAE8E8"))
        p.setColor(QPalette.Highlight,       QColor("#CC2222"))
        p.setColor(QPalette.HighlightedText, QColor("#0D0D0D"))
        QApplication.instance().setPalette(p)

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QWidget()
        toolbar.setFixedHeight(44)
        toolbar.setStyleSheet(f"""
            QWidget     {{ background:{C_BG_APP}; border-bottom:1px solid {C_BORDER}; }}
            QPushButton {{
                background:#1A0A0A; color:#FAE8E8;
                border:1px solid #8B2020; border-radius:5px;
                padding:4px 14px; font-family:'Segoe UI'; font-size:11px;
            }}
            QPushButton:hover {{ background:#2A0F0F; border-color:{C_BORDER}; }}
        """)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(10, 4, 10, 4)
        tb.setSpacing(6)

        title = QLabel("EAP-FLOWSHEET")
        title.setStyleSheet(
            f"color:{C_BORDER_ROOT}; font-family:'Consolas';"
            f" font-size:15px; font-weight:bold; background:transparent;")
        tb.addWidget(title)

        sep = QWidget()
        sep.setFixedSize(1, 26)
        sep.setStyleSheet(f"background:{C_BORDER};")
        tb.addWidget(sep)

        # CORREÇÃO: Usando *args no lambda para ignorar o boolean 'checked' enviado pelo clicked
        botoes = [
            ("🔍−", lambda *args: self.zoom_out()),
            ("🔍+", lambda *args: self.zoom_in()),
            ("⟳ 100%", lambda *args: self.update_zoom(1.0))
        ]
        
        for lbl, fn in botoes:
            b = QPushButton(lbl)
            b.clicked.connect(fn)
            tb.addWidget(b)
            
        tb.addStretch()
        layout.addWidget(toolbar)

        self.scene = QGraphicsScene()
        self.view  = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setBackgroundBrush(QBrush(QColor(C_BG_APP)))
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setStyleSheet("border:none;")
        layout.addWidget(self.view)

    # CORREÇÃO: Permite aceitar *args caso algum evento do Qt tente passar parâmetros
    def zoom_in(self, *args):  self.update_zoom(self.zoom * 1.15)
    def zoom_out(self, *args): self.update_zoom(self.zoom / 1.15)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.zoom_in() if event.angleDelta().y() > 0 else self.zoom_out()
        else:
            self.view.verticalScrollBar().setValue(
                self.view.verticalScrollBar().value() - event.angleDelta().y() // 3)

    def update_zoom(self, z):
        self.zoom       = max(0.3, min(z, 3.0))
        self.pad_x      = self.base_pad_x      * self.zoom
        self.pad_y      = self.base_pad_y      * self.zoom
        self.min_width  = self.base_min_width  * self.zoom
        self.box_height = self.base_box_height * self.zoom
        self.draw_eap()

    def _on_commit(self, node_id, new_text):
        if node_id in self.nodes:
            self.nodes[node_id]["text"] = new_text
        self.draw_eap()

    def _on_edit_start(self, node_id):
        if node_id not in self.node_positions:
            return
        nw, nh  = self.node_dimensions[node_id]
        x, y    = self.node_positions[node_id]
        scene_r = QRectF(x - nw / 2, y - nh / 2, nw, nh)
        self._float_editor.open(node_id, self.nodes[node_id]["text"],
                                scene_r, self.view)

    def _on_add_child(self, parent_id):
        new_id = self.next_id; self.next_id += 1
        self.nodes[new_id] = {"text": "", "children": [], "parent": parent_id}
        self.nodes[parent_id]["children"].append(new_id)
        self.draw_eap()
        QTimer.singleShot(60, lambda n=new_id: self._on_edit_start(n))

    def _on_add_sibling(self, node_id):
        parent_id = self.nodes[node_id]["parent"]
        if parent_id is None: return
        new_id = self.next_id; self.next_id += 1
        self.nodes[new_id] = {"text": "", "children": [], "parent": parent_id}
        self.nodes[parent_id]["children"].append(new_id)
        self.draw_eap()
        QTimer.singleShot(60, lambda n=new_id: self._on_edit_start(n))

    def _on_delete(self, node_id):
        label = self.nodes[node_id]["text"] or "nó sem nome"
        ans = QMessageBox.question(self, "Excluir",
              f"Excluir '{label}' e todas as suas sub-tarefas?",
              QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            pid = self.nodes[node_id]["parent"]
            if pid is not None:
                self.nodes[pid]["children"].remove(node_id)
            self._remove_recursively(node_id)
            self.draw_eap()

    def _remove_recursively(self, node_id):
        for cid in list(self.nodes[node_id]["children"]):
            self._remove_recursively(cid)
        del self.nodes[node_id]

    def calculate_wbs(self, node_id, wbs):
        self.wbs_numbers[node_id] = wbs
        for i, cid in enumerate(self.nodes[node_id]["children"]):
            self.calculate_wbs(cid, f"{wbs}.{i+1}")

    def pre_calcular_dimensoes(self):
        self.node_dimensions.clear()
        for nid in self.nodes:
            tmp = NodeItem(nid, self.wbs_numbers.get(nid, ""),
                           self.nodes[nid]["text"], nid == 1,
                           self.signals, self.zoom)
            self.node_dimensions[nid] = (tmp.width(), tmp.height())

    def calcular_posicoes(self, node_id, nivel):
        filhos = self.nodes[node_id]["children"]
        nw, nh = self.node_dimensions[node_id]
        y = 80 * self.zoom + nivel * (nh + self.pad_y)
        if not filhos:
            x = self.current_leaf_x + nw / 2
            self.current_leaf_x += nw + self.pad_x
        else:
            xs = [self.calcular_posicoes(c, nivel + 1) for c in filhos]
            x  = sum(xs) / len(xs)
        self.node_positions[node_id] = (x, y)
        return x

    def draw_eap(self):
        self._scene_items = []
        self.scene.clear()
        if not self.nodes: return

        self.node_positions.clear()
        self.wbs_numbers.clear()
        self.calculate_wbs(1, "1")
        self.pre_calcular_dimensoes()

        self.current_leaf_x = 80 * self.zoom
        self.calcular_posicoes(1, nivel=0)

        vw       = self.view.viewport().width() or 800
        offset_x = vw / 2 - self.node_positions[1][0]
        min_x    = min(p[0] - self.node_dimensions[n][0] / 2
                       for n, p in self.node_positions.items())
        if min_x + offset_x < 80 * self.zoom:
            offset_x = 80 * self.zoom - min_x
        for n in self.node_positions:
            x, y = self.node_positions[n]
            self.node_positions[n] = (x + offset_x, y)

        self._draw_connections(1)
        self._draw_nodes()
        self.scene.setSceneRect(
            self.scene.itemsBoundingRect().adjusted(-40, -40, 40, 40))

    def _draw_connections(self, node_id):
        filhos = self.nodes[node_id]["children"]
        if not filhos: return
        px, py = self.node_positions[node_id]
        _, ph  = self.node_dimensions[node_id]
        py_bot = py + ph / 2
        mid_y  = py_bot + self.pad_y / 2
        pen    = QPen(QColor(C_LINE), max(1, int(2 * self.zoom)),
                      Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        for cid in filhos:
            cx, cy = self.node_positions[cid]
            cy_top = cy - self.node_dimensions[cid][1] / 2
            for coords in [(px, py_bot, px, mid_y),
                           (px, mid_y,  cx, mid_y),
                           (cx, mid_y,  cx, cy_top)]:
                self._scene_items.append(self.scene.addLine(*coords, pen))
            self._draw_connections(cid)

    def _draw_nodes(self):
        for nid, (x, y) in self.node_positions.items():
            nw, nh = self.node_dimensions[nid]
            item = NodeItem(nid, self.wbs_numbers[nid],
                            self.nodes[nid]["text"],
                            nid == 1, self.signals, self.zoom)
            item.setPos(x - nw / 2, y - nh / 2)
            self.scene.addItem(item)
            self._scene_items.append(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = EAPApp()
    w.show()
    sys.exit(app.exec_())
    #versão com bug corrigido e melhorias na interface, incluindo suporte a zoom e uma barra de ferramentas para controle rápido. O código foi refatorado para melhor organização e legibilidade, mantendo a funcionalidade principal de criação e edição de fluxogramas de forma intuitiva.
