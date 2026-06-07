from .models import FileEntry


class IndexBuilder:
    def build_file_entry(self, path, symbols, imports):
        return FileEntry(
            file_id=str(path),
            path=str(path),
            language="python",
            lines=0,
            symbols=[s.symbol_id for s in symbols],
            imports=[i.module for i in imports]
        )