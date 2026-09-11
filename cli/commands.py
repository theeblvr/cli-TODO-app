import typer
from rich.console import Console
from rich.table import Table

from models import Todo

console = Console()
app = typer.Typer()

@app.command(short_help='Adds a new item to list')
def add(task: str, category: str):
    typer.echo(f"Adding {task}, {category}")
    todo = Todo(task, category)
    show()

@app.command(short_help='Removes item from list')
def delete(position: int):
    typer.echo(f"Deleting {position}")
    show()

@app.command(short_help='Edits item details')
def update(position: int, task: str, category: str = None):
    typer.echo(f"Updating {position}")
    show()

@app.command(short_help='Marks item as completed')
def complete(position: int):
    typer.echo(f"Complete {position}")
    show()

@app.command()
def show():
    tasks = [{"task": "Todo1", "category": "Coding", "done": False},
    {"task": "Todo2", "category": "Reading", "done": False}]
    console.print("[bold magenta]Todos[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column('#', style='dim', width=6)
    table.add_column('TODO', min_width=20)
    table.add_column('CATEGORY', min_width=12, justify='right')
    table.add_column('STATUS', min_width=12, justify='right')
    
    def get_category_color(category):
        COLORS = {'Coding': 'red', 'Shop': 'green', 'Reading': 'cyan'}
        if category in COLORS:
            return COLORS[category]
        return 'white'
    
    for idx, task in enumerate(tasks, start=1):
        category = task["category"]
        c = get_category_color(category)
        status = '✅' if True == 2 else '⏳'
        table.add_row(str(idx), 
                      task["task"], 
                      f'[{c}]{category}[/{c}]', 
                      status,)
    console.print(table)