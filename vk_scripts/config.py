from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["./configs/settings.yaml"],
    environments=True,
    load_dotenv=False,
)
