import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("sample_data", exist_ok=True)

def create_gradient_plate(draw, center, radius, color1, color2):
    for r in range(radius, 0, -1):
        ratio = r / radius
        r_col = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g_col = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b_col = int(color1[2] * ratio + color2[2] * (1 - ratio))
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=(r_col, g_col, b_col))

# 1. Mediterranean Salmon Bowl
def make_salmon_bowl():
    img = Image.new("RGB", (800, 600), (28, 33, 44))
    draw = ImageDraw.Draw(img)
    # Background table
    draw.rectangle([0, 0, 800, 600], fill=(35, 40, 52))
    # Plate
    draw.ellipse([150, 50, 650, 550], fill=(225, 230, 235), outline=(190, 195, 205), width=8)
    draw.ellipse([180, 80, 620, 520], fill=(245, 248, 250))
    # Quinoa base
    draw.ellipse([210, 110, 590, 490], fill=(218, 198, 155))
    # Salmon fillet
    draw.polygon([(320, 200), (480, 200), (510, 360), (350, 360)], fill=(245, 120, 85))
    for y in range(220, 350, 25):
        draw.line([(335, y), (495, y)], fill=(255, 175, 145), width=4)
    # Avocado slices
    for i in range(4):
        offset = i * 25
        draw.ellipse([230 + offset, 300 + offset, 310 + offset, 380 + offset], fill=(120, 180, 70), outline=(70, 120, 40), width=3)
    # Cherry tomatoes
    for pos in [(250, 180), (280, 230), (520, 240), (500, 380), (450, 430)]:
        draw.ellipse([pos[0], pos[1], pos[0]+45, pos[1]+45], fill=(225, 45, 35))
        draw.ellipse([pos[0]+12, pos[1]+10, pos[0]+20, pos[1]+18], fill=(255, 180, 175))
    # Leafy greens
    for pos in [(370, 120), (430, 140), (490, 170), (280, 400), (330, 440)]:
        draw.ellipse([pos[0], pos[1], pos[0]+60, pos[1]+40], fill=(50, 140, 60))
    # Lemon wedge
    draw.pieslice([400, 380, 520, 500], 180, 270, fill=(250, 220, 40), outline=(220, 180, 20), width=4)
    
    # Text badge
    draw.rectangle([20, 20, 340, 60], fill=(16, 185, 129))
    draw.text((35, 30), "SAMPLE: Mediterranean Salmon Bowl", fill=(255, 255, 255))
    img.save("sample_data/sample_salmon_bowl.jpg", quality=92)

# 2. Fresh Apple
def make_fresh_apple():
    img = Image.new("RGB", (800, 600), (22, 27, 36))
    draw = ImageDraw.Draw(img)
    # Shadow
    draw.ellipse([250, 460, 550, 520], fill=(14, 17, 24))
    # Apple body
    draw.ellipse([250, 150, 460, 480], fill=(210, 30, 30))
    draw.ellipse([340, 150, 550, 480], fill=(195, 25, 25))
    draw.ellipse([270, 180, 530, 460], fill=(220, 35, 35))
    # Highlights (glossy shine)
    draw.ellipse([300, 200, 350, 300], fill=(255, 130, 130))
    draw.ellipse([310, 215, 335, 265], fill=(255, 220, 220))
    # Stem & Leaf
    draw.line([(400, 170), (405, 110)], fill=(90, 55, 30), width=12)
    draw.ellipse([405, 100, 470, 135], fill=(70, 160, 50))
    
    draw.rectangle([20, 20, 290, 60], fill=(16, 185, 129))
    draw.text((35, 30), "SAMPLE: Fresh Crisp Apple", fill=(255, 255, 255))
    img.save("sample_data/sample_fresh_apple.jpg", quality=92)

# 3. Spoiled Moldy Strawberries
def make_spoiled_berries():
    img = Image.new("RGB", (800, 600), (25, 28, 38))
    draw = ImageDraw.Draw(img)
    # Punnet container
    draw.rectangle([180, 120, 620, 500], fill=(45, 52, 68), outline=(80, 92, 115), width=4)
    # Darkened rotting strawberries
    for pos in [(230, 200), (380, 190), (490, 230), (290, 320), (420, 340), (250, 410), (480, 400)]:
        # Rotten base color
        draw.ellipse([pos[0], pos[1], pos[0]+120, pos[1]+100], fill=(110, 30, 35))
        # Spoilage dark sunken patches
        draw.ellipse([pos[0]+20, pos[1]+20, pos[0]+80, pos[1]+70], fill=(60, 25, 30))
        # Mold fungal fuzz
        draw.ellipse([pos[0]+35, pos[1]+30, pos[0]+75, pos[1]+65], fill=(195, 210, 200))
        draw.ellipse([pos[0]+45, pos[1]+35, pos[0]+65, pos[1]+55], fill=(235, 245, 240))
        for spot in [(pos[0]+15, pos[1]+45), (pos[0]+70, pos[1]+25), (pos[0]+55, pos[1]+75)]:
            draw.ellipse([spot[0], spot[1], spot[0]+12, spot[1]+12], fill=(160, 185, 175))

    draw.rectangle([20, 20, 330, 60], fill=(239, 68, 68))
    draw.text((35, 30), "SAMPLE: Spoiled Moldy Berries", fill=(255, 255, 255))
    img.save("sample_data/sample_spoiled_berries.jpg", quality=92)

