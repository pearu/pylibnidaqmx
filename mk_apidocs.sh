#!/bin/sh

# Execute the following commands in apidocs/ when
# new documentation files are added to the svn repository:
#svn propset svn:mime-type text/css *.css
#svn propset svn:mime-type text/html *.html
#svn propset svn:mime-type image/png *.png
#svn propset svn:mime-type text/javascript *.js

#rm -rf apidocs/.buildinfo doc/_build doc/source/generated # full rebuild
cd doc && make html || exit 1
cd -
cd apidocs 
svn propset svn:mime-type text/html *.html */*.html > /dev/null || exit 1
svn propset svn:mime-type text/css  */*.css > /dev/null || exit 1
svn propset svn:mime-type text/javascript *.js */*.js > /dev/null || exit 1
svn propset svn:mime-type image/png  */*.png > /dev/null || exit 1
cd -
#echo Applying 's/.py#L/.py#/g' to all html files to support Google Code.
#perl -p -i -e 's/.py#L/.py#/g' apidocs/*.html