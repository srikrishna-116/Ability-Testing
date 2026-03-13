def update_ability(ability, result, difficulty, k=0.1):

    ability = ability + k * (result - difficulty)

    if ability < 0:
        ability = 0

    if ability > 1:
        ability = 1

    return ability