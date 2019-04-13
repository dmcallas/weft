import re
import os
import sys

def file_to_string(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
    return data


def write_to_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)


class ChunkParser:
    def __init__(self, text, linesep=os.linesep):
        self._text = text
        self._extract_chunks(text)
        self._nl = linesep


    def _extract_chunks(self, input_text: str):
        in_chunk = False
        chunk_name = ''
        chunk = ''
        self.chunks = dict()
        self.deps = dict()
        matcher = re.compile(r"<<(?P<chunk_name>.*)>>=")
        include_chunk_matcher = re.compile(r"<<(?P<chunk_name>.*?)>>")
        for line in input_text.splitlines():
            if not in_chunk:
                match = matcher.match(line)
                if match:
                    in_chunk = True
                    chunk_name = match.group('chunk_name')
                    chunk = []
                    self.deps[chunk_name] = set()
            else:
                if line == '@':
                    in_chunk = False
                    self.chunks[chunk_name] = chunk
                    chunk = ''
                    chunk_name = ''
                else:
                    included_chunks = include_chunk_matcher.findall(line)
                    self.deps[chunk_name].update(included_chunks)
                    chunk.append(line)

    def get_chunk_deps(self, chunk: str):
        return self.deps[chunk]

    def get_chunk_names(self):
        return self.chunks.keys()

    def __contains__(self, item: str):
        return item in self.chunks

    def fetch_chunk_lines(self, chunk_name: str):
        chunk_lines = self.chunks.get(chunk_name,"")
        processed_lines = []
        for line in chunk_lines:
            processed = False
            for dep in self.get_chunk_deps(chunk_name):
                # Don't process if it isn't actually a chunk name:
                dep_str = f"<<{dep}>>"
                if dep_str in line and dep in self and not processed:
                    rep_chunk_lines = self.fetch_chunk_lines(dep)
                    split = line.split(dep_str)
                    for line in rep_chunk_lines:
                        processed_lines.append(line.join(split))
                    processed = True
            if not processed:
                processed_lines.append(line)
        return processed_lines


    def fetch_chunk(self, chunk_name: str):
        chunk_lines = self.fetch_chunk_lines(chunk_name)
        return self._nl.join(chunk_lines)+self._nl

    def __getitem__(self, key: str):
        return self.fetch_chunk(key)


if __name__ == '__main__':
    file_str = file_to_string(sys.argv[1])
    chunks = ChunkParser(file_str)
    for chunk in chunks.get_chunk_names():
        if chunk.startswith('file:'):
            write_to_file(chunk[5:],chunks[chunk])
