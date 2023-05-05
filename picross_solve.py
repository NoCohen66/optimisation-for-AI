from __future__ import annotations

import signal
import sys

import click
import facile

from picross import picross


def picross_solve(
    lines: list[list[int]],
    columns: list[list[int]]
) -> tuple[facile.Solution, facile.Array]:
    print(lines, columns)
    # number of lines and columns
    n, m = len(lines), len(columns)
    print(f'{n=}, {m=}')
    # number of cluster per line and column
    m_i = [len(a_i) for a_i in lines]
    m_j = [len(a_j) for a_j in columns]

    # --- add decision variables

    # model 1 - binary
    grid = facile.Array.binary((n, m))

    # model 2 - integer
    model2_vars_rows = list()
    for i, a_i in enumerate(lines):
        s_i = [facile.variable(range(m)) for k in range(m_i[i])]
        model2_vars_rows.append(s_i)
    model2_vars_columns = list()
    for j, a_j in enumerate(columns):
        s_j = [facile.variable(range(n)) for k in range(m_j[j])]
        model2_vars_columns.append(s_j)


    # --- add constraints

    # - CONSTRAINT 1 : overlap
    print('CONSTRAINT 1 : Processing...')
    # for each row
    for i, a_i in enumerate(lines):
        if m_i[i] > 1: # if we have more than one cluster
            for k in range(m_i[i] - 1): # from each cluster (except the last one)
                facile.constraint(
                    model2_vars_rows[i][k] + a_i[k] < model2_vars_rows[i][k+1]
                )
    # for each column
    for j, a_j in enumerate(columns):
        if m_j[j] > 1: # if we have more than one cluster
            for k in range(m_j[j] - 1): # from each cluster (except the last one)
                facile.constraint(
                    model2_vars_columns[j][k] + a_j[k] < model2_vars_columns[j][k+1]
                )
    
    # - CONSTRAINT 2 - black cells limit
    print('CONSTRAINT 2 : Processing...')
    # for each row
    for i, a_i in enumerate(lines):
        sum_grid_row_i = grid[i,:].sum()
        sum_grid_cluster_k = sum(a_i)
        facile.constraint(sum_grid_row_i == sum_grid_cluster_k)
    # for each column
    for j, a_j in enumerate(columns):
        sum_grid_col_j = grid[:,j].sum()
        sum_grid_cluster_k = sum(a_j)
        facile.constraint(sum_grid_col_j == sum_grid_cluster_k)
    
    # - CONSTRAINT 3 - linking model 1/model 2
    
    # (FAST) - CONSTRAINT 3 - linking model 1/model 2
    print('CONSTRAINT 3 - FAST : Processing...')
    # for each row
    for i, a_i in enumerate(lines):
        belong_i = []
        for j in range(m):
            belong_i = [
                ( (model2_vars_rows[i][k] <= j) + (j < model2_vars_rows[i][k] + a_i[k]) )==2
                for k in range(m_i[i])
            ]
            facile.constraint(sum(belong_i) == grid[i, j])
    
    for j, a_j in enumerate(columns):
        belong_j = []
        for i in range(n):
            belong_j = [
                ( (model2_vars_columns[j][k] <= i) + (i < model2_vars_columns[j][k] + a_j[k]) )==2
                for k in range(m_j[j])
            ]
            facile.constraint(sum(belong_j) == grid[i, j])
    
    '''
    # This is a slower technique to solve this problem but we leave it as a comment for a better understanding
    # (SLOW) - CONSTRAINT 3 - linking model 1/model 2
    print('CONSTRAINT 3 - SLOW : Processing...')
    # for each row
    for i, a_i in enumerate(lines):
        for k in range(m_i[i]):
            for pos_offset in range(a_i[k]):
                facile.constraint(grid[i, model2_vars_rows[i][k] + pos_offset] == 1)
    
    # for each column
    for j, a_j in enumerate(columns):
        for k in range(m_j[j]):
            for pos_offset in range(a_j[k]):
                facile.constraint(grid[model2_vars_columns[j][k] + pos_offset, j] == 1)
    '''

    sol = facile.solve(grid)

    return sol, grid


@click.command(help="Picross solver program")
@click.argument("name", default="moon")
def main(name: str) -> None:
    lines, columns = picross[name]    

    def signal_handler(signal, frame):
        print("You pressed Ctrl+C!")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    sol, grid = picross_solve(lines, columns)

    print(sol)

    for line in grid.value():
        for item in line:
            if item == 1:
                print("██", end="")
            else:
                print("  ", end="")
        print()


if __name__ == "__main__":
    main()
