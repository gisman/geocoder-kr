from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

JUSO_DATA_DIR = env("JUSO_DATA_DIR")
