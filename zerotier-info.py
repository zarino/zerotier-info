#!/usr/bin/env python3

import datetime
import os
import sys

import humanize
import requests
from rich import box
from rich.console import Console
from rich.table import Table


console = Console()


try:
    ZEROTIER_CENTRAL_TOKEN = os.environ["ZEROTIER_CENTRAL_TOKEN"]
except KeyError:
    console.print("[bold red]Error:[/bold red] ZEROTIER_CENTRAL_TOKEN environment variable not provided to zerotier-info.py")


def main():
    networks = api("/network")
    for network in networks:
        table = Table(
            title=network["config"]["name"],
            show_header=True,
            box=box.SIMPLE,
            pad_edge=False,
            title_style='bold',
            title_justify='left'
        )

        table.add_column("Name")
        table.add_column("IP")
        table.add_column("Last seen")

        members = api(f"/network/{network['id']}/member")
        rows = []

        for member in members:
            rows.append({
                "name": member["name"],
                "ip": first(member["config"]["ipAssignments"]),
                "last_seen": member['lastSeen']
            })

        rows_sorted = sorted(
            rows,
            key=sort_member,
            reverse=True
        )

        for row in rows_sorted:
            style = 'dim' if row["last_seen"] == 0 else None
            table.add_row(
                row["name"],
                row["ip"] if row["ip"] else "–",
                ago(row["last_seen"]) if row["last_seen"] else "–",
                style=style
            )

        console.print(table)


def ago(timestamp):
    t = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
    return humanize.naturaltime(t)


def api(endpoint):
    r = requests.get(
        f"https://api.zerotier.com/api/v1/{endpoint}",
        headers={
            "Authorization": f"token {ZEROTIER_CENTRAL_TOKEN}"
        }
    )
    if r.status_code == 200:
        return r.json()
    else:
        console.print("[bold red]Error:[/bold red] 403 Authorization Required")
        console.print("Is the provided ZEROTIER_CENTRAL_TOKEN valid?")
        sys.exit(3)


def first(l):
    try:
        return l[0]
    except IndexError:
        return None


def sort_member(m):
    return (
        int(m["last_seen"]) if m["last_seen"] else 0,
        m["ip"] if m["ip"] else '',
        m["name"]
    )


if __name__ == "__main__":
    main()
