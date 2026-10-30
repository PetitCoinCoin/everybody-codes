from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from time import time

from utils.parsers import parse_args


@dataclass
class ParticipantResult:
    pid: str
    p1: int | None = None
    p2: int | None = None
    p3: int | None = None

    @property
    def parts_done(self) -> int:
        if self.p3 is not None:
            return 3
        if self.p2 is not None:
            return 2
        return 1

    @property
    def total_time(self) -> int:
        return self.p1 + (self.p2 or 0) + (self.p3 or 0)

    def __repr__(self):
        return f"pid: {self.pid}, temps: ({self.p1}, {self.p2}, {self.p3})"


@dataclass
class Quest:
    PARTS = (1, 2, 3)

    qid: str
    results: list[ParticipantResult]
    scores: dict | None = None

    def get_score(self, pid: str) -> int:
        if self.scores is None:
            self.__build_scores()
        return sum(self.scores[part].get(pid, 0) for part in self.PARTS)

    def __build_scores(self) -> None:
        self.scores = {}
        for part in self.PARTS:
            self.scores[part] = {}
            prev_value = -1
            prev_score = -1
            for i, rank in enumerate(
                sorted(
                    [
                        (sum(getattr(result, f"p{p}") for p in range(1, part + 1)), result.pid)
                        for result in self.results
                        if getattr(result, f"p{part}") is not None
                    ]
                )
            ):
                score = prev_score if rank[0] == prev_value else max((50 * part - i), 0)
                self.scores[part][rank[1]] = score
                prev_value = rank[0]
                prev_score = score


@dataclass
class Participant:
    pid: str
    quests: list[Quest]

    @property
    def parts_done(self) -> int:
        return sum(
            result.parts_done if result.pid == self.pid else 0 for quest in self.quests for result in quest.results
        )

    @property
    def total_time(self) -> int:
        return sum(
            result.total_time if result.pid == self.pid else 0 for quest in self.quests for result in quest.results
        )

    @property
    def score(self) -> int:
        return sum(quest.get_score(self.pid) for quest in self.quests)

    def __gt__(self, other_participant: Participant) -> bool:
        if self.parts_done != other_participant.parts_done:
            return self.parts_done < other_participant.parts_done
        return self.total_time > other_participant.total_time


def parse_input(raw: str) -> None:
    pattern = r"(\d+)"
    pid, qid, part, ptime = re.findall(pattern, raw)

    if pid not in data:
        data[pid] = Participant(pid=pid, quests=[])

    quest = next((quest for quest in data[pid].quests if quest.qid == qid), None)
    if quest is None:
        quest = next(
            (quest for participant in data.values() for quest in participant.quests if quest.qid == qid),
            Quest(qid=qid, results=[]),
        )
        data[pid].quests.append(quest)
    # else:
    #     print(f"participant {pid} a déjà la quete {qid}")

    result = next((result for result in quest.results if result.pid == pid), None)
    if result is None:
        result = ParticipantResult(pid=pid)
        quest.results.append(result)
    # else:
    #     print(f"le résultat de {pid} est déjà dans la quete {qid}")

    setattr(result, f"p{part}", int(ptime))


if __name__ == "__main__":
    args = parse_args()
    t = time()
    data: dict[str, Participant] = {}
    with Path(f"{Path(__file__).parent}/inputs/{Path(__file__).stem}_{args.part}.txt").open("r") as file:
        for line in file.read().strip().split("\n"):
            parse_input(line)

    checksum = 0
    if args.part != 3:
        for i, participant in enumerate(sorted(data.values()), 1):
            checksum += i * participant.total_time
    else:
        prev_value = -1
        prev_score = -1
        for i, participant in enumerate(sorted(data.values(), key=lambda p: p.score, reverse=True), 1):
            score = prev_score if participant.score == prev_value else i
            checksum += score * participant.score
            prev_value = participant.score
            prev_score = score

    print(checksum)
    print(time() - t)
