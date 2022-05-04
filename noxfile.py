import nox

nox.options.sessions = ["test"]

@nox.session
def test(session):
    session.install("-rrequirements.txt")
    session.install("-rdev-requirements.txt")
    session.install("-e.")
    session.run("pytest")
