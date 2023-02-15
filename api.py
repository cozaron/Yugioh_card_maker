import os
import pickle

import pandas as pd
import requests

import YDK


# yu gi oh data base api call
def add_spaces(text, limit):
    return text.rjust(limit, " ")


def get_card_info(card_id):
    cache_folder = "card_info_cache"

    # Create the cache folder if it doesn't exist
    if not os.path.exists(cache_folder):
        os.makedirs(cache_folder)

    cache_file = os.path.join(cache_folder, f"{card_id}.pkl")

    # Check if the information for the card is already in the cache
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)

    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card_id}"
    response = requests.get(url)
    card_info = response.json()
    atk = ''
    def_ = ''
    level = 0
    attribute = ''
    scale = ''
    link_markers = []
    if "data" in card_info:
        card = card_info["data"][0]
        type_ = card["frameType"]
        if type_ == "skill":
            return \
                [''], 1, 1, "DIVINE", " err", " err", "token", "https://images.ygoprodeck.com/images/cards_cropped" \
                                                                  "/40640057.jpg "
        image_url_cropped = card["card_images"][0]["image_url_cropped"]
        if not (type_ == "spell" or type_ == "trap"):

            atk = add_spaces(str(card["atk"]), 4)
            if type_ == "link":

                def_ = str(card["linkval"])
                link_markers = card["linkmarkers"]

            else:
                def_ = add_spaces(str(card["def"]), 4)
                level = card["level"]

            attribute = card["attribute"]

            if "pendulum" in type_:
                scale = add_spaces(str(card["scale"]), 2)

        # Save the information to the cache
        with open(cache_file, "wb") as f:
            pickle.dump((link_markers, scale, level, attribute, atk, def_, type_, image_url_cropped), f)

        # those returnes are hundled by make_card
        return link_markers, scale, level, attribute, atk, def_, type_, image_url_cropped
    else:
        print(f'no response from the server for the card: {card_id} not found.')
        YDK.create_ydk_log_file(card_id, "The card does not exist in the server")
        return [
                   ''], 1, 1, "DIVINE", " err", " err", "token", "https://images.ygoprodeck.com/images/cards_cropped" \
                                                                 "/40640057.jpg "


def get_ids(df):
    ids = [row['data']['id'] for index, row in df.iterrows()]
    return pd.DataFrame({'id': ids})


def fetch_data(start_date, end_date):
    cache_file_path = "cache/cards_id_{}_{}.pkl".format(start_date, end_date)

    if os.path.exists(cache_file_path):
        with open(cache_file_path, "rb") as cache_file:
            cards_id = pickle.load(cache_file)
        return cards_id
    else:
        try:
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
            params = {"startdate": start_date, "enddate": end_date}
            response = requests.get(f'https://db.ygoprodeck.com/api/v7/cardinfo.php?startdate={start_date}&enddate={end_date}')
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            cards_id = get_ids(df)['id'].tolist()

            os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)
            with open(cache_file_path, "wb") as cache_file:
                pickle.dump(cards_id, cache_file)

            return cards_id
        except Exception as e:
            print("Error while fetching data: {}".format(e))
