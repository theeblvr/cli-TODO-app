import typer
from services import add_service, delete_service, reset_service, update_service, complete_service, show_service

app = typer.Typer()

@app.command(short_help='Adds a new item to list')
def add(task: str, category: str):
    add_service(task, category)

@app.command(short_help='Removes item from list')
def delete(position: int):
    delete_service(position)

@app.command(short_help='Edits item details')
def update(position: int, task: str, category: str):
    update_service(position, task, category)

@app.command(short_help='Marks item as completed')
def complete(position: int):
    complete_service(position)

@app.command(short_help='Clears all todo items')
def reset():
    reset_service()

@app.command(short_help='Displays all TODOS')
def show():
    show_service()