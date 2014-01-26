Lines - structured logs for humans
==================================

And oppiniotated logging library that implements the
[lines](https://github.com/zimbatm/lines) format.

STATUS: WORK IN PROGRESS
========================

Only the lines.dump() is semi-implemented. I'm having issues with the fact
that python's dict is not ordered by default preventing to keep the kwargs
order as written in the source code.



TODO
----

Make sure the encoder never throws exceptions

Add log contextes

Add logging output
Add logging adapter
