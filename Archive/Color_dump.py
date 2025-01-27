import json

colours = {
    'BORDER': (75, 75, 75),
    'WHITE': (200, 200, 200),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (160, 160, 160),
    'RED': (175, 50, 50),
    'GREEN': (50, 130, 50),
    'LP': (175, 100, 100),
    'LG': (100, 175, 100),
    'BLUE': (100, 100, 175)
}

with open('colours.json', 'w') as json_file:
    json.dump(colours, json_file)