from fastapi import FastAPI, HTTPException
import aiosqlite
from pydantic import BaseModel
from fastapi_admin.providers.login import UsernamePasswordProvider


app = FastAPI()

# Modelo Pydantic para representar la estructura de un usuario
class Usuario(BaseModel):
    nombre_usuario: str
    rol: str
    informacion_contacto: str | None = None

# Crear un nuevo usuario
@app.post("/usuarios/")
async def crear_usuario(usuario: Usuario):
    async with aiosqlite.connect("usuarios.db") as db:
        cursor = await db.execute("INSERT INTO Usuarios (NombreUsuario, Rol, InformacionContacto) VALUES (?, ?, ?)",
                                  (usuario.nombre_usuario, usuario.rol, usuario.informacion_contacto))
        await db.commit()
        return {"UserID": cursor.lastrowid, **usuario.dict()}

# Obtener un usuario por ID
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    async with aiosqlite.connect("usuarios.db") as db:
        async with db.execute("SELECT * FROM Usuarios WHERE UserID = ?", (user_id,)) as cursor:
            usuario = await cursor.fetchone()
            if usuario:
                return {"UserID": usuario[0], "NombreUsuario": usuario[1], "Rol": usuario[2], "InformacionContacto": usuario[3]}
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Actualizar un usuario
@app.put("/usuarios/{user_id}")
async def actualizar_usuario(user_id: int, usuario: Usuario):
    async with aiosqlite.connect("usuarios.db") as db:
        await db.execute("UPDATE Usuarios SET NombreUsuario = ?, Rol = ?, InformacionContacto = ? WHERE UserID = ?",
                         (usuario.nombre_usuario, usuario.rol, usuario.informacion_contacto, user_id))
        await db.commit()
        return {"UserID": user_id, **usuario.dict()}

# Eliminar un usuario
@app.delete("/usuarios/{user_id}")
async def eliminar_usuario(user_id: int):
    async with aiosqlite.connect("usuarios.db") as db:
        await db.execute("DELETE FROM Usuarios WHERE UserID = ?", (user_id,))
        await db.commit()
        return {"message": "Usuario eliminado con éxito"}

# Ejecuta la aplicación con 'uvicorn main:app --reload' desde la línea de comandos

