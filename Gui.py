import pygame as pg
import Planet as pt
from Planet import *
import GuiMethods as gm
import os

class GUI_Planet_class():
    def __init__(self):
        self.tiles = []
        self.regions = []
        self.name = "Default name"

        for i in range(21):
            tiles = [
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
                Tile(Plains(), EmptyBuilding()),
            ]
            self.tiles.append(tiles)
            if i % 3 == 0:
                region = UpperReg(tiles)
            elif i % 3 == 1:
                region = CenterReg(tiles)
            else:
                region = LowerReg(tiles)
            self.regions.append(region)

        self.planet = Planet(Regions=self.regions, name=self.name)
    
    def updateSize(self, size, AddExtensionTop, AddExtensionMid, AddExtensionDown):
        self.tiles = []
        self.regions = []

        for i in range(size * 3):
            tiles = [Tile(Plains(), EmptyBuilding()) for _ in range(7)]
            self.tiles.append(tiles)
            if i % 3 == 0:
                region = UpperReg(tiles)
            elif i % 3 == 1:
                region = CenterReg(tiles)
            else:
                region = LowerReg(tiles)
            self.regions.append(region)

        if AddExtensionTop:
            tiles = [Tile(Plains(), EmptyBuilding()) for _ in range(7)]
            region = UpperReg(tiles)
        else:
            region = []
        self.regions.append(region)

        if AddExtensionMid:
            tiles = [Tile(Plains(), EmptyBuilding()) for _ in range(7)]
            region = CenterReg(tiles)
        else:
            region = []
        self.regions.append(region)

        if AddExtensionDown:
            tiles = [Tile(Plains(), EmptyBuilding()) for _ in range(7)]
            region = LowerReg(tiles)
        else:
            region = []
        self.regions.append(region)

        self.planet = Planet(Regions=self.regions, name=self.name)

    def updateName(self, name):
        self.name = name
        self.planet.name = name

GUI_Planet = GUI_Planet_class()

def build_texture_names():
    keys = list(pt.BuildingTypes.keys()) + list(pt.LandscapeTypes.keys())
    names = {name: f"{name}.png" for name in keys}
    names.update({
        "Lvl_0": "Lvl_0.png",
        "Lvl_1": "Lvl_1.png",
        "Lvl_2": "Lvl_2.png",
        "Lvl_3": "Lvl_3.png",
        "Lvl_4": "Lvl_4.png"
    })
    return names

def create_building(building_type, level=1):
    cls = pt.BuildingTypes.get(building_type, pt.EmptyBuilding)
    try:
        return cls(level)
    except TypeError:
        return cls()

def create_landscape(landscape_type):
    cls = pt.LandscapeTypes.get(landscape_type, pt.Plains)
    try:
        return cls()
    except TypeError:
        return cls()

