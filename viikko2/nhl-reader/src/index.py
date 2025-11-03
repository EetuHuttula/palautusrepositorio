from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    console = Console()

    season = input("Anna kausi (esim. 2024-25): ")
    nationality = input("Anna kansalaisuus (esim. FIN): ").upper()

    reader = PlayerReader(season)
    players = reader.get_players()
    stats = PlayerStats(players)

    top_players = stats.top_scorers_by_nationality(nationality)

    table = Table(title=f"Pelaajat ({nationality}) kaudella {season})")

    table.add_column("Nimi", justify="left", style="cyan", no_wrap=True)
    table.add_column("Joukkue", justify="center")
    table.add_column("Maalit", justify="right")
    table.add_column("Syötöt", justify="right")
    table.add_column("Pisteet", justify="right")

    for p in top_players:
        table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(p.points()))

    console.print(table)

if __name__ == "__main__":
    main()
