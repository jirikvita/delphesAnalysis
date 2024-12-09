// using ChatGPT4

#include "TMyConstit.h"

// Default constructor
TMyConstit::TMyConstit() : _Pt(0), _y(0), _Phi(0) {}

// Parameterized constructor
TMyConstit::TMyConstit(double pt, double y, double phi) : _Pt(pt), _y(y), _Phi(phi) {}

TMyConstit::~TMyConstit() {};

// Getter for Pt
double TMyConstit::GetPt() {
    return _Pt;
}

// Getter for y
double TMyConstit::GetY() {
    return _y;
}

// Getter for Phi
double TMyConstit::GetPhi() {
    return _Phi;
}

/*

// Setter for Pt
void TMyConstit::setPt(double pt) {
    _Pt = pt;
}

// Setter for y
void TMyConstit::setY(double y) {
    _y = y;
}

// Setter for Phi
void TMyConstit::setPhi(double phi) {
    _Phi = phi;
}
*/
