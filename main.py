# 2023 Steven Chiacchira
'''
Script for running Fantasy Flight Star Wars RPG Discord bot.
'''
import discord
import random
import yaml
from discord.ext import commands
from enum import Enum
from typing import Optional

from src.dice import *
from src.emoji import *


def add_to_gross_roll(gross_roll: RollResult, 
                      roll: RollResult) -> None:
    '''
    :brief: adds the total results from `roll` to `gross_roll`.

    :param gross_roll: the roll to be added to.
    :param roll: the roll to add to `gross_roll`.
    '''
    for key, value in roll.items():
        gross_roll[key] += value


def get_discord_api_key() -> str:
    '''
    :brief: returns the first line of the `API_KEY` file. Should contain your 
    Discord api key.

    :returns: the first line of the `API_KEY` file.
    '''
    with open('API_KEY') as stream:
        return stream.readline()
    

def get_emoji_die_summary_from_pool(pool: str) -> str:
    '''
    :brief: generates a string with an emoji for each die in `pool`.
    
    The generated emoji are ordered: force_die, proficiency_die, ability_die, 
    boost_die, challenge_die, difficulty_die, setback_die.

    :param pool: the pool of dice to generate emoji from.

    :returns: a string with an emoji for each die in `pool`.
    '''
    result: str = ''

    result += EmojiKeys.FORCE.value * pool.count(DieKeys.FORCE.value)
    result += EmojiKeys.PROFICIENCY.value * pool.count(DieKeys.PROFICIENCY.value)
    result += EmojiKeys.ABILITY.value * pool.count(DieKeys.ABILITY.value)
    result += EmojiKeys.BOOST.value * pool.count(DieKeys.BOOST.value)
    result += EmojiKeys.CHALLENGE.value * pool.count(DieKeys.CHALLENGE.value)
    result += EmojiKeys.DIFFICULTY.value * pool.count(DieKeys.DIFFICULTY.value)
    result += EmojiKeys.SETBACK.value * pool.count(DieKeys.SETBACK.value)

    return result


def get_emoji_result_summary_from_roll(roll: RollResult) -> str:
    '''
    :brief: generates a string with an emoji for each result in `roll`.

    The generated emoji are ordered: light_result, dark_result, 
    triumph_result, despair_result, success_result, failure_result, 
    advantage_result, threat_result.

    :param roll: the set of roll results to generate emoji from.

    :returns: a string with an emoji for each result in `roll`.
    '''
    result: str = ''

    result += EmojiKeys.LIGHT.value * roll[ResultKeys.LIGHT.value]
    result += EmojiKeys.DARK.value * roll[ResultKeys.DARK.value]
    result += EmojiKeys.TRIUMPH.value * roll[ResultKeys.TRIUMPH.value]
    result += EmojiKeys.DESPAIR.value * roll[ResultKeys.DESPAIR.value]
    result += EmojiKeys.SUCCESS.value * roll[ResultKeys.SUCCESS.value]
    result += EmojiKeys.FAILURE.value * roll[ResultKeys.FAILURE.value]
    result += EmojiKeys.ADVANTAGE.value * roll[ResultKeys.ADVANTAGE.value]
    result += EmojiKeys.THREAT.value * roll[ResultKeys.THREAT.value]

    return result


def get_random_text_summary(choices: list[str]) -> str:
    '''
    :brief: selects a random message from a list of messages.

    :param choices: a list of messages to select from.

    :returns: the randomly selected message.
    '''
    return choices[random.randint(0, len(choices) - 1)]


