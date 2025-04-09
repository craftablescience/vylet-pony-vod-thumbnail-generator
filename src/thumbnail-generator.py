import os
from PIL import Image, ImageDraw, ImageFont


THUMBNAIL_TEXT_COLOR = {
    "1_original": "#6c69ee",
    "2_original": "#2fb6ca",
    "3_original": "#6066bc",
    "4_original": "#541faf",
    "5_original": "#707e52",
    "6_original": "#8b75b3",
    "7": "#a99980",
    "8": "#fe2b43",
    "9": "#a0968d",
    "10_original": "#fd179e",
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
    "2024-09-26": "6_original",
    "2024-10-03": "8",
    "2024-10-07": "7",
    "2024-10-23": "8",
    "2024-10-26": "8",
    "2024-10-29": "8",
    "2024-11-01": "8",
    "2024-11-02": "9",
    "2024-11-04": "9",
    "2024-11-07": "9",  # Lost media
    "2024-11-12": "9",
    "2024-11-16": "9",
    "2024-11-18": "9",
    "2024-11-22": "9",
    "2024-11-23": "9",
    "2024-11-25": "9",
    "2024-11-27": "9",
    "2024-11-29": "9",
    "2024-12-01 (1)": "10_original",
    "2024-12-01 (2)": "10_original",
    "2024-12-05 (1)": "10_original",
    "2024-12-05 (2)": "10_original",
    "2024-12-07": "10_original",
    "2024-12-14": "10_original",
    "2024-12-17": "10_original",
    "2024-12-22": "10_original",
    "2024-12-27 (W/ Chat)": "2024_elf_stream",
    "2024-12-27 (Original)": "2024_elf_stream",
    "2024-12-29": "10_original",
    "2025-01-04": "10_original",
    "2025-01-10": "10_original",
    "2025-01-12": "10_original",
    "2025-01-14": "10_original",
    "2025-01-17": "10_original",
    "2025-01-20": "10_original",
    "2025-01-23": "10_original",
    "2025-01-24": "10_original",
    "2025-01-27": "10_original",
    "2025-02-01": "10_original",
    "2025-02-08": "10_original",
    "2025-02-10": "10_original",
    "2025-02-13 (1)": "10_original",
    "2025-02-13 (2)": "10_original",
    "2025-02-15 (1)": "10_original",
    "2025-02-15 (2)": "10_original",
    "2025-02-18 (1)": "10_original",
    "2025-02-18 (2)": "10_original",
    "2025-02-26": "10_original",
    "2025-03-03": "10_original",
    "2025-03-08 (1)": "10_original",  # Lost media
    "2025-03-08 (2)": "10_original",  # Lost media
    "2025-03-12": "10_original",
    "2025-03-14": "10_original",
    "2025-03-16 (1)": "10_original",  # Lost media
    "2025-03-16 (2)": "10_original",
    "2025-03-16 (3)": "10_original",
    "2025-03-18": "10_original",
    "2025-03-21": "10_original",
    "2025-03-23": "10_original",
    "2025-03-26": "10_original",
    "2025-04-07 (Original)": "10_original",
    "2025-04-07 (Censored)": "10_original",
    "2025-04-08": "10_original",
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
        output_path = f"../out/{date.replace('/', '_')}.jpg"
        if os.path.exists(output_path):
            continue

        image = Image.open(input_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("../assets/Equestria.ttf", FONT_SIZE)

        draw_text_in_box(image, draw, date, font, True)

        image.save(output_path, quality="web_high")
