# Importar librerías necesarias
import discord
import config
import random

# Crear el cliente de Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Registro de jugadores (ID de Discord como clave, información del jugador como valor)
players = {}


@client.event
async def on_ready():
    print(f'Conectado como {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=discord.Game(name='🐼Pandonium World RPG🐼'))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
# Comandos RPG:
    if message.content.startswith("%help"):
        await help_menu(message.author)

    elif message.content.startswith("%profile"):
        await show_profile(message.author)

    elif message.content.startswith("%hunt"):
        await go_hunting(message.author)

    elif message.content.startswith("%daily"):
        await claim_daily_reward(message.author)

    elif message.content.startswith("%explore"):
        await explore_area(message.author)

    elif message.content.startswith("%active"):
        await show_active_players(message.author)

    elif message.content.startswith("%fish"):
        await go_fishing(message.author)
    
    elif message.content.startswith("%train"):
        await train_character(message.author)

    elif message.content.startswith("%rank"):
        await show_rank(message.author)

    elif message.content.startswith("%trade"):
        await initiate_trade(message.author)

    elif message.content.startswith("%shop"):
        await access_shop(message.author)

    elif message.content.startswith("%bag"):
        await show_inventory(message.author)

    elif message.content.startswith("%chop"):
        await chop_wood(message.author)

    elif message.content.startswith("%plant"):
        await plant_seeds(message.author)
        
    elif message.content.startswith("%market"):
        await access_market(message.author)

    elif message.content.startswith("%claim"):
        await claim_rewards(message.author)

    elif message.content.startswith("%use"):
        await use_item(message.author, message.content[5:])

    elif message.content.startswith("%equip"):
        await equip_item(message.author, message.content[7:])

    elif message.content.startswith("%unequip"):
        await unequip_item(message.author, message.content[9:])

    elif message.content.startswith("%bank"):
        await access_bank(message.author)

    elif message.content.startswith("%set"):
        await configure_options(message.author, message.content[5:])

    elif message.content.startswith("%cure"):
        await cure_character(message.author)

    elif message.content.startswith("%faction"):
        await show_faction_info(message.author)

    elif message.content.startswith("%fight"):
        await initiate_combat(message.author)

    elif message.content.startswith("%time"):
        await show_server_time(message.author)

    elif message.content.startswith("%read"):
        await read_messages(message.author)

    elif message.content.startswith("%add"):
        await add_experience(message.author, message.content[5:])
        
    elif message.content.startswith("%leave"):
        await leave_faction(message.author)

    elif message.content.startswith("%mine"):
        await mine(message.author, message.content[6:])

    elif message.content.startswith("%join"):
        await join_faction(message.author, message.content[6:])

    elif message.content.startswith("%craft"):
        await craft_item(message.author, message.content[7:])

    elif message.content.startswith("%exp"):
        await spend_experience(message.author, message.content[5:])

    elif message.content.startswith("%cook"):
        await cook_item(message.author, message.content[6:])
        
    elif message.content.startswith("%give"):
        await give_item(message.author, message.content[6:])

    elif message.content.startswith("%pvp"):
        await initiate_pvp(message.author, message.mentions[0])

    elif message.content.startswith("%heal"):
        await heal_player(message.author, message.mentions[0])
        
    elif message.content.startswith("%start"):
        await start_character_creation(message.author)

        
# LOGICA PARA EL FUNCIONAMIENTO DE LOS COMANDOS:
async def help_menu(author):
    # Lista de comandos categorizados
    command_categories = {
        "Comandos de información": ["%info", "%stats", "%server"],
        "Comandos de singleplayer": ["%start", "%explore", "%home", "%mine", "%chop", "%fish", "%hunt", "%use", "%profile", "%tutorial", "%bag", "%craft", "%forge", "%train", "%equip", "%unequip", "%balance", "%sleep"],
        "Comandos multiplayer": ["%trade", "%shop", "%market", "%dungeon", "%create", "%join", "%leave", "%team", "%quest", "%search", "%fight", "%pvp", "%arena", "%slots", "%boost", "%activate", "%kill"]
    }

    # Crear el menú de ayuda
    help_embed = discord.Embed(title="Help Menu", description="Bienvenido al menú de ayuda! 🐼🎮", color=0x7289da)

    for category, commands in command_categories.items():
        command_list = "\n".join(commands)
        help_embed.add_field(name=category, value=command_list, inline=False)

    # Enviar el menú de ayuda al usuario
    await author.send(embed=help_embed)
# Funciones de los comandos RPG
async def show_profile(author):
    # Obtener información del jugador desde el registro
    player_info = players.get(str(author.id), None)

    if player_info:
        # Extraer datos del jugador
        level = player_info.get("level", 1)
        xp = player_info.get("xp", 0)
        current_rank = player_info.get("current_rank", "Novato")
        # Clase: [Luego te explico que poner aquí déjalo en blanco]
        faction = player_info.get("faction", "Sin facción")
        coins = player_info.get("coins", 0)
        backpack = player_info.get("backpack", [])

        # Crear un mensaje embed
        embed = discord.Embed(
            title=f"Perfil de {author.mention}",
            description=f"Nivel: {level}\nXP: {xp}\nRango: {current_rank}\nClase: \nFaction: {faction}\nCoins: {coins}\nMochila: {len(backpack)} ítems",
            color=0x87CEEB  # Color: Azul Plateado Claro Diamante
        )
        embed.set_footer(text="PAW PROFILE🎮")

        # Enviar el perfil como respuesta al mensaje original
        await message.reply(embed=embed)
    else:
        # Si no se encuentra información del jugador, enviar un mensaje de error como respuesta al mensaje original
        await message.reply("No se encontró información de tu perfil. ¿Te has registrado? Usa `%start` para comenzar.")

async def start_character_creation(author):
    # Crear un menú interactivo para la creación de personajes
    character_creation_embed = discord.Embed(
        title="Creación de Personaje",
        description="Elige tu raza, clase, lugar de spawn y arma inicial.",
        color=0x3498db  # Color azul claro
    )

    # Definir las opciones para cada categoría
    classes = ["Guerrero", "Comerciante", "Explorador", "Tanque", "Ingeniero", "Mercenario", "Noble", "Mago"]
    spawns = ["Castillo", "Santuario", "Volcán", "Pandonium", "Subterráneo", "Cementerio", "Bosque Oscuro", "Ciudadela Negra"]
    weapons = ["Espada", "Hacha", "Bastón", "Cuchillas", "Puños reforzados", "Libro de hechizos", "Garra reforzada"]

    class_descriptions = {
        "Guerrero": "Maestros en combate cuerpo a cuerpo, los guerreros destacan por su fuerza y habilidades tácticas.",
        "Comerciante": "Expertos en el comercio, los comerciantes poseen habilidades para obtener ganancias y negociar con éxito.",
        "Explorador": "Aventureros intrépidos, los exploradores son expertos en la supervivencia y la exploración de nuevos territorios.",
        "Tanque": "Resistentes y protectores, los tanques son la primera línea de defensa en el combate, absorbiendo daño para proteger a sus aliados.",
        "Ingeniero": "Hábiles constructores y estrategas, los ingenieros pueden crear y utilizar dispositivos avanzados.",
        "Mercenario": "Luchadores a sueldo, los mercenarios son hábiles en diversas formas de combate y trabajan por recompensas.",
        "Noble": "Miembros de la alta sociedad, los nobles poseen influencia política y habilidades sociales.",
        "Mago": "Manipuladores de la magia, los magos pueden lanzar hechizos poderosos y controlar energías arcanas."
    }

    spawn_descriptions = {
        "Castillo": "Eres originario de un antiguo castillo, aprendiste el arte de la nobleza y la estrategia militar.",
        "Santuario": "Creciste en un santuario sagrado, donde te enseñaron la conexión con lo divino y las artes curativas.",
        "Volcán": "Tu hogar es un volcán activo, y has desarrollado resistencia al fuego y habilidades relacionadas con la lava.",
        "Pandonium": "Naciste en Pandonium, la tierra de los pandas, y has aprendido sus técnicas únicas y amigables.",
        "Subterráneo": "Creciste en las profundidades subterráneas, desarrollando habilidades furtivas y conocimientos del inframundo.",
        "Cementerio": "Tu hogar es un antiguo cementerio, y has desarrollado habilidades relacionadas con la muerte y la oscuridad.",
        "Bosque Oscuro": "Naciste en un bosque oscuro y misterioso, donde aprendiste a dominar la naturaleza y la magia druídica.",
        "Ciudadela Negra": "Creciste en la Ciudadela Negra, un lugar lleno de secretos y maquinaciones, donde te entrenaron en el arte del engaño y la astucia."
    }

    weapon_descriptions = {
        "Espada": "Una espada afilada, perfecta para el combate cuerpo a cuerpo.",
        "Hacha": "Un hacha robusta, ideal para cortar madera y causar daño en combate.",
        "Bastón": "Un bastón mágico, utilizado por aquellos que desean canalizar energías místicas.",
        "Cuchillas": "Cuchillas afiladas, ideales para ataques rápidos y precisos.",
        "Puños reforzados": "Tus propios puños, endurecidos y listos para el combate cuerpo a cuerpo.",
        "Libro de hechizos": "Un libro lleno de hechizos, utilizado por magos para lanzar conjuros poderosos.",
        "Garra reforzada": "Garras afiladas y reforzadas, perfectas para desgarrar a tus enemigos."
    }

    # Definir las opciones para cada categoría
    races = ["Humano", "Panda", "Dragon", "Orco", "Zombie", "Demonio", "Angel"]

    # Agregar descripciones de razas
    race_descriptions = {
        "Humano": "Versátiles y adaptables, los humanos son conocidos por su habilidad para sobresalir en diversas áreas.",
        "Panda": "Juguetones y amigables, los pandas son expertos en técnicas de combate únicas y adoran la paz.",
        "Dragon": "Feroz y majestuoso, los dragones poseen habilidades místicas y son temidos en la batalla.",
        "Orco": "Fuertes y resistentes, los orcos son guerreros natos con una afinidad por las armas pesadas.",
        "Zombie": "Reanimados de la muerte, los zombies poseen una resistencia extraordinaria y habilidades regenerativas.",
        "Demonio": "Dotados de poderes infernales, los demonios son maestros en artes oscuras y estrategias astutas.",
        "Angel": "Celestiales y benevolentes, los ángeles poseen habilidades divinas y protegen a los inocentes."
    }

    # Agregar descripciones al embed
    for race in races:
        character_creation_embed.add_field(
            name=race,
            value=race_descriptions[race],
            inline=False
        )

    # Enviar el primer mensaje de creación de personaje
    creation_message = await author.send(embed=character_creation_embed)

    # Agregar reacciones para cada opción
    for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]:
        await creation_message.add_reaction(emoji)

    # Función para manejar la elección del usuario
    def check(reaction, user):
        return user == author and reaction.message.id == creation_message.id and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

    try:
        # Esperar la reacción del usuario
        reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=check)

        # Obtener la opción elegida por el usuario
        choice = int(reaction.emoji[0]) - 1
        chosen_race = races[choice]

        # Mostrar información de la raza seleccionada
        race_embed = discord.Embed(
            title=f"Creación de Personaje - {chosen_race}",
            description=race_descriptions[chosen_race],
            color=0x3498db
        )

        # Enviar mensaje con información de la raza y opciones de confirmación
        race_message = await author.send(embed=race_embed)
        await race_message.add_reaction("✅")
        await race_message.add_reaction("❌")

        # Función para manejar la confirmación de la elección de raza
        def race_confirmation(reaction, user):
            return user == author and reaction.message.id == race_message.id and str(reaction.emoji) in ["✅", "❌"]

        # Esperar la reacción de confirmación
        race_reaction, _ = await client.wait_for("reaction_add", timeout=60.0, check=race_confirmation)

        if str(race_reaction.emoji) == "✅":
            # El usuario confirmó la elección de raza, pasar al siguiente paso (clase)
            await author.send("¡Excelente elección! Ahora escoge tu clase.")
            await choose_class(author)

        elif str(race_reaction.emoji) == "❌":
            # El usuario quiere cambiar de raza, regresar al menú principal
            await start_character_creation(author)

    except asyncio.TimeoutError:
        # Si el usuario no reacciona a tiempo, enviar un mensaje indicando eso
        await author.send("Tiempo de espera agotado. Por favor, intenta nuevamente.")
# ...

async def choose_class(author):
    # Lógica para escoger la clase, similar a la raza
    pass
        
client.run(config.TOKEN)