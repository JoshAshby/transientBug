#/bin/bash
echo "Compiling all LESS files to CSS"
for file in *.less
do
  if [ $file != "base.less" ]; then
    FROM=$file
    echo "$FROM --> ../css/`basename $file`.css"
    lessc $FROM > ../css/`basename $file`.css
  fi
done
