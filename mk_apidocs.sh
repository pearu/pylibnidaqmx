#!/bin/sh

# Execute the following commands in apidocs/ when
# new documentation files are added to the svn repository:
#svn propset svn:mime-type text/css *.css
#svn propset svn:mime-type text/html *.html
#svn propset svn:mime-type image/png *.png
#svn propset svn:mime-type text/javascript *.js

#rm apidocs/.buildinfo # full rebuild
cd doc && make html
cd -
cd apidocs 
svn propset svn:mime-type text/html *.html */*.html > /dev/null
svn propset svn:mime-type text/css *.css */*.css > /dev/null
svn propset svn:mime-type text/javascript *.js */*.js > /dev/null
svn propset svn:mime-type image/png *.png */*.png > /dev/null
cd -
#echo Applying 's/.py#L/.py#/g' to all html files to support Google Code.
#perl -p -i -e 's/.py#L/.py#/g' apidocs/*.html