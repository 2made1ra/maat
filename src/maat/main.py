import argparse
from maat.tui import MaatApp

def main():
    parser = argparse.ArgumentParser(description="Maat - TUI for tracking media reviews")
    parser.add_argument("--db", type=str, default="sqlite:///maat.db", help="Database URL")
    args = parser.parse_args()

    app = MaatApp(db_url=args.db)
    app.run()

if __name__ == "__main__":
    main()
