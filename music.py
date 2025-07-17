from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QPoint
import sys

class MiniPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set initial size for the mini player
        self.resize(480, 290)  # Window remains resizable
        self.setWindowTitle("YouTube Music Mini Player")

        # Remove window frame to make it look like a popup
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
        )

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://music.youtube.com/"))
        self.setCentralWidget(self.browser)

        self.show()

        self.old_pos = self.pos()

    # To allow dragging the frameless window around
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.old_pos)
        if event.buttons() == Qt.LeftButton:
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MiniPlayer()
    sys.exit(app.exec_())
