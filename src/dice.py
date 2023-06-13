# 2023 Steven Chiacchira
from enum import Enum
from random import randint

RollResult = dict[str, int]


class DieKeys(Enum):
    ABILITY = 'a'
    DIFFICULTY = 'd'
    BOOST = 'b'
    SETBACK = 's'
    PROFICIENCY = 'p'
    CHALLENGE = 'c'
    FORCE = 'f'


class ResultKeys(Enum):
    LIGHT = 'light'
    DARK = 'dark'
    SUCCESS = 'success'
    FAILURE = 'failure'
    ADVANTAGE = 'advantage'
    THREAT = 'threat'
    TRIUMPH = 'triumph'
    DESPAIR = 'despair'


def get_canceled_dice(roll: RollResult) -> RollResult:
    result: RollResult = get_empty_roll_result()

    # Add other values
    for key in {ResultKeys.LIGHT, ResultKeys.DARK, ResultKeys.TRIUMPH, ResultKeys.DESPAIR}:
        result[key.value] = roll[key.value]
    
    # Note here a negative number just represents a `bad` result
    total_success: int = roll[ResultKeys.SUCCESS.value] - roll[ResultKeys.FAILURE.value]
    total_advantage: int = roll[ResultKeys.ADVANTAGE.value] - roll[ResultKeys.THREAT.value]

    # Cancel success / failure, overwriting previous values
    if total_success > 0:
        result[ResultKeys.SUCCESS.value] = abs(total_success)
    else:
        result[ResultKeys.FAILURE.value] = abs(total_success)
    
    # Cancel advantage / threat
    if total_advantage > 0:
        result[ResultKeys.ADVANTAGE.value] = abs(total_advantage)
    else:
        result[ResultKeys.THREAT.value] = abs(total_advantage)
    
    return result


def get_empty_roll_result() -> RollResult:
    empty_result: dict[str, int] = dict()
    for key in ResultKeys:
        empty_result[key.value] = 0

    return empty_result


def get_roll_result_from_die_key(die_key: str) -> RollResult:
    match(die_key):
        case DieKeys.ABILITY.value:
            return roll_ability()
        case DieKeys.DIFFICULTY.value:
            return roll_difficulty()
        case DieKeys.BOOST.value:
            return roll_boost()
        case DieKeys.SETBACK.value:
            return roll_setback()
        case DieKeys.PROFICIENCY.value:
            return roll_proficiency()
        case DieKeys.CHALLENGE.value:
            return roll_challenge()
        case DieKeys.FORCE.value:
            return roll_force()


def roll_ability() -> RollResult:
    result: RollResult = get_empty_roll_result()
    
    n: int = randint(0, 7)
    match(n):
        case 0:
            pass
        case 1 | 2:
            result[ResultKeys.ADVANTAGE.value] = 1
        case 3:
            result[ResultKeys.ADVANTAGE.value] = 2
        case 4 | 5:
            result[ResultKeys.SUCCESS.value] = 1
        case 6:
            result[ResultKeys.ADVANTAGE.value] = 1
            result[ResultKeys.SUCCESS.value] = 1
        case 7:
            result[ResultKeys.SUCCESS.value] = 2
    
    return result


def roll_difficulty() -> RollResult:
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 7)
    match(n):
        case 0:
            pass
        case 1 | 2 | 3:
            result[ResultKeys.THREAT.value] = 1
        case 4:
            result[ResultKeys.THREAT.value] = 2
        case 5:
            result[ResultKeys.FAILURE.value] = 1
        case 6:
            result[ResultKeys.THREAT.value] = 1
            result[ResultKeys.FAILURE.value] = 1
        case 7:
            result[ResultKeys.FAILURE.value] = 2
    
    return result


def roll_boost() -> RollResult:
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 5)
    match(n):
        case 0 | 1:
            pass
        case 2:
            result[ResultKeys.ADVANTAGE.value] = 1
        case 3:
            result[ResultKeys.ADVANTAGE.value] = 2
        case 4:
            result[ResultKeys.SUCCESS.value] = 1
        case 5:
            result[ResultKeys.ADVANTAGE.value] = 1
            result[ResultKeys.SUCCESS.value] = 1
        
    return result


def roll_setback() -> RollResult:
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 5)
    match(n):
        case 0 | 1:
            pass
        case 2 | 3:
            result[ResultKeys.THREAT.value] = 1
        case 4 | 5:
            result[ResultKeys.FAILURE.value] = 1
    
    return result


def roll_proficiency() -> RollResult: 
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 11)
    match(n):
        case 0:
            pass
        case 1:
            result[ResultKeys.ADVANTAGE.value] = 1
        case 2 | 3:
            result[ResultKeys.ADVANTAGE.value] = 2
        case 4 | 5:
            result[ResultKeys.SUCCESS.value] = 2
        case 6 | 7 | 8:
            result[ResultKeys.ADVANTAGE.value] = 1
            result[ResultKeys.SUCCESS.value] = 1
        case 9 | 10:
            result[ResultKeys.SUCCESS.value] = 2
        case 11:
            result[ResultKeys.TRIUMPH.value] = 1
    
    return result


def roll_challenge() -> RollResult:
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 11)
    match(n):
        case 0:
            pass
        case 1 | 2:
            result[ResultKeys.THREAT.value] = 1
        case 3 | 4:
            result[ResultKeys.THREAT.value] = 2
        case 5 | 6:
            result[ResultKeys.FAILURE.value] = 1
        case 7 | 8:
            result[ResultKeys.THREAT.value] = 1
            result[ResultKeys.FAILURE.value] = 1
        case 9 | 10:
            result[ResultKeys.FAILURE.value] = 2
        case 11:
            result[ResultKeys.DESPAIR.value] = 1
    
    return result


def roll_force() -> RollResult:
    result: RollResult = get_empty_roll_result()

    n: int = randint(0, 11)
    match(n):
        case 0 | 1:
            result[ResultKeys.LIGHT.value] = 1
        case 2 | 3 | 4 | 5 | 6 | 7:
            result[ResultKeys.DARK.value] = 1
        case 8 | 9 | 10:
            result[ResultKeys.LIGHT.value] = 2
        case 11:
            result[ResultKeys.DARK.value] = 2
    
    return result
