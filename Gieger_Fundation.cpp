// Thank you to https://tomroelandts.com/articles/simulating-a-geiger-counter for the base code and simulation idea for this project.
#include <iostream>; 
#include <cmath>;
#include <random>;

std::random_device rd;  // Obtain a random number from hardware
std::mt19937 gen(rd()); // Seed the generator

void Geiger () {
    int on = 0;
    int lambda = 10; // Average number of events per second
    int next = std::log(1.0 - rand)
    

}