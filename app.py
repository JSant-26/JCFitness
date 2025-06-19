from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QLabel,  # Añade QListWidgetItem aquí
    QDateEdit, QComboBox, QMessageBox, QTableWidget, 
    QTableWidgetItem, QHeaderView, QDialog, QDialogButtonBox, 
    QGroupBox
)
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
from database import Database

# Configuración de accesibilidad
LARGE_FONT = ("Arial", 14)
LARGE_BUTTON_STYLE = """
    QPushButton {
        font-size: 16px;
        padding: 15px;
        min-width: 150px;
        min-height: 50px;
    }
"""
LARGE_LABEL_STYLE = "QLabel { font-size: 16px; }"
LARGE_LINEEDIT_STYLE = "QLineEdit { font-size: 16px; padding: 8px; }"
LARGE_TABLE_STYLE = """
    QTableWidget {
        font-size: 14px;
    }
    QHeaderView::section {
        font-size: 14px;
        padding: 8px;
    }
"""
LARGE_TAB_STYLE = """
    QTabWidget::pane {
        font-size: 16px;
    }
    QTabBar::tab {
        font-size: 16px;
        padding: 12px;
    }
"""
LARGE_MESSAGEBOX_STYLE = """
    QMessageBox {
        font-size: 16px;
    }
    QMessageBox QLabel {
        font-size: 16px;
    }
    QMessageBox QPushButton {
        font-size: 16px;
        padding: 10px;
        min-width: 100px;
    }
"""

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Aplicar estilos de accesibilidad
        self.setStyleSheet(
            LARGE_LABEL_STYLE + 
            LARGE_LINEEDIT_STYLE + 
            LARGE_TABLE_STYLE +
            LARGE_TAB_STYLE +
            LARGE_MESSAGEBOX_STYLE
        )
        
        self.db = Database()
        self.setWindowTitle("JCFitness - Administración")
        self.resize(1200, 800)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tabs.addTab(self.create_members_tab(), "Miembros")
        self.tabs.addTab(self.create_attendance_tab(), "Asistencias")
        self.tabs.addTab(self.create_payments_tab(), "Pagos")
        self.tabs.addTab(self.create_earnings_tab(), "Ganancias")  # Nueva pestaña
        self.tabs.addTab(self.create_trainers_tab(), "Entrenadores")
        self.tabs.addTab(self.create_expenses_tab(), "Gastos")
        self.tabs.addTab(self.create_daily_expenses_tab(), "Gastos Del Día")
    
    def create_members_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Formulario de registro
        form = QFormLayout()
        self.member_name = QLineEdit()
        self.member_name.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.member_lastname = QLineEdit()
        self.member_lastname.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.member_gender = QComboBox()
        self.member_gender.addItems(["Masculino", "Femenino"])
        self.member_gender.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        form.addRow(QLabel("Nombre:"), self.member_name)
        form.addRow(QLabel("Apellido:"), self.member_lastname)
        form.addRow(QLabel("Sexo:"), self.member_gender)
        
        btn_add = QPushButton("Registrar Miembro")
        btn_add.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_add.clicked.connect(self.add_member)
        
        # Tabla de miembros
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(5)
        self.members_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Sexo", "Fecha Registro"])
        self.members_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.members_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.load_members()
        
        # Botones de acciones
        btn_layout = QHBoxLayout()
        btn_edit = QPushButton("Editar Miembro")
        btn_edit.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_edit.clicked.connect(self.edit_member)
        
        btn_delete = QPushButton("Eliminar Miembro")
        btn_delete.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_delete.clicked.connect(self.delete_member)
        
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        
        # Barra de búsqueda
        self.member_search = QLineEdit()
        self.member_search.setPlaceholderText("Buscar por nombre o apellido...")
        self.member_search.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.member_search.textChanged.connect(self.filter_members_table)
        
        layout.addLayout(form)
        layout.addWidget(btn_add)
        layout.addWidget(self.member_search)
        layout.addWidget(self.members_table)
        layout.addLayout(btn_layout)
        tab.setLayout(layout)
        return tab
    
    def create_attendance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Barra de búsqueda
        self.search_attendance = QLineEdit()
        self.search_attendance.setPlaceholderText("Buscar por nombre o apellido...")
        self.search_attendance.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.search_attendance.textChanged.connect(self.filter_members_for_attendance)
        
        # Lista de miembros
        self.attendance_list = QListWidget()
        self.attendance_list.setStyleSheet("font-size: 16px;")
        self.load_members_for_attendance()
        
        # Botones de asistencia
        btn_layout = QHBoxLayout()
        btn_checkin = QPushButton("Registrar Entrada")
        btn_checkin.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_checkin.clicked.connect(self.register_checkin)
        
        btn_checkout = QPushButton("Registrar Salida")
        btn_checkout.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_checkout.clicked.connect(self.register_checkout)
        
        btn_layout.addWidget(btn_checkin)
        btn_layout.addWidget(btn_checkout)
        
        layout.addWidget(self.search_attendance)
        layout.addWidget(self.attendance_list)
        layout.addLayout(btn_layout)
        tab.setLayout(layout)
        return tab
    
    def create_payments_tab(self):
        """Pestaña simplificada solo para registrar pagos"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Sección de registro
        form = QFormLayout()
        
        # Búsqueda de miembros
        self.payment_search = QLineEdit()
        self.payment_search.setPlaceholderText("Buscar miembro...")
        self.payment_search.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.payment_search.textChanged.connect(self.filter_members_for_payments)
        
        self.payment_member_list = QListWidget()
        self.payment_member_list.setStyleSheet("font-size: 16px;")
        self.load_members_for_payments()
        
        self.payment_amount = QLineEdit()
        self.payment_amount.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        form.addRow(QLabel("Buscar Miembro:"), self.payment_search)
        form.addRow(self.payment_member_list)
        form.addRow(QLabel("Monto:"), self.payment_amount)
        
        btn_pay = QPushButton("Registrar Pago")
        btn_pay.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_pay.clicked.connect(self.register_payment)
        
        layout.addLayout(form)
        layout.addWidget(btn_pay)
        tab.setLayout(layout)
        return tab
    
# En la función create_earnings_tab (ya existe pero hay que asegurarse que use los nombres correctos)
    def create_earnings_tab(self):
        """Crea la pestaña de Ganancias con subpestañas para mensual y diario"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Crear el widget de pestañas
        earnings_tabs = QTabWidget()
        
        # Pestaña de ganancias mensuales
        monthly_tab = QWidget()
        monthly_layout = QVBoxLayout()
        
        self.monthly_earnings_table = QTableWidget()  # Este es el nombre correcto que se usa
        self.monthly_earnings_table.setColumnCount(3)
        self.monthly_earnings_table.setHorizontalHeaderLabels(["Mes", "Total Ganancias", "N° Pagos"])
        self.monthly_earnings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.load_monthly_earnings()
        
        monthly_layout.addWidget(QLabel("<b>Ganancias Mensuales</b>"))
        monthly_layout.addWidget(self.monthly_earnings_table)
        monthly_tab.setLayout(monthly_layout)
        
        # Pestaña de ganancias diarias
        daily_tab = QWidget()
        daily_layout = QVBoxLayout()
        
        self.daily_earnings_date = QDateEdit()  # Este es el nombre correcto que se usa
        self.daily_earnings_date.setDate(QDate.currentDate())
        self.daily_earnings_date.setCalendarPopup(True)
        self.daily_earnings_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        btn_load_daily = QPushButton("Cargar Ganancias del Día")
        btn_load_daily.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_load_daily.clicked.connect(self.load_daily_earnings)
        
        self.daily_earnings_table = QTableWidget()
        self.daily_earnings_table.setColumnCount(4)
        self.daily_earnings_table.setHorizontalHeaderLabels(["Hora", "Miembro", "Monto", "Tipo"])
        self.daily_earnings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        daily_layout.addWidget(QLabel("<b>Ganancias Diarias</b>"))
        daily_layout.addWidget(self.daily_earnings_date)
        daily_layout.addWidget(btn_load_daily)
        daily_layout.addWidget(self.daily_earnings_table)
        daily_tab.setLayout(daily_layout)
        
        # Añadir las subpestañas
        earnings_tabs.addTab(monthly_tab, "Resumen Mensual")
        earnings_tabs.addTab(daily_tab, "Detalle Diario")
        
        layout.addWidget(earnings_tabs)
        tab.setLayout(layout)
        return tab

    def create_trainers_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        form_new = QFormLayout()
        self.trainer_name = QLineEdit()
        self.trainer_name.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.trainer_lastname = QLineEdit()
        self.trainer_lastname.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        form_new.addRow(QLabel("Nombre:"), self.trainer_name)
        form_new.addRow(QLabel("Apellido:"), self.trainer_lastname)
        
        btn_add = QPushButton("Registrar Entrenador")
        btn_add.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_add.clicked.connect(self.add_trainer)
        
        form_payment = QFormLayout()
        self.trainer_combo = QComboBox()
        self.trainer_combo.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.load_trainers_combo()
        
        self.trainer_amount = QLineEdit()
        self.trainer_amount.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        self.trainer_date = QDateEdit()
        self.trainer_date.setDate(QDate.currentDate())
        self.trainer_date.setCalendarPopup(True)
        self.trainer_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        form_payment.addRow(QLabel("Entrenador:"), self.trainer_combo)
        form_payment.addRow(QLabel("Monto:"), self.trainer_amount)
        form_payment.addRow(QLabel("Fecha:"), self.trainer_date)
        
        btn_pay = QPushButton("Registrar Pago")
        btn_pay.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_pay.clicked.connect(self.register_trainer_payment)
        
        self.trainer_total_label = QLabel("Total hoy: $0.00")
        self.trainer_total_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        self.trainers_table = QTableWidget()
        self.trainers_table.setColumnCount(3)
        self.trainers_table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido"])
        self.trainers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.load_trainers()
        
        layout.addLayout(form_new)
        layout.addWidget(btn_add)
        layout.addLayout(form_payment)
        layout.addWidget(btn_pay)
        layout.addWidget(self.trainer_total_label)
        layout.addWidget(self.trainers_table)
        tab.setLayout(layout)
        return tab
    
    def create_expenses_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.expense_admin = QLineEdit("0")
        self.expense_admin.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.expense_cleaning = QLineEdit("0")
        self.expense_cleaning.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.expense_trainers = QLineEdit("0")
        self.expense_trainers.setReadOnly(True)
        self.expense_trainers.setStyleSheet(LARGE_LINEEDIT_STYLE)
        self.update_trainers_total()
        
        form.addRow(QLabel("Administración:"), self.expense_admin)
        form.addRow(QLabel("Aseo:"), self.expense_cleaning)
        form.addRow(QLabel("Total Entrenadores:"), self.expense_trainers)
        
        btn_expense = QPushButton("Registrar Gastos Diarios")
        btn_expense.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_expense.clicked.connect(self.register_expenses)
        
        self.monthly_table = QTableWidget()
        self.monthly_table.setColumnCount(5)
        self.monthly_table.setHorizontalHeaderLabels(["Mes", "Administración", "Aseo", "Entrenadores", "Total"])
        self.monthly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.load_monthly_expenses()
        
        layout.addLayout(form)
        layout.addWidget(btn_expense)
        layout.addWidget(QLabel("<hr><b>Resumen Mensual de Gastos</b>"))
        layout.addWidget(self.monthly_table)
        tab.setLayout(layout)
        return tab
    
    def create_daily_expenses_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        date_layout = QHBoxLayout()
        self.daily_expenses_date = QDateEdit()
        self.daily_expenses_date.setDate(QDate.currentDate())
        self.daily_expenses_date.setCalendarPopup(True)
        self.daily_expenses_date.setStyleSheet(LARGE_LINEEDIT_STYLE)
        
        btn_load = QPushButton("Cargar Gastos del Día")
        btn_load.setStyleSheet(LARGE_BUTTON_STYLE)
        btn_load.clicked.connect(self.load_daily_expenses_details)
        
        date_layout.addWidget(QLabel("Fecha:"))
        date_layout.addWidget(self.daily_expenses_date)
        date_layout.addWidget(btn_load)
        date_layout.addStretch()
        
        general_group = QGroupBox("Gastos Generales")
        general_layout = QVBoxLayout()
        
        self.daily_general_table = QTableWidget()
        self.daily_general_table.setColumnCount(4)
        self.daily_general_table.setHorizontalHeaderLabels(["Hora", "Administración", "Aseo", "Total Entrenadores"])
        self.daily_general_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        general_layout.addWidget(self.daily_general_table)
        general_group.setLayout(general_layout)
        
        trainers_group = QGroupBox("Pagos a Entrenadores")
        trainers_layout = QVBoxLayout()
        
        self.daily_trainers_table = QTableWidget()
        self.daily_trainers_table.setColumnCount(4)
        self.daily_trainers_table.setHorizontalHeaderLabels(["Hora", "Entrenador", "Monto", "Concepto"])
        self.daily_trainers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        trainers_layout.addWidget(self.daily_trainers_table)
        trainers_group.setLayout(trainers_layout)
        
        self.daily_total_label = QLabel("Total del día: $0.00")
        self.daily_total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        layout.addLayout(date_layout)
        layout.addWidget(general_group)
        layout.addWidget(trainers_group)
        layout.addWidget(self.daily_total_label)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab

    # Funciones para miembros
    def load_members(self):
        self.members_table.setRowCount(0)
        members = self.db.buscar_miembros()
        for row, member in enumerate(members):
            self.members_table.insertRow(row)
            self.members_table.setItem(row, 0, QTableWidgetItem(str(member['id_miembro'])))
            self.members_table.setItem(row, 1, QTableWidgetItem(member['nombre']))
            self.members_table.setItem(row, 2, QTableWidgetItem(member['apellido'] or ""))
            self.members_table.setItem(row, 3, QTableWidgetItem(member['sexo'] or ""))
            self.members_table.setItem(row, 4, QTableWidgetItem(member['fecha_registro']))

    def filter_members_table(self, text):
        if not text:
            for row in range(self.members_table.rowCount()):
                self.members_table.setRowHidden(row, False)
            return
        
        members = self.db.buscar_miembro_por_nombre(text)
        found_ids = {m['id_miembro'] for m in members}
        
        for row in range(self.members_table.rowCount()):
            item = self.members_table.item(row, 0)
            if item:
                member_id = int(item.text())
                self.members_table.setRowHidden(row, member_id not in found_ids)

    def load_members_for_attendance(self):
        self.attendance_list.clear()
        members = self.db.buscar_miembros()
        for member in members:
            item_text = f"{member['nombre']} {member['apellido']}" if member['apellido'] else member['nombre']
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, member['id_miembro'])
            self.attendance_list.addItem(item)

    def filter_members_for_attendance(self, text):
        if not text:
            for i in range(self.attendance_list.count()):
                self.attendance_list.item(i).setHidden(False)
            return
        
        members = self.db.buscar_miembro_por_nombre(text)
        found_ids = {m['id_miembro'] for m in members}
        
        for i in range(self.attendance_list.count()):
            item = self.attendance_list.item(i)
            item_id = item.data(Qt.ItemDataRole.UserRole)
            item.setHidden(item_id not in found_ids)

    def load_members_for_payments(self):
        self.payment_member_list.clear()
        members = self.db.buscar_miembros()
        for member in members:
            item_text = f"{member['nombre']} {member['apellido']}" if member['apellido'] else member['nombre']
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, member['id_miembro'])
            self.payment_member_list.addItem(item)

    def filter_members_for_payments(self, text):
        if not text:
            for i in range(self.payment_member_list.count()):
                self.payment_member_list.item(i).setHidden(False)
            return
        
        members = self.db.buscar_miembro_por_nombre(text)
        found_ids = {m['id_miembro'] for m in members}
        
        for i in range(self.payment_member_list.count()):
            item = self.payment_member_list.item(i)
            item_id = item.data(Qt.ItemDataRole.UserRole)
            item.setHidden(item_id not in found_ids)

    def add_member(self):
        nombre = self.member_name.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
        
        try:
            self.db.agregar_miembro(
                nombre,
                self.member_lastname.text() or None,
                self.member_gender.currentText()
            )
            self.member_name.clear()
            self.member_lastname.clear()
            self.load_members()
            self.load_members_for_attendance()
            self.load_members_for_payments()
            QMessageBox.information(self, "Éxito", "Miembro registrado")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el miembro: {str(e)}")

    def edit_member(self):
        selected = self.members_table.currentRow()
        if selected >= 0:
            member_id = int(self.members_table.item(selected, 0).text())
            member = self.db.obtener_miembro_por_id(member_id)
            
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Miembro")
            layout = QFormLayout(dialog)
            
            nombre_edit = QLineEdit(member['nombre'])
            apellido_edit = QLineEdit(member['apellido'] or "")
            sexo_combo = QComboBox()
            sexo_combo.addItems(["Masculino", "Femenino"])
            if member['sexo']:
                sexo_combo.setCurrentText(member['sexo'])
            
            layout.addRow("Nombre:", nombre_edit)
            layout.addRow("Apellido:", apellido_edit)
            layout.addRow("Sexo:", sexo_combo)
            
            btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            btn_box.accepted.connect(dialog.accept)
            btn_box.rejected.connect(dialog.reject)
            layout.addRow(btn_box)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if self.db.actualizar_miembro(
                    member_id,
                    nombre_edit.text().strip(),
                    apellido_edit.text().strip() or None,
                    sexo_combo.currentText()
                ):
                    self.load_members()
                    self.load_members_for_attendance()
                    self.load_members_for_payments()
                    QMessageBox.information(self, "Éxito", "Miembro actualizado")

    def delete_member(self):
        selected = self.members_table.currentRow()
        if selected >= 0:
            member_id = int(self.members_table.item(selected, 0).text())
            reply = QMessageBox.question(
                self, 'Confirmar',
                '¿Estás seguro de eliminar este miembro?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.db.eliminar_miembro(member_id):
                    self.load_members()
                    self.load_members_for_attendance()
                    self.load_members_for_payments()
                    QMessageBox.information(self, "Éxito", "Miembro eliminado")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el miembro")

    # Funciones para asistencias
    def register_checkin(self):
        current_item = self.attendance_list.currentItem()
        if current_item:
            member_id = current_item.data(Qt.ItemDataRole.UserRole)
            try:
                self.db.registrar_entrada(member_id)
                QMessageBox.information(self, "Éxito", "Entrada registrada")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la entrada: {str(e)}")

    def register_checkout(self):
        current_item = self.attendance_list.currentItem()
        if current_item:
            member_id = current_item.data(Qt.ItemDataRole.UserRole)
            try:
                self.db.registrar_salida(member_id)
                QMessageBox.information(self, "Éxito", "Salida registrada")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo registrar la salida: {str(e)}")

    # Funciones para pagos
    def register_payment(self):
        try:
            current_item = self.payment_member_list.currentItem()
            if not current_item:
                raise ValueError("Seleccione un miembro")
                
            member_id = current_item.data(Qt.ItemDataRole.UserRole)
            amount_str = self.payment_amount.text().replace(",", "").strip()
            if not amount_str:
                raise ValueError("Ingrese un monto")
                
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("El monto debe ser positivo")

            if not self.db.registrar_pago(member_id, amount):
                raise Exception("No se pudo registrar el pago en la base de datos")
            
            self.payment_amount.clear()
            self.load_monthly_earnings()  # Actualizar la tabla de ganancias mensuales
            self.load_daily_earnings()    # Actualizar la tabla de ganancias diarias
            
            QMessageBox.information(
                self,
                "Pago Registrado",
                f"Pago registrado correctamente:\n\n"
                f"Miembro: {current_item.text()}\n"
                f"Monto: ${amount:,.2f}\n"
            )
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pago: {str(e)}")

    def load_monthly_payments(self):
        try:
            ganancias = self.db.obtener_ganancias_mensuales()
            self.monthly_payments_table.setRowCount(len(ganancias))
            
            for row, ganancia in enumerate(ganancias):
                self.monthly_payments_table.setItem(row, 0, QTableWidgetItem(ganancia['mes']))
                self.monthly_payments_table.setItem(row, 1, QTableWidgetItem(f"${ganancia['total']:,.2f}"))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar las ganancias mensuales: {str(e)}")

    def load_daily_payments(self):
        try:
            fecha = self.daily_payments_date.date().toString("yyyy-MM-dd")
            pagos = self.db.obtener_ganancias_diarias(fecha)
            self.daily_payments_table.setRowCount(len(pagos))
            
            for row, pago in enumerate(pagos):
                hora = pago['fecha_pago'].split()[1][:5] if ' ' in pago['fecha_pago'] else ''
                self.daily_payments_table.setItem(row, 0, QTableWidgetItem(hora))
                self.daily_payments_table.setItem(row, 1, QTableWidgetItem(f"{pago['nombre']} {pago['apellido']}"))
                self.daily_payments_table.setItem(row, 2, QTableWidgetItem(f"${pago['monto']:,.2f}"))
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los pagos diarios: {str(e)}")

    # Funciones para entrenadores
    def load_trainers_combo(self):
        self.trainer_combo.clear()
        trainers = self.db.obtener_entrenadores()
        for trainer in trainers:
            self.trainer_combo.addItem(
                f"{trainer['nombre']} {trainer['apellido']}",
                userData=trainer['id_entrenador']
            )

    def load_trainers(self):
        trainers = self.db.obtener_entrenadores()
        self.trainers_table.setRowCount(len(trainers))
        
        for row, trainer in enumerate(trainers):
            self.trainers_table.setItem(row, 0, QTableWidgetItem(str(trainer['id_entrenador'])))
            self.trainers_table.setItem(row, 1, QTableWidgetItem(trainer['nombre']))
            self.trainers_table.setItem(row, 2, QTableWidgetItem(trainer['apellido'] or ""))

    def add_trainer(self):
        nombre = self.trainer_name.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return
        
        try:
            self.db.agregar_entrenador(
                nombre,
                self.trainer_lastname.text() or None
            )
            self.trainer_name.clear()
            self.trainer_lastname.clear()
            self.load_trainers()
            self.load_trainers_combo()
            QMessageBox.information(self, "Éxito", "Entrenador registrado")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el entrenador: {str(e)}")

    def register_trainer_payment(self):
        try:
            if not self.trainer_combo.currentData():
                raise ValueError("Seleccione un entrenador")
                
            amount_str = self.trainer_amount.text().replace(",", "").strip()
            if not amount_str:
                raise ValueError("Ingrese un monto")
                
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("El monto debe ser positivo")

            trainer_id = self.trainer_combo.currentData()
            trainer_name = self.trainer_combo.currentText()
            
            if not self.db.registrar_pago_entrenador(trainer_id, amount):
                raise Exception("No se pudo registrar el pago en la base de datos")
            
            self.trainer_amount.clear()
            self.update_trainers_total()
            
            QMessageBox.information(
                self,
                "Pago Registrado",
                f"Pago registrado correctamente:\n\n"
                f"Entrenador: {trainer_name}\n"
                f"Monto: ${amount:,.2f}\n"
                f"Total acumulado hoy: {self.expense_trainers.text()}"
            )
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo registrar el pago: {str(e)}")

    def update_trainers_total(self):
        try:
            total = self.db.obtener_total_pagos_entrenadores()
            self.expense_trainers.setText(f"{total:,.2f}")
            
            if hasattr(self, 'trainer_total_label'):
                self.trainer_total_label.setText(f"Total hoy: ${total:,.2f}")
        except Exception as e:
            print(f"Error actualizando total: {e}")

    # Funciones para gastos
    def load_monthly_expenses(self):
        try:
            gastos = self.db.obtener_gastos_por_mes()
            self.monthly_table.setRowCount(len(gastos))
            
            for row, gasto in enumerate(gastos):
                self.monthly_table.setItem(row, 0, QTableWidgetItem(gasto['mes']))
                self.monthly_table.setItem(row, 1, QTableWidgetItem(f"${gasto['total_admin']:,.2f}"))
                self.monthly_table.setItem(row, 2, QTableWidgetItem(f"${gasto['total_aseo']:,.2f}"))
                self.monthly_table.setItem(row, 3, QTableWidgetItem(f"${gasto['total_entrenadores']:,.2f}"))
                self.monthly_table.setItem(row, 4, QTableWidgetItem(f"${gasto['gasto_total']:,.2f}"))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los gastos mensuales: {str(e)}")

    def load_daily_expenses_details(self):
        try:
            fecha = self.daily_expenses_date.date().toString("yyyy-MM-dd")
            detalles = self.db.obtener_detalle_gastos_diarios(fecha)
            
            if not detalles:
                QMessageBox.information(self, "Información", "No hay datos para esta fecha")
                return
            
            # Gastos generales
            self.daily_general_table.setRowCount(len(detalles['gastos_generales']))
            total_general = 0.0
            
            for row, gasto in enumerate(detalles['gastos_generales']):
                hora = gasto['fecha'].split()[1][:5] if ' ' in gasto['fecha'] else ''
                self.daily_general_table.setItem(row, 0, QTableWidgetItem(hora))
                self.daily_general_table.setItem(row, 1, QTableWidgetItem(f"${gasto['gasto_admin']:,.2f}"))
                self.daily_general_table.setItem(row, 2, QTableWidgetItem(f"${gasto['gasto_aseo']:,.2f}"))
                self.daily_general_table.setItem(row, 3, QTableWidgetItem(f"${gasto['total_entrenadores']:,.2f}"))
                
                total_general += (gasto['gasto_admin'] + gasto['gasto_aseo'] + gasto['total_entrenadores'])
            
            # Pagos a entrenadores
            self.daily_trainers_table.setRowCount(len(detalles['pagos_entrenadores']))
            total_entrenadores = 0.0
            
            for row, pago in enumerate(detalles['pagos_entrenadores']):
                hora = pago['fecha_pago'].split()[1][:5] if ' ' in pago['fecha_pago'] else ''
                self.daily_trainers_table.setItem(row, 0, QTableWidgetItem(hora))
                self.daily_trainers_table.setItem(row, 1, QTableWidgetItem(f"{pago['nombre']} {pago['apellido']}"))
                self.daily_trainers_table.setItem(row, 2, QTableWidgetItem(f"${pago['monto']:,.2f}"))
                self.daily_trainers_table.setItem(row, 3, QTableWidgetItem("Pago diario"))
                
                total_entrenadores += pago['monto']
            
            # Actualizar total
            self.daily_total_label.setText(f"Total del día: ${total_general:,.2f}")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar los detalles: {str(e)}")

    def register_expenses(self):
        try:
            admin_str = self.expense_admin.text().replace(",", "").strip()
            aseo_str = self.expense_cleaning.text().replace(",", "").strip()
            
            if not admin_str or not aseo_str:
                raise ValueError("Complete todos los campos")
                
            admin = float(admin_str)
            aseo = float(aseo_str)
            
            if admin < 0 or aseo < 0:
                raise ValueError("Los montos no pueden ser negativos")

            if not self.db.registrar_gastos(admin, aseo):
                raise Exception("No se pudo registrar los gastos")
            
            QMessageBox.information(
                self, 
                "Gastos Registrados", 
                f"Gastos registrados correctamente:\n\n"
                f"• Administración: ${admin:,.2f}\n"
                f"• Aseo: ${aseo:,.2f}\n"
                f"• Total Entrenadores: {self.expense_trainers.text()}"
            )
            
            self.expense_admin.setText("0")
            self.expense_cleaning.setText("0")
            self.load_monthly_expenses()
            self.load_daily_expenses_details()
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron registrar los gastos: {str(e)}")

    def load_monthly_earnings(self):
        """Carga las ganancias mensuales en la tabla correspondiente"""
        try:
            ganancias = self.db.obtener_ganancias_mensuales()
            self.monthly_earnings_table.setRowCount(len(ganancias))
            
            for row, ganancia in enumerate(ganancias):
                self.monthly_earnings_table.setItem(row, 0, QTableWidgetItem(ganancia['mes']))
                self.monthly_earnings_table.setItem(row, 1, QTableWidgetItem(f"${ganancia['total']:,.2f}"))
                self.monthly_earnings_table.setItem(row, 2, QTableWidgetItem(str(ganancia['cantidad_pagos'])))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron cargar las ganancias mensuales: {str(e)}")

    def load_daily_earnings(self):
        """Carga las ganancias diarias con mejor manejo de errores"""
        try:
            fecha = self.daily_earnings_date.date().toString("yyyy-MM-dd")
            ganancias = self.db.obtener_ganancias_diarias(fecha)
            
            if not ganancias:
                QMessageBox.information(self, "Información", 
                                    f"No hay registros de pagos para la fecha {fecha}")
                self.daily_earnings_table.setRowCount(0)
                return
                
            self.daily_earnings_table.setRowCount(len(ganancias))
            
            for row, ganancia in enumerate(ganancias):
                # Extraer hora (HH:MM) de la fecha completa
                hora = ganancia['fecha_pago'].split()[1][:5] if ' ' in ganancia['fecha_pago'] else '00:00'
                
                self.daily_earnings_table.setItem(row, 0, QTableWidgetItem(hora))
                self.daily_earnings_table.setItem(row, 1, QTableWidgetItem(
                    f"{ganancia['nombre']} {ganancia['apellido']}"))
                self.daily_earnings_table.setItem(row, 2, QTableWidgetItem(
                    f"${ganancia['monto']:,.2f}"))
                self.daily_earnings_table.setItem(row, 3, QTableWidgetItem("Mensualidad"))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                            f"No se pudieron cargar las ganancias diarias: {str(e)}")
            print(f"Error detallado: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'db'):
            del self.db
        event.accept()

def main():
    app = QApplication([])
    app.setStyle('Fusion')
    window = GymApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()