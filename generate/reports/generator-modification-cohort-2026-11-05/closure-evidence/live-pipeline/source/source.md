# Matrix entries: synthetic validation control

This deliberately small source lesson is authored for testing the review process.
It is not Math Academy content and must never be published to the live database.

## Lesson

A matrix is a rectangular arrangement of numbers. In the notation $a_{ij}$,
the first index specifies the row and the second specifies the column. Count
rows from the top and columns from the left, starting at 1. To find $a_{ij}$,
locate row $i$, then read its entry in column $j$. No arithmetic is needed.

This knowledge point practices reading any entry of a two-by-two matrix with
integer entries. Positive values, negative values, and zero do not change the
method. The response is one integer in a free-entry blank. Each practice item
asks for exactly one entry; matrix addition, multiplication, determinants,
transposes, diagonal sums, and arithmetic using multiple entries are later skills.

## Worked example

For $A=\begin{pmatrix}2&-3\\0&7\end{pmatrix}$, find $a_{12}$.
The first index is 1, so use the first row. The second index is 2, so use its
second column. Therefore $a_{12}=-3$.

## Complete source practice

All questions have easy difficulty, one blank with a mathematical answer,
and no answer choices, diagrams, or prerequisite operations beyond counting
to two and reading integer notation.

* fixture-q11: For $A=\begin{pmatrix}2&-3\\0&7\end{pmatrix}$, find $a_{11}$.
  Answer: 2. Solution: The first index is 1, so use row 1. The second index
  is 1, so use column 1 of that row. Thus $a_{11}=2$.
* fixture-q12: For $A=\begin{pmatrix}2&-3\\0&7\end{pmatrix}$, find $a_{12}$.
  Answer: -3. Solution: The first index is 1, so use row 1. The second index
  is 2, so use column 2 of that row. Thus $a_{12}=-3$.
* fixture-q21: For $A=\begin{pmatrix}2&-3\\0&7\end{pmatrix}$, find $a_{21}$.
  Answer: 0. Solution: The first index is 2, so use row 2. The second index
  is 1, so use column 1 of that row. Thus $a_{21}=0$.
* fixture-q22: For $A=\begin{pmatrix}2&-3\\0&7\end{pmatrix}$, find $a_{22}$.
  Answer: 7. Solution: The first index is 2, so use row 2. The second index
  is 2, so use column 2 of that row. Thus $a_{22}=7$.

The JSON source-cases file supplies the original parameters and expected values
for deterministic replay. This prose is the source of the instructional scope.
