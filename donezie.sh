# TEMPLATE_DIR="day00"

# date=$( date +%Y-%m-%d )
# current_branch=$( git branch --show-current )

if [ $date != $current_branch ];
then
    git checkout -b "$date"
fi

for i in $(ls . | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2};?)?)?[mGK]//g" | grep day); do
    > "$i/input.txt"
done

git add *
git commit -m "add today's problem"
git push origin "$date"
