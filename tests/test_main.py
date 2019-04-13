from main import ChunkParser

def test_extract_chunks():
    test_string = """
<<test1>>=
asdf
@

some text

<<test2>>=
qwerty
 zxcv
@
    """
    chunks = ChunkParser(test_string)
    assert chunks.fetch_chunk("test1") == "asdf\n"
    assert chunks["test2"] == "qwerty\n zxcv\n"

def test_only_at_terminates_chunks():
    test_string = """
<<test1>>=
asdf

some text

<<test2>>=
qwerty
 zxcv
@
    """
    chunks = ChunkParser(test_string)
    assert "test1" in chunks
    assert chunks["test1"] == "asdf\n\nsome text\n\n<<test2>>=\nqwerty\n zxcv\n"
    assert "test2" not in chunks
    assert "test2" not in chunks.get_chunk_names()


def test_with_at_in_chunk():
    test_string = """
<<test1>>=
asdf@1234
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "asdf@1234\n"

def test_construct_chunk():
    test_string = """
<<test1>>=
foo
bar
@
<<test2>>=
qwerty
<<test1>>
asdfgh
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "foo\nbar\n"
    assert chunks["test2"] == "qwerty\nfoo\nbar\nasdfgh\n"

def test_construct_chunk_preserves_indent():
    test_string = """
<<test1>>=
  foo
  bar
@
<<test2>>=
qwerty
<<test1>>
asdfgh
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "  foo\n  bar\n"
    assert chunks["test2"] == "qwerty\n  foo\n  bar\nasdfgh\n"


def test_construct_chunk_adds_indent():
    test_string = """
<<test1>>=
foo
bar
@
<<test2>>=
qwerty
  <<test1>>
asdfgh
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "foo\nbar\n"
    assert chunks["test2"] == "qwerty\n  foo\n  bar\nasdfgh\n"


def test_construct_chunk_combines_indent():
    test_string = """
<<test1>>=
  foo
  bar
@
<<test2>>=
qwerty
  <<test1>>
asdfgh
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "  foo\n  bar\n"
    assert chunks["test2"] == "qwerty\n    foo\n    bar\nasdfgh\n"

def test_construct_chunk_with_multiple_children_on_line():
    test_string = """
<<test1>>=
foo
bar
@
<<test2>>=
baz
@
<<test3>>=
qwerty
<<test1>>
<<test2>>
asdfgh
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "foo\nbar\n"
    assert chunks["test2"] == "baz\n"
    assert chunks["test3"] == "qwerty\nfoo\nbar\nbaz\nasdfgh\n"

def test_circular_include():
    test_string = """
<<test1>>=
<<test2>>
foo
@
<<test2>>=
<<test1>>
bar
@
    """
    
    chunks = ChunkParser(test_string)
    try:
        chunks["test1"]
        assert False, "Should've thrown an exception"
    except RecursionError:
        pass
        
def test_append_to_chunk():
    test_string = """
<<test1>>=
foo
@
<<test2>>=
baz
@
<<test1>>=
bar
@
    """
    chunks = ChunkParser(test_string)
    assert chunks["test1"] == "foo\nbar\n"
    assert chunks["test2"] == "baz\n"

