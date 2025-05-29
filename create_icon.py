#!/usr/bin/env python3
"""
Erstellt ein Icon für die BildVektorisierer.exe
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Erstellt ein einfaches Icon für die Anwendung"""
    
    # Icon-Größen für Windows
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Erstelle ein neues Bild
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Hintergrund-Kreis (blau)
        margin = max(2, size // 16)
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(70, 130, 180, 255), outline=(30, 90, 140, 255), width=max(1, size//32))
        
        # Vektorisierungs-Symbol (Pfeil + Linien)
        if size >= 32:
            # Pfeil von links nach rechts
            arrow_start = size // 4
            arrow_end = 3 * size // 4
            arrow_y = size // 2
            arrow_width = max(2, size // 16)
            
            # Pfeil-Linie
            draw.line([arrow_start, arrow_y, arrow_end - size//8, arrow_y], 
                     fill=(255, 255, 255, 255), width=arrow_width)
            
            # Pfeil-Spitze
            arrow_tip_size = size // 8
            draw.polygon([
                (arrow_end, arrow_y),
                (arrow_end - arrow_tip_size, arrow_y - arrow_tip_size//2),
                (arrow_end - arrow_tip_size, arrow_y + arrow_tip_size//2)
            ], fill=(255, 255, 255, 255))
            
            # Bitmap-Linien (links)
            if size >= 48:
                line_start = size // 6
                line_spacing = max(2, size // 20)
                for i in range(3):
                    y = arrow_y - line_spacing + i * line_spacing
                    draw.line([line_start, y, arrow_start - 4, y], 
                             fill=(255, 255, 255, 200), width=max(1, size//32))
            
            # Vektor-Kurven (rechts)
            if size >= 48:
                curve_end = 5 * size // 6
                curve_y1 = arrow_y - size // 8
                curve_y2 = arrow_y + size // 8
                
                # Einfache Kurven-Simulation mit Linien
                for i in range(3):
                    x = arrow_end + 4 + i * 2
                    if x < curve_end:
                        draw.line([x, curve_y1, x + size//16, curve_y1 + size//32], 
                                 fill=(255, 255, 255, 200), width=max(1, size//32))
                        draw.line([x, curve_y2, x + size//16, curve_y2 - size//32], 
                                 fill=(255, 255, 255, 200), width=max(1, size//32))
        
        images.append(img)
    
    # Speichere als ICO-Datei
    images[0].save('icon.ico', format='ICO', sizes=[(img.width, img.height) for img in images])
    print(f"[OK] Icon erstellt: icon.ico")
    
    # Erstelle auch eine PNG-Version für Vorschau
    images[-1].save('icon_preview.png', format='PNG')
    print(f"[OK] Icon-Vorschau erstellt: icon_preview.png")

if __name__ == "__main__":
    create_icon() 