def get_text_result_summary_from_roll(roll: RollResult) -> str:
    '''
    :brief: generates a result given the values present in `roll`.

    The generated results are drawn from content/text_summaries.yml

    :param roll: the roll to generate a result from.
    
    :returns: a generated result based on the values present in `roll`.
    '''
    # Unpack net roll into human-readable variables
    success = roll[ResultKeys.SUCCESS.value] > 0
    advantage = roll[ResultKeys.ADVANTAGE.value] > 0
    threat = roll[ResultKeys.THREAT.value] > 0
    triumph = roll[ResultKeys.TRIUMPH.value] > 0
    despair = roll[ResultKeys.DESPAIR.value] > 0
    light = roll[ResultKeys.LIGHT.value] > 0
    dark = roll[ResultKeys.DARK.value] > 0

    # Load text summaries from YAML file
    text_summaries = load_yaml('content/text_summaries.yml')

    # Cases for force dice
    if light and dark:
        summary_message: str = get_random_text_summary(text_summaries['light_dark'])
    elif light:
        summary_message: str = get_random_text_summary(text_summaries['light'])
    elif dark:
        summary_message: str = get_random_text_summary(text_summaries['dark'])
    
    # Cases for narrative dice
    elif triumph and despair:
        summary_message: str = get_random_text_summary(text_summaries['triumph_despair'])
    elif triumph:
        summary_message: str = get_random_text_summary(text_summaries['triumph'])
    elif despair:
        summary_message: str = get_random_text_summary(text_summaries['despair'])
    elif success and advantage:
        summary_message: str = get_random_text_summary(text_summaries['success_advantage'])
    elif success and threat:
        summary_message: str = get_random_text_summary(text_summaries['success_threat'])
    elif success:
        summary_message: str = get_random_text_summary(text_summaries['success'])
    elif advantage:
        summary_message: str = get_random_text_summary(text_summaries['failure_advantage'])
    elif threat:
        summary_message: str = get_random_text_summary(text_summaries['failure_threat'])
    else:
        summary_message: str = get_random_text_summary(text_summaries['failure'])

    return summary_message


def load_yaml(filename: str) -> dict:
    '''
    :brief: loads the YAML data in `filename`.

    :param filename: the name of the file to be read.

    :returns: dictionary read from `filename`.
    '''
    with open(filename) as stream:
        return yaml.safe_load(stream)
    

def validate_roll_args(args: str) -> bool:
    '''
    :brief: validates that all characters in `args` are valid die keys.

    :param args: a string to be checked as containing only valid die keys.

    :returns: `True` if the string contains only valid die keys, and `False` 
    otherwise.
    '''
    for char in args:
        if char not in {k.value for k in DieKeys}:
            return False
    
    return True


# Instantiate bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', 
                            intents=intents)


@bot.command()
async def roll(ctx,
               arg: Optional[str]=None) -> None:
    '''
    :brief: discord command for rolling dice.

    Accepts a string of dice to be rolled, rolls them, cancels corresponding 
    values, then sends a message to the channel the command was sent in.

    :param arg: the passed argument to the bot.
    '''
    # Case for invalid roll passed
    if arg == None or not validate_roll_args(arg.lower()):
        await ctx.send(f'{ctx.message.author.mention} Received an invalid roll! Use the highlighted characters for rolls:\r'\
                    f'**f**orce ({EmojiKeys.FORCE.value})\r'\
                    f'**p**roficiency ({EmojiKeys.PROFICIENCY.value})\r'\
                    f'**a**bility ({EmojiKeys.ABILITY.value})\r'\
                    f'**b**oost ({EmojiKeys.BOOST.value})\r'\
                    f'**c**hallenge ({EmojiKeys.CHALLENGE.value})\r'\
                    f'**d**ifficulty ({EmojiKeys.DIFFICULTY.value})\r'\
                    f'**s**etback ({EmojiKeys.SETBACK.value})\r')
        return
    
    lowercase_arg = arg.lower()
        
    # Case for valid roll
    gross_roll: RollResult = get_empty_roll_result()

    for char in lowercase_arg:
        add_to_gross_roll(gross_roll, get_roll_result_from_die_key(char))

    net_roll: RollResult = get_canceled_dice(gross_roll)
    summary_text: str = get_text_result_summary_from_roll(net_roll)
    summary_emoji_roll: str = get_emoji_die_summary_from_pool(lowercase_arg)
    summary_emoji_results: str = get_emoji_result_summary_from_roll(net_roll)

    message = f'{summary_text.format(ctx.message.author.mention)}\r'\
                   f'**Total dice pool**:  {summary_emoji_roll}\r'\
                   f'**Canceled result**: {summary_emoji_results}'

    if len(message) > 2000:
        message = f'{ctx.message.author.mention} Your roll is too large to '\
        + f'handle! Try rolling fewer dice!'

    await ctx.send(message)


@bot.command()
async def r(ctx,
            arg: str=None) -> None:
    '''
    :brief: alias for `roll()`.
    '''
    await roll(ctx, arg)


# Run bot with Discord API key
API_KEY: str = get_discord_api_key()

bot.run(API_KEY)
