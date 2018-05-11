=======
History
=======

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
