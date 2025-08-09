import json
import warnings as wrn
from Landscapes import *
from Buildings import *

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
            try:
                if other_region == region:
                    continue
                for pos1 in region.positions:
                    for pos2 in other_region.positions:
                        if self._adjacent_positions(pos1, pos2):
                            adj_regions.add(other_region)
                            break
                    if other_region in adj_regions:
                        break
            except: continue
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
            try:
                for tile in region.tiles:
                    if tile.building.type == "Town" and tile.building.level > tile.building.destroyed:
                        town_regions.add(region)
                        break
            except: continue
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