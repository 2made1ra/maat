from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import DataTable, Footer, Header, Input, Select, Button, Label, Static

from maat.models import CategoryEnum
from maat.repository import ReviewRepository

class ReviewInputForm(Container):
    """Form to add a new review."""

    def compose(self) -> ComposeResult:
        yield Label("Title")
        yield Input(placeholder="Title of the media", id="input-title")

        yield Label("Category")
        yield Select(
            ((cat.value, cat) for cat in CategoryEnum),
            prompt="Select Category",
            id="select-category",
        )

        yield Label("Score (1-10)")
        yield Input(placeholder="Score", id="input-score", type="integer")

        yield Label("Review (Optional)")
        yield Input(placeholder="Review text", id="input-text")

        with Horizontal():
            yield Button("Save", id="btn-save", variant="success")
            yield Button("Cancel", id="btn-cancel", variant="error")


class MaatApp(App):
    """Maat TUI Application."""

    CSS = """
    MaatApp {
        background: $surface;
    }

    DataTable {
        height: 1fr;
        border: solid $accent;
        margin: 1;
    }

    ReviewInputForm {
        width: 60;
        height: auto;
        border: solid $accent;
        padding: 1 2;
        margin: 2;
        background: $panel;
        align: center middle;
    }

    ReviewInputForm > Label {
        margin-top: 1;
    }

    ReviewInputForm Horizontal {
        margin-top: 2;
        align: center middle;
        height: auto;
    }

    ReviewInputForm Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_review", "Add Review"),
        ("d", "delete_review", "Delete Review"),
    ]

    def __init__(self, db_url: str = "sqlite:///maat.db", **kwargs):
        super().__init__(**kwargs)
        self.engine = create_engine(db_url)
        self.session = Session(self.engine)
        self.repo = ReviewRepository(self.session)
        self.showing_form = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield DataTable(id="reviews-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Title", "Category", "Score", "Date")
        table.cursor_type = "row"
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        reviews = self.repo.get_all()
        for r in reviews:
            table.add_row(
                str(r.id),
                r.title,
                r.category.value if hasattr(r.category, "value") else str(r.category),
                str(r.score),
                r.created_at.strftime("%Y-%m-%d"),
                key=str(r.id),
            )

    def action_add_review(self) -> None:
        if not self.showing_form:
            self.mount(ReviewInputForm())
            self.showing_form = True

    def action_delete_review(self) -> None:
        table = self.query_one(DataTable)
        if table.row_count == 0:
            return

        row_key = table.coordinate_to_cell_key(table.cursor_coordinate)
        if row_key and row_key.row_key.value:
            review_id = int(row_key.row_key.value)
            self.repo.delete(review_id)
            self.refresh_table()

    @on(Button.Pressed, "#btn-cancel")
    def cancel_add(self) -> None:
        form = self.query_one(ReviewInputForm)
        form.remove()
        self.showing_form = False

    @on(Button.Pressed, "#btn-save")
    def save_review(self) -> None:
        form = self.query_one(ReviewInputForm)

        title_input = form.query_one("#input-title", Input)
        category_select = form.query_one("#select-category", Select)
        score_input = form.query_one("#input-score", Input)
        text_input = form.query_one("#input-text", Input)

        title = title_input.value
        category_val = category_select.value
        score_val = score_input.value
        text = text_input.value

        if not title or not score_val or category_val == Select.BLANK:
            self.notify("Title, Category and Score are required!", severity="error")
            return

        try:
            score = int(score_val)
            if score < 1 or score > 10:
                raise ValueError
        except ValueError:
            self.notify("Score must be an integer between 1 and 10", severity="error")
            return

        self.repo.add(
            title=title,
            category=category_val,
            score=score,
            text=text if text else None
        )

        form.remove()
        self.showing_form = False
        self.refresh_table()
        self.notify("Review added successfully!")
