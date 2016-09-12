cd images/unopt
for i in *.svg ; do python2 /usr/bin/scour --remove-metadata --disable-embed-rasters --enable-comment-stripping --enable-id-stripping --create-groups -i $i -o ../$i ; done

