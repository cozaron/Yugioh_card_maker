from PIL import Image


def check_and_crop(art: Image) -> Image:
    def within_tolerance(ratio1, ratio2, tolerance=0.05):
        return abs(ratio1 - ratio2) <= tolerance

    original_width, original_height = 712, 908
    original_ratio = original_width / original_height
    width, height = art.size
    current_ratio = width / height

    if within_tolerance(current_ratio, original_ratio):
        cropped_height = int(height * 0.35)
        return art.crop((0, 0, width, height - cropped_height))

    original_width, original_height = 712, 528
    original_ratio = original_width / original_height
    if within_tolerance(current_ratio, original_ratio):
        cropped_width = int(width * 0.1264)
        return art.crop((cropped_width, 0, width - cropped_width, height))

    original_width, original_height = 801, 1176
    original_ratio = original_width / original_height
    if within_tolerance(current_ratio, original_ratio):
        cropped_width = int(width * 0.1211)
        cropped_height = int(height * 0.1853)
        return art.crop((cropped_width, cropped_height, width - cropped_width, height - int(height * 0.2933)))

    return art


def art_resizer(art: Image) -> Image:
    art = check_and_crop(art)
    art_resized = art.resize((382, 417))
    return art_resized
