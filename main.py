import sys
from PyQt6.QtWidgets import QApplication
from app import GymApp
from database import Database

def main():
    # Configurar aplicación
    app = QApplication(sys.argv)
    
    # Inicializar y mostrar ventana principal
    window = GymApp()
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
