import os

def get_env(var_name: str, cast_func, default=None):
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Missing environment variable: {var_name}")
    try:
        return cast_func(value)
    except ValueError as e:
        raise ValueError(f"Error converting {var_name}: {e}")