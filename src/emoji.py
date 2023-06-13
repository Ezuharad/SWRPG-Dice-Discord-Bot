# 2023 Steven Chiacchira
from enum import Enum

from src.dice import DieKeys, ResultKeys


class EmojiKeys(Enum):
    ABILITY = '<:ability_die:1117981883490390027>'
    DIFFICULTY = '<:difficulty_die:1117981891308572782>'
    BOOST = '<:boost_die:1117981886690644068>'
    SETBACK = '<:setback_die:1117982396860604577>'
    PROFICIENCY = '<:proficiency_die:1117982395874947132>'
    CHALLENGE = '<:challenge_die:1117981887873437706>'
    FORCE = '<:force_die:1117982394532773928>'

    LIGHT = '<:light_result:1117981894580121650>'
    DARK = '<:dark_result:1117981889291112569>'
    TRIUMPH = '<:triumph_result:1117981899944644638>'
    DESPAIR = '<:despair_result:1117981890234818663>'
    SUCCESS = '<:success_result:1117982397716238357>'
    FAILURE = '<:failure_result:1117981892222918706>'
    ADVANTAGE = '<:advantage_result:1117981885461692467>'
    THREAT = '<:threat_result:1117982399905669120>'