def main():
    pg.init()
    font = pg.font.SysFont(None, 20)
    fontName = pg.font.SysFont(None, 150)
    screen_W, screen_H = 1800, 900
    screen = pg.display.set_mode((screen_W, screen_H))
    pg.display.set_caption("Planet Redactor")
    gm.LoadTextures("textures")
    gm.initialize_random_textures()

    show_menu = False
    menu_type = None
    menu_items = []
    menu_rect = None
    menu_pos = (0, 0)
    selected_tile = None
    selected_building_type = None

    margin, gap = 20, 10
    y = screen_H - 400 - margin
    options = ["Green", "Dry", "Cold", "Dead", "Lithoid", "Ideal", "Ecumenopolis", "Burned", "Aquatic", "Volcanic", "Crystalline", "Swamp", "Toxic"]
    TypeOfWorld = options[0]
    selector_open = False
    selector_rect = pg.Rect(margin, y, 150, 30)

    WaterTypeWorld = '1'
    int_rect = pg.Rect(margin + 150 + gap, y, 150, 30)
    int_active = False

    UseForestValue = False
    checkbox_rect = pg.Rect(margin + 150 + gap + 150 + gap, y + 5, 20, 20)

    SizeOfPlanet = '1'
    SizeOfPlanet_rect = pg.Rect(screen_W - margin - 150, y, 150, 30)
    SizeOfPlanet_active = False

    NameOfPlanet = 'Empty planet'
    NameOfPlanet_rect = pg.Rect(screen_W - margin - 150 - gap - 350, y, 350, 30)
    NameOfPlanet_active = False

    NameOfPlanet_FONT = fontName.render(NameOfPlanet, True, (255, 255, 255))
    NameOfPlanet_FONT_rect = NameOfPlanet_FONT.get_rect(center=(screen_W // 2, screen_H - screen_H / 3))

    AddExtUp = False
    AddExtUp_rect = pg.Rect(screen_W - margin - gap - 20, y + 40, 20, 20)
    AddExtCent = False
    AddExtCent_rect = pg.Rect(screen_W - margin - gap * 2 - 40, y + 40, 20, 20)
    AddExtDown = False
    AddExtDown_rect = pg.Rect(screen_W - margin - gap * 3 - 60, y + 40, 20, 20)

    running = True
    while running:
        events = pg.event.get()
        mouse_pos = pg.mouse.get_pos()
        mouse_click = any(e.type == pg.MOUSEBUTTONDOWN and e.button == 1 for e in events)

        for event in events:
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if not NameOfPlanet_active:
                    if event.key == pg.K_s:
                        GUI_Planet.planet.dump()
                        print("Planet Saved")
                    elif event.key == pg.K_l:
                        GUI_Planet.planet.load(gm.select_json_file())
                        GUI_Planet.name = GUI_Planet.planet.name
                        GUI_Planet.updateName(GUI_Planet.name)
                        NameOfPlanet = GUI_Planet.name
                        NameOfPlanet_FONT = fontName.render(GUI_Planet.name, True, (255, 255, 255))
                        NameOfPlanet_FONT_rect = NameOfPlanet_FONT.get_rect(center=(screen_W // 2, screen_H - screen_H/3))
                        print("Planet Loaded")
                    elif event.key == pg.K_g:
                        GUI_Planet.planet.generate(int(WaterTypeWorld), TypeOfWorld, UseForestValue)
                        GUI_Planet.planet.dump()
                        GUI_Planet.planet.load()
                    elif event.key == pg.K_c:
                        print(GUI_Planet.planet.calculate())
                    elif event.key == pg.K_u:
                        GUI_Planet.updateSize(int(SizeOfPlanet), AddExtUp, AddExtCent, AddExtDown)
                        GUI_Planet.updateName(NameOfPlanet)
                        NameOfPlanet_FONT = fontName.render(GUI_Planet.name, True, (255, 255, 255))
                        NameOfPlanet_FONT_rect = NameOfPlanet_FONT.get_rect(center=(screen_W // 2, screen_H - screen_H/3))
                    elif event.key == pg.K_x:
                        GUI_Planet.updateName(NameOfPlanet)
                        NameOfPlanet_FONT = fontName.render(GUI_Planet.name, True, (255, 255, 255))
                        NameOfPlanet_FONT_rect = NameOfPlanet_FONT.get_rect(center=(screen_W // 2, screen_H - screen_H/3))

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right click
                    clicked_tile = gm.find_clicked_tile(event.pos, GUI_Planet.planet)
                    if clicked_tile:
                        selected_tile = clicked_tile
                        show_menu = True
                        menu_type = "main"
                        menu_items = ["Buildings", "Landscapes"]
                        menu_pos = event.pos
                    else:
                        show_menu = False
                elif event.button == 2:  # Middle click
                    clicked_tile = gm.find_clicked_tile(event.pos, GUI_Planet.planet)
                    if clicked_tile:
                        region, tile_index = clicked_tile
                        building = region.tiles[tile_index].building
                        if building.level >= 1:
                            max_destroyed = building.level
                            menu_items = [str(i) for i in range(max_destroyed + 1)]
                            show_menu = True
                            menu_type = "destroyed"
                            menu_pos = event.pos
                            selected_tile = (region, tile_index)
                elif event.button == 1:  # Left click
                    if show_menu and menu_rect:
                        selected_item = gm.handle_menu_click(event.pos, menu_rect, menu_items, menu_type)
                        if selected_item:
                            if menu_type == "main":
                                if selected_item == "Buildings":
                                    menu_type = "buildings"
                                    menu_items = gm.BUILDING_TYPES
                                elif selected_item == "Landscapes":
                                    menu_type = "landscapes"
                                    menu_items = gm.LANDSCAPE_TYPES
                            elif menu_type == "buildings":
                                available_levels = gm.get_available_levels(selected_item)
                                if available_levels:
                                    selected_building_type = selected_item
                                    menu_type = "levels"
                                    menu_items = available_levels
                                else:
                                    if selected_tile:
                                        region, tile_index = selected_tile
                                        new_building = create_building(selected_item, 1)
                                        old_landscape = region.tiles[tile_index].landscape
                                        try:
                                            region.tiles[tile_index] = pt.Tile(old_landscape, new_building)
                                        except Warning as w:
                                            print(f"Warning: {w}")
                                            region.tiles[tile_index] = pt.Tile(old_landscape, new_building)
                                        show_menu = False
                            elif menu_type == "levels" and selected_tile and selected_building_type:
                                region, tile_index = selected_tile
                                new_building = create_building(selected_building_type, selected_item)
                                old_landscape = region.tiles[tile_index].landscape
                                try:
                                    region.tiles[tile_index] = pt.Tile(old_landscape, new_building)
                                except Warning as w:
                                    print(f"Warning: {w}")
                                    region.tiles[tile_index] = pt.Tile(old_landscape, new_building)
                                show_menu = False
                                selected_building_type = None
                            elif menu_type == "landscapes" and selected_tile:
                                region, tile_index = selected_tile
                                new_landscape = create_landscape(selected_item)
                                old_building = region.tiles[tile_index].building
                                try:
                                    region.tiles[tile_index] = pt.Tile(new_landscape, old_building)
                                except Warning as w:
                                    print(f"Warning: {w}")
                                    region.tiles[tile_index] = pt.Tile(new_landscape, old_building)
                                show_menu = False
                            elif menu_type == "destroyed" and selected_tile:
                                region, tile_index = selected_tile
                                try:
                                    new_destroyed = int(selected_item)
                                    building = region.tiles[tile_index].building
                                    if 0 <= new_destroyed <= building.level:
                                        building.destroyed = new_destroyed
                                    else:
                                        print(f"Invalid destroyed level: {new_destroyed} for building level {building.level}")
                                except ValueError:
                                    print(f"Invalid selection: {selected_item}")
                                show_menu = False
                        else:
                            show_menu = False
                    else:
                        show_menu = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                show_menu = False

        screen.fill((125, 125, 125))
        TypeOfWorld, selector_open = gm.process_selector(selector_rect, options, TypeOfWorld, selector_open, mouse_pos, mouse_click)
        WaterTypeWorld, int_active = gm.process_int_input(int_rect, WaterTypeWorld, int_active, events)
        SizeOfPlanet, SizeOfPlanet_active = gm.process_int_input(SizeOfPlanet_rect, SizeOfPlanet, SizeOfPlanet_active, events)
        NameOfPlanet, NameOfPlanet_active = gm.process_text_input(NameOfPlanet_rect, NameOfPlanet, NameOfPlanet_active, events)
        UseForestValue = gm.process_checkbox(checkbox_rect, UseForestValue, mouse_pos, mouse_click)
        AddExtUp = gm.process_checkbox(AddExtUp_rect, AddExtUp, mouse_pos, mouse_click)
        AddExtCent = gm.process_checkbox(AddExtCent_rect, AddExtCent, mouse_pos, mouse_click)
        AddExtDown = gm.process_checkbox(AddExtDown_rect, AddExtDown, mouse_pos, mouse_click)

        gm.draw_selector(screen, font, options, TypeOfWorld, selector_open, selector_rect)
        gm.draw_int_input(screen, font, WaterTypeWorld, int_active, int_rect)
        gm.draw_checkbox(screen, UseForestValue, checkbox_rect)
        gm.draw_int_input(screen, font, SizeOfPlanet, SizeOfPlanet_active, SizeOfPlanet_rect)
        gm.draw_int_input(screen, font, NameOfPlanet, NameOfPlanet_active, NameOfPlanet_rect)
        gm.draw_checkbox(screen, AddExtUp, AddExtUp_rect)
        gm.draw_checkbox(screen, AddExtCent, AddExtCent_rect)
        gm.draw_checkbox(screen, AddExtDown, AddExtDown_rect)

        texture = gm.MakePlanet(GUI_Planet.planet)
        screen.blit(texture, (0, 0))
        screen.blit(NameOfPlanet_FONT, NameOfPlanet_FONT_rect)

        if show_menu:
            menu_rect = gm.draw_menu(screen, font, menu_type, menu_items, menu_pos)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()