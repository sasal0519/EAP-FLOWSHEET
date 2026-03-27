import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsItem,
    QListWidget, QListWidgetItem, QSplitter, QGraphicsPathItem, QMenu,
    QListView, QLineEdit, QLabel, QStackedWidget
)
from PyQt5.QtGui import (
    QPen, QBrush, QColor, QPainter, QPalette, QCursor, QPolygonF,
    QFont, QFontMetrics, QIcon, QPixmap, QPainterPath, QDrag, QLinearGradient
)
from PyQt5.QtCore import (
    Qt, QRectF, QPointF, QMimeData, QByteArray, QDataStream,
    QIODevice, QSize, QPoint, QTimer, pyqtSignal, QObject
)

# ==========================================
# CORES DO TEMA DARK INDUSTRIAL
# ==========================================
C_BG_APP       = "#0D0D0D"
C_BG_NODE      = "#1A0A0A"
C_BG_ROOT      = "#2A0F0F"
C_BORDER       = "#CC2222"
C_BORDER_ROOT  = "#E03535"
C_BORDER_EMPTY = "#8B2020"
C_TEXT_WBS     = "#CC2222"
C_TEXT_MAIN    = "#FAE8E8"
C_TEXT         = "#FAE8E8"
C_PLACEHOLDER  = "#8B2020"
C_BTN_ADD      = "#1A5C1A"
C_BTN_SIB      = "#1A3A6B"
C_BTN_DEL      = "#8B1515"
C_LINE         = "#E03535"
C_LINE_EAP     = "#8B2020"


# ==========================================
# ==========================================
#   MÓDULO FLOWSHEET
# ==========================================
# ==========================================

