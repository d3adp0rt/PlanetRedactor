from tkinter import ttk, filedialog
import tkinter as tk
import pygame as pg
import Planet as pt
import os, random

textures = {}
texture_variants = {} 
selected_variants = {}
placeholder = None

SCALE = 0.5
BUILDING_TYPES = list(pt.BuildingTypes.keys())
LANDSCAPE_TYPES = list(pt.LandscapeTypes.keys())

def get_random_texture_for_tile(texture_name: str, tile_id: str):
    tile_texture_key = f"{texture_name}_{tile_id}"
    
    if tile_texture_key in selected_variants:
        return selected_variants[tile_texture_key]
    
    if texture_name in texture_variants:
        chosen_texture = random.choice(texture_variants[texture_name])
        selected_variants[tile_texture_key] = chosen_texture
        return chosen_texture
    
    elif texture_name in textures:
        selected_variants[tile_texture_key] = textures[texture_name]
        return textures[texture_name]
    
    else:
        placeholder = create_placeholder_texture(183, 183)
        selected_variants[tile_texture_key] = placeholder
        return placeholder

def get_tile_id(region_index: int, tile_index: int):
    return f"r{region_index}_t{tile_index}"

def get_random_texture(texture_name: str):
    if texture_name in selected_variants:
        return selected_variants[texture_name]
    
    if texture_name in texture_variants:
        chosen_texture = random.choice(texture_variants[texture_name])
        selected_variants[texture_name] = chosen_texture
        return chosen_texture
    
    elif texture_name in textures:
        selected_variants[texture_name] = textures[texture_name]
        return textures[texture_name]
    
    else:
        placeholder = create_placeholder_texture(183, 183)
        selected_variants[texture_name] = placeholder
        return placeholder

