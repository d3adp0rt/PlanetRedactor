import sys
import inspect
import json
import os
from pathlib import Path

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

def load_landscapes_from_json():
    mods_path = Path("mods/Landscapes")
    
    if not mods_path.exists():
        return
    
    for mod_folder in mods_path.iterdir():
        if not mod_folder.is_dir():
            continue
            
        for json_file in mod_folder.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if not isinstance(data, dict):
                    print(f"Warning: Invalid JSON structure in {json_file}")
                    continue
                    
                mod_info = data.get("mod_info", {})
                mod_name = mod_info.get("name", mod_folder.name) 
                mod_version = mod_info.get("version", "Unknown Version")
                mod_author = mod_info.get("author", "Unknown Author")
                mod_description = mod_info.get("description", "")
                
                print("=" * 10 + " MOD INFO " + "=" * 10)
                print(f"Loading mod: {mod_name} v{mod_version} by {mod_author}")
                if mod_description:
                    print(f"Description: {mod_description}")
                print("=" * 30, '\n')
                
                if "landscapes" not in data:
                    print(f"Warning: No 'landscapes' key in {json_file}")
                    continue
                    
                for landscape_data in data["landscapes"]:
                    name = landscape_data.get("name")
                    landscape_type = landscape_data.get("type", name)
                    buildable = landscape_data.get("buildable", True)
                    
                    if not name:
                        continue
                    
                    if hasattr(current_module, name):
                        print(f"Warning: Landscape {name} already exists, skipping")
                        continue
                    
                    dynamic_class = type(name, (Landscape,), {
                        '__init__': lambda self, t=landscape_type, b=buildable: super(type(self), self).__init__(t, b)
                    })
                    
                    setattr(current_module, name, dynamic_class)
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON file {json_file}: {e}")
            except Exception as e:
                print(f"Error loading landscapes from {json_file}: {e}")

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

load_landscapes_from_json()
LandscapeTypes = get_subclasses_dict(Landscape)