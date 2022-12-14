TEMPLATE_DIR="day00"

day=$( date +%d )
dir_name="day$day"
script_name="solve$day.py"

if [ ! -d "./$dir_name" ] 
then
    cp -r "$TEMPLATE_DIR" "$dir_name"
    gsed -i "s/$TEMPLATE_DIR/$dir_name/g" "./$dir_name/solve.py"
    mv "./$dir_name/solve.py" "./$dir_name/$script_name"
    echo "Created the directory: '$dir_name'" 
else
    echo "  The directory '$dir_name' already exists."
fi


day_without_leading_zero=$(echo $day | sed 's/^0*//')
echo "  See the problem at https://adventofcode.com/2022/day/$day_without_leading_zero"
