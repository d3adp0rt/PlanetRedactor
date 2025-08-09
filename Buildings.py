
import sys
import inspect
import os
import json

current_module = sys.modules[__name__]

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

def load_building_mods():
    mods_path = "mods/Buildings"
    
    if not os.path.exists(mods_path):
        return
    
    for filename in os.listdir(mods_path):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(mods_path, filename), 'r', encoding='utf-8') as f:
                    mod_data = json.load(f)
                
                mod_info = mod_data.get("mod_info", {})
                mod_name = mod_info.get("name", "Unknown Mod")
                mod_version = mod_info.get("version", "Unknown Version")
                mod_author = mod_info.get("author", "Unknown Author")
                mod_description = mod_info.get("description", "")

                print("=" * 10 + " MOD INFO " + "=" * 10)
                print(f"Loading mod: {mod_name} v{mod_version} by {mod_author}")
                if mod_description:
                    print(f"Description: {mod_description}")
                print("=" * 30, '\n')

                if 'buildings' in mod_data:
                    for building_data in mod_data['buildings']:
                        create_building_class_from_json(building_data)
                        
                        
            except Exception as e:
                print(f"Ошибка при загрузке мода {filename}: {e}")

def create_building_class_from_json(building_data):
    """Создает класс строения из JSON данных"""
    class_name = building_data['name']
    
    resources_config = {}
    if 'resources' in building_data:
        for resource, config in building_data['resources'].items():
            resources_config[resource] = {
                'base': config.get('base', 0),
                'inc': config.get('inc', 0)
            }
    else:
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
        super(DynamicBuildingClass, self).__init__(
            type=class_name, 
            ELC=0, GoRP=0, VP=0, HP=0, GP=0, SP=0, money=0, 
            level=level, destroyed=destroyed
        )
        self.allowed_landscapes = building_data.get('allowed_landscapes', ["all"])
        self.landscape_bonuses = building_data.get('landscape_bonuses', {})
        
        if building_data.get('needs_rc', False):
            self.NeedsRC = True
    
    DynamicBuildingClass = type(class_name, (Building,), {
        'resources_config': resources_config,
        '__init__': __init__
    })
    
    setattr(current_module, class_name, DynamicBuildingClass)

load_building_mods()

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
ForestTypes = get_subclasses_dict(ForestBase)