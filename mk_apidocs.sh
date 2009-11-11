#!/bin/sh
pydoctor -c nidaqmx.cfg --make-html --html-write-function-pages --docformat=restructuredtext
echo Applying 's/.py#L/.py#/g' to all html files to support Google Code.
perl -p -i -e 's/.py#L/.py#/g' apidocs/*.html