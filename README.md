
# Picross

## Description of the problem

Picross is a popular game of a similar nature to Sudoku.  
It consists of a grid of square dimension $n \times n$ and of a list of integers for each row and each column.

![Solution for the duck problem](./picross_duck.png){ width="180px"}

You can find all of this work in the document 🚀 [Python file - **resolution optmisation**](anomalies.ipynb).

We will use the following notations:

- $b_{i,j} \in \{0, 1\}$ represents a bit, indicating a column or a row where $i, j \in \{1, ..., n\}$ represents a column or row index;
- $m_i \in \{1, ..., \lceil n/2 \rceil\}$ represents the size of the list associated to row/column $i$;
- $a_{i,k} \in \{1, ..., n\}$ is the $k$-th integer of the list associated to row/column $i$.

The goal is to darken some cells of the grid, such that in each row/column $i$ the number of successive black cells form the list $\{a_{i,1}, ..., a_{i,m_i}\}$.

To popularize the notations, we can say:

- $b_{i,j}$ : specific cell (row $i$, column $j$)
- $m_i$ : number of cluster in row/column $i$;
- $a_{i,k}$ :  in row $i$, size of $k$-th cluster

We introduce: 

- $s_{i,k}$ :  in row $i$, **starting position** of $k$-th cluster

# 1. Modelling ways

## 1.1 Binary variables

Each cell of the table is considered as a decision variables, with binary value as their domains (0 or 1)

## 1.2 Integer variables

On each row, one decision variable exist for the first position of every “cluster” of colored cell to be assigned (1 integer if there is only 1 cluster to assign, 2 integers if 2 clusters are to be assigned, ...).

*Nota : the maximum number of “cluster” per row is limited to n/2 groups (since at least one blank cell need to exist between 2 clusters)*

# 2. Overlap constraints

By using ‘Integer variable’ modelling (=(2)), we can state that the “no overlap constraint” correspond to constraint the $k$+1-th cluster ‘s starting position to be bigger than the k-th cluster’s last position with, at least, an additional blank cell between them.

We state that by using following expression:

**For each row $i$ :**

$$ s_{i,k} + a_{i,k} < s_{i,k+1} $$

with: 
* $s_{i,k}$ :  in row $i$, **starting position** of $k$-th cluster
* $a_{i,k}$ :  in row $i$, size of $k$-th cluster

**For each column $j$ :**

$$ s_{j,k} + a_{j,k} < s_{j,k+1} $$

with: 
* $s_{j,k}$ :  in column $j$, **starting position** of $k$-th cluster
* $a_{j,k}$ :  in column $j$, size of $k$-th cluster


# 3. Black cells limit

By using ‘binary variable’ modelling (=(1)), we can state that amount of s“colored black cells limit” correspond to the sum of 1 available on row/column i, and cannot be more than the sum of coefficients from the corresponding row/column i. 

We state that by using following expression:

**For each row $i$ :**

$$ \sum_{j=1}^n b_{i,j} = \sum_{k=1}^{m_i} a_{i,k} $$

with: 
- $b_{i,j}$ : specific **cell** (row $i$, column $j$)
- $a_{i,k}$ :  in row $i$, **size** of $k$-th cluster
- $m_i$ : **number of cluster** in row $i$;

**For each column $j$ :**


$$ \sum_{i=1}^n b_{i,j} = \sum_{k=1}^{m_j} a_{j,k} $$

with: 
- $b_{i,j}$ : specific **cell** (row $i$, column $j$)
- $a_{j,k}$ :  in column $j$, **size** of $k$-th cluster
- $m_j$ : **number of cluster** in column $j$;

# 4. Linking decision variables from the two modelling


For each row i, for each cluster in that row i, the binary grid cell corresponding to the ‘integer model’ ‘starting point’ decision variables is equal to 1:

**For each row i...   
    For the k-th cluster in that row i...**  
    
$$ b_{i,s_{i,k}+offset} = 1 $$

with:
- $offset \in \{[0, a_{i,k}\[}$

- $b_{i,j}$ : specific **cell** (row $i$, column $j$)
- $a_{i,k}$ :  in row $i$, size of $k$-th cluster
- $s_{i,k}$ :  in row $i$, **starting position** of $k$-th cluster

And is it the similar logic with column.

*Nota : We first started to think about this constraint defined as below, bumping into a coding problem since we used indexes slices with decision variables...We redefined the problem by using previously define concept in order to get around this coding problem.*

---

The concept for this constraint is the following one : for one row i, for the k-th “cluster”, the sum of binary decision variables in this cluster have to be equal to the size of row i’s k-th cluster.

**For each row i...   
    For each cluster in that row i...**  
    
$$ \sum_{p={s_{i,k}}}^{s_{i,k}+a_{i,k}-1} b_{i,p} =  a_{i,k} $$
    
with: 
- $b_{i,j}$ : specific **cell** (row $i$, column $j$)
- $a_{i,k}$ :  in row $i$, size of $k$-th cluster
- $s_{i,k}$ :  in row $i$, **starting position** of $k$-th cluster

**For each column j...**

$$ \sum_{p={s_{j,k}}}^{s_{j,k}+a_{j,k}-1} b_{j,p} =  a_{j,k} $$

with: 
- $b_{i,j}$ : specific **cell** (row $i$, column $j$)
- $a_{i,k}$ :  in row $i$, **size** of $k$-th cluster
- $s_{j,k}$ :  in column $j$, **starting position** of $k$-th cluster

# 🎓 Authors

Noémie Cohen
Mathieu Canto
