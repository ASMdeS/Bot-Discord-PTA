# Importando aquilo que será utilizado
import discord
from discord.ext import commands
import gspread
import gspread.utils
from oauth2client.service_account import ServiceAccountCredentials

# Discord Bot Setup
bot_token = "MTE4NTA0MTA5Nzc2MDcwNjYwMg.GhZCYd.I8J5SUIoEvoV96_44OS1UJFwZ8YxXWPNF0y9rQ"
bot_prefix = "!"

# Inicializando o Bot
bot = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "C:\\Users\\DELL\\Downloads\\pta-discord-bot-2067a8ec5dff.json", scope)
gc = gspread.authorize(credentials)
spreadsheet_key = "1YsJDL19AdF9luUYdM8QFhcxXuKxeb3j9vsS9UhmA09k"
sheet = gc.open_by_key(spreadsheet_key).sheet1

# Quando o Bot é inicializado
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

# Recebendo resposta
@bot.command(name="answer")
async def answer(ctx, column, row):
    try:
        column_mapping = {
            "receita": "B",
            "custo_fixo": "C",
            "custo_variável": "D",
            "custo_total": "E",
            "margem_de_contribuição": "F",
            "lucro": "G",
            "vendas": "H",
        }

        row_mapping = {
            "janeiro": 2,
            "fevereiro": 3,
            "março": 4,
            "abril": 5,
            "maio": 6,
            "junho": 7,
            "julho": 8,
            "agosto": 9,
            "setembro": 10,
            "outubro": 11,
            "novembro": 12,
            "dezembro": 13,
        }

        row_value = row_mapping.get(row.lower())
        if row_value is None:
            raise ValueError(f"Invalid row: {row}")

        column_value = column_mapping.get(column.lower())
        if column_value is None:
            raise ValueError(f"Invalid column: {column}")

        column_number = gspread.utils.a1_to_rowcol(column_value + '1')[1]

        cell_value = sheet.cell(row_value, column_number).value

        await ctx.send(f"The value in {column} {row} is: {cell_value}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Rodando o Bot
bot.run(bot_token)
