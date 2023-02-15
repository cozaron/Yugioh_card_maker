import os


def save_image_jpeg(card, number, folder='Anime_cards'):
    try:
        os.makedirs(folder, mode=0o777, exist_ok=True)
        filename = str(number) + ".jpeg"
        filepath = os.path.join(folder, filename)
        card_rgb = card.convert("RGB")
        card_rgb.save(filepath, "JPEG")
        print(f"Image saved as '{filepath}' successfully.")
    except Exception as e:
        print(f"Error saving image: {e}")


def save_image_png(card, number, folder='Anime_cards'):
    try:
        os.makedirs(folder, mode=0o777, exist_ok=True)
        filename = str(number) + ".png"
        filepath = os.path.join(folder, filename)
        card.save(filepath, "PNG")
        print(f"Image saved as '{filepath}' successfully.")
    except Exception as e:
        print(f"Error saving image: {e}")
