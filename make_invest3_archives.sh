
archive_dir=`pwd`/invest3-archives
mkdir $archive_dir

REPODIR=../../invest-natcap.invest-3
pushd $REPODIR

echo `pwd`

hg pull
for tag in `hg tags | egrep -o '^[^ ]+'`
do
    hg update -C -r $tag
    rm -r build
    python setup.py sdist --dist-dir $archive_dir
    hg archive $archive_dir/invest-natcap.invest-3-${tag}.zip
done


popd
