#ifndef exx2
#define exx2
#include "exx.c"
#include <iostream>
#include <unistd.h>

using namespace std;

class abc {
	public:
        abc();
        ~abc();

        int trythis(int x);
};

abc::abc(){
	cout<<"Creating abc class...\n";
}

abc::~abc() {
	cout<<"Destroying abc class...\n";
}

int abc::trythis(int x) {
	cout<<"Trythis is: "<<fact(x)<<endl;
        return fact(x);
}

/*int main(){
	abc b;
        int x = b.trythis(2);
	cout<<"boing: "<<x<<endl;
}*/

#endif