def draw_equipment(painter, symbol_type, size, is_icon=False):
    s = size / 2
    pen_color = C_TEXT if is_icon else C_BORDER

    default_pen = QPen(QColor(pen_color), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
    painter.setPen(default_pen)
    painter.setBrush(QBrush(QColor(C_BG_NODE)))

    if symbol_type == "Vaso":
        painter.drawRoundedRect(QRectF(-s*0.8, -s, s*1.6, s*2), s*0.6, s*0.6)
    elif symbol_type == "Tanque":
        painter.drawRect(QRectF(-s*0.8, -s*0.5, s*1.6, s*1.5))
        painter.drawArc(QRectF(-s*0.8, -s*1.0, s*1.6, s*1.0), 0, 180 * 16)
    elif symbol_type == "Bomba":
        painter.drawEllipse(QRectF(-s*0.8, -s*0.8, s*1.6, s*1.6))
        poly = QPolygonF([QPointF(-s*0.3, -s*0.7), QPointF(s*0.3, -s*0.7), QPointF(0, -s*1.4)])
        painter.setBrush(QBrush(QColor(pen_color)))
        painter.drawPolygon(poly)
    elif symbol_type == "Compressor":
        poly = QPolygonF([QPointF(-s*0.8, s*0.8), QPointF(s*0.8, s*0.4),
                          QPointF(s*0.8, -s*0.4), QPointF(-s*0.8, -s*0.8)])
        painter.drawPolygon(poly)
    elif symbol_type == "Soprador":
        painter.drawEllipse(QRectF(-s*0.8, -s*0.6, s*1.2, s*1.2))
        painter.drawRect(QRectF(s*0.2, -s*0.6, s*0.5, s*0.5))
    elif symbol_type == "Turbina":
        poly = QPolygonF([QPointF(s*0.8, s*0.8), QPointF(-s*0.8, s*0.4),
                          QPointF(-s*0.8, -s*0.4), QPointF(s*0.8, -s*0.8)])
        painter.drawPolygon(poly)
    elif symbol_type == "Trocador":
        painter.drawEllipse(QRectF(-s, -s, s*2, s*2))
        painter.drawLine(QPointF(-s, 0), QPointF(-s*0.5, -s*0.5))
        painter.drawLine(QPointF(-s*0.5, -s*0.5), QPointF(0, s*0.5))
        painter.drawLine(QPointF(0, s*0.5), QPointF(s*0.5, -s*0.5))
        painter.drawLine(QPointF(s*0.5, -s*0.5), QPointF(s, 0))
    elif symbol_type == "Fornalha":
        painter.drawRect(QRectF(-s, -s*0.5, s*2, s*1.5))
        poly = QPolygonF([QPointF(-s, -s*0.5), QPointF(0, -s*1.5), QPointF(s, -s*0.5)])
        painter.drawPolygon(poly)
        painter.drawLine(QPointF(-s*0.6, s*0.6), QPointF(s*0.6, s*0.2))
        painter.drawLine(QPointF(s*0.6, s*0.2), QPointF(-s*0.6, -0.2))
    elif symbol_type == "Reator":
        painter.drawRoundedRect(QRectF(-s*0.8, -s*1.2, s*1.6, s*2.4), s*0.4, s*0.4)
        painter.drawRect(QRectF(-s*0.25, -s*1.6, s*0.5, s*0.4))
        painter.drawLine(QPointF(0, -s*1.2), QPointF(0, s*0.6))
        painter.drawLine(QPointF(-s*0.4, s*0.2), QPointF(s*0.4, s*0.6))
        painter.drawLine(QPointF(s*0.4, s*0.2), QPointF(-s*0.4, s*0.6))
    elif symbol_type == "Misturador":
        painter.drawEllipse(QRectF(-s, -s, s*2, s*2))
        painter.drawLine(QPointF(-s*0.6, -s*0.6), QPointF(s*0.6, s*0.6))
        painter.drawLine(QPointF(-s*0.6, s*0.6), QPointF(s*0.6, -s*0.6))
    elif symbol_type == "Filtro":
        painter.drawEllipse(QRectF(-s, -s, s*2, s*2))
        painter.setPen(QPen(QColor(pen_color), 2, Qt.DashLine))
        painter.drawLine(QPointF(-s, 0), QPointF(s, 0))
        painter.setPen(default_pen)
    elif symbol_type == "Ciclone":
        painter.drawRect(QRectF(-s*0.6, -s*1.5, s*1.2, s))
        poly = QPolygonF([QPointF(-s*0.6, -s*0.5), QPointF(s*0.6, -s*0.5), QPointF(0, s*1.5)])
        painter.drawPolygon(poly)
    elif symbol_type == "Torre de Destilação":
        painter.drawRoundedRect(QRectF(-s*0.6, -s*2.5, s*1.2, s*5), s*0.5, s*0.5)
        for i in [-1.5, -0.75, 0, 0.75, 1.5]:
            painter.drawLine(QPointF(-s*0.6, s*i), QPointF(s*0.6, s*i))
    elif symbol_type == "Torre de Resfriamento":
        poly = QPolygonF([QPointF(-s, s*1.5), QPointF(s, s*1.5),
                          QPointF(s*0.6, -s*1.2), QPointF(-s*0.6, -s*1.2)])
        painter.drawPolygon(poly)
        painter.drawLine(QPointF(-s*0.4, -s*1.4), QPointF(s*0.4, -s*1.4))
        painter.drawLine(QPointF(0, -s*1.2), QPointF(0, -s*1.4))
    elif symbol_type == "Flare":
        painter.drawRect(QRectF(-s*0.2, -s*1.5, s*0.4, s*3))
        if not is_icon:
            painter.setBrush(QBrush(QColor("#E06622")))
        poly = QPolygonF([QPointF(-s*0.5, -s*1.5), QPointF(s*0.5, -s*1.5), QPointF(0, -s*2.5)])
        painter.drawPolygon(poly)
    elif symbol_type == "Válvula":
        poly = QPolygonF([QPointF(-s, -s*0.5), QPointF(-s, s*0.5),
                          QPointF(s, -s*0.5), QPointF(s, s*0.5)])
        painter.drawPolygon(poly)
    elif symbol_type == "Secador":
        painter.drawRoundedRect(QRectF(-s*1.2, -s*0.6, s*2.4, s*1.2), s*0.2, s*0.2)
        painter.drawLine(QPointF(-s*1.2, 0), QPointF(s*1.2, 0))
    elif symbol_type == "Evaporador":
        painter.drawRoundedRect(QRectF(-s*0.6, -s*1.5, s*1.2, s*2), s*0.6, s*0.6)
        painter.drawRect(QRectF(-s*0.6, s*0.5, s*1.2, s*1.0))
    elif symbol_type == "Permutador a Ar":
        painter.drawRect(QRectF(-s, -s*0.5, s*2, s))
        painter.drawLine(QPointF(-s*0.5, -s*0.5), QPointF(s*0.5, -s*1.2))
        painter.drawLine(QPointF(s*0.5, -s*0.5), QPointF(-s*0.5, -s*1.2))
        painter.drawEllipse(QRectF(-s*0.6, -s*1.3, s*1.2, s*0.8))
    elif symbol_type == "Separador Bifásico":
        painter.drawRoundedRect(QRectF(-s*1.5, -s*0.6, s*3.0, s*1.2), s*0.6, s*0.6)
        painter.drawLine(QPointF(-s*1.5, 0), QPointF(s*1.5, 0))
    elif symbol_type == "Ejetor":
        poly = QPolygonF([QPointF(-s, -s*0.3), QPointF(-s*0.2, -s*0.1), QPointF(s, -s*0.3),
                          QPointF(s, s*0.3), QPointF(-s*0.2, s*0.1), QPointF(-s, s*0.3)])
        painter.drawPolygon(poly)
    elif symbol_type == "Moinho":
        painter.drawRect(QRectF(-s, -s*0.5, s*2, s))
        painter.drawEllipse(QRectF(-s*0.8, -s*0.4, s*0.8, s*0.8))
        painter.drawEllipse(QRectF(0, -s*0.4, s*0.8, s*0.8))
    elif symbol_type == "Peneira":
        painter.drawRect(QRectF(-s*1.2, -s*0.8, s*2.4, s*1.6))
        painter.setPen(QPen(QColor(pen_color), 2, Qt.DashLine))
        painter.drawLine(QPointF(-s*1.2, -s*0.4), QPointF(s*1.2, s*0.4))
        painter.setPen(default_pen)
    elif symbol_type == "Caldeira":
        painter.drawRoundedRect(QRectF(-s*1.5, -s*0.8, s*3.0, s*1.6), s*0.4, s*0.4)
        for i in [-0.4, 0, 0.4]:
            painter.drawLine(QPointF(-s*1.5, s*i), QPointF(s*1.5, s*i))
    elif symbol_type == "Coluna de Absorção":
        painter.drawRoundedRect(QRectF(-s*0.6, -s*2.5, s*1.2, s*5), s*0.5, s*0.5)
        painter.drawLine(QPointF(-s*0.6, -s*1.5), QPointF(s*0.6, s*1.5))
        painter.drawLine(QPointF(s*0.6, -s*1.5), QPointF(-s*0.6, s*1.5))
    elif symbol_type == "Filtro Prensa":
        painter.drawRect(QRectF(-s*1.2, -s*0.8, s*2.4, s*1.6))
        for i in [-0.6, 0, 0.6]:
            painter.drawLine(QPointF(s*i, -s*0.8), QPointF(s*i, s*0.8))


class Edge(QGraphicsPathItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source_node = source_node
        self.dest_node = dest_node
        self.source_node.add_edge(self)
        self.dest_node.add_edge(self)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        pen = QPen(QColor(C_LINE), 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.setPen(pen)
        self.setZValue(-1)
        self.adjust()

    def adjust(self):
        if not self.source_node or not self.dest_node:
            return
        c1 = self.source_node.pos()
        c2 = self.dest_node.pos()
        p1 = self.source_node.get_closest_port(c2)
        p2 = self.dest_node.get_closest_port(c1)
        path = QPainterPath()
        path.moveTo(p1)
        rect1 = self.source_node.sceneBoundingRect()
        is_p1_horizontal = (abs(p1.y() - rect1.center().y()) < 5)
        mid_x = (p1.x() + p2.x()) / 2
        mid_y = (p1.y() + p2.y()) / 2
        if is_p1_horizontal:
            path.lineTo(mid_x, p1.y())
            path.lineTo(mid_x, p2.y())
        else:
            path.lineTo(p1.x(), mid_y)
            path.lineTo(p2.x(), mid_y)
        path.lineTo(p2)
        self.setPath(path)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet(f"""
            QMenu {{ background-color: {C_BG_NODE}; color: {C_TEXT}; border: 1px solid {C_BORDER};
                    font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; }}
            QMenu::item {{ padding: 8px 30px; }}
            QMenu::item:selected {{ background-color: {C_BORDER}; color: #FFFFFF; }}
        """)
        del_action = menu.addAction("🗑 Excluir Tubulação")
        action = menu.exec_(event.screenPos())
        if action == del_action:
            if self in self.source_node.edges:
                self.source_node.edges.remove(self)
            if self in self.dest_node.edges:
                self.dest_node.edges.remove(self)
            self.scene().removeItem(self)

    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setPen(QPen(QColor("#FFFFFF"), 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            painter.setPen(QPen(QColor(C_LINE), 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        super().paint(painter, option, widget)


class ProcessNode(QGraphicsItem):
    def __init__(self, symbol_type):
        super().__init__()
        self.symbol_type = symbol_type
        self.edges = []
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCursor(QCursor(Qt.SizeAllCursor))
        self.size = 50

    def add_edge(self, edge):
        self.edges.append(edge)

    def set_size(self, new_size):
        self.prepareGeometryChange()
        self.size = max(20, min(new_size, 300))
        for edge in self.edges:
            edge.adjust()
        self.update()

    def delete_node(self):
        for edge in list(self.edges):
            self.scene().removeItem(edge)
            if edge in edge.source_node.edges:
                edge.source_node.edges.remove(edge)
            if edge in edge.dest_node.edges:
                edge.dest_node.edges.remove(edge)
        self.scene().removeItem(self)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet(f"""
            QMenu {{ background-color: {C_BG_NODE}; color: {C_TEXT}; border: 1px solid {C_BORDER};
                    font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; padding: 5px; }}
            QMenu::item {{ padding: 8px 30px; border-radius: 4px; }}
            QMenu::item:selected {{ background-color: {C_BORDER}; color: #FFFFFF; }}
        """)
        grow_action   = menu.addAction("➕ Aumentar Tamanho")
        shrink_action = menu.addAction("➖ Diminuir Tamanho")
        menu.addSeparator()
        del_action = menu.addAction("🗑 Excluir Equipamento")
        action = menu.exec_(event.screenPos())
        if action == grow_action:
            self.set_size(self.size + 10)
        elif action == shrink_action:
            self.set_size(self.size - 10)
        elif action == del_action:
            self.delete_node()

    def get_closest_port(self, target_pos):
        rect = self.sceneBoundingRect()
        ports = [
            QPointF(rect.center().x(), rect.top()),
            QPointF(rect.center().x(), rect.bottom()),
            QPointF(rect.left(),  rect.center().y()),
            QPointF(rect.right(), rect.center().y())
        ]
        return min(ports, key=lambda p: (p.x() - target_pos.x())**2 + (p.y() - target_pos.y())**2)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
        return super().itemChange(change, value)

    def boundingRect(self):
        m = 5
        s = self.size / 2
        if self.symbol_type in ["Torre de Destilação", "Coluna de Absorção"]:
            return QRectF(-s - m, -s*2.5 - m, self.size + m*2, self.size*2.5 + m*2)
        elif self.symbol_type in ["Separador Bifásico", "Caldeira"]:
            return QRectF(-s*1.5 - m, -s - m, self.size*1.5 + m*2, self.size + m*2)
        elif self.symbol_type in ["Secador", "Peneira", "Filtro Prensa"]:
            return QRectF(-s*1.2 - m, -s - m, self.size*1.2 + m*2, self.size + m*2)
        elif self.symbol_type == "Reator":
            return QRectF(-s - m, -s*1.6 - m, self.size + m*2, self.size*1.4 + m*2)
        elif self.symbol_type == "Fornalha":
            return QRectF(-s - m, -s*1.5 - m, self.size + m*2, self.size*1.25 + m*2)
        elif self.symbol_type == "Ciclone":
            return QRectF(-s - m, -s*1.5 - m, self.size + m*2, self.size*1.5 + m*2)
        elif self.symbol_type == "Torre de Resfriamento":
            return QRectF(-s - m, -s*1.7 - m, self.size + m*2, self.size*1.6 + m*2)
        elif self.symbol_type == "Flare":
            return QRectF(-s - m, -s*2.5 - m, self.size + m*2, self.size*2 + m*2)
        return QRectF(-s - m, -s - m, self.size + m*2, self.size + m*2)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.isSelected():
            painter.setPen(QPen(QColor("#FFFFFF"), 2, Qt.DotLine))
            painter.drawRect(self.boundingRect())
        draw_equipment(painter, self.symbol_type, self.size, is_icon=False)


class SymbolPalette(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QListWidget.DragOnly)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setWordWrap(True)
        self.setGridSize(QSize(90, 80))
        self.setIconSize(QSize(36, 36))
        self.setSpacing(4)
        self.setStyleSheet(f"""
            QListWidget {{
                background-color: {C_BG_APP}; color: {C_TEXT}; border: none; outline: 0; padding: 8px;
            }}
            QListWidget::item {{
                background-color: {C_BG_NODE};
                border: 1px solid #2A0F0F;
                border-radius: 6px;
                padding: 4px;
                font-family: 'Segoe UI', Arial; font-size: 10px; font-weight: bold;
            }}
            QListWidget::item:hover {{ background-color: #251212; border: 1px solid {C_BORDER}; }}
            QListWidget::item:selected {{ background-color: {C_BORDER}; color: #FFFFFF; border: 1px solid #FF6666; }}
            QScrollBar:vertical {{ background: {C_BG_APP}; width: 6px; }}
            QScrollBar::handle:vertical {{ background: #333333; border-radius: 3px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)
        symbols = [
            "Vaso", "Tanque", "Separador Bifásico", "Bomba", "Compressor", "Soprador", "Turbina",
            "Ejetor", "Trocador", "Permutador a Ar", "Fornalha", "Caldeira", "Reator", "Misturador",
            "Moinho", "Filtro", "Filtro Prensa", "Peneira", "Ciclone", "Secador", "Evaporador",
            "Torre de Destilação", "Coluna de Absorção", "Torre de Resfriamento", "Flare", "Válvula"
        ]
        for sym in symbols:
            item = QListWidgetItem(self._create_icon(sym), sym)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignBottom)
            self.addItem(item)

    def _create_icon(self, symbol_type):
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(25, 25)
        sym_size = 28
        if symbol_type in ["Torre de Destilação", "Coluna de Absorção", "Flare"]:
            sym_size = 14
        elif symbol_type in ["Reator", "Fornalha", "Ciclone", "Torre de Resfriamento",
                              "Evaporador", "Separador Bifásico", "Caldeira"]:
            sym_size = 18
        draw_equipment(painter, symbol_type, size=sym_size, is_icon=True)
        painter.end()
        return QIcon(pixmap)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        data_stream.writeQString(item.text())
        mime_data = QMimeData()
        mime_data.setData('application/x-pfd-item', item_data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        pixmap = item.icon().pixmap(40, 40)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        drag.exec_(Qt.CopyAction)


class FlowsheetCanvas(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor(C_BG_APP)))
        self.setAcceptDrops(True)
        self.mode = "Move"
        self.temp_line = None
        self.start_item = None
        self.zoom_level = 1.0

    def zoom_in(self):  self._scale_view(1.15)
    def zoom_out(self): self._scale_view(1 / 1.15)
    def reset_zoom(self):
        self.resetTransform()
        self.zoom_level = 1.0

    def _scale_view(self, factor):
        novo_zoom = self.zoom_level * factor
        if novo_zoom < 0.2 or novo_zoom > 5.0:
            return
        self.zoom_level = novo_zoom
        self.scale(factor, factor)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-pfd-item'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-pfd-item'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-pfd-item'):
            item_data = event.mimeData().data('application/x-pfd-item')
            stream = QDataStream(item_data, QIODevice.ReadOnly)
            symbol_type = stream.readQString()
            node = ProcessNode(symbol_type)
            pos = self.mapToScene(event.pos())
            node.setPos(pos)
            self.scene().addItem(node)
            event.acceptProposedAction()

    def mousePressEvent(self, event):
        if self.mode == "Connect" and event.button() == Qt.LeftButton:
            items_under_click = self.items(event.pos())
            for item in items_under_click:
                if isinstance(item, ProcessNode):
                    self.start_item = item
                    pos = self.mapToScene(event.pos())
                    path = QPainterPath()
                    path.moveTo(pos)
                    self.temp_line = self.scene().addPath(path, QPen(QColor(C_LINE), 2, Qt.DashLine))
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == "Connect" and self.temp_line:
            target_node = None
            items_under_mouse = self.items(event.pos())
            for item in items_under_mouse:
                if isinstance(item, ProcessNode) and item != self.start_item:
                    target_node = item
                    break
            p2_raw = self.mapToScene(event.pos())
            if target_node:
                c2 = target_node.sceneBoundingRect().center()
                p2 = target_node.get_closest_port(self.start_item.sceneBoundingRect().center())
            else:
                c2, p2 = p2_raw, p2_raw
            p1 = self.start_item.get_closest_port(c2)
            path = QPainterPath()
            path.moveTo(p1)
            rect1 = self.start_item.sceneBoundingRect()
            is_p1_horizontal = (abs(p1.y() - rect1.center().y()) < 5)
            mid_x = (p1.x() + p2.x()) / 2
            mid_y = (p1.y() + p2.y()) / 2
            if is_p1_horizontal:
                path.lineTo(mid_x, p1.y())
                path.lineTo(mid_x, p2.y())
            else:
                path.lineTo(p1.x(), mid_y)
                path.lineTo(p2.x(), mid_y)
            path.lineTo(p2)
            self.temp_line.setPath(path)
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.mode == "Connect" and self.temp_line:
            target_node = None
            items_under_release = self.items(event.pos())
            for item in items_under_release:
                if isinstance(item, ProcessNode) and item != self.start_item:
                    target_node = item
                    break
            if target_node:
                edge = Edge(self.start_item, target_node)
                self.scene().addItem(edge)
            self.scene().removeItem(self.temp_line)
            self.temp_line = None
            self.start_item = None
            return
        super().mouseReleaseEvent(event)


class FlowsheetWidget(QWidget):
    """Widget completo do Flowsheet para embutir no app principal."""
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(50)
        toolbar.setStyleSheet(f"background-color: {C_BG_NODE}; border-bottom: 2px solid {C_BORDER};")
        tb_layout = QHBoxLayout(toolbar)

        btn_style = f"""
            QPushButton {{ background-color: {C_BG_APP}; color: {C_TEXT}; border: 1px solid #555;
                           padding: 8px 15px; border-radius: 4px; font-weight: bold; }}
            QPushButton:checked {{ background-color: {C_BORDER}; color: white; border-color: {C_BORDER}; }}
        """

        self.btn_toggle_palette = QPushButton("☰ Equipamentos")
        self.btn_toggle_palette.setCheckable(True)
        self.btn_toggle_palette.setChecked(True)
        self.btn_toggle_palette.setStyleSheet(btn_style)
        self.btn_toggle_palette.clicked.connect(self.toggle_palette)
        tb_layout.addWidget(self.btn_toggle_palette)

        sep0 = QWidget(); sep0.setFixedSize(2, 26)
        sep0.setStyleSheet(f"background:{C_BORDER}; margin: 0 10px;")
        tb_layout.addWidget(sep0)

        self.btn_move = QPushButton("🖐 Mover")
        self.btn_conn = QPushButton("🔗 Tubulação")
        for btn in [self.btn_move, self.btn_conn]:
            btn.setStyleSheet(btn_style)
            btn.setCheckable(True)
            tb_layout.addWidget(btn)

        self.btn_move.setChecked(True)
        self.btn_move.clicked.connect(lambda: self.set_mode("Move"))
        self.btn_conn.clicked.connect(lambda: self.set_mode("Connect"))

        sep1 = QWidget(); sep1.setFixedSize(2, 26)
        sep1.setStyleSheet(f"background:{C_BORDER}; margin: 0 10px;")
        tb_layout.addWidget(sep1)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 2000, 2000)
        self.canvas = FlowsheetCanvas(self.scene)

        zoom_style = f"""
            QPushButton {{ background-color: {C_BG_APP}; color: {C_TEXT}; border: 1px solid #8B2020;
                           border-radius: 4px; padding: 4px 14px; font-weight: bold; }}
            QPushButton:hover {{ background-color: {C_BORDER}; }}
        """
        for lbl, fn in [("🔍−", self.canvas.zoom_out), ("🔍+", self.canvas.zoom_in), ("⟳ 100%", self.canvas.reset_zoom)]:
            btn_zoom = QPushButton(lbl)
            btn_zoom.setStyleSheet(zoom_style)
            btn_zoom.clicked.connect(fn)
            tb_layout.addWidget(btn_zoom)

        tb_layout.addStretch()
        layout.addWidget(toolbar)

        self.splitter = QSplitter(Qt.Horizontal)
        self.palette_widget = SymbolPalette()
        self.splitter.addWidget(self.palette_widget)
        self.splitter.addWidget(self.canvas)
        self.splitter.setSizes([240, 1060])
        layout.addWidget(self.splitter)

    def toggle_palette(self):
        is_visible = self.btn_toggle_palette.isChecked()
        self.palette_widget.setVisible(is_visible)
        if is_visible:
            self.splitter.setSizes([240, self.width() - 240])

    def set_mode(self, mode):
        self.canvas.mode = mode
        if mode == "Move":
            self.btn_move.setChecked(True)
            self.btn_conn.setChecked(False)
            self.canvas.setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.btn_conn.setChecked(True)
            self.btn_move.setChecked(False)
            self.canvas.setCursor(QCursor(Qt.CrossCursor))


# ==========================================
# ==========================================
#   MÓDULO EAP
# ==========================================
# ==========================================

class NodeSignals(QObject):
    commit_text = pyqtSignal(int, str)
    add_child   = pyqtSignal(int)
    add_sibling = pyqtSignal(int)
    delete_node = pyqtSignal(int)
    edit_start  = pyqtSignal(int)


class NodeItem(QGraphicsItem):
    def __init__(self, node_id, wbs, text, is_root, shape, signals, zoom):
        super().__init__()
        self.node_id  = node_id
        self.wbs      = wbs
        self.text     = text
        self.is_root  = is_root
        self.shape    = shape
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
        if hasattr(fm, 'horizontalAdvance'):
            return fm.horizontalAdvance(text)
        return fm.width(text)

    def _calc_size(self):
        fm  = QFontMetrics(self._font_text)
        fmw = QFontMetrics(self._font_wbs)
        sample = self.text if self.text.strip() else "Nomear"
        pad_x = 30 * self.zoom
        pad_y = 18 * self.zoom
        if self.shape in ["ellipse", "diamond"]:
            pad_x *= 1.6
            pad_y *= 1.8
        text_w = self._get_text_width(fm, sample)
        wbs_w  = self._get_text_width(fmw, self.wbs)
        self._w = max(100 * self.zoom, max(text_w, wbs_w) + pad_x)
        self._h = max(40  * self.zoom, fm.height() + fmw.height() + pad_y)

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

        if self.shape == "roundrect":
            painter.drawRoundedRect(r, 7, 7)
        elif self.shape == "ellipse":
            painter.drawEllipse(r)
        elif self.shape == "diamond":
            poly = QPolygonF([
                QPointF(self._w / 2, 0),
                QPointF(self._w, self._h / 2),
                QPointF(self._w / 2, self._h),
                QPointF(0, self._h / 2)
            ])
            painter.drawPolygon(poly)

        if self.is_root and not empty and self.shape == "roundrect":
            painter.setBrush(QBrush(QColor(C_BORDER_ROOT)))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(0, 0, self._w, 4), 2, 2)

        if empty:
            painter.setFont(self._font_ph)
            painter.setPen(QColor(C_BORDER if self._hovered else C_PLACEHOLDER))
            painter.drawText(r, Qt.AlignCenter, "✎ Nomear")
        else:
            fmw = QFontMetrics(self._font_wbs)
            painter.setFont(self._font_wbs)
            painter.setPen(QColor(C_TEXT_WBS))
            offset_y = 6 * self.zoom
            if self.shape in ["ellipse", "diamond"]:
                offset_y += 10 * self.zoom
            painter.drawText(QRectF(0, offset_y, self._w, fmw.height()),
                             Qt.AlignHCenter | Qt.AlignVCenter, self.wbs)
            painter.setFont(self._font_text)
            painter.setPen(QColor(C_TEXT_MAIN))
            painter.drawText(QRectF(0, offset_y + fmw.height() + 2 * self.zoom,
                                    self._w, QFontMetrics(self._font_text).height()),
                             Qt.AlignCenter, self.text)

        if self._hovered:
            painter.setFont(self._font_btn)
            self._draw_btn(painter, QRectF(self._w / 2 - hbs, self._h - hbs, bs, bs), "+", C_BTN_ADD)
            if not self.is_root:
                self._draw_btn(painter, QRectF(self._w - hbs, self._h / 2 - hbs, bs, bs), "+", C_BTN_SIB)
                self._draw_btn(painter, QRectF(-hbs, self._h / 2 - hbs, bs, bs), "−", C_BTN_DEL)

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
            rects["delete"]  = QRectF(-hbs, self._h / 2 - hbs, bs, bs)
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
                    if action == "child":
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
        w  = max(100, int(scene_rect.width()))
        h  = 30
        self.setGeometry(tl.x(), tl.y() + int(scene_rect.height() / 2) - h // 2, w, h)
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


class EAPWidget(QWidget):
    """Widget completo do EAP para embutir no app principal."""
    def __init__(self):
        super().__init__()

        self.base_pad_x      = 35
        self.base_pad_y      = 60
        self.base_min_width  = 100
        self.base_box_height = 40
        self.zoom            = 1.0
        self.next_id         = 2
        self.wbs_numbers     = {}
        self.node_dimensions = {}
        self.node_positions  = {}
        self._scene_items    = []
        self.nodes = {1: {"text": "", "children": [], "parent": None, "shape": "roundrect"}}
        self.signals = NodeSignals()
        self.signals.commit_text.connect(self._on_commit)
        self.signals.add_child.connect(self._on_add_child)
        self.signals.add_sibling.connect(self._on_add_sibling)
        self.signals.delete_node.connect(self._on_delete)
        self.signals.edit_start.connect(self._on_edit_start)

        self._setup_ui()

        self._float_editor = FloatingEditor(self.view)
        self._float_editor.committed.connect(self._on_commit)
        self.update_zoom(1.0)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QWidget()
        toolbar.setFixedHeight(44)
        toolbar.setStyleSheet(f"""
            QWidget {{ background:{C_BG_APP}; border-bottom:1px solid {C_BORDER}; }}
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

        title = QLabel("EAP — Estrutura Analítica do Projeto")
        title.setStyleSheet(
            f"color:{C_BORDER_ROOT}; font-family:'Consolas';"
            f" font-size:13px; font-weight:bold; background:transparent;")
        tb.addWidget(title)

        sep = QWidget(); sep.setFixedSize(1, 26)
        sep.setStyleSheet(f"background:{C_BORDER};")
        tb.addWidget(sep)

        for lbl, fn in [("🔍−", lambda *a: self.zoom_out()),
                         ("🔍+", lambda *a: self.zoom_in()),
                         ("⟳ 100%", lambda *a: self.update_zoom(1.0))]:
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

    def _create_shape_icon(self, shape_type):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(C_BORDER), 2))
        painter.setBrush(QBrush(QColor(C_BG_NODE)))
        rect = QRectF(4, 4, 24, 24)
        if shape_type == "roundrect":
            painter.drawRoundedRect(rect, 4, 4)
        elif shape_type == "ellipse":
            painter.drawEllipse(rect)
        elif shape_type == "diamond":
            poly = QPolygonF([QPointF(16, 4), QPointF(28, 16), QPointF(16, 28), QPointF(4, 16)])
            painter.drawPolygon(poly)
        painter.end()
        return QIcon(pixmap)

    def _choose_shape(self):
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{ background-color: {C_BG_NODE}; color: {C_TEXT_MAIN};
                    border: 1px solid {C_BORDER}; font-family: 'Segoe UI'; font-size: 10pt; }}
            QMenu::item {{ padding: 6px 24px 6px 36px; }}
            QMenu::item:selected {{ background-color: {C_BORDER}; color: #0D0D0D; }}
            QMenu::icon {{ padding-left: 10px; }}
        """)
        action_rect    = menu.addAction(self._create_shape_icon("roundrect"), "Retângulo Arredondado")
        action_ellipse = menu.addAction(self._create_shape_icon("ellipse"),   "Elipse (Círculo)")
        action_diamond = menu.addAction(self._create_shape_icon("diamond"),   "Losango (Decisão)")
        selected = menu.exec_(QCursor.pos())
        if selected == action_rect:    return "roundrect"
        if selected == action_ellipse: return "ellipse"
        if selected == action_diamond: return "diamond"
        return None

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
        self._float_editor.open(node_id, self.nodes[node_id]["text"], scene_r, self.view)

    def _on_add_child(self, parent_id):
        shape = self._choose_shape()
        if not shape: return
        new_id = self.next_id; self.next_id += 1
        self.nodes[new_id] = {"text": "", "children": [], "parent": parent_id, "shape": shape}
        self.nodes[parent_id]["children"].append(new_id)
        self.draw_eap()
        QTimer.singleShot(60, lambda n=new_id: self._on_edit_start(n))

    def _on_add_sibling(self, node_id):
        parent_id = self.nodes[node_id]["parent"]
        if parent_id is None: return
        shape = self._choose_shape()
        if not shape: return
        new_id = self.next_id; self.next_id += 1
        self.nodes[new_id] = {"text": "", "children": [], "parent": parent_id, "shape": shape}
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
            shape = self.nodes[nid].get("shape", "roundrect")
            tmp = NodeItem(nid, self.wbs_numbers.get(nid, ""),
                           self.nodes[nid]["text"], nid == 1,
                           shape, self.signals, self.zoom)
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
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-40, -40, 40, 40))

    def _draw_connections(self, node_id):
        filhos = self.nodes[node_id]["children"]
        if not filhos: return
        px, py = self.node_positions[node_id]
        _, ph  = self.node_dimensions[node_id]
        py_bot = py + ph / 2
        mid_y  = py_bot + self.pad_y / 2
        pen    = QPen(QColor(C_LINE_EAP), max(1, int(2 * self.zoom)),
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
            shape  = self.nodes[nid].get("shape", "roundrect")
            item = NodeItem(nid, self.wbs_numbers[nid],
                            self.nodes[nid]["text"],
                            nid == 1, shape, self.signals, self.zoom)
            item.setPos(x - nw / 2, y - nh / 2)
            self.scene.addItem(item)
            self._scene_items.append(item)


# ==========================================
# ==========================================
#   TELA DE SELEÇÃO
# ==========================================
# ==========================================

class SelectionScreen(QWidget):
    def __init__(self, on_select):
        super().__init__()
        self.on_select = on_select
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Fundo
        self.setStyleSheet(f"background-color: {C_BG_APP};")

        # Título principal
        title = QLabel("⚙ EAP-FLOWSHEET")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {C_BORDER_ROOT};
            font-family: 'Consolas', monospace;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 4px;
            padding-bottom: 6px;
        """)
        layout.addStretch(1)
        layout.addWidget(title)

        subtitle = QLabel("Selecione o módulo que deseja utilizar")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            color: {C_PLACEHOLDER};
            font-family: 'Segoe UI';
            font-size: 13px;
            padding-bottom: 50px;
        """)
        layout.addWidget(subtitle)

        # Botões de seleção
        btn_row = QWidget()
        btn_row.setStyleSheet("background: transparent;")
        btn_layout = QHBoxLayout(btn_row)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(40)

        card_style = f"""
            QPushButton {{
                background-color: {C_BG_NODE};
                color: {C_TEXT_MAIN};
                border: 2px solid {C_BORDER};
                border-radius: 12px;
                font-family: 'Segoe UI';
                font-size: 15px;
                font-weight: bold;
                padding: 30px 50px;
                min-width: 220px;
                min-height: 120px;
            }}
            QPushButton:hover {{
                background-color: {C_BG_ROOT};
                border-color: {C_BORDER_ROOT};
                color: #FFFFFF;
            }}
            QPushButton:pressed {{
                background-color: {C_BORDER};
                color: #0D0D0D;
            }}
        """

        btn_flowsheet = QPushButton("🏭 Flowsheet\n\nDiagrama de processo\ncom equipamentos industriais")
        btn_flowsheet.setStyleSheet(card_style)
        btn_flowsheet.clicked.connect(lambda: self.on_select("flowsheet"))

        btn_eap = QPushButton("📋  EAP\n\nEstrutura Analítica\ndo Projeto (WBS)")
        btn_eap.setStyleSheet(card_style)
        btn_eap.clicked.connect(lambda: self.on_select("eap"))

        btn_layout.addWidget(btn_flowsheet)
        btn_layout.addWidget(btn_eap)
        layout.addWidget(btn_row)

        # Rodapé
        footer = QLabel("Ctrl+Scroll para zoom  •  Clique direito para opções")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet(f"""
            color: #3A1515;
            font-family: 'Segoe UI';
            font-size: 11px;
            padding-top: 50px;
        """)
        layout.addWidget(footer)
        layout.addStretch(1)


# ==========================================
# ==========================================
#   JANELA PRINCIPAL (UNIFICADA)
# ==========================================
# ==========================================

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro Eng Tools")
        self.setGeometry(100, 100, 1300, 800)
        self._setup_palette()

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        # Tela de seleção
        self._selection = SelectionScreen(self._open_module)
        self._stack.addWidget(self._selection)  # index 0

        # Módulos (criados sob demanda)
        self._flowsheet_widget = None
        self._eap_widget       = None

        self._stack.setCurrentIndex(0)

    def _setup_palette(self):
        p = QPalette()
        p.setColor(QPalette.Window,          QColor(C_BG_APP))
        p.setColor(QPalette.WindowText,      QColor(C_TEXT_MAIN))
        p.setColor(QPalette.Base,            QColor(C_BG_NODE))
        p.setColor(QPalette.AlternateBase,   QColor(C_BG_ROOT))
        p.setColor(QPalette.Text,            QColor(C_TEXT_MAIN))
        p.setColor(QPalette.Button,          QColor(C_BG_NODE))
        p.setColor(QPalette.ButtonText,      QColor(C_TEXT_MAIN))
        p.setColor(QPalette.Highlight,       QColor(C_BORDER))
        p.setColor(QPalette.HighlightedText, QColor(C_BG_APP))
        QApplication.instance().setPalette(p)

    def _open_module(self, module_name):
        if module_name == "flowsheet":
            if self._flowsheet_widget is None:
                self._flowsheet_widget = self._wrap_module(FlowsheetWidget(), "🏭  PFD Flowsheet")
                self._stack.addWidget(self._flowsheet_widget)
            self._stack.setCurrentWidget(self._flowsheet_widget)
            self.setWindowTitle("Pro Eng Tools — PFD Flowsheet")

        elif module_name == "eap":
            if self._eap_widget is None:
                self._eap_widget = self._wrap_module(EAPWidget(), "📋  EAP")
                self._stack.addWidget(self._eap_widget)
            self._stack.setCurrentWidget(self._eap_widget)
            self.setWindowTitle("Pro Eng Tools — EAP")

    def _wrap_module(self, module_widget, title):
        """Envolve o widget do módulo com uma barra de retorno ao menu."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Barra de retorno
        nav_bar = QWidget()
        nav_bar.setFixedHeight(34)
        nav_bar.setStyleSheet(
            f"background-color: {C_BG_APP}; border-bottom: 1px solid #2A0F0F;")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(8, 0, 8, 0)

        btn_back = QPushButton("◀  Menu Principal")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C_PLACEHOLDER};
                border: none; font-family: 'Segoe UI'; font-size: 11px;
                padding: 2px 10px;
            }}
            QPushButton:hover {{ color: {C_TEXT_MAIN}; }}
        """)
        btn_back.clicked.connect(self._go_home)
        nav_layout.addWidget(btn_back)

        lbl = QLabel(title)
        lbl.setStyleSheet(f"color: {C_BORDER}; font-family:'Consolas'; font-size:11px;"
                          f" font-weight:bold; background:transparent;")
        nav_layout.addStretch()
        nav_layout.addWidget(lbl)

        layout.addWidget(nav_bar)
        layout.addWidget(module_widget)
        return container

    def _go_home(self):
        self._stack.setCurrentIndex(0)
        self.setWindowTitle("Pro Eng Tools")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainApp()
    w.show()
    sys.exit(app.exec_())