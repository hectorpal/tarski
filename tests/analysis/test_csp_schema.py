import tempfile

from tarski.analysis.csp_schema import CSPCompiler, CSPInformation
from tarski.benchmarks.blocksworld import generate_strips_blocksworld_problem
from tarski.grounding import NaiveGroundingStrategy



def test_bw_csp():
    problem = generate_strips_blocksworld_problem()
    lang = problem.language
    clear, on, ontable, handempty, holding = lang.get('clear', 'on', 'ontable', 'handempty', 'holding')
    b1, b2 = lang.get('b1', 'b2')
    x = lang.variable('x', 'object')

    grounding = NaiveGroundingStrategy(problem, ignore_symbols={'total-cost'})
    state_variables = grounding.ground_state_variables()

    comp = CSPCompiler(problem, state_variables)
    csp = CSPInformation()
    comp.compile_expression(on(b1, b2) & clear(x), csp)
    assert len(csp.constraints) == 2 and \
        str(csp.constraints[0]) == 'StateVar(on(b1,b2)=True, reif=None)' and \
        str(csp.constraints[1]) == 'Table(<x>, ext(clear), reif=None)'

    csp = CSPInformation()
    comp.compile_expression(handempty() & ~handempty(), csp)
    assert len(csp.constraints) == 2 and \
        str(csp.constraints[0]) == 'StateVar(handempty()=True, reif=None)' and \
        str(csp.constraints[1]) == 'StateVar(handempty()=False, reif=None)'


def test_bw_csp_full():
    problem = generate_strips_blocksworld_problem()

    grounding = NaiveGroundingStrategy(problem, ignore_symbols={'total-cost'})
    state_variables = grounding.ground_state_variables()

    comp = CSPCompiler(problem, state_variables)
    with tempfile.TemporaryDirectory() as dirpath:
        _ = comp.process_problem(serialization_directory=dirpath)
