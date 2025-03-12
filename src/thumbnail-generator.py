import os
from PIL import Image, ImageDraw, ImageFont


THUMBNAIL_TEXT_COLOR = {
    "1_original": "#6c69ee",
    "2_original": "#2fb6ca",
    "3_original": "#6066bc",
    "4_original": "#541faf",
    "5_original": "#707e52",
    "6": "#fe2b43",
    "7": "#a0968d",
    "8_original": "#fd179e",
    "2024_elf_stream": "#435849",
}
STREAM_DATES = {
    "2021-09-24": "1_original",
    "2021-12-23": "1_original",
    "2022-04-24": "1_original",
    "2022-09-05": "2_original",
    "2023-07-06": "3_original",
    "2023-11-01": "4_original",
    "2024-06-06": "4_original",
    "2024-07-04": "4_original",
    "2024-07-17": "5_original",
    "2024-07-20": "5_original",
    "2024-07-26": "5_original",
    "2024-10-03": "6",
    "2024-10-23": "6",
    "2024-10-26": "6",
    "2024-10-29": "7",
    "2024-11-04": "7",
    "2024-11-12": "7",
    "2024-11-16": "7",
    "2024-11-17": "7",
    "2024-11-22": "7",
    "2024-11-23": "7",
    "2024-11-25": "7",
    "2024-11-27": "7",
    "2024-11-29": "7",
    "2024-12-01 (1)": "8_original",
    "2024-12-01 (2)": "8_original",
    "2024-12-05 (1)": "8_original",
    "2024-12-05 (2)": "8_original",
    "2024-12-07": "8_original",
    "2024-12-14": "8_original",
    "2024-12-17": "8_original",
    "2024-12-22": "8_original",
    "2024-12-27 (W/ Chat)": "2024_elf_stream",
    "2024-12-27 (Original)": "2024_elf_stream",
    "2024-12-29": "8_original",
    "2025-01-04": "8_original",
    "2025-01-10": "8_original",
    "2025-01-12": "8_original",
    "2025-01-14": "8_original",
    "2025-01-17": "8_original",
    "2025-01-20": "8_original",
    "2025-01-23": "8_original",
    "2025-01-24": "8_original",
    "2025-01-27": "8_original",
    "2025-02-01": "8_original",
    "2025-02-08": "8_original",
    "2025-02-10": "8_original",
    "2025-02-13 (1)": "8_original",
    "2025-02-13 (2)": "8_original",
    "2025-02-15 (1)": "8_original",
    "2025-02-15 (2)": "8_original",
    "2025-02-18 (1)": "8_original",
    "2025-02-18 (2)": "8_original",
    "2025-02-26": "8_original",
    "2025-03-03": "8_original",
    "2025-03-08": "8_original",
    "2025-03-12": "8_original",
}

BOX_OFFSET = 64
BOX_RADIUS = 16
BOX_OUTLINE_WIDTH = 4
TEXT_OFFSET = 24
FONT_SIZE = 110


def draw_text_in_box(i: Image, dr: ImageDraw, d: str, f: ImageFont, bottom: bool) -> None:
    text_bbox = f.getbbox(d)
    text_width, text_height = (text_bbox[2] - text_bbox[0]), (text_bbox[3] - text_bbox[1])

    position = (BOX_OFFSET, ((i.size[1] - BOX_OFFSET - text_height) if bottom else BOX_OFFSET) + (-TEXT_OFFSET if bottom else TEXT_OFFSET) * 2)

    dr.rounded_rectangle(
        xy=(position[0] - TEXT_OFFSET, position[1] - TEXT_OFFSET + (text_height / 2), position[0] + text_width + TEXT_OFFSET, position[1] + text_height + TEXT_OFFSET + (text_height / 2)),
        radius=BOX_RADIUS,
        fill="white",
        outline="black",
        width=BOX_OUTLINE_WIDTH
    )

    if '(' in d or ')' in d:
        position = (position[0], position[1] + text_height / 3)

    dr.text(
        xy=position,
        text=d,
        font=f,
        fill=THUMBNAIL_TEXT_COLOR[STREAM_DATES[d]]
    )


if __name__ == "__main__":
    os.makedirs("../out", exist_ok=True)
    for date, thumbnail in STREAM_DATES.items():
        input_path = f"../assets/{thumbnail}.jpg"
        if os.path.exists(input_path):
            continue

        image = Image.open(input_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("../assets/Equestria.ttf", FONT_SIZE)

        draw_text_in_box(image, draw, date, font, True)

        image.save(f"../out/{date.replace('/', '_')}.jpg", quality="web_high")
