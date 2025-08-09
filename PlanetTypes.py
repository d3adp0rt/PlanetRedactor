from abc import ABC, abstractmethod
import inspect
import sys
import Landscapes as lnd

class PlanetType(ABC):
    @abstractmethod
    def get_noise_params(self):
        pass

    @abstractmethod
    def get_terrain_landscapes(self):
        pass

    @abstractmethod
    def get_forest_chance(self):
        pass

    @abstractmethod
    def get_water_landscape(self, water_body_type, size):
        pass

class GreenPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.15, "octaves": 4, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.4], [lnd.Savannah, 0.2], [lnd.Mountains, 0.15], [lnd.Hills, 0.15]]

    def get_forest_chance(self):
        return 30

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class DryPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.12, "octaves": 3, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.6], [lnd.Scorched, 0.2], [lnd.Mountains, 0.1], [lnd.Mesa, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Oasis()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Salt_Lake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Salt_Lake()
        return lnd.Water()

class ColdPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.18, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Snow, 0.5], [lnd.Ice, 0.3], [lnd.Mountains, 0.15], [lnd.Tundra, 0.05]]

    def get_forest_chance(self):
        return 25

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class DeadPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 2, "persistence": 0.8}

    def get_terrain_landscapes(self):
        return [[lnd.Scorched, 0.7], [lnd.Wasteland, 0.2], [lnd.CraterLand, 0.1]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.AcidStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.AcidOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Acid()
        return lnd.Acid()

class LithoidPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.08, "octaves": 6, "persistence": 0.4}

    def get_terrain_landscapes(self):
        return [[lnd.Mountains, 0.4], [lnd.Plains, 0.3], [lnd.CrystalFormations, 0.2], [lnd.Caves, 0.1]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class IdealPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 3, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.6], [lnd.Gardens, 0.2], [lnd.Hills, 0.2]]

    def get_forest_chance(self):
        return 20

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class EcumenopolisPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.25, "octaves": 2, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.8], [lnd.UrbanCore, 0.2]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Reservoir()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class BurnedPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 4, "persistence": 0.8}

    def get_terrain_landscapes(self):
        return [[lnd.Lava, 0.5], [lnd.Mountains, 0.3], [lnd.VolcanicRock, 0.2]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.LavaStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.LavaLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Lava()
        return lnd.Lava()

class AquaticPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.3, "octaves": 2, "persistence": 0.3}

    def get_terrain_landscapes(self):
        return [[lnd.Islands, 0.3], [lnd.CoralReefs, 0.2], [lnd.Plains, 0.3], [lnd.Beaches, 0.2]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Channel()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.DeepOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ShallowWater()
        return lnd.ShallowWater()

class VolcanicPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.05, "octaves": 7, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Lava, 0.4], [lnd.VolcanicRock, 0.3], [lnd.Mountains, 0.2], [lnd.Geysers, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.HotSpring()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.VolcanicLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.HotSpring()
        return lnd.HotSpring()

class CrystallinePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.07, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.CrystalFormations, 0.5], [lnd.Plains, 0.2], [lnd.Mountains, 0.2], [lnd.CrystalCaves, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.CrystalStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.CrystalPool()
        return lnd.CrystalPool()

class SwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.25, "octaves": 3, "persistence": 0.4}

    def get_terrain_landscapes(self):
        return [[lnd.Swampland, 0.6], [lnd.Plains, 0.2], [lnd.BogLands, 0.2]]

    def get_forest_chance(self):
        return 40

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.SwampRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.SwampWater()
        return lnd.SwampWater()

class ToxicPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.15, "octaves": 4, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.ToxicWaste, 0.4], [lnd.Plains, 0.3], [lnd.PoisonPools, 0.2], [lnd.Wasteland, 0.1]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.ToxicRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.ToxicLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ToxicPool()
        return lnd.ToxicPool()

class ArchipelagoPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.28, "octaves": 3, "persistence": 0.45}

    def get_terrain_landscapes(self):
        return [[lnd.Islands, 0.35], [lnd.Beaches, 0.25], [lnd.CoralReefs, 0.2], [lnd.Plains, 0.2]]

    def get_forest_chance(self):
        return 30

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Channel()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.DeepOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ShallowWater()
        return lnd.ShallowWater()

class HighlandPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.09, "octaves": 6, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.Mountains, 0.5], [lnd.Hills, 0.25], [lnd.Caves, 0.15], [lnd.Plains, 0.1]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class BrackishPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.16, "octaves": 4, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.4], [lnd.Beaches, 0.2], [lnd.Salt_Lake, 0.25], [lnd.Plains, 0.15]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Oasis()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Salt_Lake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Salt_Lake()
        return lnd.Water()

class PermafrostPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.14, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Snow, 0.45], [lnd.Ice, 0.35], [lnd.Tundra, 0.15], [lnd.Plains, 0.05]]

    def get_forest_chance(self):
        return 20

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class AcidicArchipelago(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 3, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.PoisonPools, 0.4], [lnd.Wasteland, 0.3], [lnd.Plains, 0.2], [lnd.Islands, 0.1]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.AcidStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.AcidOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Acid()
        return lnd.Acid()

class CrystalArchipelago(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.12, "octaves": 5, "persistence": 0.45}

    def get_terrain_landscapes(self):
        return [[lnd.CrystalFormations, 0.4], [lnd.CrystalCaves, 0.2], [lnd.Islands, 0.2], [lnd.Beaches, 0.2]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.CrystalStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.CrystalPool()
        return lnd.CrystalPool()

class UrbanSprawlPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.24, "octaves": 2, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.6], [lnd.UrbanCore, 0.3], [lnd.Gardens, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Reservoir()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class BoggyPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 3, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Swampland, 0.6], [lnd.BogLands, 0.25], [lnd.Plains, 0.15]]

    def get_forest_chance(self):
        return 40

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.SwampRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.SwampWater()
        return lnd.SwampWater()

class VolcanicArchipelago(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.07, "octaves": 7, "persistence": 0.65}

    def get_terrain_landscapes(self):
        return [[lnd.Lava, 0.4], [lnd.VolcanicRock, 0.3], [lnd.Geysers, 0.15], [lnd.Beaches, 0.15]]

    def get_forest_chance(self):
        return 2

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.LavaStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.VolcanicLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Lava()
        return lnd.Lava()

class DesertOasisPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.11, "octaves": 4, "persistence": 0.75}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.55], [lnd.Mesa, 0.2], [lnd.Scorched, 0.15], [lnd.Plains, 0.1]]

    def get_forest_chance(self):
        return 2

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Oasis()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Salt_Lake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Salt_Lake()
        return lnd.Water()

def get_subclasses_dict(base_class):
    subclasses = {}
    current_module = sys.modules[__name__]
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
            subclasses[name] = obj
    return subclasses

PlanetTypes = get_subclasses_dict(PlanetType)