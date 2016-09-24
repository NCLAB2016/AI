//============================================================================
// Name        : EightDigits.cpp
// Author      : LIAO
// Version     :
// Copyright   : copyright (c)2016, NCLAB
// Description : Eight Digits Problem in C++, Heuristic Search
//============================================================================

#include <iostream>
#include <algorithm>
#include <stdio.h>
#include <string>
#include <sstream>
#include <queue>
#include <vector>
#include <set>

using std::cin;
using std::cout;
using std::endl;
using std::set;
using std::vector;
using std::string;
using std::priority_queue;
using std::stringstream;

const int SIZE = 3;	// row/column of board
const int RIGHT = 0;	// move up
const int UP    = 1;
const int LEFT  = 2;
const int DOWN  = 3;

class Board{
    public:
        int board[SIZE][SIZE];
        int level;	// g in f = g + h
        int cost;	// h in f = g + h
        int space_row;	// row of space
        int space_col;	// column of space
        vector<int> path;	// store the path
        Board(int l = 0, int c = 0):level(l), cost(c)
        {space_row = -1; space_col = -1;}
        void copy_from(const Board &b)
        {
            for (int i = 0; i < SIZE; ++i)
                for (int j = 0; j < SIZE; ++j)
                    board[i][j] = b.board[i][j];
            int num = b.path.size();
            for (int i = 0; i < num; ++i)
                add_to_path(b.path[i]);
            level = b.level;
            cost = b.cost;
            space_row = b.space_row;
            space_col = b.space_col;
        }
        Board(const Board& b)
        {
            copy_from(b);
        }
        inline void add_to_path(int dir)
        {
            path.insert(path.end(), dir);
        }
        bool operator<(const Board b) const
        {
            int res = this->cost + this->level < b.cost + b.level;
            if (!res) return res;
            return this->level < b.level;
        }
        void operator=(const Board &b)
        {
            copy_from(b);
        }
        bool operator==(const Board &b) const
        {
            for (int i = 0; i < SIZE; ++i)
                for (int j = 0; j < SIZE; ++j)
                    if (board[i][j] != b.board[i][j])
                        return false;
            return true;
        }
        bool operator!=(const Board &b) const {return !(*this==b);}
        string to_string() const
        {
            string res = "";
            stringstream ss;
            for (int i = 0; i < SIZE; ++i)
                for (int j = 0; j < SIZE; ++j)
                    ss << board[i][j];
            ss >> res;
            return res;
        }
        void swap_with_space(int i, int j)
        {
            board[space_row][space_col] = board[i][j];
            board[i][j] = 0;	// space
            space_row = i;
            space_col = j;
        }
        void print() const
        {
            for (int i = 0; i < SIZE; ++i)
            {
                for (int j = 0; j < SIZE; ++j) cout << board[i][j] << " ";
                cout << endl;
            }
        }
};

inline void get_board(Board &);
inline void calc_cost(Board *);
void read_from_sample();
inline int abs(int);
inline void format_print_state(const Board &);
inline int calc_manhattan(int, int, int);
void get_all_children(Board*);
void move_space_add_child(Board *, int, int, int);
bool heuristic_search();
int print_path(Board*);
bool check_sol_existed();

vector<Board*> open; // open table
set<string> closed;	// close table
Board original, target;

// sample 1
int ori[] = {7,2,4,5,0,6,8,3,1};	// original state
int tar[] = {0,1,2,3,4,5,6,7,8};	// target state

// sample 2
//int ori[] = {2,8,3,1,6,4,7,0,5};	// sample original
//int tar[] = {2,3,0,1,8,4,7,6,5};	// sample target

// sample 3
//int ori[] = {2,8,3,1,6,4,7,0,5};	// sample original
//int tar[] = {2,8,3,1,4,6,7,0,5};	// sample target

int main()
{
    read_from_sample();
    calc_cost(&original);	// calculate original cost
    open.insert(open.end(), &original);	// push original to open table
    // first check the existence of solution
    // second heuristic search (A star)
    if (!check_sol_existed() || !heuristic_search()) cout << "no result:(" << endl;
    return 0;
}

