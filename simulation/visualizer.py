"""Show the simulation in a clean, proportional visualization."""

import sys
import random
import math
from pathlib import Path

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pygame
import pygame.gfxdraw

from simulation.scenario import make_simulation, update_controls

# --- Configuration ---
SCALE = 2  # Supersampling factor (render at 2x, scale down)
FPS = 60
WINDOW_W, WINDOW_H = 1200, 400
RENDER_W, RENDER_H = WINDOW_W * SCALE, WINDOW_H * SCALE

# Minimalist Palette
COLORS = {
    "bg": (250, 250, 250),          # White/Clean
    "grid": (240, 240, 240),        # Very subtle grid
    "road": (80, 80, 80),           # Dark gray asphalt
    "markings_white": (255, 255, 255),
    "markings_yellow": (255, 215, 0),
    "shadow": (0, 0, 0, 30),        # Soft shadow alpha
    "text": (50, 50, 50),
    "ui_bg": (255, 255, 255, 220),  # Translucent white
    "cars": [
        (230, 80, 80),   # Red
        (80, 160, 220),  # Blue
        (240, 170, 60),  # Orange
        (80, 190, 130),  # Green
        (160, 100, 180), # Purple
    ],
    "collision": (230, 60, 60, 200),
}

# --- Drawing Helpers ---

