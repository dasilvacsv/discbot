import nextcord
import aiosqlite
import os
from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Define los intents que tu bot necesitará.
intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

class UsuarioModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Crear Usuario")

        self.nombre_usuario = nextcord.ui.TextInput(
            label="Nombre de Usuario",
            placeholder="Ingresa tu nombre de usuario aquí...",
        )
        self.add_item(self.nombre_usuario)

        self.rol = nextcord.ui.TextInput(
            label="Rol",
            placeholder="Ingresa tu rol aquí...",
        )
        self.add_item(self.rol)

        self.informacion_contacto = nextcord.ui.TextInput(
            label="Información de Contacto",
            placeholder="Ingresa tu información de contacto aquí...",
            required=False,  # Hace que este campo no sea obligatorio
        )
        self.add_item(self.informacion_contacto)

    async def callback(self, interaction: nextcord.Interaction):
        nombre_usuario = self.nombre_usuario.value
        rol = self.rol.value
        informacion_contacto = self.informacion_contacto.value

        async with aiosqlite.connect("usuarios.db") as db:
            await db.execute("INSERT INTO Usuarios (NombreUsuario, Rol, InformacionContacto) VALUES (?, ?, ?)",
                             (nombre_usuario, rol, informacion_contacto))
            await db.commit()

        await interaction.response.send_message(f"Usuario {nombre_usuario} creado.")

@bot.slash_command(name="crear_usuario")
async def crear_usuario(interaction: nextcord.Interaction):
    modal = UsuarioModal()
    await interaction.response.send_modal(modal)
    
# No olvides poner aquí tu token de bot real
bot.run(token)
