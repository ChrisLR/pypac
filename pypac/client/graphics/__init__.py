from pypac.client.graphics.spriteloader import SpriteLoader

sprite_loader = SpriteLoader()
sprite_loader.load_sprite_sheets(("16x16characters.png",))
sprite_loader.load_sprite_sheets(("16x16custom.png",))
sprite_sheet = sprite_loader.get_by_name("16x16characters")
tile_sheet = sprite_loader.get_by_name("16x16custom")
