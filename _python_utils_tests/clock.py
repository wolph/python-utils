"""A fake clock for the tests and doctests of ``python_utils.time``."""

import typing

import pytest

import python_utils.time

#: The doctest that sleeps on the clock, by the name pytest gives it.
TIMEOUT_GENERATOR_DOCTEST: str = 'python_utils.time.timeout_generator'


class FakeClock:
    """
    A clock that only moves when something sleeps on it.

    ``time.sleep`` promises to sleep at least as long as requested. A busy
    machine sleeps tens of milliseconds longer, and that changes how many
    items ``timeout_generator`` yields before its timeout. On this clock the
    number of items depends on the arguments alone.

    Attributes:
        now (float): The current time in seconds.
        sleeps (list[float]): Every requested sleep, in order.
    """

    def __init__(self) -> None:
        """Start at zero without any recorded sleeps."""
        self.now: float = 0.0
        self.sleeps: list[float] = []

    def perf_counter(self) -> float:
        """Return the current time, like ``time.perf_counter``."""
        return self.now

    def sleep(self, seconds: float) -> None:
        """Record the sleep and move the clock forward, without waiting."""
        self.sleeps.append(seconds)
        self.now += seconds


@pytest.fixture
def fake_clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    """Replace the ``time`` module inside ``python_utils.time``."""
    clock: FakeClock = FakeClock()
    monkeypatch.setattr(python_utils.time, 'time', clock)
    return clock


@pytest.fixture(autouse=True)
def fake_clock_in_doctest(request: pytest.FixtureRequest) -> None:
    """Run the ``timeout_generator`` doctest on the fake clock."""
    # pytest leaves `FixtureRequest.node` without a type.
    node: pytest.Item = typing.cast(pytest.Item, request.node)
    if node.name == TIMEOUT_GENERATOR_DOCTEST:
        request.getfixturevalue('fake_clock')
