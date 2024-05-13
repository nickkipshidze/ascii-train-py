import tint, time, os

def draw_edges(surface: tint.Interface):
    W, H = surface.surf_width, surface.surf_height
    surface.draw_line(0, 0, 0, W, "|")
    surface.draw_line(W, 0, W-1, H, "|")
    surface.draw_line(0, 0, W, 0, "-")
    surface.draw_line(0, H-1, W, H-1, "-")
    
def draw_rail_tracks(surface: tint.Interface, offset=0, intervals=8):
    W, H = surface.surf_width, surface.surf_height
    surface.draw_line(0, H-2, W, H-2, "=")
    for x in range(-W, W, intervals):
        surface.draw_char(x+(offset%intervals), H-2, "-")

def draw_wheel(surface: tint.Interface, frame, x, y):
    surface.draw_sprite(x, y, f"wheel-{frame}")
    
def draw_body(surface: tint.Interface, x, y):
    surface.draw_sprite(x, y, "train")

def draw_train(surface: tint.Interface, wheel, bounce, offset=0):
    W, H = surface.surf_width, surface.surf_height
    draw_wheel(surface, (round(wheel)-2)%len(os.listdir("./wheels")), 35+offset, H-4)
    draw_wheel(surface, (round(wheel)-4)%len(os.listdir("./wheels")), 64+offset, H-4)
    surface.draw_sprite(16+offset,  H-11+bounce%2, "train")
    draw_wheel(surface, (round(wheel)-1)%len(os.listdir("./wheels")), 28+offset, H-4)
    draw_wheel(surface, (round(wheel)-2)%len(os.listdir("./wheels")), 43+offset, H-4)
    draw_wheel(surface, (round(wheel)-4)%len(os.listdir("./wheels")), 56+offset, H-4)
    draw_wheel(surface, (round(wheel)-6)%len(os.listdir("./wheels")), 72+offset, H-4)

def draw_wagon(surface: tint.Interface, wheel, bounce, offset=0):
    W, H = surface.surf_width, surface.surf_height
    surface.draw_sprite(16+offset,  H-11+bounce%2, "wagon")
    draw_wheel(surface, (round(wheel)-1)%len(os.listdir("./wheels")), 28+offset, H-4)
    draw_wheel(surface, (round(wheel)-2)%len(os.listdir("./wheels")), 43+offset, H-4)
    draw_wheel(surface, (round(wheel)-4)%len(os.listdir("./wheels")), 56+offset, H-4)
    draw_wheel(surface, (round(wheel)-6)%len(os.listdir("./wheels")), 72+offset, H-4)
    
def draw_clouds(surface: tint.Interface, offset):
    W, H = surface.surf_width, surface.surf_height
    inter = 150
    for x in range(-W, W, inter):
        surface.draw_sprite(x-offset%inter+inter, 10, "cloud-1")
    inter = 230
    for x in range(-W, W, inter):
        surface.draw_sprite(x-offset%inter+inter, 30, "cloud-2")
    inter = 350
    for x in range(-W, W, inter):
        surface.draw_sprite(x-offset%inter+inter, 15, "cloud-1")

def load_sprites(UI):    
    for wheel in os.listdir("./wheels"):
        UI.make_sprite(wheel.split(".")[0], file=f"./wheels/{wheel}")
    
    UI.make_sprite("train", file="./train/train.txt")
    UI.make_sprite("wagon", file="./train/wagon.txt")
    UI.make_sprite("cloud-1", file="./clouds/cloud-1.txt")
    UI.make_sprite("cloud-2", file="./clouds/cloud-2.txt")

def main():
    UI = tint.Interface(120, 40, "center,center")
    
    load_sprites(UI)
        
    track, wheel, bounce = 0, 0, 0
    wagon_count = 10
    
    while True:
        load_sprites(UI)
        UI.update_terminal_size()
        
        UI.surf_width = UI.columns
        UI.surf_height = UI.rows - 2
        
        train_offset = UI.surf_width - 120 
        
        UI.fill(" ")
        
        track -= 1
        wheel += 0.2
        bounce += 0.02
        
        draw_rail_tracks(UI, offset=track)
        draw_train(UI, wheel, bounce, 30 + train_offset)
        
        last = 30+train_offset
        for x in range(last+(69*wagon_count), last, -69):
            draw_wagon(UI, wheel-(x%4), bounce-(((x**2)%10)/10), x-(69*wagon_count)-67)
        
        if UI.surf_height > 50: draw_clouds(UI, offset=-track)
        draw_edges(UI)
        
        UI.stdout()
        time.sleep(0.02)

main()
