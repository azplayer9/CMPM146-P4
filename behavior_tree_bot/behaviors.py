import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_highest_growth(state):
    if len(state.my_fleets()) >= len(state.my_planets()):
        return False

    # Find the enemy planet with the highest growth rate.
    growth_planet = min(state.enemy_planets(), key=lambda t: t.growth_rate, default=None)

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not growth_planet:
        # No legal source or destination
        return False
    else:
        # Send half the ships from my strongest planet to the weakest enemy planet.
        dist = state.distance(strongest_planet.ID, growth_planet.ID)
        est_enemy_ships = growth_planet.num_ships + dist * growth_planet.growth_rate

        if (strongest_planet.num_ships/2 > est_enemy_ships):    # dont want to risk too much by attacking this point
            return issue_order(state, strongest_planet.ID, growth_planet.ID, strongest_planet.num_ships/2)
    return False

def attack_nearest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= len(state.my_planets()):
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    closest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not closest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        dist = state.distance(strongest_planet.ID, closest_planet.ID)
        est_enemy_ships = closest_planet.num_ships + dist * closest_planet.growth_rate

        if (strongest_planet.num_ships > est_enemy_ships):     # willing to risk more troops to attack because this planet is closer
            return issue_order(state, strongest_planet.ID, closest_planet.ID, est_enemy_ships + 1)
    return False

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= len(state.my_planets()):
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        dist = state.distance(strongest_planet.ID, weakest_planet.ID)
        est_enemy_ships = weakest_planet.num_ships + dist * weakest_planet.growth_rate
        if (strongest_planet.num_ships/2 > est_enemy_ships):
            return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    return False

def spread_to_nearest_neutral_planet(state):
    # assume: there is a neutral planet
    # find the nearest neutral planet to our strongest planet. Send half of its troops to the neutral planet

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    closest_planet = min(state.enemy_planets(), key=lambda p: state.distance(strongest_planet.ID, p.ID), default=None)
    # closest_enemy_to_neutral = min(state.enemy_planets(), key=lambda p: state.distance(closest_planet.ID, p.ID), default=None)

    if not strongest_planet or not closest_planet:
        return False
    
    elif strongest_planet.num_ships > closest_planet.num_ships + 10 :
        # (4) Send half the ships from my strongest planet to the weakest neutral planet ONLY IF IT HAS MORE SHIPS.
            return issue_order(state, strongest_planet.ID, closest_planet.ID, closest_planet.num_ships + 10)
    else:
        return False

def closest_neutral(state, source_planet, neutral_planets):
    """ Helper function to find the closest neutral planet from a source planet. """
    if neutral_planets:
        close = neutral_planets[0]
        dist = state.distance(source_planet.ID, neutral_planets[0].ID)
        for np in neutral_planets:
            if state.distance(source_planet.ID, np.ID) < dist:
                dist = state.distance(source_planet.ID, np.ID)
                close = np
        return close
    else:
        return None

def strongest_to_weakest(state):
    if len(state.my_fleets()) >= len(state.my_planets())/3: # choose a harder condition to decentivize this action
        return False

    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # send some ships from strongest planet to the weakest planet
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships/4)