# Maat

Maat is a minimalist Terminal User Interface (TUI) application for your personal, local library of ratings and reviews for media content (movies, series, anime, books, games, music, etc.). It keeps everything stored locally in a SQLite database.

## Installation & Running (macOS / Linux)

Maat uses [`uv`](https://github.com/astral-sh/uv) for fast dependency management.

1. **Install `uv`** (if you haven't already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd maat
   ```

3. **Set up the database**:
   Before running the app for the first time, you need to apply the database migrations. This creates the local `maat.db` file.
   ```bash
   uv run alembic upgrade head
   ```

4. **Run the TUI**:
   ```bash
   uv run maat
   ```

### Shortcuts
- **`a`**: Add a new review
- **`d`**: Delete the selected review
- **`q`**: Quit the application

## Uninstallation / Cleanup

Since everything runs locally within the `uv` environment and saves data to a local file, uninstalling is completely safe and leaves no trace on your system.

1. **Delete the database** (this will permanently erase all your reviews!):
   ```bash
   rm maat.db
   ```

2. **Delete the project folder**:
   ```bash
   cd ..
   rm -rf maat
   ```

If you also want to remove the global `uv` caches (optional):
```bash
uv cache clean
```
