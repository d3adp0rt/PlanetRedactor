import random
import Planet as pt
from collections import deque
from abc import ABC, abstractmethod

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
        return [[pt.Plains, 0.4], [pt.Savannah, 0.3], [pt.Mountains, 0.15], [pt.Hills, 0.15]]

    def get_forest_chance(self):
        return 30

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.River()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Water()
        return pt.Water()

class DryPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.12, "octaves": 3, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[pt.Desert, 0.6], [pt.Scorched, 0.2], [pt.Mountains, 0.1], [pt.Mesa, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.Oasis()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.Salt_Lake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Salt_Lake()
        return pt.Water()

class ColdPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.18, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[pt.Snow, 0.5], [pt.Ice, 0.3], [pt.Mountains, 0.15], [pt.Tundra, 0.05]]

    def get_forest_chance(self):
        return 25

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.FrozenRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.FrozenSea()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Water()
        return pt.Water()

class DeadPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 2, "persistence": 0.8}

    def get_terrain_landscapes(self):
        return [[pt.Scorched, 0.7], [pt.Wasteland, 0.2], [pt.CraterLand, 0.1]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.AcidStream()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.AcidOcean()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Acid()
        return pt.Acid()

class LithoidPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.08, "octaves": 6, "persistence": 0.4}

    def get_terrain_landscapes(self):
        return [[pt.Mountains, 0.4], [pt.Plains, 0.3], [pt.CrystalFormations, 0.2], [pt.Caves, 0.1]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.River()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Water()
        return pt.Water()

class IdealPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.2, "octaves": 3, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[pt.Plains, 0.6], [pt.Gardens, 0.2], [pt.Hills, 0.2]]

    def get_forest_chance(self):
        return 20

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.River()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.Ocean()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Water()
        return pt.Water()

class EcumenopolisPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.25, "octaves": 2, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[pt.Plains, 0.8], [pt.UrbanCore, 0.2]]

    def get_forest_chance(self):
        return 15

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.Canal()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.Reservoir()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Water()
        return pt.Water()

class BurnedPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.1, "octaves": 4, "persistence": 0.8}

    def get_terrain_landscapes(self):
        return [[pt.Lava, 0.5], [pt.Mountains, 0.3], [pt.VolcanicRock, 0.2]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.LavaStream()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.LavaLake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.Lava()
        return pt.Lava()

class AquaticPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.3, "octaves": 2, "persistence": 0.3}

    def get_terrain_landscapes(self):
        return [[pt.Islands, 0.3], [pt.CoralReefs, 0.2], [pt.Plains, 0.3], [pt.Beaches, 0.2]]

    def get_forest_chance(self):
        return 10

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.Channel()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.DeepOcean()
        elif water_body_type == 'sea' and size >= 8:
            return pt.ShallowWater()
        return pt.ShallowWater()

class VolcanicPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.05, "octaves": 7, "persistence": 0.6}

    def get_terrain_landscapes(self):
        return [[pt.Lava, 0.4], [pt.VolcanicRock, 0.3], [pt.Mountains, 0.2], [pt.Geysers, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.HotSpring()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.VolcanicLake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.HotSpring()
        return pt.HotSpring()

class CrystallinePlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.07, "octaves": 5, "persistence": 0.5}

    def get_terrain_landscapes(self):
        return [[pt.CrystalFormations, 0.5], [pt.Plains, 0.2], [pt.Mountains, 0.2], [pt.CrystalCaves, 0.1]]

    def get_forest_chance(self):
        return 5

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.CrystalStream()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.CrystalLake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.CrystalPool()
        return pt.CrystalPool()

class SwampPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.25, "octaves": 3, "persistence": 0.4}

    def get_terrain_landscapes(self):
        return [[pt.Swampland, 0.6], [pt.Plains, 0.2], [pt.BogLands, 0.2]]

    def get_forest_chance(self):
        return 40

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.SwampRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.SwampLake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.SwampWater()
        return pt.SwampWater()

class ToxicPlanet(PlanetType):
    def get_noise_params(self):
        return {"scale": 0.15, "octaves": 4, "persistence": 0.7}

    def get_terrain_landscapes(self):
        return [[pt.ToxicWaste, 0.4], [pt.Plains, 0.3], [pt.PoisonPools, 0.2], [pt.Wasteland, 0.1]]

    def get_forest_chance(self):
        return 0

    def get_water_landscape(self, water_body_type, size):
        if water_body_type == 'river':
            return pt.ToxicRiver()
        elif water_body_type == 'ocean' and size >= 20:
            return pt.ToxicLake()
        elif water_body_type == 'sea' and size >= 8:
            return pt.ToxicPool()
        return pt.ToxicPool()

