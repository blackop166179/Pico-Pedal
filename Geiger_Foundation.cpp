#include <iostream>
#include <cmath>
#include <random>

float Geiger(float lambda){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dis(0.0, 1.0);
    float P = dis(gen);
    return -log(1-P)/lambda;
}
int main (){
    std::cout << Geiger(4.0) << std::endl;
}
