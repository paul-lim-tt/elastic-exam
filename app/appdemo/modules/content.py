from typing import Literal

from lingua import Language, LanguageDetectorBuilder

LANGUAGES = [Language.ENGLISH, Language.JAPANESE]
DETECTOR = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()
type AvailableLanguage = Literal["ja", "en"]


def detect_language(content: str) -> AvailableLanguage:
    language = DETECTOR.detect_language_of(content)
    if language == Language.JAPANESE:
        return "ja"
    return "en"


def fit_quadrilateral(polygon_vertices: list[float | int]) -> list[float | int]:

    coords = list(zip(polygon_vertices[0::2], polygon_vertices[1::2]))
    x_coords = [point[0] for point in coords]
    y_coords = [point[1] for point in coords]

    x_min = min(x_coords)
    y_min = min(y_coords)
    x_max = max(x_coords)
    y_max = max(y_coords)

    w = x_max - x_min
    h = y_max - y_min

    return [x_min, y_min, w, h]
