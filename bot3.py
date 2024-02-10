### desarrollo de funcionalidad user + rol will go to database
import nextcord
import aiosqlite
import os
from dotenv import load_dotenv
from nextcord.ext import commands, tasks
from nextcord import Interaction, ButtonStyle, ui 
from nextcord.ui import Button, View
from datetime import datetime
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Define los intents que tu bot necesitará.
intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# ID del canal donde se enviarán las solicitudes
ID_CANAL_SOLICITUDES = 1205982519992909854 # Reemplaza con el ID real del canal

class Confirmacion(ui.View):
    def __init__(self, user: nextcord.User, rol: str):
        super().__init__()
        self.user = user
        self.rol = rol

    @ui.button(label="Aceptar", style=ButtonStyle.green)
    async def confirmar(self, button: ui.Button, interaction: Interaction):
        timestamp_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("usuarios.db") as db:
            await db.execute("INSERT INTO Usuarios (NombreUsuario, UID, Rol, Timestamp) VALUES (?, ?, ?, ?)",
                             (self.user.name, self.user.id, self.rol, timestamp_registro))
            await db.commit()
        await interaction.response.send_message(f"Solicitud aprobada para {self.user.name}.", ephemeral=True)
        self.stop()

    @ui.button(label="Rechazar", style=ButtonStyle.red)
    async def cancelar(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message(f"Solicitud rechazada para {self.user.name}.", ephemeral=True)
        self.stop()

@bot.slash_command(name="registrar")
async def registrar(interaction: Interaction, rol: str):
    await interaction.response.send_message("Procesando tu solicitud...", ephemeral=True)
    
    # Aquí envías el mensaje al canal de solicitudes
    canal_solicitudes = bot.get_channel(ID_CANAL_SOLICITUDES)
    embed = nextcord.Embed(title="Nueva Solicitud de Registro", description="Un usuario ha solicitado unirse.")
    embed.add_field(name="Usuario", value=interaction.user.name)
    embed.add_field(name="UID", value=str(interaction.user.id))
    embed.add_field(name="Rol", value=rol)
    embed.set_footer(text="Usa los botones para aceptar o rechazar esta solicitud.")
    
    view = Confirmacion(interaction.user, rol)
    mensaje_solicitud = await canal_solicitudes.send(embed=embed, view=view)
    
    # Opcional: eliminar el mensaje de solicitud después de un tiempo
    # await tasks.sleep(120)  # Espera 2 minutos antes de eliminar el mensaje
    # await mensaje_solicitud.delete()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    
# No olvides poner aquí tu token de bot real
bot.run(token)
