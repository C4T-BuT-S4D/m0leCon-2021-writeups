Left or right?
---

In this challenge we could reorder L-R sequences (L for the left move and R for the right) and needed to minimize the
absolute value of the leftmost point reached if the selected order of movements is applied from the point 0.

We applied the branch and bound algorithm with the following optimizations:

1. Small cases are solved in `O(n!)` by bruteforcing all permutations of the sequences.

2. Sequences are sorted in such an order that all "good" ones are at the started and sorted by their leftmost point in
   ascending order, and all "bad" ones are at the end sorted by their leftmost point in descending order. We consider
   the sequence "good" if in total it moves us right and "bad" otherwise. This is purely a heuristic that has shown the
   best results.

3. We store the best reached value yet and, if by applying the next sequence during the bruteforce we reach some worse
   point, we can terminate the branch.

4. We use caching by `(current point, left sequences)` to terminate duplicate branches.

5. If we're close to a time limit, we return the best answer yet and pray we've reached the optimal state.

6. The final optimization is running the code using PyPy, not the regular Python.

The full solution is in the [sploit](./sploit.py).

Running the script for a few times yields the flag: `ptm{45_r16h7_45_p0551bl3}`.
