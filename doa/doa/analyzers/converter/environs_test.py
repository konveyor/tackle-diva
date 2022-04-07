"experiment on environs"
from environs import Env

if __name__ == "__main__":
    env = Env(expand_vars=True)
    env.read_env()
    print(env)
    print(env("FOO"))  # checks if variables in .env can be read
    print(env("BAR"))  # checks if variables in .env can be read
    print(env("BAZ"))  # checks if variables in .env can be read
    print(env("HOSTNAME"))  # checks if environment variables can be read
    print(env.int("SHLVL"))  # checks if int-conversion works
