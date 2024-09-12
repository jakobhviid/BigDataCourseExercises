from utils import (
    FILENAME,
    MAPPING,
    TARGET_REGISTRY,
    get_new_image_name,
    pull_tag_push,
    read_images_file,
)


def main() -> None:

    images = read_images_file(FILENAME)
    assert len(images) > 0, f"No images found in {FILENAME}"

    for image_name in images:
        if image_name.startswith(TARGET_REGISTRY):
            continue
        try:
            new_image_name = get_new_image_name(**MAPPING.get(image_name))
        except Exception as e:
            print(f"ERROR: {e} - {image_name}")

        else:
            print(image_name, new_image_name)
            pull_tag_push(image_name, new_image_name)
            print("\n\n")


if __name__ == "__main__":
    main()
