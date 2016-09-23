#include <iostream>
#include <algorithm>
#include <string>
#include <stdio.h>
#include <vector>
#include <set>

using std::cin;
using std::cout;
using  std::endl;
using  std::set;
using std::string;
using std::vector;

const string SUC_STATE("1111");	// success state
const int NUMS = SUC_STATE.length();
const int FARMER  = 0;
const int WOLF    = 1;
const int SHEEP   = 2;
const int CABBAGE = 3;

vector<string> cross_order;   // order of crossing river

set<string> closed;	// closed table

string ori_state("0000");	// original state

inline bool crossed(string);
inline void take_step(string&, int);
string river_cross(string);
bool check_valid(string);
void print_path();

int main (int argc, char* argv[])
{
    // give the original state by command line
    if (argc > 1) ori_state = string(argv[1]);
    
    cout << "农夫-" << FARMER << " 狼-" << WOLF << " 羊-"
        << SHEEP << " 白菜-" << CABBAGE << endl;
    // cross the river
    if (crossed(river_cross(ori_state))) cout << "成功^_^" << endl;
    // print the path
    print_path();
	return 0;
}

// check if crossed successfully
inline bool crossed(string state)
{
	return state.compare(SUC_STATE) == 0;
}

// take a step to cross the river
inline void take_step(string& state, int who)
{
	state[who] = '1' - state[who] + '0';
}

// check this state is valid or not, such as wolf and sheep...
bool check_valid(string state)
{
	bool suc = true;
	if (state[WOLF] == state[SHEEP]
		&& state[WOLF] != state[FARMER] )
	{
		cout << "羊被吃了" << endl;
		suc = false;
	}
	if (state[SHEEP] == state[CABBAGE]
		&& state[FARMER] != state[SHEEP])
	{
		cout << "白菜被吃了" << endl;
		suc = false;
	}
	return suc;
}

// print all the crossing river steps
void print_path()
{
    vector<string>::iterator it;
    cout << endl << "Steps: " << ori_state;
    for (it = cross_order.begin(); it != cross_order.end(); ++it)
        cout << " => " << *it;
    cout << endl;
}

// recursively cross the river, return changed state
// if failure, return ""
string river_cross(string state)
{
	// failure or has crossed
	if (state == "")
	{
		cout << "翻船!" << endl << endl;
	 	return state;
	}
	if (crossed(state)) return state;

	// find state in closed table
	if (closed.find(state) != closed.end()) return "";

	// add to closed table
	closed.insert(state);

	// check if valid
	if (!check_valid(state)) return "";

	string try_a_step(state);

	// try cross river lonely ---- must be farmer
	take_step(try_a_step, FARMER);
	cout << state << "=>" << try_a_step << endl;

	// if success, save the path,
	if (crossed(river_cross(try_a_step)))
    {
        cross_order.insert(cross_order.begin(), try_a_step);
        return SUC_STATE;
    }

    cout << "重试.." << endl;
    // remove this invalid state from the path
    //cross_order.erase(find(cross_order.begin(), cross_order.end(), try_a_step));

	// try cross with a partner
	for (int i = 1; i < NUMS; ++i)
	{
		// farmer take who in his sider
		if (state[i] == state[FARMER])
		{
			take_step(try_a_step, i);	// select a partner
			cout << state << "=>" <<  try_a_step << endl;
			if (crossed(river_cross(try_a_step)))
            {
                cross_order.insert(cross_order.begin(), try_a_step);
                return SUC_STATE;
            }
            cout << "重试.." << endl;
			take_step(try_a_step, i);	// recorver the state
		}
	}
	return "";
}
