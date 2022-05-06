import nox

nox.options.sessions = ["test"]

@nox.session(reuse_venv=True)
def test(session):
    session.install("-rrequirements.txt")
    session.install("-rdev-requirements.txt")
    #session.install(".")
    session.install(".")
    session.run("pytest")
