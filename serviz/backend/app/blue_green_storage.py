from typing import Any, Dict, Set
from multiprocessing import Value, Lock
from attrs import define, field


@define
class BGStore:
    store: dict[str, Any] = field(init=False)
    is_color_blue: str = field(init=False)
    write_lock = field(init=False)
    read_lock = field(init=False)
    updated_entries: Set = field(init=False)

    def __attrs_post_init__(self):

        self.store = {
            "blue": {},
            "green": {},
        }
        self.is_color_blue = Value("i", 1)
        self.write_lock = Lock()
        self.read_lock = Lock()
        self.updated_entries = set()

    def get_read_color(self):
        return "blue" if self.is_color_blue.value == 1 else "green"

    def get_write_color(self):
        return "green" if self.is_color_blue.value == 1 else "blue"

    def write(self, data: Dict):
        with self.write_lock:
            write_store = self.store[self.get_write_color()]

            for key in data.keys():
                if key not in self.updated_entries:
                    write_store[key] = data[key]
                    self.updated_entries.add(key)

    def rewrite(self, data: Dict):
        with self.write_lock:
            write_store = self.store[self.get_write_color()]

            for key in data.keys():
                write_store[key] = data[key]

    def fetch(self):
        with self.read_lock:
            read_store = self.store[self.get_read_color()]
            return read_store

    def switch(self):
        with self.write_lock and self.read_lock:
            self.updated_entries.clear()
            read_color = self.get_read_color()
            write_color = self.get_write_color()
            self.store[read_color] = self.store[write_color].copy()
            self.is_color_blue.value = self.is_color_blue.value * -1

    def clear(self):
        with self.write_lock:
            self.store[self.get_write_color()].clear()
            self.updated_entries.clear()

