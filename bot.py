import discord
from discord.ext import commands
import aiosqlite
import os
from dotenv import load_dotenv

# Define los intents que tu bot necesitará.
intents = discord.Intents.default()
intents = discord.Intents().all()

#cargar variables de entorno
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Instancia el bot con los intents.
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='crear_usuario')
async def crear_usuario(ctx, nombre_usuario: str, rol: str, informacion_contacto: str = None):
    async with aiosqlite.connect("usuarios.db") as db:
        await db.execute(
            "INSERT INTO Usuarios (NombreUsuario, Rol, InformacionContacto) VALUES (?, ?, ?)",
            (nombre_usuario, rol, informacion_contacto),
        )
        await db.commit()
    await ctx.send(f"Usuario {nombre_usuario} creado.")

bot.run(token)
