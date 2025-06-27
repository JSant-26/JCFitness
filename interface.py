# --- START OF FILE interface.py ---

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QListWidget, QLabel, QDateEdit, QComboBox, 
    QTableWidget, QHeaderView, QGroupBox, QTabWidget
)
from PyQt6.QtCore import QDate, Qt, QSize
from PyQt6.QtGui import QIcon

# --- ESTILOS (Puedes moverlos a un archivo separado si quieres) ---
LARGE_BUTTON_STYLE = """
    QPushButton {
        font-size: 15px; padding: 12px; min-width: 150px;
    }"""
LARGE_LABEL_STYLE = "QLabel { font-size: 16px; }"
LARGE_LINEEDIT_STYLE = "QLineEdit, QDateEdit, QComboBox { font-size: 16px; padding: 8px; }"
LARGE_TABLE_STYLE = """
    QTableWidget { font-size: 14px; }
    QHeaderView::section { font-size: 14px; padding: 8px; background-color: #f0f0f0; }
"""
DASHBOARD_BOX_STYLE = """
    QGroupBox {
        font-size: 18px;
        font-weight: bold;
        border: 1px solid #cccccc;
        border-radius: 8px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 5px 10px;
    }
    QLabel {
        font-size: 16px;
        font-weight: normal;
    }
    QLabel#valueLabel {
        font-size: 32px;
        font-weight: bold;
        color: #007BFF;
    }
"""

