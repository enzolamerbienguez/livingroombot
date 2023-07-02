import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.parse
import openai
import base64
import datetime
import subprocess

# Configuration du bot Discord
bot_token = "MTEyNDc3MjI5NTY0MzI0NjgzMg.GSSVK1.x238Msq_JiPpiRB32BFOko2VBq1e4zP5DVrLm4"
bot_prefix = "/"

riot_api_key = "RGAPI-8197e440-7911-451e-9dfd-111126fa2e0d"

# Configuration de l'API OpenAI
openai.api_key = "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"

# Initialisation des intents
intents = discord.Intents.default()
intents.message_content = True

# Initialisation du client Discord
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Dictionnaire pour stocker l'historique de conversation pour chaque utilisateur
conversation_history = {}

# Événement lorsque le bot est prêt
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user.name}")


# Fonction de recherche de jeux sur cracked-games.org
def search_cracked_games(game_name):
    # URL du site cracked-games.org
    url = "https://cracked-games.org/"

    # Effectuer la requête de recherche
    response = requests.get(url, params={"search": game_name})
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver les résultats de recherche
    search_results = soup.find_all("a", class_="title")
    return search_results

# Fonction de recherche de jeux sur fitgirl-repacks.site
def search_fitgirl_repacks(game_name):
    # URL du site fitgirl-repacks.site
    url = "https://fitgirl-repacks.site/"

    # Effectuer la requête de recherche
    response = requests.get(url, params={"s": game_name})
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver les résultats de recherche
    search_results = soup.find_all("article", class_="post")
    return search_results

# Commande "/gamesearch"
@bot.command()
async def gamesearch(ctx, *game_name):
    game_name = " ".join(game_name)  # Convertir les mots en une phrase

    # Rechercher sur cracked-games.org
    cracked_games_results = search_cracked_games(game_name)

    # Rechercher sur fitgirl-repacks.site
    fitgirl_results = search_fitgirl_repacks(game_name)

    if cracked_games_results:
        # Prendre le premier résultat de recherche sur cracked-games.org
        first_result = cracked_games_results[0]
        game_title = first_result.text.strip()
        game_link = first_result["href"]

        await ctx.send(f"Un jeu correspondant a été trouvé sur cracked-games.org: {game_title}\nLien : {game_link}")
    elif fitgirl_results:
        # Prendre le premier résultat de recherche sur fitgirl-repacks.site
        first_result = fitgirl_results[0]
        game_title = first_result.find("h1", class_="entry-title").text.strip()
        game_link = first_result.find("a")["href"]

        await ctx.send(f"Un jeu correspondant a été trouvé sur fitgirl-repacks.site: {game_title}\nLien : https://fitgirl-repacks.site/?s={game_title}")
    else:
        await ctx.send("Aucun jeu trouvé correspondant à la recherche.")



# Vérifier les rôles autorisés pour le redémarrage
def is_allowed_role(ctx):
    allowed_roles = ["Fondateur", "Sous-fondateur"]  # Remplacez par les noms exacts de vos rôles autorisés
    return any(role.name in allowed_roles for role in ctx.author.roles)

# Commande de redémarrage
@bot.command()
@commands.check(is_allowed_role)  # Vérifier les rôles autorisés
async def restart(ctx):
    await ctx.send("Redémarrage en cours...")
    subprocess.Popen("py D:\livingroombot.py", shell=True)
    await bot.logout()

# Commande de calculatrice
@bot.command()
async def calc(ctx, *, expression):
    try:
        result = eval(expression)
        await ctx.send(f"Résultat : {result}")
    except:
        await ctx.send("Erreur de calcul. Veuillez vérifier votre expression.")

# Commande "/youtube"
@bot.command()
async def youtube(ctx, query):
    # URL de recherche sur YouTube
    search_query = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={search_query}"

    # Effectuer la requête de recherche
    response = requests.get(search_url)
    data = response.text

    # Extraire le premier lien vidéo de la page de résultats
    video_id = None
    start_index = data.find("watch?v=")
    if start_index != -1:
        end_index = data.find('"', start_index)
        if end_index != -1:
            video_id = data[start_index + 8 : end_index]

    if video_id:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        await ctx.send(f"Vidéo YouTube trouvée : {video_url}")
    else:
        await ctx.send("Aucune vidéo YouTube trouvée correspondant à la recherche.")

# Lancer le bot Discord
bot.run(bot_token)