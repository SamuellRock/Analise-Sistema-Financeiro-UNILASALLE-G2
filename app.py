"""Streamlit entrypoint for the financial analysis dashboard."""

from views.layout.dashboard import render_dashboard
from views.layout.theme import apply_theme, configure_page


def main() -> None:
    configure_page()
    apply_theme()
    render_dashboard()


if __name__ == "__main__":
    main()
