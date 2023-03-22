##Written By Emmett 2021

## Final Project. Use an API to access data. 

## Chosen API is Discord. https://discord.com/developers/docs/intro
## Using discord.py library https://github.com/Rapptz/discord.py 

## Plan to make a bot, which recognises new users, and assigns roles based on responses. # enable logging, to surface errors in console
import logging
logging.basicConfig(level=logging.INFO)

# import discord, and set intents (permissions for the bot)
import discord
intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

# set variable for bot user id, bot token, and guild id
bot_id = YOUR_BOT_ID_HERE
bot_token = YOUR_BOT_TOKEN_HERE
guild_id = YOUR_GUILD_ID_HERE

# set emoji variables
yn_emote = ['✔️', '❌']
c_emote = ['🟦', '🟩', '🟨', '🟥']

# set role variables
member_role = YOUR_ROLE_ID
team_blue = YOUR_ROLE_ID_BLUE
team_green = YOUR_ROLE_ID_GREEN
team_yellow = YOUR_ROLE_ID_YELLOW
team_red = YOUR_ROLE_ID_RED

# confirm client is running
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# recognise user joining, and send welcome direct message
@client.event
async def on_member_join(member):
    await member.send(f'Hello {member.name} Welcome to the testing server! Would you like to join? Choose either {yn_emote[0]} or {yn_emote[1]}')
    # print name in console
    print (member.name, 'joined')
    # member = member
    # return member



# ensure emotes are only added to the apropriate message, and only when the message is created by the bot
@client.event
async def on_message(message):
    # add yn_emote reactions to welcome message, to act as graphical options for the user to select
    if "hello" in (message.content.lower()) and (message.author.id) == bot_id:
        for emote in yn_emote:
            await message.add_reaction(emote)
        return
    # add c_emotes for team selection
    elif "fantastic" in (message.content.lower()) and (message.author.id) == bot_id:
        for emote in c_emote:
            await message.add_reaction(emote)
        return
    else:
        return

# recognise when user reacts to yn_emote, but ignore when bot adds reaction
# assign inital role if check is selected, or kick if cross is selected
# it is nessecary to target the correct guild, as the interaction is occuring in Direct Message. 
# As such trying to apply roles within DM fails, as guild is not present
# passing the guild ID alone, seems to be insufficiant, instead the full object must be loaded through get_guild()
# The same must be applied to member, as the user in the DM is a separate object from guild member
# role also requires a full object to be loaded, the ID as well is not sufficiant while within a DM. 

@client.event
async def on_reaction_add(reaction, user):
    user_id = (user.id)
    guild = client.get_guild(guild_id)
    member = guild.get_member(user_id)
    m_role = guild.get_role(member_role)
    b_role = guild.get_role(team_blue)
    g_role = guild.get_role(team_green)
    y_role = guild.get_role(team_yellow)
    r_role = guild.get_role(team_red)
    all_team_roles = [b_role, g_role, y_role, r_role]
    all_member_roles = member.roles

    #checking for reation emote used, checking that the user reacting is not the bot, and checking that the message was written by the bot

    # starting with yn_emote reactions, adding member role if check is selected
    if (user.id) != bot_id and (reaction.message.author.id) == bot_id:
        if (reaction.emoji) == yn_emote[0]:
            await member.add_roles(m_role)
            await member.send(f'Fantastic, you are now a member. Time to choose your team, pick a colour!')

        # kicking user if cross is selected
        elif (reaction.emoji) == yn_emote[1]:
            await member.send(f'No worries, perhaps another time!')
            await guild.kick(member, reason="test")

        #checking if user already has a team role
        elif any(item in all_team_roles for item in all_member_roles) == True:
            await member.send(f'You already have a team role, it cannot be changed. \nYou can tap ❌ above to leave and start again\nOr you can visit your team chat')

        # Now checking for the c_emote reactions, to assign team roles
        # Blue Team
        elif (reaction.emoji) == c_emote[0]:
            await member.add_roles(b_role)
            await member.send(f'{c_emote[0]} Weclome to the Blue Team!')    

        # Green Team
        elif (reaction.emoji) == c_emote[1]:
            await member.add_roles(g_role)
            await member.send(f'{c_emote[1]} Weclome to the Green Team!')

        # Yellow Team
        elif (reaction.emoji) == c_emote[2]:
            await member.add_roles(y_role)
            await member.send(f'{c_emote[2]} Weclome to the Yellow Team!')

        # Red team
        elif (reaction.emoji) == c_emote[3]:
            await member.add_roles(r_role)
            await member.send(f'{c_emote[3]} Weclome to the Red Team!')

        else:
            await member.send(f'{reaction.emoji} is not a valid response')
    else: return


#run discord client
client.run(bot_token)
