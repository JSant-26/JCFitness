import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'jcfitness.db')
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Conexión silenciosa a la base de datos"""
        try:
            self.conn = sqlite3.connect(
                self.db_path,
                timeout=20,
                check_same_thread=False,
                isolation_level=None
            )
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error:
            raise

    # region Tablas
    def create_tables(self):
        """Crea todas las tablas necesarias sin mensajes de consola"""
        try:
            cursor = self.conn.cursor()
            
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Miembros (
                id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT,
                sexo TEXT CHECK (sexo IN ('Masculino', 'Femenino')),
                fecha_registro DATE DEFAULT (date('now')) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS Asistencias (
                id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                fecha DATE DEFAULT (date('now')) NOT NULL,
                hora_entrada TIME,
                hora_salida TIME,
                FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE,
                CONSTRAINT unique_asistencia UNIQUE (id_miembro, fecha)
            );
            CREATE TABLE IF NOT EXISTS PagosMensualidades (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                fecha_pago TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                monto REAL NOT NULL CHECK(monto > 0),
                FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS Entrenadores (
                id_entrenador INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT
            );
            CREATE TABLE IF NOT EXISTS PagosDiariosEntrenadores (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_entrenador INTEGER NOT NULL,
                fecha_pago TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                monto REAL NOT NULL CHECK(monto > 0),
                FOREIGN KEY (id_entrenador) REFERENCES Entrenadores(id_entrenador) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS Gastos (
                id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                gasto_admin REAL DEFAULT 0 CHECK(gasto_admin >= 0),
                gasto_aseo REAL DEFAULT 0 CHECK(gasto_aseo >= 0),
                total_entrenadores REAL DEFAULT 0 CHECK(total_entrenadores >= 0)
            );
            CREATE INDEX IF NOT EXISTS idx_miembros_nombre ON Miembros(nombre);
            CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON Asistencias(fecha);
            CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON PagosMensualidades(fecha_pago);
            CREATE INDEX IF NOT EXISTS idx_pagos_entrenadores_fecha ON PagosDiariosEntrenadores(fecha_pago);
            """)
            
            self.conn.commit()
        except sqlite3.Error:
            raise
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
    #endregion

    # ... (Todos los métodos de Miembros, Asistencias, Pagos, etc. van aquí, no los repetiré por brevedad) ...
    # ... Tu código para esas secciones ya está bien. Lo importante es la sección del Dashboard ...

    # region Miembros, Asistencias, Pagos, etc.
    # (El resto de tus métodos de la A a la Z que ya tenías)
    # Copiaré la última versión buena que teníamos para asegurar que todo esté aquí
    def agregar_miembro(self, nombre, apellido=None, sexo=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO Miembros (nombre, apellido, sexo, fecha_registro) VALUES (?, ?, ?, date('now'))", (nombre, apellido, sexo))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e: self.conn.rollback(); raise e
        finally: cursor.close()
    def buscar_miembros(self, nombre=None):
        cursor = self.conn.cursor()
        if nombre:
            cursor.execute("SELECT * FROM Miembros WHERE nombre LIKE ? OR apellido LIKE ? ORDER BY nombre", (f"%{nombre}%", f"%{nombre}%"))
        else:
            cursor.execute("SELECT * FROM Miembros ORDER BY nombre")
        return cursor.fetchall()
    def buscar_miembro_por_nombre(self, nombre):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Miembros WHERE nombre LIKE ? OR apellido LIKE ? ORDER BY nombre", (f"%{nombre}%", f"%{nombre}%"))
        return cursor.fetchall()
    def obtener_miembro_por_id(self, id_miembro):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Miembros WHERE id_miembro = ?", (id_miembro,))
        return cursor.fetchone()
    def actualizar_miembro(self, id_miembro, nombre, apellido=None, sexo=None):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE Miembros SET nombre = ?, apellido = ?, sexo = ? WHERE id_miembro = ?", (nombre, apellido, sexo, id_miembro))
        self.conn.commit()
        return cursor.rowcount > 0
    def eliminar_miembro(self, id_miembro):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Miembros WHERE id_miembro = ?", (id_miembro,))
        self.conn.commit()
        return cursor.rowcount > 0
    def registrar_entrada(self, id_miembro):
        try:
            now = datetime.now()
            fecha, hora = now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO Asistencias (id_miembro, fecha) VALUES (?, ?)",(id_miembro, fecha))
            cursor.execute("UPDATE Asistencias SET hora_entrada = ? WHERE id_miembro = ? AND fecha = ? AND hora_entrada IS NULL",(hora, id_miembro, fecha))
            self.conn.commit()
            return True
        except sqlite3.Error as e: self.conn.rollback(); print(f"Error entrada: {e}"); return False
    def registrar_salida(self, id_miembro):
        try:
            now = datetime.now()
            fecha, hora = now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")
            cursor = self.conn.cursor()
            cursor.execute("UPDATE Asistencias SET hora_salida = ? WHERE id_miembro = ? AND fecha = ? AND hora_salida IS NULL",(hora, id_miembro, fecha))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e: self.conn.rollback(); print(f"Error salida: {e}"); return False
    def registrar_pago(self, id_miembro, monto, fecha=None):
        try:
            cursor = self.conn.cursor()
            hora_actual = datetime.now().strftime("%H:%M:%S")
            fecha_completa = f"{fecha} {hora_actual}" if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO PagosMensualidades (id_miembro, monto, fecha_pago) VALUES (?, ?, ?)", (id_miembro, monto, fecha_completa))
            self.conn.commit()
            return True
        except sqlite3.Error as e: self.conn.rollback(); print(f"Error pago: {e}"); return False
    def obtener_ganancias_diarias(self, fecha=None):
        fecha = fecha or datetime.now().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.nombre, m.apellido, p.monto, p.fecha_pago FROM PagosMensualidades p
            JOIN Miembros m ON p.id_miembro = m.id_miembro WHERE date(p.fecha_pago) = date(?) ORDER BY p.fecha_pago DESC
        """, (fecha,))
        return cursor.fetchall()
    def obtener_ganancias_mensuales(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT strftime('%Y-%m', fecha_pago) as mes, SUM(monto) as total, COUNT(*) as cantidad_pagos
            FROM PagosMensualidades GROUP BY strftime('%Y-%m', fecha_pago) ORDER BY mes DESC
        """)
        return cursor.fetchall()
    def obtener_membresias_activas(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.id_miembro, m.nombre, m.apellido, p.fecha_pago, date(p.fecha_pago, '+31 days') as fecha_fin
                FROM PagosMensualidades p JOIN Miembros m ON p.id_miembro = m.id_miembro
                WHERE p.monto >= 55000 AND date(p.fecha_pago, '+31 days') >= date('now') ORDER BY fecha_fin ASC
            """)
            return cursor.fetchall()
        except (sqlite3.Error, Exception): return None
    def agregar_entrenador(self, nombre, apellido=None):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Entrenadores (nombre, apellido) VALUES (?, ?)", (nombre, apellido))
        self.conn.commit()
        return cursor.lastrowid
    def obtener_entrenadores(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Entrenadores ORDER BY nombre")
        return cursor.fetchall()
    def registrar_pago_entrenador(self, id_entrenador, monto):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO PagosDiariosEntrenadores (id_entrenador, monto, fecha_pago) VALUES (?, ?, datetime('now', 'localtime'))", (id_entrenador, monto))
            self.conn.commit()
            return self.obtener_total_pagos_entrenadores()
        except sqlite3.Error: self.conn.rollback(); return None
    def obtener_total_pagos_entrenadores(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM PagosDiariosEntrenadores WHERE date(fecha_pago, 'localtime') = date('now', 'localtime')")
            return float(cursor.fetchone()[0])
        except sqlite3.Error: return 0.0
    def registrar_gastos(self, admin, aseo):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id_gasto FROM Gastos WHERE date(fecha, 'localtime') = date('now', 'localtime') LIMIT 1")
            if cursor.fetchone(): raise Exception("Ya existen gastos registrados para hoy")
            total_entrenadores = self.obtener_total_pagos_entrenadores()
            cursor.execute("INSERT INTO Gastos (gasto_admin, gasto_aseo, total_entrenadores, fecha) VALUES (?, ?, ?, datetime('now', 'localtime'))", (admin, aseo, total_entrenadores))
            self.conn.commit()
            return True
        except sqlite3.Error: self.conn.rollback(); return False
        except Exception as e: raise e
    def obtener_detalle_gastos_diarios(self, fecha=None):
        try:
            cursor = self.conn.cursor()
            fecha_param = fecha or datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT strftime('%H:%M', fecha) as hora, gasto_admin, gasto_aseo, total_entrenadores
                FROM Gastos WHERE date(fecha) = date(?) ORDER BY fecha
            """, (fecha_param,))
            gastos_dia = cursor.fetchall()
            cursor.execute("""
                SELECT strftime('%H:%M', p.fecha_pago) as hora, e.nombre || COALESCE(' ' || e.apellido, '') as entrenador, p.monto, 'Pago diario' as concepto
                FROM PagosDiariosEntrenadores p JOIN Entrenadores e ON p.id_entrenador = e.id_entrenador
                WHERE date(p.fecha_pago) = date(?) ORDER BY p.fecha_pago
            """, (fecha_param,))
            pagos_entrenadores = cursor.fetchall()
            return {'gastos_generales': gastos_dia, 'pagos_entrenadores': pagos_entrenadores}
        except (sqlite3.Error, Exception): return None
    def obtener_gastos_por_mes(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT strftime('%Y-%m', fecha) as mes, SUM(gasto_admin) as total_admin, SUM(gasto_aseo) as total_aseo,
                SUM(total_entrenadores) as total_entrenadores, SUM(gasto_admin + gasto_aseo + total_entrenadores) as gasto_total
                FROM Gastos GROUP BY strftime('%Y-%m', fecha) ORDER BY fecha DESC
            """)
            return cursor.fetchall()
        except sqlite3.Error: return []
    #endregion
    
    # region Dashboard Queries
    def get_todays_earnings_total(self):
        """Calcula el total de ganancias del día de hoy."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM PagosMensualidades WHERE date(fecha_pago, 'localtime') = date('now', 'localtime')")
            return float(cursor.fetchone()[0])
        except sqlite3.Error:
            return 0.0

    # --- MÉTODO QUE FALTABA AÑADIR ---
    def get_todays_expenses_total(self):
        """Calcula el total de gastos del día de hoy."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(gasto_admin + gasto_aseo + total_entrenadores), 0) 
                FROM Gastos 
                WHERE date(fecha, 'localtime') = date('now', 'localtime')
            """)
            gastos_generales = float(cursor.fetchone()[0])

            if gastos_generales == 0:
                 return self.obtener_total_pagos_entrenadores()
            
            return gastos_generales
        except sqlite3.Error:
            return 0.0

    def get_members_present_today(self):
        """Cuenta cuántos miembros registraron entrada hoy."""
        try:
            today_date = datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT id_miembro) FROM Asistencias WHERE fecha = ? AND hora_entrada IS NOT NULL", (today_date,))
            return int(cursor.fetchone()[0])
        except sqlite3.Error:
            return 0
            
    def get_active_memberships_count(self):
        """Cuenta el número total de membresías mensuales activas."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(id_pago) FROM PagosMensualidades WHERE monto >= 55000 AND date(fecha_pago, '+31 days') >= date('now', 'localtime')")
            return int(cursor.fetchone()[0])
        except sqlite3.Error:
            return 0

    def get_expiring_memberships_count(self, days=7):
        """Cuenta membresías que vencen en los próximos X días."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"""
                SELECT COUNT(id_pago) FROM PagosMensualidades
                WHERE monto >= 55000 AND date(fecha_pago, '+31 days') >= date('now', 'localtime')
                AND date(fecha_pago, '+31 days') < date('now', 'localtime', '+{days+1} days')
            """)
            return int(cursor.fetchone()[0])
        except sqlite3.Error:
            return 0
    #endregion

    def __del__(self):
        if self.conn:
            self.conn.close()
