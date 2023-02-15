from datetime import datetime

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import requests
import Crops
import api
import YDK
import image_operations


def add_link_marks(card: Image, link_markers: str, x=0, y=0) -> Image:
    path = f'assets/Link_markers/{link_markers}.png'
    art_resized = Image.open(path)
    temp_ = card.copy()
    temp_.paste(art_resized, (x, y), mask=art_resized)

    return temp_


def add_attribute(card: Image, attr: str, x: int, y: int) -> Image:
    path = f'assets/Attribute/{attr}.png'
    art_resized = Image.open(path)
    temp_ = card.copy()
    temp_.paste(art_resized, (x, y), mask=art_resized)

    return temp_


def add_level(card: Image, level: int, card_type: str) -> Image:
    if not (card_type == "xyz"):
        path = f'assets/Levels/Level{level}.png'
    else:
        path = f'assets/Ranks/Rank{level}.png'
    art_resized = Image.open(path)
    temp_ = card.copy()
    temp_.paste(art_resized, (2, 456), mask=art_resized)

    return temp_


# putting the actual art in the card base after checking the type
def art_in_card(art_resized: Image, card_type: str) -> Image:
    ## need if to check if file existe
    base = Image.open('assets/base.png')
    path = f'assets/{card_type}.png'
    card_base = Image.open(path)
    base.paste(art_resized, (9, 9))

    base.paste(card_base, (0, 0), mask=card_base)

    return base


# resizing the art of the image to 382 by 417


# draw the atk and defence of monsters
def set_text(card: Image, left_text: str, right_text: str, left_x, left_y, right_x, right_y, font_size=47,
             font="ITC Souvenir LT Light.ttf") -> Image:
    font = ImageFont.truetype(font, font_size)
    # function to make sure the text is 4 characters
    draw = ImageDraw.Draw(card)
    draw.text((left_x, left_y), left_text, (0, 0, 0), font=font)
    draw.text((right_x, right_y), right_text, (0, 0, 0), font=font)
    return card


def make_card(card_id: int) -> Image:
    card_info = api.get_card_info(card_id)
    if card_info:
        link_markers, scale, levle, attribute, ATK, DEF, card_type, image_url_cropped = card_info
    backup_url = f'https://images.ygoprodeck.com/images/cards/{card_id}.jpg'
    try:
        response = requests.get(image_url_cropped)
        response.raise_for_status()
        art = Image.open(BytesIO(response.content))

    except requests.exceptions.HTTPError as e:
        try:
            response = requests.get(backup_url)
            YDK.create_ydk_log_file(card_id, "there is no cropped art")
            response.raise_for_status()
            art = Image.open(BytesIO(response.content))

        except requests.exceptions.HTTPError as e:
            print(f"Failed to fetch image from both URLs: {e}")
            YDK.create_ydk_log_file(card_id, "there is no art")
            response = requests.get("https://images.ygoprodeck.com/images/cards_cropped/40640057.jpg")
            response.raise_for_status()
            art = Image.open(BytesIO(response.content))

    art_resized = Crops.art_resizer(art)
    temp_card = art_in_card(art_resized, card_type)

    if not (card_type == "spell" or card_type == "trap"):
        if card_type == "link":
            temp_card = set_text(temp_card, ATK, '', 52, 502, 278, 502, 47)
            temp_card = set_text(temp_card, '', DEF, 52, 502, 275, 513, 42, "Axion.ttf")
            temp_card = add_attribute(temp_card, attribute, 179, 452)
            for marker in link_markers:
                temp_card = add_link_marks(temp_card, marker)
        else:
            temp_card = set_text(temp_card, ATK, DEF, 52, 502, 236, 502, 47)
            temp_card = add_attribute(temp_card, attribute, 326, 451)
            temp_card = add_level(temp_card, levle, card_type)

    if "pendulum" in card_type:
        temp_card = set_text(temp_card, scale, scale, 10, 400, 360, 400, 24)

    return temp_card


def make_card_date(start_date,end_date):
    print(f' this is the start date {start_date} nad this is the end date {end_date}')
    numbers = api.fetch_data(start_date, end_date)

    for number in numbers:
        card_temp = make_card(number)
        image_operations.save_image_png(card_temp, number)


def reformat_date(date):
    return date.strftime('%m/%d/%Y')

