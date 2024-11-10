#include <iostream>
#include <string>

using namespace std;
int main()
{
    cout << "Time to make a ghastly cyberbrew!" << endl;
    cout << "Tell me how much of each ingredient to put in." << endl;
    int crypto = 0, forensics = 0, osint = 0, pwn = 0, rev = 0, web = 0, water = 0;
    cout << "How many crypto crickets? (int)" << endl;
    cin >> crypto;
    cout << "How many forensics fungi? (int)" << endl;
    cin >> forensics;
    cout << "How many osint oreos? (int)" << endl;
    cin >> osint;
    cout << "How many plants of pwn? (int)" << endl;
    cin >> pwn;
    cout << "How many rev redcaps? (int)" << endl;
    cin >> rev;
    cout << "How many cobwebs? (int)" << endl;
    cin >> web;
    cout << "How many ounces of water? (int)" << endl;
    cin >> water;
    cin.ignore();

    string secret;
    cout << "What secret ingredient? (string)" << endl;
    getline(cin, secret);

    int max_ingredient = 0;
    int second_ingredient = 0;
    for (int x : {crypto, forensics, osint, pwn, rev, web}) {
        max_ingredient = max(max_ingredient, x);
    }
    for (int x : {crypto, forensics, osint, pwn, rev, web}) {
        second_ingredient = x >= max_ingredient ? second_ingredient : max(second_ingredient, x);
    }

    if (max_ingredient == 0) {
        if (water > 0) {
            cout << "You poured a nice glass of water." << endl;
        } else {
            cout << "You created... nothing." << endl;
        }
    } else if (water <= 0) {
        cout << "You created a salad." << endl;
    } else if (max_ingredient == crypto) {
        if (second_ingredient == forensics && forensics > 0) {
            cout << "You created a draught of decoding :}" << endl;
        } else if (second_ingredient == web && web > 0) {
            cout << "You created a slosh of secure sending :}" << endl;
        } else {
            cout << "You created an elixir of encoding :}" << endl;
        }
    } else if (max_ingredient == forensics) {
        if (second_ingredient == osint && osint > 0) {
            cout << "You created an ichor of investigation :}" << endl;
        } else {
            cout << "You created an infusion of forensics :}" << endl;
        }
    } else if (max_ingredient == osint) {
        cout << "You created a goo of googling :}" << endl;
    } else if (max_ingredient == pwn || max_ingredient == rev) {
        if (crypto == 7914 && forensics == 111100 && osint == 2310 && pwn == 51337 && rev == 42154142 && web == 9111 && secret == "decompiler") {
            cout << "You created a philter of flag charming :}" << endl;
            cout << "CYBORG{RECIPE=" << crypto << "-" << forensics << "-" << osint << "-" << pwn << "-" << rev << "-" << web << "-" << secret << "}" << endl;
        } else if (second_ingredient == crypto && crypto > 0) {
            cout << "You created a balsam of buried secrets :}" << endl;
        } else {
            cout << "You created a salve of shattered secrets :}" << endl;
        }
    } else if (max_ingredient == web) {
        if (second_ingredient == pwn && pwn > 0) {
            cout << "You created an essence of exploitation :}" << endl;
        } else {
            cout << "You created a tonic of TCP :}" << endl;
        }
    } else {
        cout << "You created a mysterious smoothie :}" << endl;
    }

}