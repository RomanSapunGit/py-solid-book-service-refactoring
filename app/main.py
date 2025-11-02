from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ElementTree


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


class XmlSerializer(Serializer):
    def serialize(self, title: str, content: str) -> str:
        root = ElementTree.Element("book")
        title_element = ElementTree.SubElement(root, "title")
        title_element.text = title
        content_element = ElementTree.SubElement(root, "content")
        content_element.text = content
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


class ReverseDisplayer(Displayer):
    def display(self, content: str) -> None:
        print(content[::-1])


class ConsoleDisplayer(Displayer):
    def display(self, content: str) -> None:
        print(content)


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.book_displayer = BookDisplayer(self)
        self.book_printer = BookPrinter(self)
        self.book_serializer = BookSerializer(self)

    def raise_value_error(self, type_element: str, value: str) -> None:
        raise ValueError(f"Unknown {type_element} type: {value}")


class BookSerializer:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.json_serializer = JsonSerializer()
        self.xml_serializer = XmlSerializer()

    def serialize(self, serialize_type: str) -> str:
        if serialize_type == "json":
            return self.json_serializer.serialize(
                self.book.title, self.book.content
            )
        elif serialize_type == "xml":
            return self.xml_serializer.serialize(
                self.book.title, self.book.content
            )
        else:
            self.book.raise_value_error("serialize", serialize_type)
            return ""


class BookPrinter:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.console_printer = ConsolePrinter()
        self.reverse_printer = ReversePrinter()

    def print_book(self, print_type: str) -> None:
        if print_type == "console":
            self.console_printer.print(self.book.title, self.book.content)
        elif print_type == "reverse":
            self.reverse_printer.print(self.book.title, self.book.content)
        else:
            self.book.raise_value_error("print", print_type)


class BookDisplayer:
    def __init__(self, book: Book) -> None:
        self.book = book
        self.console_displayer = ConsoleDisplayer()
        self.reverse_displayer = ReverseDisplayer()

    def display(self, display_type: str) -> None:
        if display_type == "console":
            self.console_displayer.display(self.book.content)
        elif display_type == "reverse":
            self.reverse_displayer.display(self.book.content)
        else:
            self.book.raise_value_error("display", display_type)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            book.book_displayer.display(method_type)
        elif cmd == "print":
            book.book_printer.print_book(method_type)
        elif cmd == "serialize":
            return book.book_serializer.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
