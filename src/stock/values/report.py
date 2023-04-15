from src.stock.values.entry import Entry
from src.stock.values.strategy import Strategy, Sorting, Cutoff, Filter
from datetime import datetime
from prettytable import PrettyTable


class Report:
    def __init__(self, date, entries, number_of_positions=None):
        if number_of_positions is None:
            self.entries: list[Entry] = entries
        else:
            self.entries: list[Entry] = entries[:number_of_positions]

        self.date: datetime = date

    def filter_by(self, filters: list[Filter]) -> "Report":
        entries = []

        for entry in self.entries:
            check = [Filter.check_entry(entry, f) for f in filters]
            if all(check):
                entries.append(entry)

        return Report(self.date, entries)

    def sort_by(self, sorting: Sorting) -> "Report":
        entries = Sorting.sort(self.entries, sorting)
        return Report(self.date, entries)

    def cutoff(self, cutoff: Cutoff) -> "Report":
        return Report(self.date, self.entries, number_of_positions=cutoff.value)

    def run_strategy(self, strategy: Strategy) -> "Report":
        return (
            self.filter_by(strategy.filters)
            .sort_by(strategy.initial_sort)
            .cutoff(strategy.cutoff)
            .sort_by(strategy.secondary_sort)
        )

    def get(self, stock):
        for entry in self.entries:
            if entry.stock == stock:
                return entry

        return None

    def __str__(self):
        str_entries = [str(entry) for entry in self.entries]
        report = [f"Report for {self.date.isoformat()}"] + str_entries
        return "\n".join(report)

    def pretty(self):
        headers = [
            "Stock",
            "Close Price",
            "Open Price",
            "2Y Momentum",
            "1Y Momentum",
            "Accel",
            "RSI14",
            "RSI28",
            "Column",
            "Trend",
        ]
        table = PrettyTable(headers)

        for entry in self.entries:
            table.add_row(entry.to_list()[1:])

        return table
