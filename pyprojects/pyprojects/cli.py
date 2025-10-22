import random
import sys
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.prompt import Prompt

app = typer.Typer(add_completion=False, help="Python mini-projects CLI")


@app.command()
def quote(tag: Optional[str] = typer.Option(None, help="Filter by tag")):
    """Fetch and display a random quote from Quotable API."""
    try:
        import requests
    except Exception as exc:
        print(f"[red]requests not installed: {exc}")
        raise typer.Exit(1)

    url = "https://api.quotable.io/random"
    params = {"tags": tag} if tag else None
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        content = data.get("content")
        author = data.get("author")
        print(f"\n[bold cyan]\"{content}\"[/] — [green]{author}[/]\n")
    except Exception as exc:
        print(f"[red]Failed to fetch quote: {exc}")
        raise typer.Exit(1)


@app.command()
def guess(low: int = 1, high: int = 100, attempts: int = 7):
    """Number guessing game in the terminal."""
    if low >= high:
        print("[red]low must be < high")
        raise typer.Exit(1)

    secret = random.randint(low, high)
    print(f"Guess a number between {low} and {high}. You have {attempts} attempts.")
    for turn in range(1, attempts + 1):
        raw = Prompt.ask(f"Attempt {turn}")
        try:
            n = int(raw)
        except ValueError:
            print("[yellow]Please enter an integer.")
            continue
        if n == secret:
            print(f"[bold green]Correct![/] The number was {secret}.")
            return
        hint = "higher" if n < secret else "lower"
        print(f"[cyan]Try {hint}.")
    print(f"[red]Out of attempts! The number was {secret}.")


@app.command()
def dice(count: int = 2, sides: int = 6, rolls: int = 1):
    """Roll dice and show totals."""
    if count < 1 or sides < 2 or rolls < 1:
        print("[red]count>=1, sides>=2, rolls>=1 required")
        raise typer.Exit(1)
    totals = []
    for _ in range(rolls):
        result = [random.randint(1, sides) for _ in range(count)]
        total = sum(result)
        totals.append(total)
        print(f"Roll: {result} -> total {total}")
    if rolls > 1:
        avg = sum(totals) / len(totals)
        print(f"Average total over {rolls} rolls: [bold]{avg:.2f}[/]")


@app.command()
def ytdl(url: str = typer.Argument(..., help="Video URL"),
         audio_only: bool = typer.Option(False, help="Download audio only"),
         out: Optional[Path] = typer.Option(None, help="Output directory")):
    """Download a video or audio via yt-dlp."""
    try:
        import yt_dlp as ytdlp
    except Exception as exc:
        print(f"[red]yt-dlp not installed: {exc}")
        raise typer.Exit(1)

    outdir = Path(out) if out else Path.cwd()
    outdir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'outtmpl': str(outdir / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'nocheckcertificate': True,
        'restrictfilenames': True,
    }
    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    try:
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as exc:
        print(f"[red]Download failed: {exc}")
        raise typer.Exit(1)


@app.callback()
def main():
    """Commands: quote, guess, dice, ytdl"""
    return
