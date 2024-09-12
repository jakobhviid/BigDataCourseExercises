from utils import (
    FILENAME,
    MAPPING,
    TARGET_REGISTRY,
    get_new_image_name,
    pull_save_import,
    read_images_file,
)


def main() -> None:

    images = read_images_file(FILENAME)
    assert len(images) > 0, f"No images found in {FILENAME}"

    for image_name in images:
        try:
            if image_name.startswith(TARGET_REGISTRY):
                new_image_name = image_name
            else:
                new_image_name = get_new_image_name(**MAPPING.get(image_name))
        except Exception as e:
            print(f"ERROR: {e} - {image_name}")
        else:

            print(new_image_name)
            pull_save_import(new_image_name)
            print("\n\n")


if __name__ == "__main__":
    main()
