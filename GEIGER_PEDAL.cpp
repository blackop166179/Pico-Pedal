#include <iostream>
#include <cmath>
#include <random>


float Geiger(float lambda){
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static std::uniform_real_distribution<float>dist(0.0f, 1.0f); 

    float P = dist(gen);
    float tic = -std::log(1.0f - P) / lambda;
    return tic;
}
void main() {
    std::cout << "Geiger(4.0f) = " << std::endl;
}
