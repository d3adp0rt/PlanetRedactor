import json
import warnings as wrn
import sys
import inspect

class Building:
    def __init__(self, type: str, ELC: int, GoRP: int, VP: int, HP: int, GP: int, SP: int, money: int, level: int, destroyed: int = 0):
        self.type = type
        self.ELC = ELC
        self.GoRP = GoRP
        self.VP = VP
        self.HP = HP
        self.GP = GP
        self.SP = SP
        self.money = money
        self.level = level
        self.destroyed = min(destroyed, level)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}

    def to_dict(self):
        data = {
            "type": self.type,
            "ELC": self.ELC,
            "GoRP": self.GoRP,
            "VP": self.VP,
            "HP": self.HP,
            "GP": self.GP,
            "SP": self.SP,
            "money": self.money,
            "level": self.level,
            "destroyed": self.destroyed
        }
        if hasattr(self, "NeedsRC"):
            data["NeedsRC"] = self.NeedsRC
        return data

    def get_base_resources(self, eff_level):
        if eff_level <= 0:
            return {resource: 0 for resource in self.resources_config}
        return {resource: config["base"] + config["inc"] * (eff_level - 1) for resource, config in self.resources_config.items()}

class EmptyBuilding(Building):
    resources_config = {
        "ELC": {"base": 0, "inc": 0},
        "GoRP": {"base": 0, "inc": 0},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level=0):
        super().__init__(type="EmptyBuilding", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=0, destroyed=0)
        self.allowed_landscapes = ["all"]