class AdvancedPlanetGenerator:
    def __init__(self):
        self.noise_cache = {}
        self.planet_types = {
            cls.__name__.replace("Planet", ""): cls()
            for cls in PlanetType.__subclasses__()
        }
    def perlin_noise(self, x, y, scale=0.1, octaves=4, persistence=0.5):
        key = (x, y, scale, octaves, persistence)
        if key in self.noise_cache:
            return self.noise_cache[key]
        
        value = 0
        amplitude = 1
        frequency = scale
        max_value = 0
        
        for _ in range(octaves):
            nx = x * frequency
            ny = y * frequency
            ix = int(nx)
            iy = int(ny)
            fx = nx - ix
            fy = ny - iy
            
            a = self._hash(ix, iy)
            b = self._hash(ix + 1, iy)
            c = self._hash(ix, iy + 1)
            d = self._hash(ix + 1, iy + 1)
            
            i1 = self._lerp(a, b, fx)
            i2 = self._lerp(c, d, fx)
            noise_value = self._lerp(i1, i2, fy)
            
            value += noise_value * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= 2
            
        result = value / max(1e-10, max_value)
        self.noise_cache[key] = result
        return result
    
    def _hash(self, x, y):
        return random.uniform(-1.0, 1.0)
    
    def _lerp(self, a, b, t):
        return a + t * (b - a)

    def weighted_choice(self, landscape_list):
        if not landscape_list:
            return pt.Plains()
        weighted = [(item[0] if isinstance(item, (list, tuple)) else item, 
                    item[1] if isinstance(item, (list, tuple)) else 1.0) for item in landscape_list]
        total = sum(w for _, w in weighted)
        if total <= 0:
            return weighted[0][0]()
        r = random.uniform(0, total)
        upto = 0
        for landscape, weight in weighted:
            if upto + weight >= r:
                return landscape()
            upto += weight
        return weighted[-1][0]()

    def get_water_parameters(self, water_type):
        params = {
            1: {"water_level": -0.9, "ocean_chance": 0.0, "sea_chance": 0.0, "lake_chance": 0.0, "river_chance": 0.05, "max_water_body_size": 0},
            2: {"water_level": -0.6, "ocean_chance": 0.0, "sea_chance": 0.15, "lake_chance": 0.1, "river_chance": 0.2, "max_water_body_size": 8},
            3: {"water_level": -0.3, "ocean_chance": 0.3, "sea_chance": 0.25, "lake_chance": 0.15, "river_chance": 0.3, "max_water_body_size": 15},
            4: {"water_level": 0.0, "ocean_chance": 0.6, "sea_chance": 0.3, "lake_chance": 0.1, "river_chance": 0.25, "max_water_body_size": 25},
            5: {"water_level": 0.2, "ocean_chance": 0.8, "sea_chance": 0.2, "lake_chance": 0.05, "river_chance": 0.15, "max_water_body_size": 35},
            6: {"water_level": 0.4, "ocean_chance": 0.9, "sea_chance": 0.1, "lake_chance": 0.02, "river_chance": 0.1, "max_water_body_size": 45},
            7: {"water_level": 0.6, "ocean_chance": 0.95, "sea_chance": 0.05, "lake_chance": 0.0, "river_chance": 0.05, "max_water_body_size": 60}
        }
        return params.get(water_type, params[3])

    def generate_height_map(self, positions, planet_type):
        height_map = {}
        params = planet_type.get_noise_params()
        for pos in positions:
            height = self.perlin_noise(pos[0], pos[1], **params)
            height_map[tuple(pos)] = height
        return height_map

    def generate_adaptive_water_bodies(self, height_map, water_params, planet_type):
        water_tiles = set()
        water_level = water_params["water_level"]
        max_size = water_params["max_water_body_size"]
        
        low_areas = [(pos, height) for pos, height in height_map.items() if height < water_level]
        low_areas.sort(key=lambda x: x[1])
        
        processed = set()
        water_bodies = []
        
        for pos, height in low_areas:
            if pos in processed:
                continue
            depth_factor = min(1.0, (water_level - height) * 1.5)
            if random.random() < depth_factor:
                water_body = self._flood_fill_water_limited(pos, height_map, water_level, processed, max_size)
                if water_body:
                    water_bodies.append(water_body)
                    water_tiles.update(water_body)
        
        classified_bodies = self._classify_water_bodies(water_bodies, water_params)
        return water_tiles, classified_bodies

    def _flood_fill_water_limited(self, start_pos, height_map, water_level, processed, max_size):
        water_body = set()
        queue = deque([start_pos])
        processed.add(start_pos)
        
        while queue and len(water_body) < max_size:
            pos = queue.popleft()
            if pos not in height_map:
                continue
            height = height_map[pos]
            if height >= water_level:
                continue
            water_body.add(pos)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (pos[0] + dx, pos[1] + dy)
                    if neighbor not in processed and neighbor in height_map:
                        neighbor_height = height_map[neighbor]
                        spread_threshold = 0.05 + (len(water_body) / max(1, max_size)) * 0.1
                        if neighbor_height <= height + spread_threshold:
                            queue.append(neighbor)
                            processed.add(neighbor)
        return water_body if len(water_body) >= 2 else set()

    def _classify_water_bodies(self, water_bodies, water_params):
        classified = {'oceans': [], 'seas': [], 'lakes': [], 'ponds': []}
        for body in water_bodies:
            size = len(body)
            if size >= 20:
                classified['oceans'].append(body)
            elif size >= 8:
                classified['seas'].append(body)
            elif size >= 3:
                classified['lakes'].append(body)
            else:
                classified['ponds'].append(body)
        return classified

    def generate_smart_rivers(self, height_map, water_tiles, water_params, planet_type):
        rivers = set()
        river_chance = water_params["river_chance"]
        if river_chance == 0:
            return rivers
        
        high_points = [(pos, height) for pos, height in height_map.items() if height > 0.2 and pos not in water_tiles]
        max_rivers = max(1, int(len(high_points) * river_chance))
        selected_sources = random.sample(high_points, min(max_rivers, len(high_points)))
        
        for pos, _ in selected_sources:
            if random.random() < 0.7:
                river_path = self._trace_smart_river(pos, height_map, water_tiles)
                if len(river_path) >= 3:
                    rivers.update(river_path)
        return rivers

    def _trace_smart_river(self, start_pos, height_map, water_tiles):
        river_path = set()
        current_pos = start_pos
        max_length = 20
        min_descent = 0.02
        
        for _ in range(max_length):
            if current_pos in water_tiles:
                river_path.add(current_pos)
                break
            river_path.add(current_pos)
            current_height = height_map.get(current_pos, 0)
            neighbors = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (current_pos[0] + dx, current_pos[1] + dy)
                    if neighbor in height_map and neighbor not in river_path:
                        neighbors.append((neighbor, height_map[neighbor]))
            if not neighbors:
                break
            neighbors.sort(key=lambda x: x[1])
            next_candidates = [n for n in neighbors if n[1] < current_height - min_descent/2]
            if not next_candidates:
                next_candidates = [n for n in neighbors if n[1] < current_height]
            if not next_candidates:
                break
            next_pos = next_candidates[1][0] if len(next_candidates) > 1 and random.random() < 0.3 else next_candidates[0][0]
            current_pos = next_pos
        return river_path

    def get_mountain_ranges(self, height_map, planet_type):
        mountain_ranges = set()
        high_areas = [(pos, height) for pos, height in height_map.items() if height > 0.5]
        processed = set()
        for pos, _ in high_areas:
            if pos in processed:
                continue
            mountain_range = self._find_connected_high_area(pos, height_map, 0.4, processed)
            if len(mountain_range) >= 3:
                mountain_ranges.update(mountain_range)
        return mountain_ranges

    def _find_connected_high_area(self, start_pos, height_map, min_height, processed):
        connected_area = set()
        queue = deque([start_pos])
        processed.add(start_pos)
        while queue:
            pos = queue.popleft()
            if height_map.get(pos, 0) < min_height:
                continue
            connected_area.add(pos)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor = (pos[0] + dx, pos[1] + dy)
                    if neighbor not in processed and neighbor in height_map:
                        if height_map[neighbor] >= min_height:
                            queue.append(neighbor)
                            processed.add(neighbor)
        return connected_area

    def apply_climate_effects(self, tile, pos, height_map, planet_type):
        height = height_map.get(tuple(pos), 0)
        if height > 0.7:
            if isinstance(planet_type, GreenPlanet) and random.random() < 0.3:
                tile.landscape = pt.Snow()
            elif isinstance(planet_type, DryPlanet) and random.random() < 0.2:
                tile.landscape = pt.Mountains()
        elif height < -0.3:
            if isinstance(planet_type, VolcanicPlanet) and random.random() < 0.4:
                tile.landscape = pt.Lava()
        return tile

    def generate(self, name, num_regions, water_type, terrain_type, use_forest, regions_st):
        if not isinstance(water_type, int) or water_type < 1 or water_type > 7:
            water_type = 3
        if terrain_type not in self.planet_types:
            terrain_type = "Green"
        if not isinstance(num_regions, int) or num_regions < 0:
            num_regions = 0
        if not isinstance(regions_st, list) or len(regions_st) < num_regions:
            regions_st = [[] for _ in range(num_regions)]
            
        planet_type = self.planet_types[terrain_type]
        water_params = self.get_water_parameters(water_type)
        
        all_positions = []
        for i in range(num_regions):
            if not regions_st[i]:
                continue
            reg_type_name = ["UpperReg", "CenterReg", "LowerReg"][i % 3]
            base_positions = {
                "CenterReg": [[0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1]],
                "UpperReg": [[-1, -2], [0, -2], [-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0]],
                "LowerReg": [[0, 0], [1, 0], [-1, 1], [0, 1], [1, 1], [-1, 2], [0, 2]]
            }[reg_type_name]
            offset = [3 * (i // 3), 0]
            positions = [[p[0] + offset[0], p[1] + offset[1]] for p in base_positions]
            all_positions.extend(positions)
        
        height_map = self.generate_height_map(all_positions, planet_type)
        water_tiles, classified_bodies = self.generate_adaptive_water_bodies(height_map, water_params, planet_type)
        river_tiles = self.generate_smart_rivers(height_map, water_tiles, water_params, planet_type)
        mountain_tiles = self.get_mountain_ranges(height_map, planet_type)
        terrain_landscapes = planet_type.get_terrain_landscapes()
        forest_chance = planet_type.get_forest_chance()
        
        water_body_map = {}
        for body_type, bodies in classified_bodies.items():
            for body in bodies:
                for pos in body:
                    water_body_map[pos] = (body_type, len(body))
        
        regions = []
        all_tiles = {}
        
        for i in range(num_regions):
            if not regions_st[i]:
                regions.append([])
                continue
            reg_type_name = ["UpperReg", "CenterReg", "LowerReg"][i % 3]
            base_positions = {
                "CenterReg": [[0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1]],
                "UpperReg": [[-1, -2], [0, -2], [-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0]],
                "LowerReg": [[0, 0], [1, 0], [-1, 1], [0, 1], [1, 1], [-1, 2], [0, 2]]
            }[reg_type_name]
            offset = [3 * (i // 3), 0]
            positions = [[p[0] + offset[0], p[1] + offset[1]] for p in base_positions]
            
            tiles = []
            counter = 0
            for pos in positions:
                pos_tuple = tuple(pos)
                if pos_tuple in river_tiles:
                    landscape = planet_type.get_water_landscape('river', 1)
                elif pos_tuple in water_tiles:
                    body_type, size = water_body_map.get(pos_tuple, ('lake', 3))
                    landscape = planet_type.get_water_landscape(body_type, size)
                elif pos_tuple in mountain_tiles:
                    landscape = pt.Mountains()
                else:
                    landscape = self.weighted_choice(terrain_landscapes)
                
                building = (pt.EmptyBuilding() if regions_st[i].tiles[counter].building.type in 
                           ["EmptyBuilding", "Forest", "ArcticForest", "SwampVegetation"] 
                           else regions_st[i].tiles[counter].building)
                
                if landscape.type == "Plains" and random.randint(0, 100) < forest_chance and use_forest:
                    building = pt.Forest()
                elif landscape.type == "Snow" and random.randint(0, 100) < forest_chance and use_forest:
                    building = pt.ArcticForest()
                elif landscape.type == "Swampland" and random.randint(0, 100) < (forest_chance // 2) and use_forest:
                    building = pt.SwampVegetation()
                
                tile = pt.Tile(landscape, building)
                tile = self.apply_climate_effects(tile, pos, height_map, planet_type)
                
                tiles.append(tile)
                all_tiles[pos_tuple] = tile
                counter += 1
            
            region = pt.Region(tiles, positions, reg_type_name)
            regions.append(region)
        
        return pt.Planet(name, regions)
    
    def _get_neighbors(self, pos, all_positions):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (pos[0] + dx, pos[1] + dy)
                if neighbor in all_positions:
                    neighbors.append(neighbor)
        return neighbors