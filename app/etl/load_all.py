from app.config.pipeline_config import PIPELINE_TABLES
from app.etl.pipeline import Pipeline


def main():

    for filename, model in PIPELINE_TABLES:
        Pipeline.run(filename, model)


if __name__ == "__main__":
    main()