def draw_rounded_rect(surface, rect, color, radius=0.4):
    """
    Draw a filled rounded rectangle.
    rect: (x, y, w, h)
    radius: 0.0 to 1.0 (relative to height/2)
    """
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    pos = rect.topleft
    
    # Calculate pixel radius
    r = int(min(rect.w, rect.h) * radius / 2)
    
    # Draw rounded shape
    x, y = pos
    w, h = rect.size
    
    # Clamp radius
    r = max(0, min(r, w//2, h//2))
    
    if r < 2:
        pygame.draw.rect(surface, color, rect)
        return

    # Corners
    pygame.draw.circle(surface, color, (x+r, y+r), r)
    pygame.draw.circle(surface, color, (x+w-r, y+r), r)
    pygame.draw.circle(surface, color, (x+r, y+h-r), r)
    pygame.draw.circle(surface, color, (x+w-r, y+h-r), r)
    
    # Fillers
    pygame.draw.rect(surface, color, (x+r, y, w-2*r, h))
    pygame.draw.rect(surface, color, (x, y+r, w, h-2*r))


def draw_car_sprite(surface, x, y, w, h, color, car_id):
    """Draw a car shape."""
    # Body
    draw_rounded_rect(surface, (x, y, w, h), color, 0.4)
    
    # Roof highlight
    roof_w = w * 0.5
    roof_h = h * 0.7
    roof_x = x + (w - roof_w) / 2
    roof_y = y + (h - roof_h) / 2
    
    # Highlight
    highlight = [min(c + 30, 255) for c in color[:3]]
    draw_rounded_rect(surface, (roof_x, roof_y, roof_w, roof_h), highlight, 0.3)


def run_visualizer(dt=0.05, fps=60):
    sim = make_simulation()
    road_length = sim.road.length
    
    pygame.init()
    try:
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
    except:
        pass
        
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.DOUBLEBUF)
    pygame.display.set_caption("Simulation Visualization")
    
    # Render surface (2x size)
    canvas = pygame.Surface((RENDER_W, RENDER_H))
    
    clock = pygame.time.Clock()
    
    # Dimensions in RENDER space
    margin_x = 50 * SCALE
    margin_y = 50 * SCALE
    
    # Proportional rendering: fit road to width, scaling everything else
    road_w_px = RENDER_W - 2 * margin_x
    
    # Fixed road height in meters? Or just visual height.
    # Visual height is better fixed for visibility.
    road_h_px = 120 * SCALE 
    lane_h_px = road_h_px / 2
    
    road_top = (RENDER_H - road_h_px) // 2
    road_bottom = road_top + road_h_px
    road_center_y = road_top + lane_h_px
    road_left = margin_x
    
    # Pixels per meter
    px_per_m = road_w_px / road_length

    # Fonts
    font_name = pygame.font.match_font('segoeui') or pygame.font.match_font('helveticaneue') or pygame.font.match_font('arial')
    font_ui = pygame.font.Font(font_name, int(24 * SCALE)) if font_name else pygame.font.SysFont(None, int(24 * SCALE))
    font_label = pygame.font.Font(font_name, int(16 * SCALE)) if font_name else pygame.font.SysFont(None, int(16 * SCALE))
    font_alert = pygame.font.Font(font_name, int(60 * SCALE)) if font_name else pygame.font.SysFont(None, int(60 * SCALE))

    t = 0
    running = True
    collision = False
    
    while running:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Step
        if not collision:
            update_controls(sim, t)
            sim.step(dt)
            t += dt
            if sim.check_collision():
                collision = True

        # --- Draw to Canvas (Supersampled) ---
        canvas.fill(COLORS["bg"])
        
        # Grid (Dots)
        grid_spacing = 50 * SCALE
        for x in range(0, RENDER_W, grid_spacing):
            for y in range(0, RENDER_H, grid_spacing):
                pygame.draw.circle(canvas, COLORS["grid"], (x, y), 2 * SCALE)

        # Road Surface
        pygame.draw.rect(canvas, COLORS["road"], (road_left, road_top, road_w_px, road_h_px))
        
        # Lane Markings
        # Edges (White)
        pygame.draw.line(canvas, COLORS["markings_white"], (road_left, road_top), (road_left+road_w_px, road_top), 4*SCALE)
        pygame.draw.line(canvas, COLORS["markings_white"], (road_left, road_bottom), (road_left+road_w_px, road_bottom), 4*SCALE)
        
        # Center Line (Dashed Yellow)
        dash_len = 40 * SCALE
        gap_len = 30 * SCALE
        cx = road_left
        while cx < road_left + road_w_px:
            w = min(dash_len, road_left + road_w_px - cx)
            if w > 0:
                pygame.draw.rect(canvas, COLORS["markings_yellow"], (cx, road_center_y - 3*SCALE, w, 6*SCALE))
            cx += dash_len + gap_len

        # Cars
        for i, car in enumerate(sim.cars):
            # Proportional mapping
            # car.position is distance from start (0)
            front_x = road_left + car.position * px_per_m
            back_x = road_left + (car.position - car.length) * px_per_m
            
            # Car visual width
            car_w_px = abs(front_x - back_x)
            
            # If car is extremely small, enforce min width?
            # User wants "proportional". 
            # If road is 10km and car is 5m, car is 1/2000 of width. On 2000px screen, that's 1px.
            # So cars will be tiny on long roads. That is physically correct.
            # But let's enforce a minimum 4px so it's visible as a speck.
            car_w_px = max(4*SCALE, car_w_px)
            
            car_x = min(front_x, back_x)
            
            # Lane
            lane_offset = car.lane * lane_h_px
            car_h_px = lane_h_px * 0.55
            car_y = road_top + lane_offset + (lane_h_px - car_h_px) / 2
            
            color = COLORS["cars"][i % len(COLORS["cars"])]
            
            draw_car_sprite(canvas, car_x, car_y, car_w_px, car_h_px, color, car.id)
            
            # Label
            lbl = font_label.render(car.id, True, COLORS["text"])
            canvas.blit(lbl, (car_x + (car_w_px - lbl.get_width())//2, car_y - lbl.get_height() - 5*SCALE))

        # UI Overlay (Time)
        time_str = f"{t:.1f}s"
        pill_w, pill_h = 140 * SCALE, 60 * SCALE
        pill_x, pill_y = 30 * SCALE, 30 * SCALE
        draw_rounded_rect(canvas, (pill_x, pill_y, pill_w, pill_h), COLORS["ui_bg"], 1.0)
        
        pygame.draw.circle(canvas, COLORS["text"], (pill_x + 30*SCALE, pill_y + 30*SCALE), 12*SCALE, 3*SCALE)
        pygame.draw.line(canvas, COLORS["text"], (pill_x + 30*SCALE, pill_y + 30*SCALE), (pill_x + 30*SCALE, pill_y + 18*SCALE), 2*SCALE)
        pygame.draw.line(canvas, COLORS["text"], (pill_x + 30*SCALE, pill_y + 30*SCALE), (pill_x + 38*SCALE, pill_y + 30*SCALE), 2*SCALE)
        
        ts = font_ui.render(time_str, True, COLORS["text"])
        canvas.blit(ts, (pill_x + 60*SCALE, pill_y + (pill_h - ts.get_height())//2))

        # Collision Overlay
        if collision:
            overlay = pygame.Surface((RENDER_W, RENDER_H), pygame.SRCALPHA)
            overlay.fill((COLORS["collision"][0], COLORS["collision"][1], COLORS["collision"][2], 180))
            canvas.blit(overlay, (0,0))
            
            txt = font_alert.render("COLLISION", True, (255,255,255))
            canvas.blit(txt, ((RENDER_W - txt.get_width())//2, (RENDER_H - txt.get_height())//2))

        # --- Scale down and Blit to Window ---
        frame = pygame.transform.smoothscale(canvas, (WINDOW_W, WINDOW_H))
        window.blit(frame, (0, 0))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_visualizer()
