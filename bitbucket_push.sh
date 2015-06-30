archive_username=jdouglass
echo Your bitbucket password:
read -s archive_password

for repo_name in `ls -d natcap-dev*`
do
    curl -X POST --user $archive_username:$archive_password \
        https://api.bitbucket.org/1.0/repositories/ \
        -d "name=$repo_name" \
        -d "has_issues=0" \
        -d "has_wiki=0" \
        -d "is_private=0" \
        -d "description=Migrated from code.google.com/p/$repo_name"

    pushd $repo_name
    hg push ssh://hg@bitbucket.org/${archive_username}/$repo_name
    popd
done
