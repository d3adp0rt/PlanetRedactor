from abc import ABC, abstractmethod
import inspect
import sys
import Landscapes as lnd
import json
import os

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

class CrystallinePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.07, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.CrystalFormations, 0.5], [lnd.Mountains, 0.2], [lnd.CrystalCaves, 0.1]]

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

class TropicalParadisePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.22, "octaves": 4, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.Plains, 0.4], [lnd.Gardens, 0.3], [lnd.Beaches, 0.2], [lnd.Hills, 0.1]]

    def get_forest_chance(self):
        return 45

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class MountainousPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.08, "octaves": 6, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.Mountains, 0.6], [lnd.Hills, 0.2], [lnd.Caves, 0.1], [lnd.Plains, 0.1]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.DeepOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Water()
        return lnd.Water()

class FrozenCrystalPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Ice, 0.4], [lnd.CrystalFormations, 0.3], [lnd.Snow, 0.2], [lnd.Mountains, 0.1]]

    def get_forest_chance(self):
        return 8

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.CrystalStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.CrystalPool()
        return lnd.CrystalPool()

class DesertCraterPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.13, "octaves": 4, "persistence": 0.65}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.4], [lnd.CraterLand, 0.3], [lnd.Scorched, 0.2], [lnd.Mesa, 0.1]]

    def get_forest_chance(self):
        return 3

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Oasis()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Salt_Lake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Salt_Lake()
        return lnd.Salt_Lake()

class CoastalParadisePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.25, "octaves": 3, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Beaches, 0.4], [lnd.Plains, 0.3], [lnd.Gardens, 0.2], [lnd.CoralReefs, 0.1]]

    def get_forest_chance(self):
        return 25

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ShallowWater()
        return lnd.ShallowWater()

class IndustrialPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 2, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.UrbanCore, 0.5], [lnd.Plains, 0.3], [lnd.Wasteland, 0.2]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Reservoir()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ToxicPool()
        return lnd.ToxicPool()

class CrystalDesertPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.11, "octaves": 5, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.4], [lnd.CrystalFormations, 0.3], [lnd.Mesa, 0.2], [lnd.Scorched, 0.1]]

    def get_forest_chance(self):
        return 4

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.CrystalStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.CrystalPool()
        return lnd.CrystalPool()

class ToxicSwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.18, "octaves": 4, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.Swampland, 0.4], [lnd.ToxicWaste, 0.3], [lnd.BogLands, 0.2], [lnd.PoisonPools, 0.1]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.ToxicRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ToxicPool()
        return lnd.ToxicPool()

class FrozenWastePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.15, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Ice, 0.4], [lnd.Wasteland, 0.3], [lnd.Snow, 0.2], [lnd.CraterLand, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Ice()
        return lnd.Ice()

class VolcanicIslandsPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.16, "octaves": 6, "persistence": 0.65}

    def get_terrain_landscapes(self):
        return [[lnd.Islands, 0.4], [lnd.VolcanicRock, 0.3], [lnd.Beaches, 0.2], [lnd.Geysers, 0.1]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.LavaStream()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.VolcanicLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.HotSpring()
        return lnd.HotSpring()

class CrystalSwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.14, "octaves": 4, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Swampland, 0.4], [lnd.CrystalFormations, 0.3], [lnd.BogLands, 0.2], [lnd.CrystalCaves, 0.1]]

    def get_forest_chance(self):
        return 20

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.SwampRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.SwampWater()
        return lnd.SwampWater()

class UrbanCrystalPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.22, "octaves": 3, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.UrbanCore, 0.4], [lnd.CrystalFormations, 0.3], [lnd.Plains, 0.2], [lnd.CrystalCaves, 0.1]]

    def get_forest_chance(self):
        return 8

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Reservoir()
        return lnd.Reservoir()

class ToxicDesertPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.12, "octaves": 4, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.4], [lnd.ToxicWaste, 0.3], [lnd.Scorched, 0.2], [lnd.PoisonPools, 0.1]]

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

class FrozenSwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.17, "octaves": 4, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[lnd.Swampland, 0.4], [lnd.Ice, 0.3], [lnd.Snow, 0.2], [lnd.BogLands, 0.1]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.FrozenSea()
        return lnd.FrozenSea()

class UrbanOasisPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 3, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.UrbanCore, 0.4], [lnd.Plains, 0.3], [lnd.Gardens, 0.2], [lnd.Desert, 0.1]]

    def get_forest_chance(self):
        return 12

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.Reservoir()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Oasis()
        return lnd.Oasis()

class CoralMountainPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.13, "octaves": 5, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.Mountains, 0.4], [lnd.CoralReefs, 0.3], [lnd.Hills, 0.2], [lnd.Beaches, 0.1]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.River()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.DeepOcean()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.ShallowWater()
        return lnd.ShallowWater()

class MountainousSwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.15, "octaves": 5, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[lnd.Mountains, 0.4], [lnd.Swampland, 0.3], [lnd.BogLands, 0.2], [lnd.Hills, 0.1]]

    def get_forest_chance(self):
        return 25

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.SwampRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.SwampWater()
        return lnd.SwampWater()

class VolcanicDesertPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 6, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[lnd.Desert, 0.4], [lnd.VolcanicRock, 0.3], [lnd.Scorched, 0.2], [lnd.Geysers, 0.1]]

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

class ArcticCraterPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.14, "octaves": 5, "persistence": 0.55}

    def get_terrain_landscapes(self):
        return [[lnd.Snow, 0.4], [lnd.CraterLand, 0.3], [lnd.Ice, 0.2], [lnd.Tundra, 0.1]]

    def get_forest_chance(self):
        return 8

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return lnd.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return lnd.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return lnd.Ice()
        return lnd.Ice()

def get_subclasses_dict(base_class):
    subclasses = {}
    current_module = sys.modules[__name__]
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
            subclasses[name] = obj
    return subclasses

PlanetTypes = get_subclasses_dict(PlanetType)

def load_planet_type_mods():
    mods_path = "mods/PlanetTypes"
    
    if not os.path.exists(mods_path):
        return
    
    for filename in os.listdir(mods_path):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(mods_path, filename), 'r', encoding='utf-8') as f:
                    mod_data = json.load(f)
                
                mod_info = mod_data.get('mod_info', {})
                print("========== MOD INFO ==========")
                print(f"Loading mod: {mod_info.get('name', 'Unknown')} v{mod_info.get('version', '1.0.0')} by {mod_info.get('author', 'Unknown')}")
                print(f"Description: {mod_info.get('description', 'No description')}")
                print("==============================")
                
                for planet_type_data in mod_data.get('planet_types', []):
                    create_dynamic_planet_type(planet_type_data)
                    
            except Exception as e:
                print(f"Ошибка загрузки мода {filename}: {e}")

def create_dynamic_planet_type(planet_data):
    class_name = planet_data['name']
    
    def __init__(self):
        pass
    
    def get_noise_params(self):
        return planet_data.get('noise_params', {"scale": 0.15, "octaves": 4, "persistence": 0.6})
    
    def get_terrain_landscapes(self):
        terrain_data = planet_data.get('terrain_landscapes', [])
        result = []
        for terrain in terrain_data:
            landscape_class = getattr(lnd, terrain['landscape'])
            result.append([landscape_class, terrain['probability']])
        return result
    
    def get_forest_chance(self):
        return planet_data.get('forest_chance', 0)
    
    def get_water_landscape(self, water_body_type, size):
        water_mapping = planet_data.get('water_landscapes', {})
        
        if water_body_type == 'river':
            landscape_name = water_mapping.get('river', 'Water')
        elif water_body_type == 'ocean' and size >= 20:
            landscape_name = water_mapping.get('ocean', 'Ocean')
        elif water_body_type == 'sea' and size >= 8:
            landscape_name = water_mapping.get('sea', 'Water')
        else:
            landscape_name = water_mapping.get('default', 'Water')
            
        return getattr(lnd, landscape_name)()
    
    dynamic_class = type(class_name, (PlanetType,), {
        '__init__': __init__,
        'get_noise_params': get_noise_params,
        'get_terrain_landscapes': get_terrain_landscapes,
        'get_forest_chance': get_forest_chance,
        'get_water_landscape': get_water_landscape
    })
    
    globals()[class_name] = dynamic_class
    PlanetTypes[class_name] = dynamic_class

load_planet_type_mods()