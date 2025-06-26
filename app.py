# --- START OF FILE app.py (VERSIÓN FINAL Y COMPLETA) ---

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QListWidget, QListWidgetItem, QStackedWidget, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox,
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QProgressDialog
from datetime import datetime
from database import Database
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import tempfile
import shutil

class EmailBackup:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def send_backup(self, to_email, smtp_user, smtp_password, smtp_server="smtp.gmail.com", smtp_port=587):
        """Envía la base de datos como archivo adjunto por correo electrónico"""
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = "Respaldo Base de Datos JCFitness"
            
            # Cuerpo del mensaje
            body = "Adjunto se encuentra el respaldo de la base de datos de JCFitness generado automáticamente."
            msg.attach(MIMEText(body, 'plain'))
            
            # Adjuntar archivo
            with open(self.db_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(self.db_path)}')
                msg.attach(part)
            
            # Enviar correo
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False

# Importamos TODAS las páginas de la UI
from interface import (
    DashboardPage, MembersPage, AttendancePage, PaymentsPage,
    MembershipsPage, EarningsPage, TrainersPage, ExpensesPage
)

GLOBAL_STYLE = """
    QMainWindow { background-color: #fdfdfd; }
    QListWidget { 
        border: none; outline: 0; background-color: #e8eff6; font-size: 16px;
    }
    QListWidget::item { 
        padding: 15px 20px; border-bottom: 1px solid #dce5ee; color: #333;
    }
    QListWidget::item:hover { background-color: #d8e2ec; }
    QListWidget::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2a9dff, stop: 1 #007bff);
        color: white; font-weight: bold; border-left: 5px solid #0056b3;
        border-bottom-color: #0056b3;
    }
    QMessageBox { font-size: 16px; }
    QMessageBox QLabel { font-size: 16px; }
    QMessageBox QPushButton { font-size: 16px; padding: 10px; min-width: 100px; }
"""

class GymApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.email_backup = EmailBackup(self.db.db_path)
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
        self.connect_signals()

        self.nav_menu.setCurrentRow(0)
        self.load_all_data()

    def change_page(self, current_item):
        row = self.nav_menu.row(current_item)
        self.pages.setCurrentIndex(row)
        
        page_loaders = {
            0: lambda: self.update_dashboard_data(show_message=False),
            1: self.load_members,
            2: self.load_members_for_attendance,
            3: self.load_members_for_payments,
            4: self.load_active_memberships,
            5: self.load_earnings_data,
            6: self.load_trainers_data,
            7: self.load_expenses_data
        }
        if row in page_loaders:
            page_loaders[row]()

    def load_all_data(self):
        """Carga los datos para todas las páginas sin cambiar la vista."""
        # Este método ahora solo se enfoca en cargar los datos en las tablas
        # para que estén listas cuando el usuario navegue a ellas.
        self.load_members()
        self.load_members_for_attendance()
        self.load_members_for_payments()
        self.load_active_memberships()
        self.load_earnings_data()
        self.load_trainers_data()
        self.load_expenses_data()

    def connect_signals(self):
        # Dashboard
        self.dashboard_page.refresh_button.clicked.connect(self.update_dashboard_data)
        self.email_backup = EmailBackup(self.db.db_path)
        # Miembros
        self.members_page.btn_add.clicked.connect(self.add_member)
        self.members_page.btn_edit.clicked.connect(self.edit_member)
        self.members_page.btn_delete.clicked.connect(self.delete_member)
        self.members_page.member_search.textChanged.connect(self.filter_members_table)
        # Asistencias
        self.attendance_page.search_attendance.textChanged.connect(self.filter_members_for_attendance)
        self.attendance_page.btn_checkin.clicked.connect(self.register_checkin)
        self.attendance_page.btn_checkout.clicked.connect(self.register_checkout)
        self.attendance_page.btn_load_attendance.clicked.connect(self.load_attendance_records)
        # Pagos
        self.payments_page.payment_search.textChanged.connect(self.filter_members_for_payments)
        self.payments_page.btn_daily.clicked.connect(lambda: self.register_payment(4000, "Pago Diario"))
        self.payments_page.btn_monthly.clicked.connect(lambda: self.register_payment(55000, "Pago Mensual"))
        # Membresías
        self.memberships_page.btn_refresh.clicked.connect(self.load_active_memberships)
        self.memberships_page.membership_search.textChanged.connect(self.filter_memberships)
        # Ganancias
        self.earnings_page.btn_load_daily.clicked.connect(self.load_daily_earnings)
        # Entrenadores
        self.trainers_page.btn_add_trainer.clicked.connect(self.add_trainer)
        self.trainers_page.btn_pay_trainer.clicked.connect(self.register_trainer_payment)
        # Gastos
        self.expenses_page.btn_register_expenses.clicked.connect(self.register_expenses)
        self.expenses_page.btn_load_daily_expenses.clicked.connect(self.load_daily_expenses_details)

    # --- LÓGICA DE LA APLICACIÓN ---
    
    #region Dashboard
    def update_dashboard_data(self, show_message=True):
        try:
            # 1. Obtener ganancias brutas
            earnings_gross = self.db.get_todays_earnings_total()
            
            # 2. Obtener gastos totales del día
            expenses_total = self.db.get_todays_expenses_total()
            
            # 3. Calcular la ganancia NETA
            net_earnings = earnings_gross - expenses_total

            # Obtener los otros datos del dashboard
            present = self.db.get_members_present_today()
            active = self.db.get_active_memberships_count()
            expiring = self.db.get_expiring_memberships_count(days=7)

            # 4. Actualizar la etiqueta con la ganancia NETA
            self.dashboard_page.earnings_label.setText(f"${net_earnings:,.0f}")
            
            # Actualizar el resto de etiquetas
            self.dashboard_page.present_label.setText(str(present))
            self.dashboard_page.active_label.setText(str(active))
            self.dashboard_page.expiring_label.setText(str(expiring))
            
            if show_message:
                QMessageBox.information(self, "Actualizado", "Los datos del dashboard han sido actualizados.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo actualizar el dashboard: {e}")

    def send_database_backup(self):
        """Método para manejar el envío del respaldo"""
        # Crear diálogo para ingresar credenciales
        dialog = QDialog(self)
        dialog.setWindowTitle("Configuración de Respaldo")
        layout = QFormLayout(dialog)
        
        # Campos del formulario
        email_edit = QLineEdit()
        email_edit.setPlaceholderText("tu@email.com")
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        destination_edit = QLineEdit()
        destination_edit.setPlaceholderText("destino@email.com")
        
        # Botones
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(dialog.accept)
        btn_box.rejected.connect(dialog.reject)
        
        # Añadir widgets al layout
        layout.addRow("Tu correo (Gmail):", email_edit)
        layout.addRow("Contraseña (App Password):", password_edit)
        layout.addRow("Enviar a:", destination_edit)
        layout.addRow(btn_box)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Obtener valores
            smtp_user = email_edit.text().strip()
            smtp_pass = password_edit.text().strip()
            to_email = destination_edit.text().strip()
            
            if not all([smtp_user, smtp_pass, to_email]):
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
                return
                
            # Mostrar progreso
            progress = QProgressDialog("Enviando respaldo...", "Cancelar", 0, 0, self)
            progress.setWindowTitle("Enviando correo")
            progress.setWindowModality(Qt.WindowModality.WindowModal)
            progress.setCancelButton(None)  # No permitir cancelar
            progress.show()
            
            # Forzar actualización de la UI
            QApplication.processEvents()
            
            try:
                # Intentar enviar el correo
                success = self.email_backup.send_backup(
                    to_email=to_email,
                    smtp_user=smtp_user,
                    smtp_password=smtp_pass
                )
                
                progress.close()
                
                if success:
                    QMessageBox.information(self, "Éxito", "Respaldo enviado correctamente")
                else:
                    QMessageBox.critical(self, "Error", "No se pudo enviar el respaldo. Verifica tus credenciales y conexión.")
                    
            except Exception as e:
                progress.close()
                QMessageBox.critical(self, "Error", f"Error al enviar el respaldo: {str(e)}")

    #endregion
            
    #region Members
    def load_members(self):
        table = self.members_page.members_table
        table.setRowCount(0)
        members = self.db.buscar_miembros()
        for row, member in enumerate(members):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(member['id_miembro'])))
            table.setItem(row, 1, QTableWidgetItem(member['nombre']))
            table.setItem(row, 2, QTableWidgetItem(member['apellido'] or ""))
            table.setItem(row, 3, QTableWidgetItem(member['sexo'] or ""))
            table.setItem(row, 4, QTableWidgetItem(member['fecha_registro']))

    def filter_members_table(self, text):
        table = self.members_page.members_table
        if not text:
            for r in range(table.rowCount()): table.setRowHidden(r, False)
            return
        found_ids = {m['id_miembro'] for m in self.db.buscar_miembro_por_nombre(text)}
        for r in range(table.rowCount()):
            table.setRowHidden(r, int(table.item(r, 0).text()) not in found_ids)

    def add_member(self):
        nombre = self.members_page.member_name.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio"); return
        try:
            self.db.agregar_miembro(nombre, self.members_page.member_lastname.text() or None, self.members_page.member_gender.currentText())
            self.members_page.member_name.clear(); self.members_page.member_lastname.clear()
            self.load_all_data(); QMessageBox.information(self, "Éxito", "Miembro registrado")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar el miembro: {e}")

    def edit_member(self):
        table = self.members_page.members_table
        selected = table.currentRow()
        if selected < 0: QMessageBox.warning(self, "Atención", "Seleccione un miembro para editar."); return
        member_id = int(table.item(selected, 0).text())
        member = self.db.obtener_miembro_por_id(member_id)
        dialog = QDialog(self); dialog.setWindowTitle("Editar Miembro")
        layout = QFormLayout(dialog)
        nombre_edit = QLineEdit(member['nombre']); apellido_edit = QLineEdit(member['apellido'] or "")
        sexo_combo = QComboBox(); sexo_combo.addItems(["Masculino", "Femenino"]); sexo_combo.setCurrentText(member['sexo'] or "Masculino")
        layout.addRow("Nombre:", nombre_edit); layout.addRow("Apellido:", apellido_edit); layout.addRow("Sexo:", sexo_combo)
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(dialog.accept); btn_box.rejected.connect(dialog.reject); layout.addRow(btn_box)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.db.actualizar_miembro(member_id, nombre_edit.text().strip(), apellido_edit.text().strip() or None, sexo_combo.currentText()):
                self.load_all_data(); QMessageBox.information(self, "Éxito", "Miembro actualizado.")

    def delete_member(self):
        table = self.members_page.members_table
        selected = table.currentRow()
        if selected < 0: QMessageBox.warning(self, "Atención", "Seleccione un miembro para eliminar."); return
        member_id = int(table.item(selected, 0).text())
        reply = QMessageBox.question(self, 'Confirmar', '¿Estás seguro de eliminar este miembro?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.eliminar_miembro(member_id): self.load_all_data(); QMessageBox.information(self, "Éxito", "Miembro eliminado.")
            else: QMessageBox.warning(self, "Error", "No se pudo eliminar el miembro.")
    #endregion

    #region Attendance
    def load_members_for_attendance(self):
        table = self.attendance_page.attendance_table_reg
        table.setRowCount(0)
        members = sorted(self.db.buscar_miembros(), key=lambda x: (x['nombre'].lower(), x['apellido'].lower() if x['apellido'] else ""))
        for row, member in enumerate(members):
            table.insertRow(row)
            id_item = QTableWidgetItem(str(member['id_miembro'])); id_item.setData(Qt.ItemDataRole.UserRole, member['id_miembro'])
            table.setItem(row, 0, id_item); table.setItem(row, 1, QTableWidgetItem(member['nombre'])); table.setItem(row, 2, QTableWidgetItem(member['apellido'] or ""))

    def filter_members_for_attendance(self, text):
        table = self.attendance_page.attendance_table_reg; text = text.lower()
        for r in range(table.rowCount()):
            nombre = table.item(r, 1).text().lower(); apellido = table.item(r, 2).text().lower()
            table.setRowHidden(r, text not in nombre and text not in apellido)

    def register_checkin(self):
        table = self.attendance_page.attendance_table_reg
        current_row = table.currentRow()
        if current_row < 0: QMessageBox.warning(self, "Advertencia", "Seleccione un miembro primero"); return
        member_id = table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
        member_name = table.item(current_row, 1).text()
        try:
            if self.db.registrar_entrada(member_id):
                QMessageBox.information(self, "Éxito", f"Entrada registrada para: {member_name}")
                self.update_dashboard_data(show_message=False)
            else: QMessageBox.warning(self, "Error", "No se pudo registrar la entrada. ¿Ya hay una entrada registrada hoy?")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar la entrada: {e}")

    def register_checkout(self):
        table = self.attendance_page.attendance_table_reg
        current_row = table.currentRow()
        if current_row < 0: QMessageBox.warning(self, "Advertencia", "Seleccione un miembro primero"); return
        member_id = table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
        try:
            if self.db.registrar_salida(member_id):
                QMessageBox.information(self, "Éxito", f"Salida registrada para: {table.item(current_row, 1).text()}")
            else: QMessageBox.warning(self, "Error", "No se encontró entrada para registrar salida o ya tiene salida registrada.")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar la salida: {e}")

    def load_attendance_records(self):
        table = self.attendance_page.attendance_table_view
        try:
            fecha = self.attendance_page.attendance_view_date.date().toString("yyyy-MM-dd")
            records = self.db.conn.cursor().execute("""
                SELECT m.id_miembro, m.nombre, m.apellido, a.hora_entrada, a.hora_salida FROM Asistencias a
                JOIN Miembros m ON a.id_miembro = m.id_miembro WHERE date(a.fecha) = ? AND a.hora_entrada IS NOT NULL ORDER BY a.hora_entrada
            """, (fecha,)).fetchall()
            table.setRowCount(len(records))
            for row, record in enumerate(records):
                table.setItem(row, 0, QTableWidgetItem(str(record['id_miembro'])))
                table.setItem(row, 1, QTableWidgetItem(record['nombre']))
                table.setItem(row, 2, QTableWidgetItem(record['apellido'] or ""))
                h_in = record['hora_entrada'] or ""; h_out = record['hora_salida'] or ""
                table.setItem(row, 3, QTableWidgetItem(h_in)); table.setItem(row, 4, QTableWidgetItem(h_out))
                total_t = ""
                if h_in and h_out:
                    try:
                        diff = datetime.strptime(h_out, "%H:%M:%S") - datetime.strptime(h_in, "%H:%M:%S")
                        total_t = f"{diff.seconds // 3600}h {(diff.seconds % 3600) // 60}m"
                    except ValueError: total_t = "Error"
                table.setItem(row, 5, QTableWidgetItem(total_t))
        except Exception as e: QMessageBox.warning(self, "Error", f"No se pudieron cargar las asistencias: {e}"); table.setRowCount(0)
    #endregion
    
    #region Payments
    def load_members_for_payments(self):
        table = self.payments_page.payment_member_table
        table.setRowCount(0)
        members = sorted(self.db.buscar_miembros(), key=lambda x: (x['nombre'].lower(), x['apellido'].lower() if x['apellido'] else ""))
        for row, member in enumerate(members):
            table.insertRow(row)
            id_item = QTableWidgetItem(str(member['id_miembro'])); id_item.setData(Qt.ItemDataRole.UserRole, member['id_miembro'])
            table.setItem(row, 0, id_item); table.setItem(row, 1, QTableWidgetItem(member['nombre'])); table.setItem(row, 2, QTableWidgetItem(member['apellido'] or ""))

    def filter_members_for_payments(self, text):
        table = self.payments_page.payment_member_table; text = text.lower()
        for r in range(table.rowCount()):
            nombre = table.item(r, 1).text().lower(); apellido = table.item(r, 2).text().lower()
            table.setRowHidden(r, text not in nombre and text not in apellido)

    def register_payment(self, amount, payment_type):
        table = self.payments_page.payment_member_table
        current_row = table.currentRow()
        if current_row < 0: QMessageBox.warning(self, "Error", "Seleccione un miembro"); return
        member_id = table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
        fecha_pago = self.payments_page.payment_date.date().toString("yyyy-MM-dd")
        try:
            if not self.db.registrar_pago(member_id, amount, fecha_pago): raise Exception("Fallo en la base de datos")
            QMessageBox.information(self, "Pago Registrado", f"{payment_type} de ${amount:,.0f} registrado.")
            self.load_all_data()
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar el pago: {e}")
    #endregion
    
    #region Memberships
    def load_active_memberships(self):
        table = self.memberships_page.memberships_table
        try:
            table.setRowCount(0)
            membresias = self.db.obtener_membresias_activas()
            if membresias is None: return
            today = datetime.now().date()
            validas = []
            for m in membresias:
                try:
                    fecha_fin = datetime.strptime(m['fecha_fin'], "%Y-%m-%d").date()
                    dias = (fecha_fin - today).days
                    if dias >= 0: validas.append((m, dias))
                except (ValueError, TypeError): continue
            table.setRowCount(len(validas))
            for row, (miembro, dias_restantes) in enumerate(validas):
                table.setItem(row, 0, QTableWidgetItem(str(miembro['id_miembro'])))
                table.setItem(row, 1, QTableWidgetItem(miembro['nombre']))
                table.setItem(row, 2, QTableWidgetItem(miembro['apellido'] or ""))
                fecha_pago = miembro['fecha_pago'].split()[0] if ' ' in miembro['fecha_pago'] else miembro['fecha_pago']
                table.setItem(row, 3, QTableWidgetItem(fecha_pago))
                table.setItem(row, 4, QTableWidgetItem(miembro['fecha_fin']))
                dias_item = QTableWidgetItem(str(dias_restantes))
                if dias_restantes <= 1: dias_item.setBackground(QColor(255, 200, 200)) # Rojo
                elif dias_restantes <= 5: dias_item.setBackground(QColor(255, 255, 150)) # Amarillo
                table.setItem(row, 5, dias_item)
        except Exception as e: QMessageBox.critical(self, "Error", f"Error al cargar membresías: {e}")

    def filter_memberships(self, text):
        table = self.memberships_page.memberships_table; text = text.lower()
        for r in range(table.rowCount()):
            nombre = table.item(r, 1).text().lower(); apellido = table.item(r, 2).text().lower()
            table.setRowHidden(r, text not in nombre and text not in apellido)
    #endregion

    #region Earnings
    def load_earnings_data(self):
        self.load_monthly_earnings()
        self.load_daily_earnings()

    def load_monthly_earnings(self):
        table = self.earnings_page.monthly_earnings_table
        try:
            ganancias = self.db.obtener_ganancias_mensuales()
            gastos = {g['mes']: g['gasto_total'] for g in self.db.obtener_gastos_por_mes()}
            table.setRowCount(len(ganancias))
            for row, g in enumerate(ganancias):
                gasto_mes = gastos.get(g['mes'], 0.0)
                neta = g['total'] - gasto_mes
                table.setItem(row, 0, QTableWidgetItem(g['mes']))
                table.setItem(row, 1, QTableWidgetItem(f"${g['total']:,.2f}"))
                table.setItem(row, 2, QTableWidgetItem(f"${gasto_mes:,.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"${neta:,.2f}"))
                table.setItem(row, 4, QTableWidgetItem(str(g['cantidad_pagos'])))
        except Exception as e: QMessageBox.warning(self, "Error", f"No se pudieron cargar las ganancias mensuales: {e}")

    def load_daily_earnings(self):
        table = self.earnings_page.daily_earnings_table
        try:
            fecha = self.earnings_page.daily_earnings_date.date().toString("yyyy-MM-dd")
            ganancias = self.db.obtener_ganancias_diarias(fecha)
            gastos_dia = self.db.obtener_detalle_gastos_diarios(fecha)
            table.setRowCount(len(ganancias))
            total_g = sum(g['monto'] for g in ganancias)
            total_e = sum(g['gasto_admin'] + g['gasto_aseo'] + g['total_entrenadores'] for g in gastos_dia.get('gastos_generales',[]))
            for row, g in enumerate(ganancias):
                hora = g['fecha_pago'].split()[1][:5] if ' ' in g['fecha_pago'] else '00:00'
                table.setItem(row, 0, QTableWidgetItem(hora))
                table.setItem(row, 1, QTableWidgetItem(f"{g['nombre']} {g['apellido']}"))
                table.setItem(row, 2, QTableWidgetItem(f"${g['monto']:,.2f}"))
            self.earnings_page.daily_net_total.setText(f"Total Neto: ${total_g - total_e:,.2f}")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudieron cargar las ganancias diarias: {e}"); self.earnings_page.daily_net_total.setText("Total Neto: $0.00")
    #endregion
    
    #region Trainers
    def load_trainers_data(self):
        self.load_trainers()
        self.load_trainers_combo()

    def load_trainers_combo(self):
        combo = self.trainers_page.trainer_combo; combo.clear()
        for t in self.db.obtener_entrenadores():
            combo.addItem(f"{t['nombre']} {t['apellido']}", userData=t['id_entrenador'])

    def load_trainers(self):
        table = self.trainers_page.trainers_table
        trainers = self.db.obtener_entrenadores(); table.setRowCount(len(trainers))
        for row, t in enumerate(trainers):
            table.setItem(row, 0, QTableWidgetItem(str(t['id_entrenador'])))
            table.setItem(row, 1, QTableWidgetItem(t['nombre'])); table.setItem(row, 2, QTableWidgetItem(t['apellido'] or ""))

    def add_trainer(self):
        nombre = self.trainers_page.trainer_name.text().strip()
        if not nombre: QMessageBox.warning(self, "Error", "El nombre es obligatorio"); return
        try:
            self.db.agregar_entrenador(nombre, self.trainers_page.trainer_lastname.text() or None)
            self.trainers_page.trainer_name.clear(); self.trainers_page.trainer_lastname.clear()
            self.load_trainers_data(); QMessageBox.information(self, "Éxito", "Entrenador registrado")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar el entrenador: {e}")

    def register_trainer_payment(self):
        try:
            trainer_id = self.trainers_page.trainer_combo.currentData()
            amount_str = self.trainers_page.trainer_amount.text().replace(",", "").strip()
            if not trainer_id: raise ValueError("Seleccione un entrenador")
            if not amount_str: raise ValueError("Ingrese un monto")
            amount = float(amount_str); 
            if amount <= 0: raise ValueError("El monto debe ser positivo")
            
            if self.db.registrar_pago_entrenador(trainer_id, amount) is None: raise Exception("No se pudo registrar")
            
            self.trainers_page.trainer_amount.clear()
            self.load_expenses_data() # Actualizar total en la otra pestaña
            QMessageBox.information(self, "Pago Registrado", f"Pago de ${amount:,.2f} a {self.trainers_page.trainer_combo.currentText()} registrado.")
        except ValueError as e: QMessageBox.warning(self, "Error", f"Dato inválido: {e}")
        except Exception as e: QMessageBox.critical(self, "Error", f"No se pudo registrar el pago: {e}")
    #endregion
    
    #region Expenses
    def load_expenses_data(self):
        self.update_trainers_total_in_expenses()
        self.load_monthly_expenses()
        self.load_daily_expenses_details()

    def update_trainers_total_in_expenses(self):
        try: self.expenses_page.expense_trainers.setText(f"{self.db.obtener_total_pagos_entrenadores():,.2f}")
        except: self.expenses_page.expense_trainers.setText("0.00")

    def load_monthly_expenses(self):
        table = self.expenses_page.monthly_expenses_table
        try:
            gastos = self.db.obtener_gastos_por_mes(); table.setRowCount(len(gastos))
            for row, g in enumerate(gastos):
                table.setItem(row, 0, QTableWidgetItem(g['mes']))
                table.setItem(row, 1, QTableWidgetItem(f"${g['total_admin']:,.2f}"))
                table.setItem(row, 2, QTableWidgetItem(f"${g['total_aseo']:,.2f}"))
                table.setItem(row, 3, QTableWidgetItem(f"${g['total_entrenadores']:,.2f}"))
                table.setItem(row, 4, QTableWidgetItem(f"${g['gasto_total']:,.2f}"))
        except Exception as e: QMessageBox.warning(self, "Error", f"No se pudieron cargar los gastos mensuales: {e}")

    def register_expenses(self):
        try:
            admin = float((self.expenses_page.expense_admin.text().replace(",", "").strip()) or "0")
            aseo = float((self.expenses_page.expense_cleaning.text().replace(",", "").strip()) or "0")
            if admin < 0 or aseo < 0: raise ValueError("Los montos no pueden ser negativos")
            if not self.db.registrar_gastos(admin, aseo): raise Exception("Verifique si ya existen gastos registrados para hoy.")
            
            self.load_all_data()
            QMessageBox.information(self, "Gastos Registrados", "Gastos del día registrados correctamente.")
        except ValueError as e: QMessageBox.warning(self, "Error", f"Dato inválido: {e}")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

    def load_daily_expenses_details(self):
        fecha = self.expenses_page.daily_expenses_date.date().toString("yyyy-MM-dd")
        g_table = self.expenses_page.daily_general_table
        t_table = self.expenses_page.daily_trainers_table
        g_table.setRowCount(0); t_table.setRowCount(0)
        try:
            resumen = self.db.obtener_detalle_gastos_diarios(fecha)
            if resumen is None: return
            
            gastos_g = resumen.get('gastos_generales', [])
            g_table.setRowCount(len(gastos_g))
            total_dia = 0
            for row, g in enumerate(gastos_g):
                g_table.insertRow(row)
                g_table.setItem(row, 0, QTableWidgetItem(g['hora']))
                g_table.setItem(row, 1, QTableWidgetItem(f"${g['gasto_admin']:,.2f}"))
                g_table.setItem(row, 2, QTableWidgetItem(f"${g['gasto_aseo']:,.2f}"))
                g_table.setItem(row, 3, QTableWidgetItem(f"${g['total_entrenadores']:,.2f}"))
                total_dia += g['gasto_admin'] + g['gasto_aseo'] + g['total_entrenadores']

            pagos_t = resumen.get('pagos_entrenadores', [])
            t_table.setRowCount(len(pagos_t))
            for row, p in enumerate(pagos_t):
                t_table.insertRow(row)
                t_table.setItem(row, 0, QTableWidgetItem(p['hora']))
                t_table.setItem(row, 1, QTableWidgetItem(p['entrenador']))
                t_table.setItem(row, 2, QTableWidgetItem(f"${p['monto']:,.2f}"))
                t_table.setItem(row, 3, QTableWidgetItem(p['concepto']))
                if not gastos_g: total_dia += p['monto'] # Sumar solo si no hay un gasto general que ya lo incluya
            
            self.expenses_page.daily_expenses_total.setText(f"Total del Día: ${total_dia:,.2f}")
        except Exception as e: QMessageBox.warning(self, "Error", f"Error inesperado al cargar gastos: {e}")
    #endregion


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = GymApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
