import typer
from typing import Annotated, Optional
from . import service
from .models import Status
from rich import print
from rich.table import Table

app = typer.Typer()

@app.command("add")
def add_task(description: Annotated[str, typer.Argument()]):
    service.add_task(description)

@app.command("delete")
def delete_task(task_id: Annotated[int, typer.Argument()]):
    service.delete_task(task_id)

@app.command("update")
def update_task(task_id: Annotated[int, typer.Argument()], 
            description: Annotated[Optional[str], typer.Option()] = None, 
            status: Annotated[Optional[Status], typer.Option()] = None):
    if description is None and status is None:
        print(":warning: Description or status must be provided")
        return
    service.update_task(task_id, description, status)

@app.command("list")
def list_tasks():
    table = Table(title="Tasks")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Status", justify="right", style="green")
    tasks = service.get_tasks()
    for task in tasks:
        table.add_row(str(task.id), task.description, task.status)
    print(table)

if __name__ == "__main__":
    app()