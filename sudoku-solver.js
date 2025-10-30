/**
 * Journey of Kindness - Sudoku Solver
 * 
 * Data structure inspired by Sarika Deol's C++ SudokuGrid implementation
 * Backtracking algorithm and solving logic: Original implementation by Mei-Hsien Hsu
 * 
 * References:
 * - Grid validation logic adapted from Sarika Deol's SudokuGrid.cpp
 * - Backtracking solver algorithm: original design
 */

class SudokuGrid {
    constructor() {
        // Initialize 9x9 grid with empty spaces
        this.grid = Array(9).fill(null).map(() => Array(9).fill(' '));
        this.solution = null;
        this.moveHistory = [];
    }

    // Get cell value at position (row, col)
    // Throws error if out of bounds
    getCell(row, col) {
        if (row >= 9 || col >= 9 || row < 0 || col < 0) {
            throw new Error('getCell error: row/col out of bounds');
        }
        return this.grid[row][col];
    }

    // Set cell value at position (row, col)
    // Throws error if out of bounds or invalid value
    setCell(row, col, value) {
        if (row >= 9 || col >= 9 || row < 0 || col < 0) {
            throw new Error('setCell error: row/col out of bounds');
        }
        if (this.invalidValue(value)) {
            throw new Error('setCell error: invalid value');
        }
        this.grid[row][col] = value;
        this.moveHistory.push({row, col, value});
    }

    // Check if a value is invalid (not ' ' or '1'-'9')
    invalidValue(value) {
        if (value === ' ') {
            return false;
        }
        if (value >= '1' && value <= '9') {
            return false;
        }
        return true;
    }

    // Check if a specific row is solved (contains all digits 1-9)
    // Logic adapted from Sarika Deol's rowSolved() method
    rowSolved(rowIndex) {
        const seen = new Set();
        for (let col = 0; col < 9; col++) {
            const value = this.grid[rowIndex][col];
            if (value === ' ') return false;
            if (seen.has(value)) return false;
            seen.add(value);
        }
        return seen.size === 9;
    }

    // Check if a specific column is solved
    // Logic adapted from Sarika Deol's columnSolved() method
    columnSolved(colIndex) {
        const seen = new Set();
        for (let row = 0; row < 9; row++) {
            const value = this.grid[row][colIndex];
            if (value === ' ') return false;
            if (seen.has(value)) return false;
            seen.add(value);
        }
        return seen.size === 9;
    }

    // Check if a specific 3x3 block is solved
    // Logic adapted from Sarika Deol's blockSolved() method
    blockSolved(blockRow, blockCol) {
        const seen = new Set();
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const row = blockRow * 3 + i;
                const col = blockCol * 3 + j;
                const value = this.grid[row][col];
                if (value === ' ') return false;
                if (seen.has(value)) return false;
                seen.add(value);
            }
        }
        return seen.size === 9;
    }

    // Check if entire grid is solved
    // Logic adapted from Sarika Deol's isSolved() method
    isSolved() {
        // Check all rows
        for (let row = 0; row < 9; row++) {
            if (!this.rowSolved(row)) return false;
        }
        
        // Check all columns
        for (let col = 0; col < 9; col++) {
            if (!this.columnSolved(col)) return false;
        }
        
        // Check all 3x3 blocks
        for (let blockRow = 0; blockRow < 3; blockRow++) {
            for (let blockCol = 0; blockCol < 3; blockCol++) {
                if (!this.blockSolved(blockRow, blockCol)) return false;
            }
        }
        
        return true;
    }

    // Check if placing a number at (row, col) is valid
    // Original implementation for solver
    isValidPlacement(row, col, num) {
        // Check row
        for (let c = 0; c < 9; c++) {
            if (this.grid[row][c] === num) return false;
        }
        
        // Check column
        for (let r = 0; r < 9; r++) {
            if (this.grid[r][col] === num) return false;
        }
        
        // Check 3x3 block
        const blockRow = Math.floor(row / 3) * 3;
        const blockCol = Math.floor(col / 3) * 3;
        for (let r = blockRow; r < blockRow + 3; r++) {
            for (let c = blockCol; c < blockCol + 3; c++) {
                if (this.grid[r][c] === num) return false;
            }
        }
        
        return true;
    }

    // Find next empty cell (returns [row, col] or null if none)
    findEmptyCell() {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (this.grid[row][col] === ' ') {
                    return [row, col];
                }
            }
        }
        return null;
    }

    // Backtracking solver algorithm - Original implementation
    // This is the core AI solving logic
    solve() {
        const emptyCell = this.findEmptyCell();
        
        // Base case: no empty cells means puzzle is solved
        if (!emptyCell) {
            return true;
        }
        
        const [row, col] = emptyCell;
        
        // Try digits 1-9
        for (let num = 1; num <= 9; num++) {
            const numChar = num.toString();
            
            if (this.isValidPlacement(row, col, numChar)) {
                // Place the number
                this.grid[row][col] = numChar;
                
                // Recursively try to solve rest of puzzle
                if (this.solve()) {
                    return true;
                }
                
                // Backtrack if this didn't work
                this.grid[row][col] = ' ';
            }
        }
        
        // No valid number found, need to backtrack
        return false;
    }

    // Create a copy of current grid state
    copyGrid() {
        return this.grid.map(row => [...row]);
    }

    // Load a grid state
    loadGrid(gridData) {
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                this.grid[row][col] = gridData[row][col];
            }
        }
    }

    // Print grid to console (for debugging)
    print() {
        const divider = '+-----+-----+-----+';
        console.log(divider);
        for (let row = 0; row < 9; row++) {
            let line = '|';
            for (let col = 0; col < 9; col++) {
                line += this.grid[row][col];
                if (col === 2 || col === 5 || col === 8) {
                    line += '|';
                } else {
                    line += ' ';
                }
            }
            console.log(line);
            if (row === 2 || row === 5) {
                console.log(divider);
            }
        }
        console.log(divider);
    }

    // Get number of filled cells
    getFilledCount() {
        let count = 0;
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (this.grid[row][col] !== ' ') {
                    count++;
                }
            }
        }
        return count;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SudokuGrid;
}