class Town(Building):
    resources_config = {
        "ELC": {"base": -200, "inc": -120},
        "GoRP": {"base": 0, "inc": 0},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": -120, "inc": -100},
        "SP": {"base": -100, "inc": -80},
        "money": {"base": 0, "inc": 400}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Town", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}

class Mining(Building):
    resources_config = {
        "ELC": {"base": -150, "inc": -75},
        "GoRP": {"base": 200, "inc": 150},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": -40, "inc": -20},
        "SP": {"base": -25, "inc": -25},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Mining", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all", "Mountains"]
        self.landscape_bonuses = {"Mountains": {"GoRP": 80}}

class Fortress(Building):
    resources_config = {
        "ELC": {"base": -200, "inc": -75},
        "GoRP": {"base": 0, "inc": 0},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": -5, "inc": 0},
        "GP": {"base": -50, "inc": -20},
        "SP": {"base": -15, "inc": -25},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Fortress", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}

class Electrostation(Building):
    resources_config = {
        "ELC": {"base": 1000, "inc": 800},
        "GoRP": {"base": -75, "inc": -75},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Electrostation", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {"Desert": {"ELC": 100}}
        self.NeedsRC = True

class CivilIndustry(Building):
    resources_config = {
        "ELC": {"base": -400, "inc": -300},
        "GoRP": {"base": -40, "inc": -40},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 200, "inc": 150},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="CivilIndustry", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}
        self.NeedsRC = True

class Farm(Building):
    resources_config = {
        "ELC": {"base": -100, "inc": -60},
        "GoRP": {"base": -20, "inc": -20},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": -40, "inc": -40},
        "SP": {"base": 275, "inc": 75},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Farm", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}

class Military(Building):
    resources_config = {
        "ELC": {"base": -400, "inc": -400},
        "GoRP": {"base": -75, "inc": -75},
        "VP": {"base": 200, "inc": 120},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Military", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}
        self.NeedsRC = True

class ChemicalIndustry(Building):
    resources_config = {
        "ELC": {"base": -400, "inc": -400},
        "GoRP": {"base": -50, "inc": -50},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 100, "inc": 50},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="ChemicalIndustry", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}
        self.NeedsRC = True

class Science(Building):
    resources_config = {
        "ELC": {"base": -200, "inc": -200},
        "GoRP": {"base": -40, "inc": -20},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": -25, "inc": -25},
        "GP": {"base": -50, "inc": -50},
        "SP": {"base": -25, "inc": -25},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="Science", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}

class ForestBase(Building):
    resources_config = {
        "ELC": {"base": 0, "inc": 0},
        "GoRP": {"base": 0, "inc": 0},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, typeL):
        super().__init__(type=typeL, ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=0, destroyed=0)
        self.allowed_landscapes = ["all"]

class Forest(ForestBase):
    def __init__(self):
        super().__init__("Forest")

class SwampVegetation(ForestBase):
    def __init__(self):
        super().__init__("SwampVegetation")
        
class ArcticForest(ForestBase):
    def __init__(self):
        super().__init__("ArcticForest")

class PowerLines(Building):
    resources_config = {
        "ELC": {"base": 0, "inc": 0},
        "GoRP": {"base": 0, "inc": 0},
        "VP": {"base": 0, "inc": 0},
        "HP": {"base": 0, "inc": 0},
        "GP": {"base": 0, "inc": 0},
        "SP": {"base": 0, "inc": 0},
        "money": {"base": 0, "inc": 0}
    }

    def __init__(self, level: int, destroyed: int = 0):
        super().__init__(type="PowerLines", ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, level=level, destroyed=destroyed)
        self.allowed_landscapes = ["all"]
        self.landscape_bonuses = {}
        self.NeedsRC = False

class Landscape:
    def __init__(self, typeL: str, buildable: bool):
        self.type = typeL
        self.buildable = buildable

    def to_dict(self):
        return {
            "type": self.type,
            "buildable": self.buildable
        }

class Mountains(Landscape):
    def __init__(self):
        super().__init__("Mountains", False)

class Water(Landscape):
    def __init__(self):
        super().__init__("Water", False)

class AcidOcean(Landscape):
    def __init__(self):
        super().__init__("AcidOcean", False)

class AcidStream(Landscape):
    def __init__(self):
        super().__init__("AcidStream", False)

class Canal(Landscape):
    def __init__(self):
        super().__init__("Canal", True)

class Channel(Landscape):
    def __init__(self):
        super().__init__("Channel", True)

class CrystalLake(Landscape):
    def __init__(self):
        super().__init__("CrystalLake", False)

class CrystalPool(Landscape):
    def __init__(self):
        super().__init__("CrystalPool", False)

class CrystalStream(Landscape):
    def __init__(self):
        super().__init__("CrystalStream", False)

class DeepOcean(Landscape):
    def __init__(self):
        super().__init__("DeepOcean", False)

class FrozenRiver(Landscape):
    def __init__(self):
        super().__init__("FrozenRiver", True)

class FrozenSea(Landscape):
    def __init__(self):
        super().__init__("FrozenSea", True)

class HotSpring(Landscape):
    def __init__(self):
        super().__init__("HotSpring", True)

class LavaLake(Landscape):
    def __init__(self):
        super().__init__("LavaLake", False)

class LavaStream(Landscape):
    def __init__(self):
        super().__init__("LavaStream", False)

class Oasis(Landscape):
    def __init__(self):
        super().__init__("Oasis", True)

class Ocean(Landscape):
    def __init__(self):
        super().__init__("Ocean", False)

class Reservoir(Landscape):
    def __init__(self):
        super().__init__("Reservoir", False)

class River(Landscape):
    def __init__(self):
        super().__init__("River", False)

class Salt_Lake(Landscape):
    def __init__(self):
        super().__init__("Salt_Lake", False)

class ShallowWater(Landscape):
    def __init__(self):
        super().__init__("ShallowWater", False)

class SwampLake(Landscape):
    def __init__(self):
        super().__init__("SwampLake", False)

class SwampRiver(Landscape):
    def __init__(self):
        super().__init__("SwampRiver", False)

class SwampWater(Landscape):
    def __init__(self):
        super().__init__("SwampWater", False)

class ToxicLake(Landscape):
    def __init__(self):
        super().__init__("ToxicLake", False)

class ToxicPool(Landscape):
    def __init__(self):
        super().__init__("ToxicPool", False)

class ToxicRiver(Landscape):
    def __init__(self):
        super().__init__("ToxicRiver", False)

class VolcanicLake(Landscape):
    def __init__(self):
        super().__init__("VolcanicLake", False)

class Acid(Landscape):
    def __init__(self):
        super().__init__("Acid", False)

class Lava(Landscape):
    def __init__(self):
        super().__init__("Lava", False)

class Ice(Landscape):
    def __init__(self):
        super().__init__("Ice", True)

class Hills(Landscape):
    def __init__(self):
        super().__init__("Hills", True)

class Mesa(Landscape):
    def __init__(self):
        super().__init__("Mesa", True)

class Tundra(Landscape):
    def __init__(self):
        super().__init__("Tundra", True)

class Wasteland(Landscape):
    def __init__(self):
        super().__init__("Wasteland", True)

class CraterLand(Landscape):
    def __init__(self):
        super().__init__("CraterLand", True)

class CrystalFormations(Landscape):
    def __init__(self):
        super().__init__("CrystalFormations", True)

class Caves(Landscape):
    def __init__(self):
        super().__init__("Caves", False)

class Gardens(Landscape):
    def __init__(self):
        super().__init__("Gardens", True)

class UrbanCore(Landscape):
    def __init__(self):
        super().__init__("UrbanCore", True)

class VolcanicRock(Landscape):
    def __init__(self):
        super().__init__("VolcanicRock", False)

class Islands(Landscape):
    def __init__(self):
        super().__init__("Islands", True)

class CoralReefs(Landscape):
    def __init__(self):
        super().__init__("CoralReefs", False)

class Beaches(Landscape):
    def __init__(self):
        super().__init__("Beaches", True)

class Geysers(Landscape):
    def __init__(self):
        super().__init__("Geysers", True)

class CrystalCaves(Landscape):
    def __init__(self):
        super().__init__("CrystalCaves", False)

class Swampland(Landscape):
    def __init__(self):
        super().__init__("Swampland", False)

class BogLands(Landscape):
    def __init__(self):
        super().__init__("BogLands", True)

class ToxicWaste(Landscape):
    def __init__(self):
        super().__init__("ToxicWaste", False)

class PoisonPools(Landscape):
    def __init__(self):
        super().__init__("PoisonPools", False)

class Snow(Landscape):
    def __init__(self):
        super().__init__("Snow", True)

class Plains(Landscape):
    def __init__(self):
        super().__init__("Plains", True)

class Desert(Landscape):
    def __init__(self):
        super().__init__("Desert", True)

class Savannah(Landscape):
    def __init__(self):
        super().__init__("Savannah", True)

class Scorched(Landscape):
    def __init__(self):
        super().__init__("Scorched", True)

class Tile:
    def __init__(self, landscape: Landscape, building: Building):
        self.landscape = landscape
        self.building = building
        
        if building.type != "EmptyBuilding":
            if "all" in building.allowed_landscapes:
                pass
            else:
                if landscape.type not in building.allowed_landscapes:
                    wrn.warn(f"[WARNING]: Cannot build {building.type} on {landscape.type} because it is not in allowed landscapes.")
                else:
                    if not landscape.buildable:
                        print(f"Building {building.type} can be placed on {landscape.type} despite it being globally forbidden.")

    def to_dict(self):
        return {
            "landscape": self.landscape.to_dict(),
            "building": self.building.to_dict()
        }

    def get_effective_resources(self):
        building = self.building
        eff_level = building.level - building.destroyed
        resources = building.get_base_resources(eff_level)
        
        if eff_level > 0 and hasattr(building, "landscape_bonuses") and self.landscape.type in building.landscape_bonuses:
            bonuses = building.landscape_bonuses[self.landscape.type]
            for resource, bonus in bonuses.items():
                if resource in resources:
                    resources[resource] += bonus * eff_level
        return resources

class Region:
    def __init__(self, tiles: list, positions: list, typeL: str):
        self.typeL = typeL
        self.tiles = tiles
        self.positions = positions
        if len(tiles) != 7:
            raise ValueError("Region must have exactly 7 tiles")
        
        has_town = any(tile.building.type == "Town" for tile in tiles)
        has_mining = any(tile.building.type == "Mining" for tile in tiles)
        if has_town and has_mining:
            wrn.warn("[WARNING]: Region contains both Town and Mining buildings")

    def to_dict(self):
        return {
            "typeL": self.typeL,
            "tiles": [tile.to_dict() for tile in self.tiles],
            "positions": self.positions
        }

class CenterReg(Region):
    def __init__(self, tiles: list):
        super().__init__(tiles, [[0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1]], "CenterReg")

class UpperReg(Region):
    def __init__(self, tiles: list):
        super().__init__(tiles, [[-1, -2], [0, -2], [-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0]], "UpperReg")

class LowerReg(Region):
    def __init__(self, tiles: list):
        super().__init__(tiles, [[0, 0], [1, 0], [-1, 1], [0, 1], [1, 1], [-1, 2], [0, 2]], "LowerReg")

current_module = sys.modules[__name__]

def get_subclasses_dict(base_class, exclude=None):
    exclude = exclude or set()
    subclasses = {}
    for name, obj in inspect.getmembers(current_module):
        if (
            inspect.isclass(obj) and 
            issubclass(obj, base_class) and 
            obj is not base_class and 
            obj not in exclude
        ):
            subclasses[name] = obj
    return subclasses

BuildingTypes = get_subclasses_dict(Building, exclude={ForestBase})
LandscapeTypes = get_subclasses_dict(Landscape)
ForestTypes = get_subclasses_dict(ForestBase)

class Planet:
    def __init__(self, name: str, Regions: list):
        self.name = name
        self.Regions = Regions

    def _adjacent_positions(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        dz = abs((x2 + y2) - (x1 + y1))
        return max(dx, dy, dz) == 1

    def _find_electrostation(self):
        stations = []
        for region in self.Regions:
            try:
                for pos, tile in zip(region.positions, region.tiles):
                    if tile.building.type == "Electrostation" and tile.building.level > tile.building.destroyed:
                        stations.append((region, pos))
            except: continue
        return stations

    def _find_towns(self):
        towns = []
        for region in self.Regions:
            try:
                for pos, tile in zip(region.positions, region.tiles):
                    if tile.building.type == "Town" and tile.building.level > tile.building.destroyed:
                        towns.append((region, pos))
            except: continue
        return towns

    def _find_farms(self):
        farms = []
        for region in self.Regions:
            try:
                for pos, tile in zip(region.positions, region.tiles):
                    if tile.building.type == "Farm" and tile.building.level > tile.building.destroyed:
                        farms.append((region, pos))
            except: continue
        return farms

    def get_adjacent_regions(self, region):
        adj_regions = set()
        for other_region in self.Regions:
            if other_region == region:
                continue
            for pos1 in region.positions:
                for pos2 in other_region.positions:
                    if self._adjacent_positions(pos1, pos2):
                        adj_regions.add(other_region)
                        break
                if other_region in adj_regions:
                    break
        return adj_regions

    def calculate(self):
        total = {
            "ELC": 0,
            "GoRP": 0,
            "VP": 0,
            "HP": 0,
            "GP": 0,
            "SP": 0,
            "money": 0
        }

        warnings = []
        stations = self._find_electrostation()
        towns = self._find_towns()
        farms = self._find_farms()

        # Determine regions with RC availability
        town_regions = set()
        for region in self.Regions:
            for tile in region.tiles:
                if tile.building.type == "Town" and tile.building.level > tile.building.destroyed:
                    town_regions.add(region)
                    break
        rc_available_regions = set(town_regions)
        for region in town_regions:
            rc_available_regions.update(self.get_adjacent_regions(region))

        for region in self.Regions:
            try:
                for pos, tile in zip(region.positions, region.tiles):
                    b = tile.building
                    eff_level = b.level - b.destroyed
                    if eff_level <= 0:
                        continue
                    resources = tile.get_effective_resources()
                    for resource, value in resources.items():
                        total[resource] += value

                    if resources["ELC"] < 0:
                        has_power = False
                        for reg_station, pos_station in stations:
                            station_tile = None
                            for t, p in zip(reg_station.tiles, reg_station.positions):
                                if p == pos_station:
                                    station_tile = t
                                    break
                            if station_tile and station_tile.building.level <= station_tile.building.destroyed:
                                continue
                            if reg_station == region and self._adjacent_positions(pos, pos_station):
                                has_power = True
                                break
                            if reg_station != region:
                                for p in reg_station.positions:
                                    idx = reg_station.positions.index(p)
                                    neighbor_tile = reg_station.tiles[idx]
                                    if neighbor_tile.building.level <= neighbor_tile.building.destroyed:
                                        continue
                                    if self._adjacent_positions(pos, p):
                                        has_power = True
                                        break
                            if has_power:
                                break
                        if not has_power:
                            warnings.append(f"[WARNING]: No electricity for {b.type} at {pos} in region {self.Regions.index(region)}")

                    if hasattr(b, "NeedsRC") and b.NeedsRC:
                        if region not in rc_available_regions:
                            warnings.append(f"[WARNING]: No RC for {b.type} at {pos} in region {self.Regions.index(region)}")
            except: continue

        for reg_farm, pos_farm in farms:
            for reg_town, pos_town in towns:
                if reg_farm == reg_town:
                    warnings.append(f"[WARNING]: Farm at {pos_farm} and Town at {pos_town} are in the same region {self.Regions.index(reg_farm)}")

        towns_pos = []
        minings_pos = []
        for region in self.Regions:
            try:
                for pos, tile in zip(region.positions, region.tiles):
                    if tile.building.type == "Town" and tile.building.level > tile.building.destroyed:
                        towns_pos.append((region, pos))
                    if tile.building.type == "Mining" and tile.building.level > tile.building.destroyed:
                        minings_pos.append((region, pos))
            except: continue
        for reg_town, pos_town in towns_pos:
            for reg_mining, pos_mining in minings_pos:
                if self.Regions.index(reg_town) == self.Regions.index(reg_mining) and self._adjacent_positions(pos_town, pos_mining):
                    wrn.warn(f"[ERROR]: Town at {pos_town} in region {self.Regions.index(reg_town)} is adjacent to Mining at {pos_mining} in region {self.Regions.index(reg_mining)}")

        negatives = {k: v for k, v in total.items() if v < 0 and k != "money"}
        if negatives:
            msg = "[WARNING]: Negative resources detected:\n"
            for k, v in negatives.items():
                msg += f"  - {k}: {v}\n"
            warnings.append(msg)

        if warnings:
            wrn.warn("\n".join(warnings))
        
        return total

    def generate(self, WaterType: int, TerrainType: str, UseForest: bool):
        from PlanetGenerator import AdvancedPlanetGenerator
        generator = AdvancedPlanetGenerator()
        new_planet = generator.generate(self.name, len(self.Regions), WaterType, TerrainType, UseForest, self.Regions)
        self.Regions = new_planet.Regions
        return self

    def dump(self):
        file = f"{self.name}.json"
        data = {
            "name": self.name,
            "regions": [],
            "unique_elements": {}
        }
        
        unique_map = {}
        unique_id = 0
        
        def get_unique_id(landscape, building):
            nonlocal unique_id
            key = (landscape.type, building.type, building.level, building.destroyed)
            if key not in unique_map:
                unique_map[key] = str(unique_id)
                data["unique_elements"][str(unique_id)] = {
                    "landscape": {"type": landscape.type},
                    "building": {
                        "type": building.type,
                        "level": building.level,
                        "destroyed": building.destroyed
                    }
                }
                unique_id += 1
            return unique_map[key]
        
        for region in self.Regions:
            try:
                region_data = {
                    "typeL": region.typeL,
                    "tiles": []
                }
                for i, tile in enumerate(region.tiles):
                    uid = get_unique_id(tile.landscape, tile.building)
                    region_data["tiles"].append({
                        "tile_index": i,
                        "element_id": uid
                    })
                data["regions"].append(region_data)
            except:
                region_data = {
                    "typeL": "Emp",
                    "tiles": []
                }
                data["regions"].append(region_data)
        
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self, name=None):
        if name is None:
            file = f"{self.name}.json"
        else:
            file = f"{name}.json"

        with open(file, 'r') as f:
            data = json.load(f)
        
        self.name = data["name"]
        self.Regions = []
        
        unique_elements = {}
        for uid, elem in data["unique_elements"].items():
            landscape_type = elem["landscape"]["type"]
            if landscape_type not in LandscapeTypes:
                raise ValueError(f"Unknown landscape type: {landscape_type}")
            landscape = LandscapeTypes[landscape_type]()
            
            building_data = elem["building"]
            building_type = building_data["type"]
            level = building_data["level"]
            destroyed = building_data["destroyed"]
            
            if building_type not in BuildingTypes:
                raise ValueError(f"Unknown building type: {building_type}")
            
            if building_type in ["EmptyBuilding", "Forest", "ArcticForest", "SwampVegetation"]:
                building = BuildingTypes[building_type]()
            else:
                building = BuildingTypes[building_type](level, destroyed)
            
            unique_elements[uid] = (landscape, building)
        
        for region_data in data["regions"]:
            tiles = []
            sorted_tiles = sorted(region_data["tiles"], key=lambda x: x["tile_index"])
            for tile_data in sorted_tiles:
                uid = tile_data["element_id"]
                landscape, building = unique_elements[uid]
                tile = Tile(landscape, building)
                tiles.append(tile)
            
            region_type = region_data["typeL"]
            if region_type == "CenterReg":
                region = CenterReg(tiles)
            elif region_type == "UpperReg":
                region = UpperReg(tiles)
            elif region_type == "LowerReg":
                region = LowerReg(tiles)
            elif region_type == "Emp":
                region = []
            else:
                raise ValueError(f"Unknown region type: {region_type}")
            
            self.Regions.append(region)