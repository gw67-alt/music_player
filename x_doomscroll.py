from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPoint, QTimer
import sys

EMBED_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body, html { margin: 0; padding: 0; overflow:hidden; }
    </style>
  </head>
  <body>
    <a class="twitter-timeline" data-theme="dark" data-height="480" href="https://twitter.com/">Tweets</a>
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
  </body>
</html>
"""

class TwitterScroller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(380, 480)
        self.setWindowTitle("Twitter Scroller Mini")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.browser = QWebEngineView()
        self.browser.setHtml(EMBED_HTML)
        self.setCentralWidget(self.browser)
        self.show()

        self.old_pos = self.pos()

        # Autoscroll parameters
        self.scroll_amount = 2   # pixels per tick
        self.scroll_interval = 60  # milliseconds per tick

        self.current_scrollY = 0

        self.autoscroll_timer = QTimer(self)
        self.autoscroll_timer.timeout.connect(self.scroll_down)
        # Wait for content to load before starting autoscroll:
        self.browser.loadFinished.connect(self.start_autoscroll)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.old_pos)
        if event.buttons() == Qt.LeftButton:
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def start_autoscroll(self):
        # Start the timer after the page loads
        self.autoscroll_timer.start(self.scroll_interval)

    def scroll_down(self):
        # Scroll by incrementing the Y position
        self.current_scrollY += self.scroll_amount
        js = f"window.scrollTo(0, {self.current_scrollY})"
        self.browser.page().runJavaScript(js)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scroller = TwitterScroller()
    sys.exit(app.exec_())
