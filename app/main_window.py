# --- START OF FILE app/main_window.py ---

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QListWidget, QStackedWidget, QMessageBox, QDialog, 
    QFormLayout, QLineEdit, QComboBox, QDialogButtonBox,
    QTableWidgetItem, QHeaderView, QTabWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from datetime import datetime

# Importaciones relativas a la nueva estructura del proyecto
from .database_manager import DatabaseManager
from .interface import (
    DashboardPage, MembersPage, AttendancePage, PaymentsPage,
    MembershipsPage, EarningsPage, TrainersPage, ExpensesPage,
    PaymentConfirmationDialog, EditPaymentDialog, EditExpenseDialog,
    EditTrainerPaymentDialog, OtherPaymentsDialog
)

GLOBAL_STYLE = "QMainWindow { background-color: #fdfdfd; } QListWidget { border: none; outline: 0; background-color: #e8eff6; font-size: 16px; } QListWidget::item { padding: 15px 20px; border-bottom: 1px solid #dce5ee; color: #333; } QListWidget::item:hover { background-color: #d8e2ec; } QListWidget::item:selected { background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2a9dff, stop: 1 #007bff); color: white; font-weight: bold; border-left: 5px solid #0056b3; border-bottom-color: #0056b3; } QMessageBox { font-size: 16px; } QMessageBox QLabel { font-size: 16px; } QMessageBox QPushButton { font-size: 16px; padding: 10px; min-width: 100px; }"

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Instancia del gestor de base de datos
        self.db_manager = DatabaseManager()
        
        # --- LÓGICA DE CONEXIÓN TEMPORAL PARA PRUEBAS ---
        # En el siguiente paso, esto será reemplazado por la pantalla de login.
        # Por ahora, nos conectaremos a un tenant de prueba.
        
        # 1. (Simulado) Crear un tenant de prueba si no existe
        self.db_manager.create_tenant("testuser", "testpass", "Gimnasio de Prueba")
        
        # 2. Obtener la conexión para ese tenant
        self.db_conn = self.db_manager.get_tenant_connection("tenant_testuser")
        
        if not self.db_conn:
            QMessageBox.critical(self, "Error de Conexión", 
                                 "No se pudo establecer la conexión con la base de datos del tenant.\n"
                                 "La aplicación se cerrará.")
            sys.exit(1) # Cierra la aplicación si no hay conexión
        # ----------------------------------------------------

        self.setWindowTitle("JCFitness - Administración")
        self.resize(1400, 900)
        self.setStyleSheet(GLOBAL_STYLE)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_widget)

        self.nav_menu = QListWidget()
        self.nav_menu.setFixedWidth(220)
        self.nav_menu.addItems(["Dashboard", "Miembros", "Asistencias", "Pagos", "Membresías", "Ganancias", "Entrenadores", "Gastos"])
        
        self.pages = QStackedWidget()
        
        # Instanciar TODAS las páginas
        self.dashboard_page = DashboardPage(self)
        self.members_page = MembersPage(self)
        self.attendance_page = AttendancePage(self)
        self.payments_page = PaymentsPage(self)
        self.memberships_page = MembershipsPage(self)
        self.earnings_page = EarningsPage(self)
        self.trainers_page = TrainersPage(self)
        self.expenses_page = ExpensesPage(self)
        
        # Añadir TODAS las páginas al StackedWidget
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.members_page)
        self.pages.addWidget(self.attendance_page)
        self.pages.addWidget(self.payments_page)
        self.pages.addWidget(self.memberships_page)
        self.pages.addWidget(self.earnings_page)
        self.pages.addWidget(self.trainers_page)
        self.pages.addWidget(self.expenses_page)

        main_layout.addWidget(self.nav_menu)
        main_layout.addWidget(self.pages)
        
        self.nav_menu.currentItemChanged.connect(self.change_page)
        # self.connect_signals() # Conectaremos las señales en el siguiente paso

        self.nav_menu.setCurrentRow(0)
        # self.load_all_data() # Cargaremos los datos en el siguiente paso

    def change_page(self, current_item):
        row = self.nav_menu.row(current_item)
        self.pages.setCurrentIndex(row)
        # La lógica de carga de datos se añadirá aquí después

    def closeEvent(self, event):
        """Asegura que la conexión a la base de datos se cierre al salir."""
        if self.db_conn:
            self.db_conn.close()
            print("Conexión a la base de datos del tenant cerrada.")
        super().closeEvent(event)

    # Aquí irán todas las demás funciones de lógica (load_members, register_payment, etc.)
    # Las añadiremos en el siguiente paso, adaptadas para usar self.db_conn.