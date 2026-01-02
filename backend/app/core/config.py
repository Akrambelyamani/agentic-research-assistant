from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    RUNS_DIR: str = "app/runs"
    USER_AGENT: str = "OSMHealthLocator/1.0 (contact: demo@example.com)"
    NOMINATIM_EMAIL: str = "demo@example.com"

    OPENMETEO_GEOCODE_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org/search"

    OVERPASS_URLS: str = (
        "https://overpass-api.de/api/interpreter,"
        "https://overpass.kumi.systems/api/interpreter,"
        "https://overpass.nchc.org.tw/api/interpreter"
    )

    GEOCODE_CACHE_TTL_S: int = 604800
    GEOCODE_TIMEOUT_S: int = 15
    GEOCODE_RETRIES: int = 2

    OVERPASS_TIMEOUT_S: int = 45
    OVERPASS_RETRIES: int = 2

settings = Settings()
