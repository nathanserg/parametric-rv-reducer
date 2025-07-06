
############### Parameters range ###############
cycloidal_values = range(8, 51) # Cycloidal reduction ratio
planet_values = range(12, 41)   # Planet gear teeth range
sun_values = range(12, 41)      # Sun gear teeth range

############### Cycloidal parameters ###############
cycloidal_excentricity = 0.85       # Excentricity of the cycloidal drive
cycloidal_diameter = 65             # Base diameter of the cycloidal disk
cycloidal_roller_diameter = 3.95    # Diameter of the cycloidal rollers
cycloidal_min_wall_thickness = 1.5  # Minimum wall thickness between the lobes of the disk and the inside diameter of the disk

############### Gears parameters ###############
unit_gear_ratio = True      # True if you want to include the unit gear ratio (1:1) in the results

nb_planets = 3              # Number of planets
gear_modulus = 1            # Module of the gears
gear_minimum_modulus = 0.9  # Minimum module of the gears you can print
gear_dist_to_disk = 1       # Distance from the gear to the inside of the cycloidal disk

############### Filters ###############
R_min = 28                      # Minimum reduction ratio
R_max = 32                      # Maximum reduction ratio
filter_by_given_modulus = False # True if you want to filter by gear_modulus, False if you want to filter by maximum gear modulus


def get_all_combinations(cycloidal_values, planet_values, sun_values, R_min, R_max, unit_gear_ratio):
    valid_results = [] # Valid results [cycloidal ratio, sun gear teeth, planet gear teeth, final reduction ratio]
    for x in cycloidal_values:
        for y in planet_values:
            for z in sun_values:
                gear_ratio = y / z
                if gear_ratio < 1:
                    continue
                if not unit_gear_ratio and gear_ratio == 1:
                    continue
                if 1.8 < gear_ratio:
                    continue
                R = (x * y) / z
                if R.is_integer() and R_min <= R <= R_max:
                    valid_results.append([x, y, z, int(R)])
    return valid_results

def filter_by_number_of_planet(valid_results, nb_planets=3):
    new_valid_results = []
    for result in valid_results:
        x, y, z, R = result
        ring_nb_teeth = 2*y + z
        sun_by_nb_planet = z / nb_planets
        ring_by_nb_planet = ring_nb_teeth / nb_planets
        if sun_by_nb_planet.is_integer() and ring_by_nb_planet.is_integer():
            new_valid_results.append(result)
    return new_valid_results

def calculate_cycloidal_inside_diam(cycloidal_excentricity, cycloidal_diameter, cycloidal_roller_diameter, cycloidal_min_wall_thickness):
    # Calculate the inside diameter of the cycloidal drive
    return cycloidal_diameter - 2*cycloidal_excentricity - cycloidal_roller_diameter - 2*cycloidal_min_wall_thickness

def filter_by_gear_diam(valid_results, gear_modulus, cycloidal_inside_diam, gear_dist_to_disk):
    new_valid_results = []
    for result in valid_results:
        x, y, z, R = result
        ring_nb_teeth = 2*y + z
        ring_outside_diam = gear_modulus*(ring_nb_teeth + 2)
        if ring_outside_diam <= cycloidal_inside_diam - 2*gear_dist_to_disk:
            new_valid_results.append(result)
    return new_valid_results

def filter_max_gear_modulus(valid_results, cycloidal_inside_diam, gear_dist_to_disk, gear_minimum_modulus):
    new_valid_results = []
    for result in valid_results:
        x, y, z, R = result
        ring_nb_teeth = 2*y + z
        max_gear_modulus = (cycloidal_inside_diam - 2*gear_dist_to_disk) / (ring_nb_teeth + 2)
        if max_gear_modulus < gear_minimum_modulus:
            continue
        new_valid_results.append(result + [max_gear_modulus])
    return new_valid_results

valid_results = get_all_combinations(cycloidal_values, planet_values, sun_values, R_min, R_max, unit_gear_ratio)
valid_results = filter_by_number_of_planet(valid_results, nb_planets)
cycloidal_inside_diam = calculate_cycloidal_inside_diam(cycloidal_excentricity, cycloidal_diameter, cycloidal_roller_diameter, cycloidal_min_wall_thickness)
if filter_by_given_modulus:
    valid_results = filter_by_gear_diam(valid_results, gear_modulus, cycloidal_inside_diam, gear_dist_to_disk)
else:
    valid_results = filter_max_gear_modulus(valid_results, cycloidal_inside_diam, gear_dist_to_disk, gear_minimum_modulus)

# Affichage
print(len(valid_results), "valid combinations found")
print(f"cycloidal inside diameter = {cycloidal_inside_diam:.2f} mm\n")

for combo in valid_results:
    if len(combo) == 5:
        print(f"cycloid ratio = {combo[0]}, planet nb teeth = {combo[1]}, sun nb teeth = {combo[2]}, total ratio = {combo[3]}, max gear modulus = {combo[4]:.2f}, gear ratio = {combo[1]/combo[2]:.2f}")
    else:
        print(f"cycloid ratio = {combo[0]}, planet nb teeth = {combo[1]}, sun nb teeth = {combo[2]}, total ratio = {combo[3]}, gear ratio = {combo[1]/combo[2]:.2f}")
