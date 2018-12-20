subjects='03 04 05 06 07 08 09 10 11 12 14 16 17 18 19 20 21 22 23 25 26 27'

for subject in $subjects
do
  python3 prepare_connectivity_matrices.py $subject
done

echo "All done"
date
