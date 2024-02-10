## desarrollo de funcionalidad user + rol will go to database
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

# ID del canal donde los usuarios eligen su rol
ID_CANAL_SELECCIONROL = 1181245935846703187 # Reemplaza con el ID real del canal

class RolView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(self, interaction: Interaction, rol: str):
        # Este timestamp representa el momento en que el usuario selecciona su rol.
        timestamp_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Se guarda el nombre del usuario para usarlo más adelante en la confirmación.
        usuario_nombre = interaction.user.display_name



        embed = nextcord.Embed(title="Solicitud de Registro", description=f"**{interaction.user}** quiere registrarse como **{rol}**.")
        embed.add_field(name="Nombre de Usuario", value=interaction.user.display_name, inline=True)
        embed.add_field(name="UID", value=str(interaction.user.id), inline=True)
        embed.add_field(name="Rol Solicitado", value=rol, inline=True)
        embed.add_field(name="Timestamp de Registro", value=timestamp_registro, inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        canal_solicitudes = bot.get_channel(ID_CANAL_SOLICITUDES)
        mensaje_solicitud = await canal_solicitudes.send(embed=embed, view=Confirmacion(interaction.user, rol, timestamp_registro))

        await interaction.response.send_message(f"{usuario_nombre}, Tu solicitud como **{rol}** ha sido enviada y está pendiente de aprobación.", ephemeral=True)

    @ui.button(label="Cajero", style=ButtonStyle.green, emoji="🏦")
    async def cajero_button(self, button: ui.Button, interaction: Interaction):
        await self.handle_click(interaction, "Cajero")

    @ui.button(label="Asociado", style=ButtonStyle.blurple, emoji="🤝")
    async def asociado_button(self, button: ui.Button, interaction: Interaction):
        await self.handle_click(interaction, "Asociado")

class Confirmacion(ui.View):
    def __init__(self, user: nextcord.User, rol: str, timestamp_registro: str):
        super().__init__(timeout=None)
        self.user = user
        self.rol = rol
        self.timestamp_registro = timestamp_registro
        
    async def interaction_check(self, interaction: Interaction) -> bool:
        # Asegúrate de que solo el rol adecuado pueda interactuar con los botones
        return interaction.user.get_role(1205983428001013770) is not None

    @ui.button(label="Aceptar", style=ButtonStyle.green, emoji="✅")
    async def confirmar(self, button: ui.Button, interaction: Interaction):
        timestamp_aceptacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        async with aiosqlite.connect("usuarios.db") as db:
            await db.execute("INSERT INTO Usuarios (NombreUsuario, UID, Rol, TimestampRegistro, TimestampAceptacion) VALUES (?, ?, ?, ?, ?)",
                             (self.user.display_name, self.user.id, self.rol, self.timestamp_registro, timestamp_aceptacion))
            await db.commit()
        await interaction.response.send_message(f"Solicitud aprobada para {self.user.display_name}.", ephemeral=True)
        await interaction.message.delete()

    @ui.button(label="Rechazar", style=ButtonStyle.red, emoji="❌")
    async def cancelar(self, button: ui.Button, interaction: Interaction):
        timestamp_rechazo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("usuarios.db") as db:
            await db.execute(
                "INSERT INTO SolicitudesRechazadas (NombreUsuario, UID, Rol, TimestampRegistro, TimestampRechazo) VALUES (?, ?, ?, ?, ?)",
                (self.user.display_name, self.user.id, self.rol, self.timestamp_registro, timestamp_rechazo)
            )
            await db.commit()
        await interaction.response.send_message(f"Solicitud rechazada para {self.user.display_name}.", ephemeral=True)
        await interaction.message.delete()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    canal_seleccionrol = bot.get_channel(ID_CANAL_SELECCIONROL)
    embed = nextcord.Embed(title="Elige tu rol | Choose your role",
                           description="Selecciona tu rol en la casa de cambio | Select your role in the exchange",
                           color=nextcord.Color.blue())
    embed.add_field(name="Cajero", value="Breve Descripcion de Cajero", inline=False)
    embed.add_field(name="Asociado", value="Breve descripción de Asociado", inline=False)
    embed.set_footer(text="Haz clic en un botón para registrar tu rol | Click a button to register your role")
    await canal_seleccionrol.send(embed=embed, view=RolView())


    
# No olvides poner aquí tu token de bot real
bot.run(token)
