import os
import sys
import requests
import pygame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton


class Delcatty(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicialização do mixer do pygame
        pygame.mixer.init()
        # Carrega o arquivo de áudio da trilha sonora
        trilha_sonora = pygame.mixer.music.load("OST.mp3")
        # Reproduz a trilha sonora em loop
        pygame.mixer.music.play(-1)
        self.setWindowTitle("Delcatty atrairá gatinhos!")
        self.setFixedSize(800, 600)

        # Definir o ícone da janela
        icon = QIcon("Delcatty.ico")  # Substitua pelo caminho do arquivo do ícone desejado
        self.setWindowIcon(icon)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(800, 600)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Definindo o fundo como preto
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)

        self.start_pause_button = QPushButton("Começar", self)
        self.start_pause_button.setFixedSize(100, 30)
        self.start_pause_button.move(20, 20)
        self.start_pause_button.setObjectName("control-button")
        self.start_pause_button.clicked.connect(self.start_pause_button_clicked)

        self.save_button = QPushButton("Salvar", self)
        self.save_button.setFixedSize(100, 30)
        self.save_button.move(20, 60)
        self.save_button.setObjectName("control-button")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_button_clicked)

        self.image_urls = []
        self.current_image_index = -1
        self.save_counter = 1
        self.save_directory = "gatinhos"
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_image)

        self.setStyleSheet(
            """
            #control-button {
                border: 3px groove rgba(0, 0, 0, 0.15);
                background-color: #F699BE;
            }
            #control-button:hover {
                border: 3px groove rgba(0, 0, 0, 0.25);
            }
            #control-button:pressed {
                border: 3px groove rgba(0, 0, 0, 0.35);
            }
            """
        )

    def start_pause_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_pause_button.setText("Começar")
            self.save_button.setEnabled(True)
        else:
            if not self.image_urls:
                self.search_cat_images()

            self.timer.start(5000)
            self.start_pause_button.setText("Pausar")
            self.save_button.setEnabled(False)

    def save_button_clicked(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_urls):
            image_url = self.image_urls[self.current_image_index]
            response = requests.get(image_url)
            if response.status_code == 200:
                # Cria o diretório "gatinhos" se não existir
                if not os.path.exists("gatinhos"):
                    os.makedirs("gatinhos")
                
                # Conta a quantidade de arquivos existentes no diretório "gatinhos"
                existing_files = len(os.listdir("gatinhos"))

                file_extension = os.path.splitext(image_url)[1]
                file_name = f"cat_image_{existing_files + 1}{file_extension}"
                file_path = os.path.join("gatinhos", file_name)
                
                with open(file_path, "wb") as file:
                    file.write(response.content)

    def search_cat_images(self):
        response = requests.get("https://api.thecatapi.com/v1/images/search?limit=10")
        if response.status_code == 200:
            data = response.json()
            self.image_urls = [image_data["url"] for image_data in data]

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_urls)
        image_url = self.image_urls[self.current_image_index]
        response = requests.get(image_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Delcatty()
    window.show()
    sys.exit(app.exec_())