bool heuristic_search()
{
    while (!open.empty())
    {
        // action simulate the priority queue pop the first
    	vector<Board*>::iterator  it = open.begin();
        for (vector<Board*>::iterator tit = open.begin(); tit != open.end(); ++tit)
        {
        	if ((*tit)->cost + (*tit)->level < (*it)->cost + (*it)->level) it = tit;
        	else if ((*tit)->cost + (*tit)->level == (*it)->cost + (*it)->level
        			&& (*tit)->level > (*it)->level)
        		it = tit;
        }
        Board *state = *it;
        if (*state == target)
        {
            print_path(state);
            return true;
        }
        open.erase(it);
        closed.insert(state->to_string());	// add him to closed table
        get_all_children(state);		// get all children of state
        if (*state != original) delete state;
    }
    return false;
}

// check the existence of solution: based on same parity
bool check_sol_existed()
{
	int f = 0, g = 0;
	for (int i = 0; i < SIZE * SIZE; ++i)
		for (int j = 0; j < i; ++j)
		{
			if (ori[i] && ori[j] && ori[i] > ori[j]) ++f;
			if (tar[i] && tar[j] && tar[i] > tar[j]) ++g;
		}
	if ((f % 2) != (g % 2)) return false;
	return true;
}

// read original and target state from sample pre-defined
void read_from_sample()
{
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
        {
            if (!ori[i*SIZE+j]) {original.space_row=i;original.space_col=j;}
            original.board[i][j] = ori[i*SIZE+j];
            if (!tar[i*SIZE+j]) {target.space_row=i;target.space_col=j;}
            target.board[i][j] = tar[i*SIZE+j];
        }
}

// move space to certain position, generate new child
void move_space_add_child(Board *state,
    int row, int col, int direction)
{
    Board* b = new Board(*state);
    b->swap_with_space(row, col);

    // if not found in closed table
    if (closed.find(b->to_string()) == closed.end())
    {
        b->level = state->level + 1;
        calc_cost(b);
        b->add_to_path(direction);
        vector<Board*>::iterator it;
        for (it=open.begin(); it != open.end(); ++it) if (*it == b) break;
        if (it == open.end()) open.insert(open.end(), b);
        else if ((*it)->cost > b->cost)
        {
            open.erase(it);
            open.insert(open.end(), b);
        }
    }
}

// get all children state of this state
void get_all_children(Board *state)
{
    int row = state->space_row, col = state->space_col;
    if (row > 0)	// up
        move_space_add_child(state, row - 1 , col, UP);
    if (row < SIZE - 1)	// down
        move_space_add_child(state, row + 1, col, DOWN);
    if (col > 0)	// left
        move_space_add_child(state, row, col - 1, LEFT);
    if (col < SIZE - 1)	// right
        move_space_add_child(state, row, col + 1, RIGHT);
}

// calculate manhattan distance
inline int calc_manhattan(int i, int j, int value)
{
    for (int ii = 0; ii < SIZE; ++ii)
        for (int jj = 0; jj < SIZE; ++jj)
            if (target.board[ii][jj] == value)
                return abs(i - ii) + abs(j - jj);
    return 0;
}

// calculate this state's cost, assign to himself
inline void calc_cost(Board* state)
{
    int h = 0;
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
            if (state->board[i][j])	// there is no effect for space
                h += calc_manhattan(i, j, state->board[i][j]);
    state->cost = h;
}

inline int abs(int x) {return x < 0 ? -x : x;}

inline void format_print_state(const Board &state)
{
    cout << "level: " << state.level << " cost: " <<
        state.cost << endl;
    state.print();
    cout << endl;
}

// print the path moving, return the number of steps
int print_path(Board* b)
{
    Board c(original);
    int num = b->path.size();
    cout << "total number of move: " << num << endl << endl;
    c.print();
    for (int i = 0; i < num; ++i)
    {
        cout << " | " <<  endl << " V " << endl;
        switch (b->path[i])
        {
            case UP:
                c.swap_with_space(c.space_row - 1, c.space_col);
                break;
            case DOWN:
                c.swap_with_space(c.space_row + 1, c.space_col);
                break;
            case LEFT:
                c.swap_with_space(c.space_row, c.space_col - 1);
                break;
            case RIGHT:
                c.swap_with_space(c.space_row, c.space_col + 1);
                break;
        }
        c.print();
    }
    return num;
}

// Reserve: read digit from standard input
inline void get_board(Board &b)
{
    int digit;
    for (int i = 0; i < SIZE; ++i)
        for (int j = 0; j < SIZE; ++j)
        {
            cin >> digit;
            if (!digit) {b.space_row = i; b.space_col = j;}
            b.board[i][j] = digit;
        }
}
