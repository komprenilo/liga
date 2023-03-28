## Developers' Guide
### Cheatsheet for mill
``` bash
## IDE
bin/mill mill.bsp.BSP/install

## liga
bin/mill 'liga[2.12].test'
bin/mill 'liga[2.12].assembly'

## image
bin/mill 'image[2.12].test'
bin/mill 'image[2.12].assembly'

## video
bin/mill 'video[2.12].test'
bin/mill 'video[2.12].test.testOnly' '**.MLImageTest.scala'
bin/mill 'video[2.12].assembly'

## format
bin/mill mill.scalalib.scalafmt.ScalafmtModule/checkFormatAll __.sources
bin/mill mill.scalalib.scalafmt.ScalafmtModule/reformatAll __.sources
```

### Cheatsheet for Pants
```
ROOTDIR=`pwd` ./pants test python/tests/liga/sklearn/codegen_test.py:../../liga@resolve=spark_3_3_1 -- -k test_sklearn_random_forest
```