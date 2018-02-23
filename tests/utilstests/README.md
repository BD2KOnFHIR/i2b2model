# utilstests directory
Secondary tests for the testing utilities (utils)

| File | Test | Function | Dependencies |
| ---- | ---- | -------- | -------- |
| test_base_test_case.py | test_almost_now | Test the `almostnow` and `almostequals` functions in `base_test_case.py` | (none) |
| test_crctestcase.py | test_clean_exit | Determine whether the test cases cleaned up after themselves | (none)
| | test_sourcesystem_cd | Test the sourcsystem code assignment stack | |
| | test_sourcesystem_cd_2 | Deliberate assertion failure to test cleanup on error | |
| | test_zsourcesystem_cd | Followup test for test_sourcesystem_cd_2.  Assumes that this runs last | |

## TODO:
1) Add tests for `make_and_clear_directory`