#
# Makefile
#
# CSC309 Assignment 2
#
# There is only 1 command, which deletes all
# files that you should not submit, except
# for the virtual environment (venv).
#

.PHONY: clean
clean:
	del /s /q db.sqlite3
	for /r %%x in (__pycache__) do (rmdir /s /q "%%x")
	del /s /q */migrations/0*.py
	del /s /q *.pyc

