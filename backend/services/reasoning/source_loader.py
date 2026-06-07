from pathlib import Path


class SourceLoader:

    def get_source(
        self,
        file_path: str,
        start_line: int,
        end_line: int
    ):

        path = Path(file_path)

        if not path.exists():
            return ""

        lines = path.read_text(
            encoding="utf-8",
            errors="ignore"
        ).splitlines()

        return "\n".join(
            lines[start_line - 1:end_line]
        )