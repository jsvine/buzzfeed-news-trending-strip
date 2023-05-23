#!/usr/bin/env python
import csv
import gzip
import itertools
import typing
from dataclasses import dataclass
from operator import itemgetter


@dataclass
class Link:
    position: str
    text: str
    url: str


@dataclass
class Strip:
    timestamp_first: str
    timestamp_last: str
    links: list[Link]


def dedupe(reader: typing.Iterable[dict[str, str]]) -> tuple[list[str], list[Strip]]:
    timestamps: list[str] = []
    deduped: list[Strip] = []

    grouped = itertools.groupby(reader, key=itemgetter("timestamp"))

    for timestamp, rows in grouped:
        timestamps.append(timestamp)
        links = [Link(row["position"], row["text"], row["url"]) for row in rows]

        if len(deduped) and links == deduped[-1].links:
            deduped[-1].timestamp_last = timestamp
        else:
            deduped.append(Strip(timestamp, timestamp, links))

    return timestamps, deduped


def main() -> None:
    # Open gzipped file and dedupe
    with gzip.open("data/bfn-trending-strip-raw.tsv.gz", "rt") as f:
        reader = csv.DictReader(f, delimiter="\t")
        timestamps, deduped = dedupe(reader)

    # Write all timestamps to file
    with open("data/all-timestamps.tsv", "w") as f:
        ts_writer = csv.writer(f)
        ts_writer.writerow(["timestamp"])
        ts_writer.writerows([[x] for x in timestamps])

    # Write deduped results to file
    with open("data/bfn-trending-strip-deduped.tsv", "w") as f:
        fieldnames = ["timestamp_first", "timestamp_last", "position", "text", "url"]
        dd_writer = csv.DictWriter(f, delimiter="\t", fieldnames=fieldnames)
        dd_writer.writeheader()
        for entry in deduped:
            for link in entry.links:
                to_write = {
                    **{
                        "timestamp_first": entry.timestamp_first,
                        "timestamp_last": entry.timestamp_last,
                    },
                    **link.__dict__,
                }
                dd_writer.writerow(to_write)


if __name__ == "__main__":
    main()
