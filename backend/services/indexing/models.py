from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FileEntry:
    file_id: str
    path: str
    language: str
    lines: int

    symbols: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)


@dataclass
class SymbolEntry:
    symbol_id: str
    name: str
    type: str  # function | class | method | variable

    file: str

    start_line: int
    end_line: int

    parent: Optional[str] = None

    calls: List[str] = field(default_factory=list)
    referenced_vars: List[str] = field(default_factory=list)


@dataclass
class ImportEntry:
    file: str
    module: str
    alias: Optional[str]
    type: str  # stdlib | third_party | local