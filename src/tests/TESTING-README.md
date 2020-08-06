# Notes on Testing
This is where anything noteworthy about our tests will be recorded.

### Unit Test Mocking
We use the [Pymox](https://pymox.readthedocs.io/en/latest/) library for creating mocks during unit tests.  The
top-level library object is accessible via the `mox` fixture for unit tests.

With Pymox, one first creates the necessary mock objects or functions, which start off in _record mode,_ where all
calls are saved to provide the "script" of expected inputs and responses.  Once this is done, calling `mox.ReplayAll()`
puts the mocks into _replay mode,_ where the desired responses are returned in response to the inputs. Pymox will detect
if the mocked calls are made "out of order," or if too many calls are made.  At the end of the test, `mox.VerifyAll()`
is used to validate that all expected mock calls were, in fact, made.

**Example:**

```python
def test_sample_mock(mox):
    system_under_test = TargetObject()
    mox.StubOutWithMock(system_under_test, 'get_name')
    system_under_test.get_name().AndReturn("Penelope")
    mox.ReplayAll()
    assert system_under_test.get_name() == "Penelope"
    mox.VerifyAll()
```

Pymox has many capabilities beyond this: consult [the documentation](https://pymox.readthedocs.io/en/latest/)
for more details.

