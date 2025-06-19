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
        """Conexión segura a la base de datos"""
        try:
            self.conn = sqlite3.connect(
                self.db_path,
                timeout=20,
                check_same_thread=False,
                isolation_level=None
            )
            self.conn.execute("PRAGMA journal_mode=WAL")
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Error conectando a la base de datos: {e}")
            raise

    def create_tables(self):
        """Crea todas las tablas con constraints y valores por defecto adecuados"""
        try:
            cursor = self.conn.cursor()
            
            cursor.executescript("""
            -- Tabla Miembros
            CREATE TABLE IF NOT EXISTS Miembros (
                id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT,
                sexo TEXT CHECK (sexo IN ('Masculino', 'Femenino')),
                fecha_registro DATE DEFAULT (date('now')) NOT NULL
            );

            -- Tabla Asistencias
            CREATE TABLE IF NOT EXISTS Asistencias (
                id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                fecha DATE DEFAULT (date('now')) NOT NULL,
                hora_entrada TIME,
                hora_salida TIME,
                FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE,
                CONSTRAINT unique_asistencia UNIQUE (id_miembro, fecha)
            );

            -- Tabla PagosMensualidades (versión corregida)
            CREATE TABLE IF NOT EXISTS PagosMensualidades (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                fecha_pago TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                monto REAL NOT NULL CHECK(monto > 0),
                FOREIGN KEY (id_miembro) REFERENCES Miembros(id_miembro) ON DELETE CASCADE
            );

            -- Tabla Entrenadores
            CREATE TABLE IF NOT EXISTS Entrenadores (
                id_entrenador INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT
            );

            -- Tabla Pagos a Entrenadores
            CREATE TABLE IF NOT EXISTS PagosDiariosEntrenadores (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_entrenador INTEGER NOT NULL,
                fecha_pago TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                monto REAL NOT NULL CHECK(monto > 0),
                FOREIGN KEY (id_entrenador) REFERENCES Entrenadores(id_entrenador) ON DELETE CASCADE
            );

            -- Tabla Gastos
            CREATE TABLE IF NOT EXISTS Gastos (
                id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP NOT NULL DEFAULT (datetime('now')),
                gasto_admin REAL DEFAULT 0 CHECK(gasto_admin >= 0),
                gasto_aseo REAL DEFAULT 0 CHECK(gasto_aseo >= 0),
                total_entrenadores REAL DEFAULT 0 CHECK(total_entrenadores >= 0)
            );

            -- Índices para mejorar rendimiento
            CREATE INDEX IF NOT EXISTS idx_miembros_nombre ON Miembros(nombre);
            CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON Asistencias(fecha);
            CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON PagosMensualidades(fecha_pago);
            CREATE INDEX IF NOT EXISTS idx_pagos_entrenadores_fecha ON PagosDiariosEntrenadores(fecha_pago);
            """)
            
            self.conn.commit()
            print("Tablas creadas/existentes verificadas correctamente")
            
        except sqlite3.Error as e:
            print(f"Error en create_tables: {e}")
            raise
        finally:
            cursor.close()

    # Operaciones Miembros
    def agregar_miembro(self, nombre, apellido=None, sexo=None):
        """Registra un nuevo miembro con fecha actual automática"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Miembros (nombre, apellido, sexo) VALUES (?, ?, ?)",
            (nombre, apellido, sexo)
        )
        self.conn.commit()
        return cursor.lastrowid

    def buscar_miembros(self, nombre=None):
        """Busca todos los miembros o filtra por nombre/apellido"""
        cursor = self.conn.cursor()
        if nombre:
            cursor.execute(
                "SELECT * FROM Miembros WHERE nombre LIKE ? OR apellido LIKE ? ORDER BY nombre",
                (f"%{nombre}%", f"%{nombre}%")
            )
        else:
            cursor.execute("SELECT * FROM Miembros ORDER BY nombre")
        return cursor.fetchall()

    def buscar_miembro_por_nombre(self, nombre):
        """Busca miembros por coincidencia parcial de nombre o apellido"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Miembros WHERE nombre LIKE ? OR apellido LIKE ? ORDER BY nombre",
            (f"%{nombre}%", f"%{nombre}%")
        )
        return cursor.fetchall()

    def obtener_miembro_por_id(self, id_miembro):
        """Obtiene un miembro específico por su ID"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM Miembros WHERE id_miembro = ?",
            (id_miembro,)
        )
        return cursor.fetchone()

    def obtener_miembro_exacto(self, nombre_completo):
        """Busca un miembro por nombre completo exacto"""
        partes = nombre_completo.split(maxsplit=1)
        cursor = self.conn.cursor()
        if len(partes) == 1:
            cursor.execute(
                "SELECT * FROM Miembros WHERE nombre = ?",
                (partes[0],)
            )
        else:
            cursor.execute(
                "SELECT * FROM Miembros WHERE nombre = ? AND apellido = ?",
                (partes[0], partes[1])
            )
        return cursor.fetchone()

    def actualizar_miembro(self, id_miembro, nombre, apellido=None, sexo=None):
        """Actualiza los datos de un miembro existente"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Miembros SET nombre = ?, apellido = ?, sexo = ? WHERE id_miembro = ?",
            (nombre, apellido, sexo, id_miembro)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def eliminar_miembro(self, id_miembro):
        """Elimina un miembro y sus registros relacionados (por CASCADE)"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM Miembros WHERE id_miembro = ?", (id_miembro,))
        self.conn.commit()
        return cursor.rowcount > 0

    # Operaciones Asistencias
    def registrar_entrada(self, id_miembro):
        """Registra la hora de entrada de un miembro"""
        hora = datetime.now().strftime("%H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Asistencias (id_miembro, hora_entrada) VALUES (?, ?)",
            (id_miembro, hora)
        )
        self.conn.commit()

    def registrar_salida(self, id_miembro):
        """Registra la hora de salida de un miembro"""
        hora = datetime.now().strftime("%H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Asistencias SET hora_salida = ? "
            "WHERE id_miembro = ? AND fecha = date('now') AND hora_salida IS NULL",
            (hora, id_miembro)
        )
        self.conn.commit()

    # Operaciones Pagos

    def registrar_pago(self, id_miembro, monto):
        """Registra un pago con fecha/hora exacta"""
        try:
            cursor = self.conn.cursor()
            
            # 1. Validar que el miembro existe
            cursor.execute("SELECT id_miembro FROM Miembros WHERE id_miembro = ?", (id_miembro,))
            if not cursor.fetchone():
                raise ValueError("ID de miembro no existe")
            
            # 2. Crear timestamp con formato exacto
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 3. Insertar con fecha explícita
            cursor.execute(
                "INSERT INTO PagosMensualidades (id_miembro, monto, fecha_pago) VALUES (?, ?, ?)",
                (id_miembro, monto, timestamp)
            )
            
            # 4. Verificar inserción
            cursor.execute("""
                SELECT id_pago, monto, datetime(fecha_pago) as fecha 
                FROM PagosMensualidades 
                WHERE rowid = ?""", 
                (cursor.lastrowid,))
            
            pago_verificado = cursor.fetchone()
            print(f"Pago registrado - ID: {pago_verificado['id_pago']}, "
                f"Monto: {pago_verificado['monto']}, "
                f"Fecha: {pago_verificado['fecha']}")
            
            self.conn.commit()
            return True
            
        except Exception as e:
            self.conn.rollback()
            print(f"Error al registrar pago: {str(e)}")
            return False

    def obtener_ganancias_diarias(self, fecha=None):
        """Versión más robusta con manejo de fechas mejorado"""
        try:
            fecha = fecha or datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            
            # Verificación de depuración
            cursor.execute("SELECT date(?) as fecha_verificada", (fecha,))
            fecha_verificada = cursor.fetchone()['fecha_verificada']
            print(f"Buscando pagos para fecha (formato normalizado): {fecha_verificada}")
            
            # Consulta principal
            cursor.execute("""
                SELECT 
                    m.nombre,
                    m.apellido,
                    p.monto,
                    p.fecha_pago,
                    date(p.fecha_pago) as fecha_normalizada
                FROM PagosMensualidades p
                JOIN Miembros m ON p.id_miembro = m.id_miembro
                WHERE date(p.fecha_pago) = date(?)
                ORDER BY p.fecha_pago DESC
            """, (fecha,))
            
            resultados = cursor.fetchall()
            print(f"Registros encontrados: {len(resultados)}")
            return resultados
            
        except sqlite3.Error as e:
            print(f"Error en obtener_ganancias_diarias: {e}")
            return []

    def obtener_ganancias_mensuales(self, año=None, mes=None):
        """Obtiene las ganancias totales por mes"""
        try:
            query = """
            SELECT 
                strftime('%Y-%m', fecha_pago) as mes,
                SUM(monto) as total,
                COUNT(*) as cantidad_pagos
            FROM PagosMensualidades
            """
            params = []
            
            if año and mes:
                query += " WHERE strftime('%Y-%m', fecha_pago) = ?"
                params.append(f"{año}-{mes:02d}")
            elif año:
                query += " WHERE strftime('%Y', fecha_pago) = ?"
                params.append(str(año))
            
            query += " GROUP BY strftime('%Y-%m', fecha_pago) ORDER BY mes DESC"
            
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo ganancias mensuales: {e}")
            return []

    # Operaciones Entrenadores
    def agregar_entrenador(self, nombre, apellido=None):
        """Registra un nuevo entrenador"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Entrenadores (nombre, apellido) VALUES (?, ?)",
            (nombre, apellido)
        )
        self.conn.commit()
        return cursor.lastrowid

    def obtener_entrenadores(self):
        """Obtiene todos los entrenadores registrados"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM Entrenadores ORDER BY nombre")
        return cursor.fetchall()

    def registrar_pago_entrenador(self, id_entrenador, monto):
        """Registra pago a entrenador con timestamp exacto"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO PagosDiariosEntrenadores (id_entrenador, monto, fecha_pago) VALUES (?, ?, datetime('now'))",
                (id_entrenador, monto)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error registrando pago entrenador: {e}")
            return False

    def obtener_total_pagos_entrenadores(self):
        """Obtiene suma de pagos del día actual"""
        try:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT SUM(monto) FROM PagosDiariosEntrenadores WHERE date(fecha_pago) = date(?)",
                (fecha_hoy,)
            )
            resultado = cursor.fetchone()[0]
            return float(resultado) if resultado is not None else 0.0
        except sqlite3.Error as e:
            print(f"Error calculando total entrenadores: {e}")
            return 0.0

    # Operaciones Gastos
    def registrar_gastos(self, admin, aseo):
        """Registra gastos con total automático de entrenadores"""
        try:
            total_entrenadores = self.obtener_total_pagos_entrenadores()
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Gastos (fecha, gasto_admin, gasto_aseo, total_entrenadores) VALUES (datetime('now'), ?, ?, ?)",
                (admin, aseo, total_entrenadores)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error registrando gastos: {e}")
            return False

    def obtener_gastos_por_mes(self, año=None, mes=None):
        """Obtiene el resumen de gastos por mes"""
        try:
            query = """
            SELECT 
                strftime('%Y-%m', fecha) as mes,
                SUM(gasto_admin) as total_admin,
                SUM(gasto_aseo) as total_aseo,
                SUM(total_entrenadores) as total_entrenadores,
                SUM(gasto_admin + gasto_aseo + total_entrenadores) as gasto_total
            FROM Gastos
            """
            params = []
            
            if año and mes:
                query += " WHERE strftime('%Y-%m', fecha) = ?"
                params.append(f"{año}-{mes:02d}")
            elif año:
                query += " WHERE strftime('%Y', fecha) = ?"
                params.append(str(año))
            
            query += " GROUP BY strftime('%Y-%m', fecha) ORDER BY fecha DESC"
            
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo gastos por mes: {e}")
            return []

    def obtener_detalle_gastos_diarios(self, fecha=None):
        """Obtiene el detalle diario de gastos"""
        try:
            fecha = fecha or datetime.now().strftime("%Y-%m-%d")
            cursor = self.conn.cursor()
            
            # Gastos generales
            cursor.execute("""
                SELECT fecha, gasto_admin, gasto_aseo, total_entrenadores 
                FROM Gastos 
                WHERE date(fecha) = date(?)
                ORDER BY fecha DESC
            """, (fecha,))
            gastos_dia = cursor.fetchall()
            
            # Detalle de pagos a entrenadores
            cursor.execute("""
                SELECT e.nombre, e.apellido, p.monto, p.fecha_pago
                FROM PagosDiariosEntrenadores p
                JOIN Entrenadores e ON p.id_entrenador = e.id_entrenador
                WHERE date(p.fecha_pago) = date(?)
                ORDER BY p.fecha_pago
            """, (fecha,))
            pagos_entrenadores = cursor.fetchall()
            
            return {
                'gastos_generales': gastos_dia,
                'pagos_entrenadores': pagos_entrenadores
            }
        except sqlite3.Error as e:
            print(f"Error obteniendo detalle diario: {e}")
            return None

    def __del__(self):
        if self.conn:
            self.conn.close()