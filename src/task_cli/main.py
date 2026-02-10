import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def hello(name: Annotated[str, typer.Option()] = "penis"):
    print(f"Hello {name}")

if __name__ == "__main__":
    app()