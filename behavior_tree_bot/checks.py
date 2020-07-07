def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
         + sum(fleet.num_ships for fleet in state.my_fleets()) \
         > sum(planet.num_ships for planet in state.enemy_planets()) \
         + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_my_strongest_is_stronger(state):
    strongest_ally = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    strongest_enemy = max(state.enemy_planets(), key=lambda p: p.num_ships, default=None)
    return strongest_ally.num_ships > strongest_enemy.num_ships

