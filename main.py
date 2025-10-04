import sys
from PyQt6.QtWidgets import QApplication
# Importamos la ventana principal desde su nuevo archivo
from app.main_window import GymApp 

def main():
    """Punto de entrada principal de la aplicación."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Creamos una instancia de nuestra aplicación
    window = GymApp()
    window.show()
    
    # Ejecutamos el bucle de eventos de la aplicación
    sys.exit(app.exec())

if __name__ == "__main__":
    main()