
from tarski.grounding.ops import classify_symbols
from tarski.syntax.util import get_symbols

from ..io.common import reader, collect_strips_benchmarks, collect_fstrips_benchmarks
from ..common import parcprinter, gripper


SAMPLE_STRIPS_INSTANCES = [
    "settlers-sat18-adl:p01.pddl",
    "visitall-sat11-strips:problem12.pddl",
    "trucks:p01.pddl",  # quantified formulas
    "blocks:probBLOCKS-4-1.pddl",
    "gripper:prob01.pddl",
    "elevators-opt08-strips:p01.pddl",  # action costs
    "sokoban-opt08-strips:p01.pddl",  # action costs
    "parking-sat11-strips:pfile08-031.pddl",  # action costs
    "transport-opt08-strips:p01.pddl",  # action costs
    "spider-sat18-strips:p01.pddl",
    "nurikabe-sat18-adl:p01.pddl"
]

SAMPLE_FSTRIPS_INSTANCES = [
    "counters-fn:instance_4.pddl",  # functions, ints
]


def pytest_generate_tests(metafunc):
    # This is called once for each test method, and allows us to pass different parameters to the test method,
    # in this case as many instances as desired, so that each instance is mapped into a different test.
    # @see http://pytest.org/latest/example/parametrize.html#parametrizing-test-methods-through-per-class-configuration
    if metafunc.function != test_symbol_classification:
        return

    argnames = ['instance_file', 'domain_file']
    argvalues = collect_strips_benchmarks(SAMPLE_STRIPS_INSTANCES) + \
        collect_fstrips_benchmarks(SAMPLE_FSTRIPS_INSTANCES)
    metafunc.parametrize(argnames, argvalues)


def test_symbol_classification(instance_file, domain_file):
    # Test the symbol classification procedure for a few standard benchmarks that we parse entirely
    problem = reader().read_problem(domain_file, instance_file)
    fluent, static = classify_symbols(problem)

    expected = {  # A compilation of the expected values for each tested domain (including total-cost terms!)
        "grid-visit-all": (2, 1),
        "Trucks": (6, 4),
        "BLOCKS": (5, 0),
        "gripper-strips": (4, 3),
        "elevators-sequencedstrips": (5, 6),
        "sokoban-sequential": (4, 3),
        "parking": (6, 0),
        "transport": (4, 3),
        "spider": (16, 6),
        "counters-fn": (1, 1),
        "settlers": (27, 23),
        "nurikabe": (9, 3),
    }
    # First make sure that the amount of expected fluent + static add up to the total number of symbols
    assert len(set(get_symbols(problem.language, include_builtin=False))) == sum(expected[problem.domain_name])
    assert (len(fluent), len(static)) == expected[problem.domain_name]


def test_symbol_classification_in_parcprinter():
    prob = parcprinter.create_small_task()
    fluent, static = classify_symbols(prob)
    assert (len(fluent), len(static)) == (4, 3)


def test_symbol_classification_in_gripper():
    prob = gripper.create_sample_problem()
    fluent, static = classify_symbols(prob)
    assert (len(fluent), len(static)) == (4, 3)

    fluent, static = classify_symbols(prob, include_builtin=True)
    assert (len(fluent), len(static)) == (4, 5)  # Same as before plus "=" and "!="


