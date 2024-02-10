import sqlite3

# Conectar a la base de datos SQLite (esto la creará si no existe)
conn = sqlite3.connect('usuarios.db')
c = conn.cursor()

# Crear una tabla
c.execute('''
CREATE TABLE IF NOT EXISTS MovimientosCuenta (
    MovimientoID INTEGER PRIMARY KEY AUTOINCREMENT,
    CuentaID INTEGER NOT NULL,
    TransaccionID INTEGER,
    ValorAnterior REAL NOT NULL,
    ValorAñadido REAL NOT NULL,
    NuevoValor REAL NOT NULL,
    FechaHora TEXT NOT NULL,
    TipoMovimiento TEXT NOT NULL,
    Descripcion TEXT,
    FOREIGN KEY (CuentaID) REFERENCES CuentasBancarias(CuentaID),
    FOREIGN KEY (TransaccionID) REFERENCES Transacciones(TransaccionID)
);
''')

# Guardar (confirmar) los cambios y cerrar la conexión a la base de datos
conn.commit()
conn.close()
