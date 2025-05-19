from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def is_valid(board, num, pos):
    row, col = pos
    for x in range(9):
        if board[row][x] == num and x != col:
            return False
        if board[x][col] == num and x != row:
            return False

    box_x, box_y = col // 3, row // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    board = data.get('board')

    if not board or len(board) != 9 or any(len(row) != 9 for row in board):
        return jsonify({"error": "Invalid board"}), 400

    # Convert strings to int if needed
    for i in range(9):
        board[i] = [int(num) if num else 0 for num in board[i]]

    if solve(board):
        return jsonify({"solution": board})
    else:
        return jsonify({"error": "No solution exists"}), 400

if __name__ == '__main__':
    app.run(debug=True)
