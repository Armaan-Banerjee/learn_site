from dataclasses import dataclass
import sqlite3
from datetime import datetime
from abc import ABC, abstractmethod
import contextlib

@dataclass
class Page:
    id: str
    title: str
    data: str
    tags: [str]

class Repository[T](ABC):
    @abstractmethod
    def get(self, id: str) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    def create(self):
        raise NotImplementedError

class PageRepository(Repository[Page]):
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    @contextlib.contextmanager
    def connect(self):
        with sqlite3.connect(self.db_path) as conn:
            yield conn.cursor()

    def create_table(self) -> None:
        with self.connect() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS page (id TEXT PRIMARY KEY, title TEXT, data TEXT)"
            )
            
