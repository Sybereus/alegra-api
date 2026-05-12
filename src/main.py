from src.gui.app import AlegraApp
from src.utils.logger import setup_logger


def main():
    setup_logger()
    app = AlegraApp()
    app.mainloop()


if __name__ == "__main__":
    main()
