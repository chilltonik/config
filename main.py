from env_loader import EnvLoader

# ───────────────────────────────────────────────────────────────
# Main Entrypoint
# ───────────────────────────────────────────────────────────────


def main() -> None:
    """
    Example usage of the EnvLoader.
    """
    config = EnvLoader(".env")

    print(f"App Name: {config.APP_NAME}")
    print(f"Secret Key: {config.SECRET_KEY}")


# python3 main.py
if __name__ == "__main__":
    main()
