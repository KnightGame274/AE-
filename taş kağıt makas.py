import random
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taş - Kağıt - Makas Oyunu")
        self.setFixedSize(500, 600)
        
        self.user_score = 0
        self.computer_score = 0
        self.round_count = 0
        
        self.initUI()
        
    def initUI(self):
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Başlık
        title = QLabel("Taş - Kağıt - Makas")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        # Skor paneli
        score_layout = QHBoxLayout()
        self.user_score_label = QLabel("Sen: 0")
        self.computer_score_label = QLabel("Bilgisayar: 0")
        self.round_label = QLabel("Round: 0")
        
        for label in [self.user_score_label, self.computer_score_label, self.round_label]:
            label.setFont(QFont("Arial", 14))
            label.setStyleSheet("color: #34495e;")
            score_layout.addWidget(label)
        
        # Seçim görüntüleme alanı
        self.choice_display = QLabel()
        self.choice_display.setAlignment(Qt.AlignCenter)
        self.choice_display.setMinimumHeight(150)
        self.choice_display.setStyleSheet("border: 2px solid #bdc3c7; border-radius: 10px;")
        
        # Sonuç gösterimi
        self.result_label = QLabel("İlk oyuncu sen olmak için bir seçim yap!")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #7f8c8d; margin: 10px;")
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        self.rock_btn = QPushButton("Taş")
        self.paper_btn = QPushButton("Kağıt")
        self.scissors_btn = QPushButton("Makas")
        
        buttons = [self.rock_btn, self.paper_btn, self.scissors_btn]
        for btn in buttons:
            btn.setFont(QFont("Arial", 14))
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
            button_layout.addWidget(btn)
        
        # Buton eventleri
        self.rock_btn.clicked.connect(lambda: self.play_game('taş'))
        self.paper_btn.clicked.connect(lambda: self.play_game('kağıt'))
        self.scissors_btn.clicked.connect(lambda: self.play_game('makas'))
        
        # Yeniden başlat butonu
        restart_btn = QPushButton("Yeniden Başlat")
        restart_btn.setFont(QFont("Arial", 12))
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        restart_btn.clicked.connect(self.reset_game)
        
        # Layout'a widget'ları ekle
        layout.addWidget(title)
        layout.addLayout(score_layout)
        layout.addWidget(self.choice_display)
        layout.addWidget(self.result_label)
        layout.addLayout(button_layout)
        layout.addWidget(restart_btn)
        
        central_widget.setLayout(layout)
    
    def play_game(self, user_choice):
        choices = ['taş', 'kağıt', 'makas']
        computer_choice = random.choice(choices)
        
        self.round_count += 1
        self.round_label.setText(f"Round: {self.round_count}")
        
        # Sonuç hesapla
        result = self.determine_winner(user_choice, computer_choice)
        
        # Görsel gösterim
        display_text = f"Sen: {user_choice.upper()}  vs  Bilgisayar: {computer_choice.upper()}"
        self.choice_display.setText(display_text)
        
        # Sonucu göster ve skoru güncelle
        if result == 'user':
            self.user_score += 1
            self.result_label.setText("Kazandın! 🎉")
            self.result_label.setStyleSheet("color: #27ae60; font-size: 16px;")
        elif result == 'computer':
            self.computer_score += 1
            self.result_label.setText("Bilgisayar kazandı! 🤖")
            self.result_label.setStyleSheet("color: #e74c3c; font-size: 16px;")
        else:
            self.result_label.setText("Berabere! 🤝")
            self.result_label.setStyleSheet("color: #f39c12; font-size: 16px;")
        
        # Skorları güncelle
        self.user_score_label.setText(f"Sen: {self.user_score}")
        self.computer_score_label.setText(f"Bilgisayar: {self.computer_score}")
        
        # 5 round'da bir durumu göster
        if self.round_count % 5 == 0:
            self.show_progress()
    
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'tie'
        
        winning_conditions = {
            'taş': 'makas',
            'kağıt': 'taş',
            'makas': 'kağıt'
        }
        
        if winning_conditions[user_choice] == computer_choice:
            return 'user'
        else:
            return 'computer'
    
    def show_progress(self):
        if self.user_score > self.computer_score:
            message = "Tebrikler! Öndesiniz! 🚀"
        elif self.computer_score > self.user_score:
            message = "Bilgisayar önde! Daha iyisini yapabilirsin! 💪"
        else:
            message = "Berabere! İyi mücadele! ⚔️"
        
        QMessageBox.information(self, "5 Round Durumu", 
                               f"{message}\n\nSen: {self.user_score}\nBilgisayar: {self.computer_score}")
    
    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.round_count = 0
        
        self.user_score_label.setText("Sen: 0")
        self.computer_score_label.setText("Bilgisayar: 0")
        self.round_label.setText("Round: 0")
        self.choice_display.setText("")
        self.result_label.setText("İlk oyuncu sen olmak için bir seçim yap!")
        self.result_label.setStyleSheet("color: #7f8c8d; font-size: 16px;")

def main():
    app = QApplication(sys.argv)
    
    # Uygulama stilini ayarla
    app.setStyle('Fusion')
    
    game = RockPaperScissorsGame()
    game.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
