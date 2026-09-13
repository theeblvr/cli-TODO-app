import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from models import Todo
from database import insert_todo, get_all_todos, delete_todo, reset_todos, update_todo, complete_todo

console = Console()

def add_service(task: str, category: str):
    typer.echo(f"Adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show_service()

def delete_service(position: int):
    typer.echo(f"Deleting {position}")
    delete_todo(position - 1)
    show_service()

def reset_service():
    typer.echo("Resetting todo list")
    reset_todos()
    show_service()

def update_service(position: int, task: str, category: str = None):
    typer.echo(f"Updating {position}")
    update_todo(position - 1, task, category)
    show_service()

def complete_service(position: int):
    typer.echo(f"Complete {position}")
    complete_todo(position - 1)
    show_service()

def show_service():
    tasks = get_all_todos()
    console.print("[bold cyan]   ==========  ╔══════════════════════════════╗  ========== [/bold cyan]")
    console.print("[bold cyan]               ║           TODO APP           ║[/bold cyan]")
    console.print("[bold cyan]   ==========  ╚══════════════════════════════╝  ==========[/bold cyan]")

    table = Table(
        header_style="bold white on blue",
        show_lines=True
    )
    table.add_column('#', style='dim', width=6)
    table.add_column('TODO', min_width=20)
    table.add_column('CATEGORY', min_width=12, justify='center')
    table.add_column('STATUS', min_width=6, justify='center')
    
    def get_category_color(category):
        COLORS = {'Coding': 'magenta', 'Shop': 'green', 'Reading': 'yellow'}
        if category in COLORS:
            return COLORS[category]
        return 'white'
    
    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        if task.status == 2:
            status = '✅'  
        else:
            status = '▢'
        table.add_row(str(idx), 
                      task.task, 
                      f'[{c}]{task.category}[/{c}]', 
                      status,)
    console.print(Panel.fit(table, border_style="cyan"))