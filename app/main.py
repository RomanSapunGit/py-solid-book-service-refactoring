from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ElementTree
from typing import Any


class Serializer(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


class Printer(ABC):
    @abstractmethod
    def print(self, title: str, content: str) -> None:
        pass


class Displayer(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


# === Concrete Implementations ===

class XmlSerializer(Serializer):
    def serialize(self, title: str, content: str) -> str:
        root = ElementTree.Element("book")
        title_el = ElementTree.SubElement(root, "title")
        title_el.text = title
        content_el = ElementTree.SubElement(root, "content")
        content_el.text = content
        return ElementTree.tostring(root, encoding="unicode")


class JsonSerializer(Serializer):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class ConsolePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrinter(Printer):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class ConsoleDisplayer(Displayer):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplayer(Displayer):
    def display(self, content: str) -> None:
        print(content[::-1])


# === High-level Book Entities (Depend on Abstractions) ===

class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    def raise_value_error(self, type_: str, value: Any) -> None:
        raise ValueError(f"Unknown {type_} type: {value}")


class BookSerializer:
    def __init__(self, book: Book, serializers: dict[str, Serializer]) -> None:
        self.book = book
        self.serializers = serializers

    def serialize(self, serialize_type: str) -> str:
        serializer = self.serializers.get(serialize_type)
        if not serializer:
            self.book.raise_value_error("serialize", serialize_type)
        return serializer.serialize(self.book.title, self.book.content)


class BookPrinter:
    def __init__(self, book: Book, printers: dict[str, Printer]) -> None:
        self.book = book
        self.printers = printers

    def print_book(self, print_type: str) -> None:
        printer = self.printers.get(print_type)
        if not printer:
            self.book.raise_value_error("print", print_type)
        printer.print(self.book.title, self.book.content)


class BookDisplayer:
    def __init__(self, book: Book, displayers: dict[str, Displayer]) -> None:
        self.book = book
        self.displayers = displayers

    def display(self, display_type: str) -> None:
        displayer = self.displayers.get(display_type)
        if not displayer:
            self.book.raise_value_error("display", display_type)
        displayer.display(self.book.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None:
    serializer = BookSerializer(book, {
        "json": JsonSerializer(),
        "xml": XmlSerializer()
    })

    printer = BookPrinter(book, {
        "console": ConsolePrinter(),
        "reverse": ReversePrinter()
    })

    displayer = BookDisplayer(book, {
        "console": ConsoleDisplayer(),
        "reverse": ReverseDisplayer()
    })

    for cmd, method_type in commands:
        if cmd == "display":
            displayer.display(method_type)
        elif cmd == "print":
            printer.print_book(method_type)
        elif cmd == "serialize":
            return serializer.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
