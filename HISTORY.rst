=======
History
=======

0.3.0 (2023-11-27)
-------------------

* Removed travis-ci integration and replaced it with GitHub Actions
* Update of supported Python versions: dropped EOL'd Python 3.5 and 3.6 and added Python 3.9, 3.10, 3.11 and 3.12

0.2.0 (2020-07-04)
-------------------

* Update supported Python versions: drop Python 3.4 and added Python 3.8
* zkpytb.pandas: describe_numeric_1d(series): handle case where input series is empty

0.1.1 (2019-08-29)
-------------------

* setup.py: add 'Programming Language :: Python :: 3.7' trove classifier

0.1.0 (2019-08-29)
-------------------

* zkpytb.dicts: Add dict_value_map()
* zkpytb.pandas: add describe_numeric_1d(series)
* Add py 3.7 to tox.ini and .travis.yml

0.0.10 (2018-05-30)
-------------------

* Add AutoDict and AutoOrderedDict classes in zkpytb.dicts
* zkpytb.dicts.hashdict and JsonEncoder: normalize path separator to ensure stable representation and hash for windows and linux.
* Fix tests test_compare_df_cols_*() to reach 100% coverage.

0.0.9 (2018-05-11)
------------------

* Add module zkpytb.json with a custom JSONEncoder class, and use it in hashdict().

0.0.8 (2018-05-11)
------------------

* Add tests for zkpytb.logging

0.0.7 (2018-05-11)
------------------

* zkpytb.dicts: add hashdict() helper.

0.0.6 (2018-04-17)
------------------

* zkpytb.pandas: only try to import statsmodels when using mad()
* Minor changes missed while relasing previous version.

0.0.5 (2018-04-17)
------------------

* Add an implementation of PriorityQueue based on heapqueue in zkpytb.priorityqueue
* Add mad(c) (median absolute deviation) and percentile(q) functions in zkpytb.pandas
* Add code coverage and coveralls
* Add tests for zkpytb.pandas
* Fix requirements_dev.txt because pandas>=0.21 is not compatible with py34

0.0.4 (2017-06-27)
------------------

* zkpytb.utils: add hashstring() and get_git_hash() helpers.
* Add tests for zkpytb.dicts and zkpytb.utils modules.

0.0.3 (2017-06-23)
------------------

* Add first version of zkpytb.logging module with function setup_simple_console_and_file_logger().

0.0.2 (2017-06-22)
------------------

* Disable universal wheel.

0.0.1 (2017-06-22)
------------------

* First release on PyPI.
