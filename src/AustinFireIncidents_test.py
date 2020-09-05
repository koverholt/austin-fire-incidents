from . import AustinFireIncidents

def test_AustinFireIncidents():
    assert AustinFireIncidents.apply("Jane") == "hello Jane"
