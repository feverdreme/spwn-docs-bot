from git import Repo
import os
from src.Entry import Entry
from dotenv import load_dotenv

load_dotenv()
DOCS_URL = os.getenv('DOCS_URL')

class Collector:
    def __init__(self):
        self._clone_repo()
        self._collect_builtins()

    def _clone_repo(self):
        if not os.path.isdir("data/docs/.git"):
            Repo.clone_from(
                "https://github.com/Spu7Nix/spwn_docs.git", "data/docs")
            print("Successfully cloned repository")

        else:
            Repo("data/docs").remotes.origin.pull()
            print("Successfully updated repository")

    def _collect_builtins(self):
        with open("data/docs/builtins.md", 'r') as f:
            lines: list[str] = f.readlines()[1:]  # trims off the title

        entries: list[Entry] = []

        current_entry: Entry
        first: bool = True
        for index, line in enumerate(lines):
            if line.startswith('##'):
                if not first:
                    entries.append(current_entry)
                else:
                    first = False

                current_entry = Entry.new()
                current_entry.title = line.lstrip('## $.').rstrip('\n')
                current_entry.url = DOCS_URL + 'builtins/?id=%s' % line.lstrip('## $.').rstrip('\n')
                current_entry.prefix = '$'

            else:
                current_entry.lines.append(line)

        self.builtins = entries
