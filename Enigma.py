from typing import Mapping, Any


class Enigma:

    def __init__(self, id: int, name: str, description: str, answer: str, author: str, score: int, details: str):
        self.id = id
        self.name = name
        self.description = description
        self.answer = answer
        self.author = author
        self.score = score
        self.details = details
        return

    def __str__(self):
        return f"Enigma {self.id} {self.description}"

    def __repr__(self):
        return str(self)

    def get_html_enigma(self) -> str:
        """Return the HTML representation of the enigma."""
        return f"<b>{self.name}</b> {self.score} points\n{self.description}\n"

    def get_html_answer(self) -> str:
        """Return the HTML representation of the answer."""
        return f"<b>{self.name}</b> {self.score} points\n{self.description}\n<u>Answer: </u>\n{self.answer}\n<i>Details</i>{self.details}\n"

    def answer_is_correct(self, answer: str) -> bool:
        """Return True if the answer is correct."""
        return self.answer == answer

    def get_id(self) -> int:
        """Return the id of the enigma."""
        return self.id

    @classmethod
    def from_dict(cls, enigma_dict: Mapping[str, Any]) -> "Enigma":
        """Return an Enigma from a dict."""
        return cls(
            id=enigma_dict["id"],
            name=enigma_dict["name"],
            description=enigma_dict["description"],
            answer=enigma_dict["answer"],
            author=enigma_dict["author"],
            score=enigma_dict["score"],
            details=enigma_dict["details"],
        )

    def to_dict(self) -> Mapping[str, Any]:
        """Return a dict from the Enigma."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "answer": self.answer,
            "author": self.author,
            "score": self.score,
            "details": self.details,
        }

    @staticmethod
    def from_str(text: str):
        """Return an Enigma from a string."""
        enigma_dict = {}
        for line in text.splitlines()[1:]:
            key, value = line.split(": ")
            enigma_dict[key] = value
        try:
            enigma_dict["id"] = int(enigma_dict["id"])
            enigma_dict["score"] = int(enigma_dict["score"])
        except ValueError:
            print("The value and the score must be integers\n" + text)
            return None
        try:
            enigma = Enigma.from_dict(enigma_dict)
            return enigma
        except KeyError:
            print("Error while parsing the enigma\n" + text)
            return None
