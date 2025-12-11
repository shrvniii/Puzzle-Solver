import time
from queue import PriorityQueue
import tkinter as tk
from copy import deepcopy

def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return i, j
    return -1, -1

def is_valid(grid, r, c, val):
    n_rows, n_cols = len(grid), len(grid[0])
    if any(grid[r][x] == val for x in range(n_cols)): return False
    if any(grid[x][c] == val for x in range(n_rows)): return False
    box_r, box_c = r - r % 2, c - c % 3
    for i in range(2):
        for j in range(3):
            if grid[box_r+i][box_c+j] == val:
                return False
    return True

def sudoku_backtrack(grid, steps):
    row, col = find_empty(grid)
    if row == -1:
        return True
    for num in range(1, 7):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            steps.append([row, col, num])
            if sudoku_backtrack(grid, steps):
                return True
            grid[row][col] = 0
            steps.append([row, col, 0])
    return False

def get_mrv_cell(grid):
    min_count = 7
    best = (-1,-1)
    for r in range(6):
        for c in range(6):
            if grid[r][c] == 0:
                count = sum(1 for num in range(1,7) if is_valid(grid,r,c,num))
                if count < min_count:
                    min_count = count
                    best = (r,c)
    return best

def sudoku_bnb(grid, steps):
    r, c = get_mrv_cell(grid)
    if r == -1:
        return True
    for num in range(1,7):
        if is_valid(grid, r, c, num):
            grid[r][c] = num
            steps.append([r, c, num])
            if sudoku_bnb(grid, steps):
                return True
            grid[r][c] = 0
            steps.append([r, c, 0])
    return False


goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
MAX_DEPTH_15PUZZLE = 10

def find_blank(p):
    for i in range(4):
        for j in range(4):
            if p[i][j]==0: return i,j

def copy_puzzle(p):
    return deepcopy(p)

def manhattan(p):
    dist = 0
    for i in range(4):
        for j in range(4):
            val = p[i][j]
            if val==0: continue
            gi, gj = divmod(val-1,4)
            dist += abs(i-gi)+abs(j-gj)
    return dist

def dfs_solve_15puzzle(puzzle, depth, max_depth, visited, steps):
    if puzzle==goal_state: return True
    if depth>=max_depth: return False
    bi,bj = find_blank(puzzle)
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for di,dj in dirs:
        ni,nj = bi+di, bj+dj
        if 0<=ni<4 and 0<=nj<4:
            new_p = copy_puzzle(puzzle)
            new_p[bi][bj], new_p[ni][nj] = new_p[ni][nj], new_p[bi][bj]
            tup = tuple(sum(new_p,[]))
            if tup in visited: continue
            visited.add(tup)
            steps.append(new_p)
            if dfs_solve_15puzzle(new_p, depth+1, max_depth, visited, steps): return True
    return False

def bnb_solve_15puzzle(start):
    pq = PriorityQueue()
    pq.put((manhattan(start), 0, start, []))
    visited=set()
    while not pq.empty():
        f,g,state,path = pq.get()
        tup = tuple(sum(state,[]))
        if tup in visited: continue
        visited.add(tup)
        if state==goal_state: return path+[state]
        bi,bj = find_blank(state)
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        for di,dj in dirs:
            ni,nj = bi+di, bj+dj
            if 0<=ni<4 and 0<=nj<4:
                new_state = copy_puzzle(state)
                new_state[bi][bj], new_state[ni][nj] = new_state[ni][nj], new_state[bi][bj]
                if tuple(sum(new_state,[])) not in visited:
                    h = manhattan(new_state)
                    pq.put((h+g+1, g+1, new_state, path+[state]))
    return None


class PuzzleSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("Puzzle Solver: Backtracking vs Branch & Bound")
        self.sudoku_results = {'bt':{'time':-1,'steps':[],'success':False}, 'bnb':{'time':-1,'steps':[],'success':False}}
        self.puzzle_results = {'dfs':{'time':-1,'steps':[],'success':False}, 'bnb':{'time':-1,'steps':[],'success':False}}
        self.main_frame = tk.Frame(master,padx=10,pady=10)
        self.main_frame.pack()
        tk.Label(self.main_frame,text="Select Puzzle Type:",font=('Arial',14,'bold')).pack(pady=10)
        tk.Button(self.main_frame,text="Sudoku (6x6)", command=self.show_sudoku_ui,width=25).pack(pady=5)
        tk.Button(self.main_frame,text="15-Puzzle (4x4)", command=self.show_15puzzle_ui,width=25).pack(pady=5)
        self.current_puzzle_frame=None
        self.visualize_delay_ms=tk.IntVar(value=50)


    def clear_current_frame(self):
        if self.current_puzzle_frame:
            self.current_puzzle_frame.destroy()
            self.current_puzzle_frame=None

    def show_sudoku_ui(self):
        self.clear_current_frame()
        self.current_puzzle_frame=tk.Frame(self.master,padx=10,pady=10)
        self.current_puzzle_frame.pack()
        self.sudoku_grid_default = [
            [0,0,0,4,0,0],
            [0,2,0,0,5,0],
            [0,0,3,0,0,1],
            [1,0,0,5,0,0],
            [0,4,0,0,2,0],
            [0,0,5,0,0,0]
        ]
        tk.Label(self.current_puzzle_frame,text="6x6 Sudoku Solver",font=('Arial',16,'bold')).grid(row=0,column=0,columnspan=6,pady=5)
        self.sudoku_cells={}
        for r in range(6):
            for c in range(6):
                color = 'lightgray' if (r//2+c//3)%2==0 else 'white'
                val=self.sudoku_grid_default[r][c]
                cell = tk.Entry(self.current_puzzle_frame,width=2,font=('Arial',18,'bold'),justify='center',bg=color,relief='raised',bd=1)
                if val!=0: cell.insert(0,str(val)); cell.config(fg='black',state='readonly')
                else: cell.config(fg='blue')
                cell.grid(row=r+1,column=c,padx=(0,2 if (c+1)%3==0 and c!=5 else 0),pady=(0,2 if (r+1)%2==0 and r!=5 else 0),ipady=5)
                self.sudoku_cells[(r,c)]=cell
        control_frame=tk.Frame(self.current_puzzle_frame)
        control_frame.grid(row=7,column=0,columnspan=6,pady=10)
        tk.Button(control_frame,text="Run Backtracking (DFS)", command=lambda:self.solve_sudoku('bt'),bg='lightblue').pack(side='left',padx=5)
        tk.Button(control_frame,text="Run Branch & Bound (MRV)", command=lambda:self.solve_sudoku('bnb'),bg='lightgreen').pack(side='left',padx=5)
        tk.Button(control_frame,text="Reset Grid", command=self.show_sudoku_ui).pack(side='left',padx=10)
        self.sudoku_bt_label = tk.Label(self.current_puzzle_frame,text="Backtracking: ---",font=('Arial',10,'bold'),fg='darkblue')
        self.sudoku_bt_label.grid(row=8,column=0,columnspan=6,pady=2,sticky='w')
        self.sudoku_bnb_label = tk.Label(self.current_puzzle_frame,text="B&B (MRV): ---",font=('Arial',10,'bold'),fg='darkgreen')
        self.sudoku_bnb_label.grid(row=9,column=0,columnspan=6,pady=2,sticky='w')
        self.sudoku_status_label = tk.Label(self.current_puzzle_frame,text="Ready. Click a button to solve.",font=('Arial',10))
        self.sudoku_status_label.grid(row=10,column=0,columnspan=6,pady=5)

    def solve_sudoku(self, method):
        self.sudoku_status_label.config(text=f"Running {'Backtracking' if method=='bt' else 'B&B (MRV)'}... Please wait.")
        self.master.update()
        temp_grid=deepcopy(self.sudoku_grid_default)
        steps=[]
        start=time.time()
        solver_func = sudoku_backtrack if method=='bt' else sudoku_bnb
        success = solver_func(temp_grid,steps)
        solve_time = time.time()-start
        self.sudoku_results[method]['time']=solve_time
        self.sudoku_results[method]['steps']=steps
        self.sudoku_results[method]['success']=success
        label = self.sudoku_bt_label if method=='bt' else self.sudoku_bnb_label
        method_name = "Backtracking" if method=='bt' else "B&B (MRV)"
        if success:
            label.config(text=f"{method_name}: Time: {solve_time*1000:.2f} ms | Steps: {len(steps)}")
            self.sudoku_status_label.config(text=f"{method_name} solved! Starting visualization...")
            self.master.after(100, lambda:self.visualize_sudoku(self.sudoku_grid_default,steps))
        else:
            label.config(text=f"{method_name}: FAILED | Time: {solve_time*1000:.2f} ms")
            self.sudoku_status_label.config(text=f"{method_name} failed to solve.")

    def visualize_sudoku(self, grid, steps):
        for r in range(6):
            for c in range(6):
                if grid[r][c]==0:
                    cell=self.sudoku_cells[(r,c)]
                    cell.config(state='normal',fg='blue',bg='white')
                    cell.delete(0,'end')
        def animate(idx):
            if idx>=len(steps):
                self.sudoku_status_label.config(text="Visualization Done! ✅")
                for r in range(6):
                    for c in range(6):
                        if grid[r][c]==0:
                            self.sudoku_cells[(r,c)].config(bg='lightgreen')
                return
            r,c,val=steps[idx]
            cell=self.sudoku_cells[(r,c)]
            cell.config(state='normal')
            cell.delete(0,'end')
            if val!=0:
                cell.insert(0,str(val))
                cell.config(fg='red',bg='yellow')
                self.master.after(50,lambda: cell.config(fg='blue',bg='white'))
            else:
                cell.config(fg='red',bg='salmon')
                self.master.after(50,lambda: cell.config(fg='blue',bg='white'))
            self.master.after(self.visualize_delay_ms.get(),lambda: animate(idx+1))
        animate(0)


    def show_15puzzle_ui(self):
        self.clear_current_frame()
        self.current_puzzle_frame=tk.Frame(self.master,padx=10,pady=10)
        self.current_puzzle_frame.pack()
        self.puzzle_grid_default=[[1,2,3,4],[5,6,0,8],[9,10,7,12],[13,14,11,15]]
        tk.Label(self.current_puzzle_frame,text="15-Puzzle Solver",font=('Arial',16,'bold')).grid(row=0,column=0,columnspan=4,pady=5)
        self.puzzle_cells={}
        for r in range(4):
            for c in range(4):
                val=self.puzzle_grid_default[r][c]
                cell=tk.Label(self.current_puzzle_frame,text=str(val) if val!=0 else "",font=('Arial',24,'bold'),width=3,height=1,relief='raised',bg='lightblue',bd=2)
                if val==0: cell.config(bg='gray')
                cell.grid(row=r+1,column=c,padx=3,pady=3)
                self.puzzle_cells[(r,c)]=cell
        control_frame=tk.Frame(self.current_puzzle_frame)
        control_frame.grid(row=5,column=0,columnspan=4,pady=10)
        tk.Button(control_frame,text=f"Run Backtracking (DFS, Max Depth={MAX_DEPTH_15PUZZLE})",command=lambda:self.solve_15puzzle('dfs'),bg='lightblue').pack(side='left',padx=5)
        tk.Button(control_frame,text="Run Branch & Bound (A*)",command=lambda:self.solve_15puzzle('bnb'),bg='lightgreen').pack(side='left',padx=5)
        tk.Button(control_frame,text="Reset Grid",command=self.show_15puzzle_ui).pack(side='left',padx=10)
        self.puzzle_dfs_label=tk.Label(self.current_puzzle_frame,text="Backtracking (DFS): ---",font=('Arial',10,'bold'),fg='darkblue')
        self.puzzle_dfs_label.grid(row=6,column=0,columnspan=4,pady=2,sticky='w')
        self.puzzle_bnb_label=tk.Label(self.current_puzzle_frame,text="B&B (A*/Manhattan): ---",font=('Arial',10,'bold'),fg='darkgreen')
        self.puzzle_bnb_label.grid(row=7,column=0,columnspan=4,pady=2,sticky='w')
        self.puzzle_status_label=tk.Label(self.current_puzzle_frame,text="Ready. Click a button to solve.",font=('Arial',10))
        self.puzzle_status_label.grid(row=8,column=0,columnspan=4,pady=5)

    def update_puzzle_display(self,grid):
        for r in range(4):
            for c in range(4):
                val=grid[r][c]
                cell=self.puzzle_cells[(r,c)]
                cell.config(text=str(val) if val!=0 else "",bg='lightblue' if val!=0 else 'gray')

    def solve_15puzzle(self,method):
        self.puzzle_status_label.config(text=f"Running {'DFS' if method=='dfs' else 'B&B'}... Please wait.")
        self.master.update()
        temp_grid=deepcopy(self.puzzle_grid_default)
        steps=[]
        start=time.time()
        success=False
        if method=='dfs':
            visited={tuple(sum(temp_grid,[]))}
            success=dfs_solve_15puzzle(temp_grid,0,MAX_DEPTH_15PUZZLE,visited,steps)
        else:
            result=bnb_solve_15puzzle(temp_grid)
            if result:
                steps=result
                success=True
        solve_time=time.time()-start
        self.puzzle_results[method]['time']=solve_time
        self.puzzle_results[method]['steps']=steps
        self.puzzle_results[method]['success']=success
        label=self.puzzle_dfs_label if method=='dfs' else self.puzzle_bnb_label
        name="DFS (Backtracking)" if method=='dfs' else "B&B (A*)"
        if success:
            label.config(text=f"{name}: Time: {solve_time*1000:.2f} ms | Steps: {len(steps)}")
            self.puzzle_status_label.config(text=f"{name} solved! Starting visualization...")
            self.master.after(100,lambda:self.visualize_15puzzle(steps))
        else:
            label.config(text=f"{name}: FAILED | Time: {solve_time*1000:.2f} ms")
            self.puzzle_status_label.config(text=f"{name} failed to solve.")

    def visualize_15puzzle(self,steps):
        def animate(idx):
            if idx>=len(steps):
                self.puzzle_status_label.config(text="Visualization Done! ✅")
                for cell in self.puzzle_cells.values(): cell.config(bg='lightgreen')
                return
            self.update_puzzle_display(steps[idx])
            self.master.after(200,lambda:animate(idx+1))
        animate(0)

if __name__=="__main__":
    root=tk.Tk()
    app=PuzzleSolverApp(root)
    root.mainloop()