def _find_mods_root(candidate_path: str):
    candidates = [
        os.path.join(candidate_path, "mods"),
        os.path.join(os.path.dirname(candidate_path), "mods"),
        os.path.join(os.getcwd(), "mods"),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None

def _search_mods_for_texture(mods_root: str, category: str, texture_name: str):
    category_root = os.path.join(mods_root, category)
    if not os.path.isdir(category_root):
        return None, None
    for modname in sorted(os.listdir(category_root)):
        modpath = os.path.join(category_root, modname)
        if not os.path.isdir(modpath):
            continue
        for root, dirs, files in os.walk(modpath):
            if texture_name in dirs:
                candidate = os.path.join(root, texture_name)
                pngs = [f for f in os.listdir(candidate) if f.lower().endswith('.png')]
                if pngs:
                    return candidate, True
            pname = f"{texture_name}.png"
            if pname in files:
                return os.path.join(root, pname), False
    return None, None

def _load_pngs_from_folder(folder_path: str, target_size):
    variants = []
    png_files = [f for f in sorted(os.listdir(folder_path)) if f.lower().endswith('.png')]
    for png in png_files:
        try:
            tex = pg.image.load(os.path.join(folder_path, png)).convert_alpha()
            tex = pg.transform.scale(tex, target_size)
            variants.append(tex)
        except pg.error as e:
            print(f"Ошибка загрузки текстуры {os.path.join(folder_path, png)}: {e}")
    return variants

def _load_single_png(file_path: str, target_size):
    try:
        tex = pg.image.load(file_path).convert_alpha()
        tex = pg.transform.scale(tex, target_size)
        return tex
    except pg.error as e:
        print(f"Ошибка загрузки текстуры {file_path}: {e}")
        return None

def load_texture_variants(path: str, texture_name: str, target_size=(183, 183), category_hint="both"):
    variants = []
    texture_folder = os.path.join(path, texture_name)
    if os.path.isdir(texture_folder):
        variants = _load_pngs_from_folder(texture_folder, target_size)
    if not variants:
        single_path = os.path.join(path, f"{texture_name}.png")
        if os.path.exists(single_path):
            tex = _load_single_png(single_path, target_size)
            if tex:
                variants = [tex]
    if not variants:
        mods_root = _find_mods_root(path)
        if mods_root:
            cats = []
            if category_hint == "landscapes":
                cats = ["Landscapes"]
            elif category_hint == "buildings":
                cats = ["Buildings"]
            else:
                cats = ["Landscapes", "Buildings"]
            found = False
            for cat in cats:
                found_path, is_folder = _search_mods_for_texture(mods_root, cat, texture_name)
                if found_path:
                    if is_folder:
                        loaded = _load_pngs_from_folder(found_path, target_size)
                        if loaded:
                            variants = loaded
                            print(f"[INFO]: Для {texture_name} найдено {len(loaded)} вариантов в моде ({found_path})")
                            found = True
                            break
                    else:
                        tex = _load_single_png(found_path, target_size)
                        if tex:
                            variants = [tex]
                            print(f"[INFO]: Для {texture_name} найден файл в модах: {found_path}")
                            found = True
                            break
            if not found:
                print(f"[INFO]: {texture_name} не найден в стандартной папке и не найден в {mods_root}. Будет использован placeholder.")
        else:
            print(f"[INFO]: {texture_name} не найден в стандартной папке и папка 'mods' не обнаружена. Будет использован placeholder.")
    if not variants:
        variants.append(create_placeholder_texture(*target_size))
        print(f"[INFO]: Для {texture_name} используется placeholder текстура")
    return variants

def LoadTextures(path: str):
    global textures, texture_variants, placeholder
    placeholder = pg.image.load("textures/PlaceHolder.png").convert_alpha()
    placeholder = pg.transform.scale(placeholder, (183, 183))
    landscape_types = list(pt.LandscapeTypes.keys())
    forest_buildings = list(pt.ForestTypes.keys())
    for landscape_type in landscape_types:
        texture_variants[landscape_type] = load_texture_variants(path, landscape_type, (183, 183), category_hint="landscapes")
    for forest_type in forest_buildings:
        texture_variants[forest_type] = load_texture_variants(path, forest_type, (183, 183), category_hint="landscapes")
    building_types = [bt for bt in pt.BuildingTypes.keys() if bt not in forest_buildings]
    for building_type in building_types:
        variants = load_texture_variants(path, building_type, (183, 183), category_hint="buildings")
        texture_variants[building_type] = variants
        textures[building_type] = variants[0] if variants else create_placeholder_texture(183, 183)
    level_textures = ["Lvl_0", "Lvl_1", "Lvl_2", "Lvl_3", "Lvl_4", "DES_Lvl_1", "DES_Lvl_2", "DES_Lvl_3", "DES_Lvl_4"]
    for level_name in level_textures:
        variants = load_texture_variants(path, level_name, (183, 183), category_hint="buildings")
        texture_variants[level_name] = variants
        textures[level_name] = variants[0]
    regions = {
        "CenterReg": ("CenterReg.png", (517, 455)),
        "LowerReg": ("LowerReg.png", (517, 455)),
        "UpperReg": ("UpperReg.png", (517, 455)),
    }
    for region_name, (filename, size) in regions.items():
        standard_path = os.path.join(path, filename)
        if os.path.exists(standard_path):
            try:
                textures[region_name] = pg.image.load(standard_path).convert_alpha()
                textures[region_name] = pg.transform.scale(textures[region_name], size)
            except pg.error as e:
                print(f"Ошибка загрузки {region_name}: {e}")
                textures[region_name] = create_placeholder_texture(*size)
        else:
            variants = load_texture_variants(path, os.path.splitext(filename)[0], size, category_hint="landscapes")
            textures[region_name] = variants[0]

def reset_texture_selection():
    global selected_variants
    selected_variants.clear()

def initialize_random_textures():
    landscape_types = list(pt.LandscapeTypes.keys())
    forest_buildings = list(pt.ForestTypes.keys())
    
    for landscape_type in landscape_types:
        get_random_texture(landscape_type)
    
    for forest_type in forest_buildings:
        get_random_texture(forest_type)

def get_json_files():
    return [f[:-5] for f in os.listdir('.') if f.endswith('.json')]

def select_json_file(start_path="."):
    result = {"selected": None}

    def get_json_files():
        return [f[:-5] for f in os.listdir(start_path) if f.endswith('.json')]

    def on_select(event=None):
        result["selected"] = combo.get()
        root.destroy()

    def choose_custom_file():
        filepath = filedialog.askopenfilename(
            title="Выберите JSON файл",
            filetypes=[("JSON файлы", "*.json")]
        )
        if filepath:
            filename = os.path.basename(filepath)
            name_without_ext = os.path.splitext(filename)[0]
            if name_without_ext not in combo["values"]:
                combo["values"] = (*combo["values"], name_without_ext)
            combo.set(name_without_ext)
            result["selected"] = name_without_ext
            root.destroy()

    root = tk.Tk()
    root.title("Выбор JSON файла")
    root.geometry("300x120")

    combo = ttk.Combobox(root, values=get_json_files(), state="readonly")
    combo.pack(padx=10, pady=10)

    btn = tk.Button(root, text="Выбрать файл...", command=choose_custom_file)
    btn.pack(pady=5)

    combo.bind("<<ComboboxSelected>>", on_select)

    root.mainloop()
    return result["selected"]

def create_placeholder_texture(w, h):
    surf = pg.Surface((w, h), pg.SRCALPHA)
    surf.blit(placeholder, (0, 0))
    return surf

def MakeTile(tile: pt.Tile, region_index: int = 0, tile_index: int = 0):
    texture = pg.Surface((183, 183), pg.SRCALPHA)
    
    tile_id = get_tile_id(region_index, tile_index)
    
    landscape_texture = get_random_texture_for_tile(tile.landscape.type, tile_id)
    texture.blit(landscape_texture, (0, 0))
    
    if tile.building.type != "EmptyBuilding":
        building_texture = get_random_texture_for_tile(tile.building.type, tile_id)
        texture.blit(building_texture, (0, 0))
    
    if tile.building.type not in ["PowerLines", "EmptyBuilding"] + list(pt.ForestTypes.keys()):
        level_texture = textures.get(f"Lvl_{tile.building.level}", create_placeholder_texture(183, 183))
        texture.blit(level_texture, (0, 0))
        for i in range(tile.building.destroyed):
            levelDES_texture = textures.get(f"DES_Lvl_{tile.building.level-i}", create_placeholder_texture(183, 183))
            texture.blit(levelDES_texture, (0, 0))
    
    return texture

def MakeRegion(region: pt.Region, region_index: int = 0):
    center_x, center_y = 540/2, 460/2
    half_hex = 90
    center_x1, center_y1 = center_x, center_y
    center_x -= half_hex
    center_y -= half_hex

    texture = pg.Surface((550, 460), pg.SRCALPHA)
    
    tiles = [MakeTile(tile, region_index, tile_index) for tile_index, tile in enumerate(region.tiles[:7])]

    if region.typeL == "CenterReg":
        positions = [
            (center_x - half_hex + 20, center_y - half_hex - 28),
            (center_x + half_hex - 21, center_y - half_hex - 28),
            (center_x - half_hex - half_hex + 42, center_y),
            (center_x, center_y),
            (center_x + half_hex + half_hex - 42, center_y),
            (center_x - half_hex + 20, center_y + half_hex + 28),
            (center_x + half_hex - 21, center_y + half_hex + 28)
        ]
        for tile_texture, pos in zip(tiles, positions):
            texture.blit(tile_texture, pos)
        texture.blit(textures["CenterReg"], (center_x1 - 517/2 + 3, center_y1 - 456/2 + 3))
    elif region.typeL == "UpperReg":
        positions = [
            (center_x - half_hex + 20, center_y - half_hex - 28),
            (center_x + half_hex - 21, center_y - half_hex - 28),
            (center_x + half_hex * 2 + 25, center_y - half_hex - 28),
            (center_x - half_hex - half_hex + 41, center_y + 2),
            (center_x, center_y + 2),
            (center_x + half_hex + half_hex - 40, center_y + 2),
            (center_x + half_hex - 21, center_y + half_hex + 28 + 4)
        ]
        for tile_texture, pos in zip(tiles, positions):
            texture.blit(tile_texture, pos)
        texture.blit(textures["UpperReg"], (center_x1 - 231, center_y1 - 223))
    else:  # LowerReg
        positions = [
            (center_x + half_hex - 21, center_y - half_hex - 30),
            (center_x - half_hex - half_hex + 43, center_y),
            (center_x + 1, center_y),
            (center_x + half_hex + half_hex - 40, center_y),
            (center_x - half_hex + 21, center_y + half_hex + 29),
            (center_x + half_hex - 21, center_y + half_hex + 29),
            (center_x + half_hex * 2 + 28, center_y + half_hex + 29)
        ]
        for tile_texture, pos in zip(tiles, positions):
            texture.blit(tile_texture, pos)
        texture.blit(textures["LowerReg"], (center_x1 - 229, center_y1 - 232))

    texture = pg.transform.scale(texture, (texture.get_width() * SCALE, texture.get_height() * SCALE))
    return texture

def MakeBlock(regionUp: pt.Region, regionCent: pt.Region, regionDown: pt.Region, block_index: int = 0):
    texture = pg.Surface((550, 960), pg.SRCALPHA)
    
    base_region_index = block_index * 3
    
    if regionUp:
        texture.blit(MakeRegion(regionUp, base_region_index), (72, 1))
    if regionCent:
        texture.blit(MakeRegion(regionCent, base_region_index + 1), (2, 123))
    if regionDown:
        texture.blit(MakeRegion(regionDown, base_region_index + 2), (70, 244))
    return texture

def MakePlanet(planet: pt.Planet):
    texture = pg.Surface((1800, 960), pg.SRCALPHA)
    blocks = [planet.Regions[i:i + 3] for i in range(0, len(planet.Regions), 3)]
    
    for block_index, block in enumerate(blocks):
        args = [block[i] if i < len(block) else None for i in range(3)]
        texture.blit(MakeBlock(*args, block_index), (208 * block_index, 0))
    
    return texture

def point_in_hexagon(point, center, size):
    px, py = point
    cx, cy = center
    r = size * 0.5
    vertices = [
        (cx, cy - r),
        (cx + r * 0.866, cy - r * 0.5),
        (cx + r * 0.866, cy + r * 0.5),
        (cx, cy + r),
        (cx - r * 0.866, cy + r * 0.5),
        (cx - r * 0.866, cy - r * 0.5)
    ]
    inside = False
    j = len(vertices) - 1
    for i in range(len(vertices)):
        if ((vertices[i][1] > py) != (vertices[j][1] > py)) and \
           (px < (vertices[j][0] - vertices[i][0]) * (py - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]):
            inside = not inside
        j = i
    return inside

def get_tile_positions(region_type, block_x, region_offset_x, region_offset_y):
    center_x, center_y = 540/2, 460/2
    half_hex = 90
    center_x -= half_hex
    center_y -= half_hex
    if region_type == "CenterReg":
        tile_offsets = [
            (center_x - half_hex + 20, center_y - half_hex - 28),
            (center_x + half_hex - 21, center_y - half_hex - 28),
            (center_x - half_hex - half_hex + 42, center_y),
            (center_x, center_y),
            (center_x + half_hex + half_hex - 42, center_y),
            (center_x - half_hex + 20, center_y + half_hex + 28),
            (center_x + half_hex - 21, center_y + half_hex + 28)
        ]
    elif region_type == "UpperReg":
        tile_offsets = [
            (center_x - half_hex + 20, center_y - half_hex - 28),
            (center_x + half_hex - 21, center_y - half_hex - 28),
            (center_x + half_hex * 2 + 25, center_y - half_hex - 28),
            (center_x - half_hex - half_hex + 41, center_y + 2),
            (center_x, center_y + 2),
            (center_x + half_hex + half_hex - 40, center_y + 2),
            (center_x + half_hex - 21, center_y + half_hex + 28 + 4)
        ]
    else:  # LowerReg
        tile_offsets = [
            (center_x + half_hex - 21, center_y - half_hex - 30),
            (center_x - half_hex - half_hex + 43, center_y),
            (center_x + 1, center_y),
            (center_x + half_hex + half_hex - 40, center_y),
            (center_x - half_hex + 21, center_y + half_hex + 29),
            (center_x + half_hex - 21, center_y + half_hex + 29),
            (center_x + half_hex * 2 + 28, center_y + half_hex + 29)
        ]
    return [(offset[0] * SCALE + block_x + region_offset_x, offset[1] * SCALE + region_offset_y) for offset in tile_offsets]

def find_clicked_tile(mouse_pos, planet):
    mx, my = mouse_pos
    BLOCK_WIDTH = 208
    total_blocks = (len(planet.Regions) + 2) // 3
    for block_idx in range(total_blocks):
        base_x = block_idx * BLOCK_WIDTH
        block_regions = planet.Regions[block_idx*3:block_idx*3 + 3]
        offsets = [(72, 1), (2, 123), (70, 244)]
        for i, region in enumerate(block_regions):
            try:
                off_x, off_y = offsets[i]
                positions = get_tile_positions(region.typeL, 0, base_x + off_x, off_y)
                tile_size = 183 * SCALE
                for idx, (tile_cx, tile_cy) in enumerate(positions):
                    if point_in_hexagon((mx, my), (tile_cx + tile_size / 2, tile_cy + tile_size / 2), tile_size):
                        return region, idx
            except: continue
    return None

def get_preview_texture(item_name: str):
    if item_name in textures:
        return textures[item_name]
    
    if item_name in texture_variants and texture_variants[item_name]:
        return texture_variants[item_name][0]
    
    return None

def draw_menu(screen, font, menu_type, items, mouse_pos):
    menu_width = 250
    item_height = 35
    padding = 10
    if menu_type == "main":
        title_height = 0
    else:
        title_height = 25
    max_height = screen.get_height() - 40
    max_rows = max((max_height - title_height - padding * 2) // item_height, 1)
    num_columns = (len(items) + max_rows - 1) // max_rows
    menu_height = min(len(items), max_rows) * item_height + title_height + padding * 2
    total_width = num_columns * menu_width
    menu_x = min(mouse_pos[0], screen.get_width() - total_width)
    menu_y = min(mouse_pos[1], screen.get_height() - menu_height)
    menu_rect = pg.Rect(menu_x, menu_y, total_width, menu_height)
    pg.draw.rect(screen, (40, 40, 40), menu_rect)
    pg.draw.rect(screen, (255, 255, 255), menu_rect, 2)
    
    if title_height > 0:
        if menu_type == "buildings":
            title = "Select Building Type"
        elif menu_type == "landscapes":
            title = "Select Landscape Type"
        elif menu_type == "levels":
            title = "Select Building Level"
        elif menu_type == "destroyed":
            title = "Set Destroyed Level"
        else:
            title = ""
        title_surface = font.render(title, True, (255, 255, 0))
        screen.blit(title_surface, (menu_x + 5, menu_y + 5))
    
    for index, item in enumerate(items):
        col = index // max_rows
        row = index % max_rows
        item_x = menu_x + col * menu_width
        item_y = menu_y + title_height + padding + row * item_height
        item_rect = pg.Rect(item_x, item_y, menu_width, item_height)
        
        if item_rect.collidepoint(pg.mouse.get_pos()):
            pg.draw.rect(screen, (80, 80, 80), item_rect)
        
        preview_x = item_x + 5
        text_x = item_x + 40
        
        if isinstance(item, str):
            preview_texture = get_preview_texture(item)
            if preview_texture:
                scaled_preview = pg.transform.scale(preview_texture, (30, 30))
                screen.blit(scaled_preview, (preview_x, item_y + 2))
        
        display_text = f"Level {item}" if menu_type == "levels" else str(item)
        text = font.render(display_text, True, (255, 255, 255))
        screen.blit(text, (text_x, item_y + item_height // 2 - text.get_height() // 2))
    
    return menu_rect

def handle_menu_click(mouse_pos, menu_rect, items, menu_type):
    if not menu_rect.collidepoint(mouse_pos):
        return None

    menu_width = 250
    item_height = 35
    padding = 10
    title_height = 25 if menu_type != "main" else 0

    max_height = menu_rect.height - padding * 2 - title_height
    max_rows = max(max_height // item_height, 1)
    num_columns = (len(items) + max_rows - 1) // max_rows

    relative_x = mouse_pos[0] - menu_rect.x
    relative_y = mouse_pos[1] - menu_rect.y - title_height

    if relative_y < 0:
        return None

    col = relative_x // menu_width
    row = relative_y // item_height
    index = col * max_rows + row

    if 0 <= index < len(items):
        return items[index]
    return None

def get_available_levels(building_type):
    if building_type in ["EmptyBuilding"] + list(pt.ForestTypes.keys()):
        return []
    elif building_type == "PowerLines":
        return [1]
    else:
        return [1, 2, 3, 4]

def process_selector(rect, options, selected, open_flag, mouse_pos, mouse_click, max_height=100):
    max_items_per_col = max_height // rect.height
    num_cols = (len(options) + max_items_per_col - 1) // max_items_per_col

    if mouse_click and rect.collidepoint(mouse_pos):
        open_flag = not open_flag
    elif mouse_click and open_flag:
        inside_list = False
        for col in range(num_cols):
            for i in range(max_items_per_col):
                idx = col * max_items_per_col + i
                if idx >= len(options):
                    break
                option_rect = pg.Rect(
                    rect.x + col * rect.width,
                    rect.y + rect.height + i * rect.height,
                    rect.width,
                    rect.height
                )
                if option_rect.collidepoint(mouse_pos):
                    inside_list = True
                    break
            if inside_list:
                break
        if not inside_list and not rect.collidepoint(mouse_pos):
            open_flag = False

    if open_flag and mouse_click:
        for col in range(num_cols):
            for i in range(max_items_per_col):
                idx = col * max_items_per_col + i
                if idx >= len(options):
                    break
                option_rect = pg.Rect(
                    rect.x + col * rect.width,
                    rect.y + rect.height + i * rect.height,
                    rect.width,
                    rect.height
                )
                if option_rect.collidepoint(mouse_pos):
                    selected = options[idx]
                    open_flag = False
                    break

    return selected, open_flag

def process_int_input(rect, text, active, events):
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            active = rect.collidepoint(event.pos)
        if event.type == pg.KEYDOWN and active:
            if event.key == pg.K_BACKSPACE:
                text = text[:-1]
            elif event.unicode.isdigit() or (event.unicode == '-' and not text):
                text += event.unicode
    return text, active

def process_text_input(rect, text, active, events, allow_negative=False, digits_only=False):
    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            active = rect.collidepoint(event.pos)

        if event.type == pg.KEYDOWN and active:
            if event.key == pg.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pg.K_RETURN:
                pass
            else:
                char = event.unicode
                if digits_only:
                    if char.isdigit() or (allow_negative and char == '-' and not text):
                        text += char
                else:
                    text += char
    return text, active

def process_checkbox(rect, value, mouse_pos, mouse_click):
    if mouse_click and rect.collidepoint(mouse_pos):
        value = not value
    return value

def draw_selector(screen, font, options, selected, is_open, rect, max_height=100):
    pg.draw.rect(screen, (70, 70, 70), rect)
    txt_surf = font.render(selected, True, (255, 255, 255))
    screen.blit(txt_surf, (rect.x + 5, rect.y + 5))
    pg.draw.rect(screen, (255, 255, 255), rect, 2)

    if is_open:
        max_items_per_col = max_height // rect.height
        num_cols = (len(options) + max_items_per_col - 1) // max_items_per_col

        for col in range(num_cols):
            for i in range(max_items_per_col):
                idx = col * max_items_per_col + i
                if idx >= len(options):
                    break
                option_rect = pg.Rect(
                    rect.x + col * rect.width,
                    rect.y + rect.height + i * rect.height,
                    rect.width,
                    rect.height
                )
                pg.draw.rect(screen, (50, 50, 50), option_rect)
                opt_txt = font.render(options[idx], True, (200, 200, 200))
                screen.blit(opt_txt, (option_rect.x + 5, option_rect.y + 5))
                pg.draw.rect(screen, (255, 255, 255), option_rect, 1)

def draw_int_input(screen, font, text, is_active, rect):
    pg.draw.rect(screen, (70, 70, 70), rect)
    color = (255, 255, 255) if is_active else (150, 150, 150)
    pg.draw.rect(screen, color, rect, 2)
    txt_surf = font.render(text, True, (255, 255, 255))
    screen.blit(txt_surf, (rect.x + 5, rect.y + 5))

def draw_checkbox(screen, value, rect):
    pg.draw.rect(screen, (70, 70, 70), rect)
    pg.draw.rect(screen, (255, 255, 255), rect, 2)
    if value:
        pg.draw.line(screen, (0, 255, 0), (rect.x + 3, rect.y + 3), (rect.x + rect.w - 3, rect.y + rect.h - 3), 3)
        pg.draw.line(screen, (0, 255, 0), (rect.x + 3, rect.y + rect.h - 3), (rect.x + rect.w - 3, rect.y + 3), 3)