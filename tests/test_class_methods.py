from tests.utils import RE_TIME_MESSAGE, CustomClass


def test_timer_with_class_methods(capsys):
    c = CustomClass()
    c.waste_time()
    stdout, stderr = capsys.readouterr()
    assert RE_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""