# --- PÁGINA DEL DASHBOARD ---
class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel("Resumen General - JCFitness")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Contenedor para las cajas de resumen
        summary_layout = QHBoxLayout()
        
        # Caja 1: Ganancias del día
        self.earnings_box = QGroupBox("Ganancias de Hoy")
        self.earnings_box.setStyleSheet(DASHBOARD_BOX_STYLE)
        box1_layout = QVBoxLayout()
        self.earnings_label = QLabel("$0")
        self.earnings_label.setObjectName("valueLabel")
        box1_layout.addWidget(self.earnings_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.earnings_box.setLayout(box1_layout)
        
        # Caja 2: Miembros Presentes
        self.present_box = QGroupBox("Miembros Presentes")
        self.present_box.setStyleSheet(DASHBOARD_BOX_STYLE)
        box2_layout = QVBoxLayout()
        self.present_label = QLabel("0")
        self.present_label.setObjectName("valueLabel")
        box2_layout.addWidget(self.present_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.present_box.setLayout(box2_layout)
        
        # Caja 3: Membresías Activas
        self.active_box = QGroupBox("Membresías Activas")
        self.active_box.setStyleSheet(DASHBOARD_BOX_STYLE)
        box3_layout = QVBoxLayout()
        self.active_label = QLabel("0")
        self.active_label.setObjectName("valueLabel")
        box3_layout.addWidget(self.active_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.active_box.setLayout(box3_layout)

        # Caja 4: Membresías por Vencer
        self.expiring_box = QGroupBox("Por Vencer (7 días)")
        self.expiring_box.setStyleSheet(DASHBOARD_BOX_STYLE)
        box4_layout = QVBoxLayout()
        self.expiring_label = QLabel("0")
        self.expiring_label.setObjectName("valueLabel")
        box4_layout.addWidget(self.expiring_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.expiring_box.setLayout(box4_layout)
        
        summary_layout.addWidget(self.earnings_box)
        summary_layout.addWidget(self.present_box)
        summary_layout.addWidget(self.active_box)
        summary_layout.addWidget(self.expiring_box)
        
        layout.addLayout(summary_layout)

        # Botón de refrescar
        self.refresh_button = QPushButton("Actualizar Datos")
        self.refresh_button.setStyleSheet(LARGE_BUTTON_STYLE)
        layout.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

# --- PÁGINA DE MIEMBROS ---
class MembersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        self.member_name = QLineEdit()
        self.member_lastname = QLineEdit()
        self.member_gender = QComboBox()
        self.member_gender.addItems(["Masculino", "Femenino"])
        
        form.addRow(QLabel("Nombre:"), self.member_name)
        form.addRow(QLabel("Apellido:"), self.member_lastname)
        form.addRow(QLabel("Sexo:"), self.member_gender)
        
        self.btn_add = QPushButton("Registrar Miembro")
        
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(5)
        self.members_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Sexo", "Fecha Registro"])
        self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.members_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        btn_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Editar Miembro")
        self.btn_delete = QPushButton("Eliminar Miembro")
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        
        self.member_search = QLineEdit()
        self.member_search.setPlaceholderText("Buscar por nombre o apellido...")
        
        # Aplicar estilos
        for widget in [self.member_name, self.member_lastname, self.member_gender, self.member_search]:
            widget.setStyleSheet(LARGE_LINEEDIT_STYLE)
        for btn in [self.btn_add, self.btn_edit, self.btn_delete]:
            btn.setStyleSheet(LARGE_BUTTON_STYLE)
        self.members_table.setStyleSheet(LARGE_TABLE_STYLE)
        
        layout.addLayout(form)
        layout.addWidget(self.btn_add)
        layout.addWidget(QLabel("<h3>Buscar Miembros</h3>"))
        layout.addWidget(self.member_search)
        layout.addWidget(self.members_table)
        layout.addLayout(btn_layout)

# --- PÁGINA DE ASISTENCIAS ---
class AttendancePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        attendance_tabs = QTabWidget()
        
        # Subpestaña de Registro
        reg_tab = QWidget()
        reg_layout = QVBoxLayout(reg_tab)
        self.search_attendance = QLineEdit()
        self.search_attendance.setPlaceholderText("Buscar por nombre o apellido...")
        self.attendance_table_reg = QTableWidget()
        self.attendance_table_reg.setColumnCount(3)
        self.attendance_table_reg.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido"])
        self.attendance_table_reg.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.attendance_table_reg.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        header = self.attendance_table_reg.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        btn_layout_reg = QHBoxLayout()
        self.btn_checkin = QPushButton("Registrar Entrada")
        self.btn_checkout = QPushButton("Registrar Salida")
        btn_layout_reg.addWidget(self.btn_checkin)
        btn_layout_reg.addWidget(self.btn_checkout)
        
        reg_layout.addWidget(self.search_attendance)
        reg_layout.addWidget(self.attendance_table_reg)
        reg_layout.addLayout(btn_layout_reg)
        
        # Subpestaña de Visualización
        view_tab = QWidget()
        view_layout = QVBoxLayout(view_tab)
        date_layout = QHBoxLayout()
        self.attendance_view_date = QDateEdit(QDate.currentDate())
        self.attendance_view_date.setCalendarPopup(True)
        self.btn_load_attendance = QPushButton("Cargar Asistencias")
        date_layout.addWidget(QLabel("Fecha:"))
        date_layout.addWidget(self.attendance_view_date)
        date_layout.addWidget(self.btn_load_attendance)
        date_layout.addStretch()
        
        self.attendance_table_view = QTableWidget()
        self.attendance_table_view.setColumnCount(6)
        self.attendance_table_view.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Entrada", "Salida", "Tiempo Total"])
        self.attendance_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        view_layout.addLayout(date_layout)
        view_layout.addWidget(self.attendance_table_view)
        
        attendance_tabs.addTab(reg_tab, "Registro de Asistencia")
        attendance_tabs.addTab(view_tab, "Ver Asistencias por Día")
        
        # Estilos
        self.search_attendance.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.attendance_view_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.btn_checkin.setStyleSheet(LARGE_BUTTON_STYLE)
        self.btn_checkout.setStyleSheet(LARGE_BUTTON_STYLE)
        self.btn_load_attendance.setStyleSheet(LARGE_BUTTON_STYLE)
        self.attendance_table_reg.setStyleSheet(LARGE_TABLE_STYLE)
        self.attendance_table_view.setStyleSheet(LARGE_TABLE_STYLE)
        
        layout.addWidget(attendance_tabs)
        
# --- Y así sucesivamente para las otras páginas (Pagos, Membresías, etc.) ---
# Por brevedad, solo he incluido las 3 primeras. El patrón es el mismo:
# 1. Crear una clase que herede de QWidget.
# 2. Copiar el código de creación de la UI del método `create_..._tab` original.
# 3. Guardar los widgets importantes (tablas, lineedits, botones) como atributos de la clase (e.g., self.mi_widget).

class PaymentsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.payment_search = QLineEdit()
        self.payment_search.setPlaceholderText("Buscar por nombre o apellido...")
        
        self.payment_member_table = QTableWidget()
        self.payment_member_table.setColumnCount(3)
        self.payment_member_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido"])
        self.payment_member_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.payment_member_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        header = self.payment_member_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        self.payment_date = QDateEdit(QDate.currentDate())
        self.payment_date.setCalendarPopup(True)
        self.payment_date.setDisplayFormat("dd/MM/yyyy")
        
        form.addRow(QLabel("Buscar Miembro:"), self.payment_search)
        form.addRow(self.payment_member_table)
        form.addRow(QLabel("Fecha de Pago:"), self.payment_date)
        
        payment_buttons = QHBoxLayout()
        self.btn_daily = QPushButton("Pago Diario ($4,000)")
        self.btn_monthly = QPushButton("Pago Mensual ($55,000)")
        payment_buttons.addWidget(self.btn_daily)
        payment_buttons.addWidget(self.btn_monthly)
        
        layout.addLayout(form)
        layout.addLayout(payment_buttons)

        # Estilos
        self.payment_search.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.payment_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.payment_member_table.setStyleSheet(LARGE_TABLE_STYLE)
        self.btn_daily.setStyleSheet(LARGE_BUTTON_STYLE)
        self.btn_monthly.setStyleSheet(LARGE_BUTTON_STYLE)

# --- PÁGINA DE MEMBRESÍAS ---
class MembershipsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        search_layout = QHBoxLayout()
        self.membership_search = QLineEdit()
        self.membership_search.setPlaceholderText("Buscar por nombre o apellido...")
        self.btn_refresh = QPushButton("Actualizar Lista")
        search_layout.addWidget(QLabel("Buscar:"))
        search_layout.addWidget(self.membership_search)
        search_layout.addWidget(self.btn_refresh)
        
        self.memberships_table = QTableWidget()
        self.memberships_table.setColumnCount(6)
        self.memberships_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Fecha Pago", "Vencimiento", "Días Restantes"])
        self.memberships_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.memberships_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addLayout(search_layout)
        layout.addWidget(self.memberships_table)
        
        # Estilos
        self.membership_search.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.btn_refresh.setStyleSheet(LARGE_BUTTON_STYLE)
        self.memberships_table.setStyleSheet(LARGE_TABLE_STYLE)

# --- PÁGINA DE GANANCIAS ---
class EarningsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        earnings_tabs = QTabWidget()
        
        # Pestaña Mensual
        monthly_tab = QWidget()
        monthly_layout = QVBoxLayout(monthly_tab)
        self.monthly_earnings_table = QTableWidget()
        self.monthly_earnings_table.setColumnCount(5)
        self.monthly_earnings_table.setHorizontalHeaderLabels(["Mes", "Total Ganancias", "Gastos", "Ganancia Neta", "N° Pagos"])
        self.monthly_earnings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        monthly_layout.addWidget(QLabel("<b>Ganancias Mensuales</b>"))
        monthly_layout.addWidget(self.monthly_earnings_table)
        
        # Pestaña Diaria
        daily_tab = QWidget()
        daily_layout = QVBoxLayout(daily_tab)
        top_daily_layout = QHBoxLayout()
        self.daily_earnings_date = QDateEdit(QDate.currentDate())
        self.daily_earnings_date.setCalendarPopup(True)
        self.btn_load_daily = QPushButton("Cargar Día")
        self.daily_net_total = QLabel("Total Neto: $0.00")
        self.daily_net_total.setStyleSheet("font-weight: bold; font-size: 16px;")
        top_daily_layout.addWidget(QLabel("Fecha:"))
        top_daily_layout.addWidget(self.daily_earnings_date)
        top_daily_layout.addWidget(self.btn_load_daily)
        top_daily_layout.addStretch()
        top_daily_layout.addWidget(self.daily_net_total)
        
        self.daily_earnings_table = QTableWidget()
        self.daily_earnings_table.setColumnCount(3)
        self.daily_earnings_table.setHorizontalHeaderLabels(["Hora", "Miembro", "Monto"])
        self.daily_earnings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        daily_layout.addWidget(QLabel("<b>Ganancias Diarias</b>"))
        daily_layout.addLayout(top_daily_layout)
        daily_layout.addWidget(self.daily_earnings_table)
        
        earnings_tabs.addTab(monthly_tab, "Resumen Mensual")
        earnings_tabs.addTab(daily_tab, "Detalle Diario")
        layout.addWidget(earnings_tabs)

        # Estilos
        self.monthly_earnings_table.setStyleSheet(LARGE_TABLE_STYLE)
        self.daily_earnings_table.setStyleSheet(LARGE_TABLE_STYLE)
        self.daily_earnings_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.btn_load_daily.setStyleSheet(LARGE_BUTTON_STYLE)

# --- PÁGINA DE ENTRENADORES ---
class TrainersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        reg_group = QGroupBox("Registrar Nuevo Entrenador")
        form_new = QFormLayout(reg_group)
        self.trainer_name = QLineEdit()
        self.trainer_lastname = QLineEdit()
        self.btn_add_trainer = QPushButton("Registrar Entrenador")
        form_new.addRow(QLabel("Nombre:"), self.trainer_name)
        form_new.addRow(QLabel("Apellido:"), self.trainer_lastname)
        form_new.addRow(self.btn_add_trainer)
        
        payment_group = QGroupBox("Registrar Pago a Entrenador")
        form_payment = QFormLayout(payment_group)
        self.trainer_combo = QComboBox()
        self.trainer_amount = QLineEdit()
        self.trainer_date = QDateEdit(QDate.currentDate())
        self.trainer_date.setCalendarPopup(True)
        self.btn_pay_trainer = QPushButton("Registrar Pago")
        form_payment.addRow(QLabel("Entrenador:"), self.trainer_combo)
        form_payment.addRow(QLabel("Monto:"), self.trainer_amount)
        form_payment.addRow(QLabel("Fecha:"), self.trainer_date)
        form_payment.addRow(self.btn_pay_trainer)
        
        self.trainers_table = QTableWidget()
        self.trainers_table.setColumnCount(3)
        self.trainers_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido"])
        self.trainers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(reg_group)
        layout.addWidget(payment_group)
        layout.addWidget(QLabel("<h3>Entrenadores Registrados</h3>"))
        layout.addWidget(self.trainers_table)

        # Estilos
        for widget in [self.trainer_name, self.trainer_lastname, self.trainer_combo, self.trainer_amount, self.trainer_date]:
            widget.setStyleSheet(LARGE_LINEEDIT_STYLE)
        for btn in [self.btn_add_trainer, self.btn_pay_trainer]:
            btn.setStyleSheet(LARGE_BUTTON_STYLE)
        self.trainers_table.setStyleSheet(LARGE_TABLE_STYLE)
        
# --- PÁGINA DE GASTOS ---
class ExpensesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Pestañas para Gastos Diarios y Gastos del Día
        expenses_tabs = QTabWidget()

        # Sub-pestaña para Registrar Gastos Diarios
        daily_reg_tab = QWidget()
        daily_reg_layout = QVBoxLayout(daily_reg_tab)

        form = QFormLayout()
        self.expense_admin = QLineEdit("0")
        self.expense_cleaning = QLineEdit("0")
        self.expense_trainers = QLineEdit("0")
        self.expense_trainers.setReadOnly(True)
        self.btn_register_expenses = QPushButton("Registrar Gastos de Hoy")
        
        form.addRow(QLabel("Gasto Administración:"), self.expense_admin)
        form.addRow(QLabel("Gasto Aseo:"), self.expense_cleaning)
        form.addRow(QLabel("Total Entrenadores (Automático):"), self.expense_trainers)

        self.monthly_expenses_table = QTableWidget()
        self.monthly_expenses_table.setColumnCount(5)
        self.monthly_expenses_table.setHorizontalHeaderLabels(["Mes", "Administración", "Aseo", "Entrenadores", "Total"])
        self.monthly_expenses_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        daily_reg_layout.addLayout(form)
        daily_reg_layout.addWidget(self.btn_register_expenses)
        daily_reg_layout.addWidget(QLabel("<hr><b>Resumen Mensual de Gastos</b>"))
        daily_reg_layout.addWidget(self.monthly_expenses_table)
        expenses_tabs.addTab(daily_reg_tab, "Registro y Resumen Mensual")

        # Sub-pestaña para ver Gastos del Día
        daily_view_tab = QWidget()
        daily_view_layout = QVBoxLayout(daily_view_tab)
        top_layout = QHBoxLayout()
        self.daily_expenses_date = QDateEdit(QDate.currentDate())
        self.daily_expenses_date.setCalendarPopup(True)
        self.btn_load_daily_expenses = QPushButton("Cargar Gastos del Día")
        self.daily_expenses_total = QLabel("Total del Día: $0.00")
        self.daily_expenses_total.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        top_layout.addWidget(QLabel("Fecha:"))
        top_layout.addWidget(self.daily_expenses_date)
        top_layout.addWidget(self.btn_load_daily_expenses)
        top_layout.addStretch()
        top_layout.addWidget(self.daily_expenses_total)
        
        general_group = QGroupBox("Gastos Generales")
        general_layout = QVBoxLayout(general_group)
        self.daily_general_table = QTableWidget()
        self.daily_general_table.setColumnCount(4)
        self.daily_general_table.setHorizontalHeaderLabels(["Hora", "Administración", "Aseo", "Total Entrenadores"])
        self.daily_general_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        general_layout.addWidget(self.daily_general_table)
        
        trainers_group = QGroupBox("Pagos Detallados a Entrenadores")
        trainers_layout = QVBoxLayout(trainers_group)
        self.daily_trainers_table = QTableWidget()
        self.daily_trainers_table.setColumnCount(4)
        self.daily_trainers_table.setHorizontalHeaderLabels(["Hora", "Entrenador", "Monto", "Concepto"])
        self.daily_trainers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        trainers_layout.addWidget(self.daily_trainers_table)
        
        daily_view_layout.addLayout(top_layout)
        daily_view_layout.addWidget(general_group)
        daily_view_layout.addWidget(trainers_group)
        expenses_tabs.addTab(daily_view_tab, "Detalle de Gastos por Día")

        layout.addWidget(expenses_tabs)
        # Estilos
        for widget in [self.expense_admin, self.expense_cleaning, self.expense_trainers, self.daily_expenses_date]:
            widget.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.btn_register_expenses.setStyleSheet(LARGE_BUTTON_STYLE)
        self.btn_load_daily_expenses.setStyleSheet(LARGE_BUTTON_STYLE)
        for table in [self.monthly_expenses_table, self.daily_general_table, self.daily_trainers_table]:
            table.setStyleSheet(LARGE_TABLE_STYLE)
