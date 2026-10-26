from pathlib import Path

from PIL import Image

from .metadata import Metadata


class ImageInspector:
    SUPPORTED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
        ".tiff",
    }

    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Path does not exist: {dataset_path}"
            )

    def inspect(self):
        files = Metadata.get_files(
            self.dataset_path
        )

        df = Metadata.build(
            files,
            self.SUPPORTED_EXTENSIONS
        )

        total_files = len(df)

        supported_files = df.loc[
            df["supported"],
            "file"
        ]

        unsupported_files = int(
            (~df["supported"]).sum()
        )

        valid_images = 0
        corrupt_files = 0
        formats = {}

        for file_path in supported_files:
            try:
                with Image.open(file_path) as img:
                    img.verify()

                with Image.open(file_path) as img:
                    fmt = img.format

                    formats[fmt] = (
                        formats.get(fmt, 0) + 1
                    )

                    valid_images += 1

            except Exception:
                corrupt_files += 1

        results = {
            "total_files": total_files,
            "valid_images": valid_images,
            "corrupt_files": corrupt_files,
            "unsupported_files": unsupported_files,
            "formats": formats,
        }

        print("=== Image Inspection Report ===")

        for key, value in results.items():
            print(f"{key}: {value}")

        return results