# 4. Commercial Kitchen Compliant
def make_commercial_kitchen():
    img = Image.new("RGB", (800, 600), (30, 35, 48))
    draw = ImageDraw.Draw(img)
    # Stainless prep counter
    draw.polygon([(50, 380), (750, 380), (800, 600), (0, 600)], fill=(170, 180, 195))
    draw.line([(50, 380), (750, 380)], fill=(220, 230, 245), width=6)
    # Tiled wall
    for y in range(40, 380, 50):
        draw.line([(0, y), (800, y)], fill=(45, 52, 68), width=2)
    for x in range(0, 800, 80):
        draw.line([(x, 0), (x, 380)], fill=(45, 52, 68), width=2)
    # Sanitizer dispenser bottle on counter
    draw.rectangle([100, 280, 160, 390], fill=(240, 245, 250), outline=(50, 120, 200), width=3)
    draw.rectangle([120, 250, 140, 280], fill=(50, 120, 200))
    draw.text((105, 320), "SAN-Q+", fill=(20, 80, 160))
    # Stainless Steel Bowl & Clean Cutting Board
    draw.rectangle([240, 420, 460, 540], fill=(230, 235, 240), outline=(120, 130, 145), width=3)
    draw.ellipse([500, 400, 680, 520], fill=(190, 200, 215), outline=(225, 235, 250), width=4)
    # Chef figure with hairnet & gloves
    draw.ellipse([340, 80, 460, 210], fill=(235, 195, 170))
    # Hairnet
    draw.arc([335, 75, 465, 170], 180, 360, fill=(70, 130, 220), width=14)
    # Clean Chef Whites
    draw.polygon([(290, 210), (510, 210), (560, 380), (240, 380)], fill=(248, 250, 252))
    # Blue Nitrile Gloves
    draw.ellipse([270, 380, 320, 430], fill=(30, 110, 230))
    draw.ellipse([480, 380, 530, 430], fill=(30, 110, 230))

    draw.rectangle([20, 20, 380, 60], fill=(16, 185, 129))
    draw.text((35, 30), "SAMPLE: Audited Commercial Kitchen (Compliant)", fill=(255, 255, 255))
    img.save("sample_data/sample_kitchen_compliant.jpg", quality=92)

# 5. Cross Contamination Hazard
def make_kitchen_hazard():
    img = Image.new("RGB", (800, 600), (32, 28, 28))
    draw = ImageDraw.Draw(img)
    # Wood cutting board
    draw.rectangle([150, 220, 650, 540], fill=(180, 120, 75), outline=(120, 80, 50), width=6)
    # Raw poultry piece directly touching board
    draw.ellipse([220, 300, 420, 460], fill=(245, 185, 180), outline=(210, 140, 135), width=4)
    draw.text((250, 360), "RAW CHICKEN", fill=(160, 60, 60))
    # Leafy salad greens touching the raw poultry juice directly
    draw.ellipse([390, 270, 520, 360], fill=(60, 170, 70))
    draw.ellipse([450, 330, 580, 420], fill=(80, 190, 80))
    draw.ellipse([380, 360, 490, 440], fill=(50, 150, 60))
    draw.text((450, 360), "READY-TO-EAT GREENS", fill=(20, 80, 20))
    # Red warning overlap zone
    draw.ellipse([370, 320, 430, 380], outline=(239, 68, 68), width=5)
    draw.line([(370, 320), (430, 380)], fill=(239, 68, 68), width=4)
    # No gloves bare hand nearby
    draw.ellipse([100, 380, 180, 460], fill=(225, 175, 150))
    draw.text((90, 480), "NO GLOVES", fill=(239, 68, 68))

    draw.rectangle([20, 20, 440, 60], fill=(239, 68, 68))
    draw.text((35, 30), "SAMPLE: Cross-Contamination & PPE Violation", fill=(255, 255, 255))
    img.save("sample_data/sample_kitchen_hazard.jpg", quality=92)

make_salmon_bowl()
make_fresh_apple()
make_spoiled_berries()
make_commercial_kitchen()
make_kitchen_hazard()
print("Sample images created successfully!")
