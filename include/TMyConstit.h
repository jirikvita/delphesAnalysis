// JK 2.8.2024
// using ChatGPT4


#ifndef TMYCONSTIT_H
#define TMYCONSTIT_H

class TMyConstit {

 private:
    double _Pt;
    double _y;
    double _Phi;

 public:
    // Constructors
    TMyConstit();
    TMyConstit(double pt, double y, double phi);
    ~TMyConstit();
    
    // Getters
    double GetPt();
    double GetY();
    double GetPhi();
    /*
    // Setters
    void SetPt(double pt);
    void SetY(double y);
    void SetPhi(double phi);
    */
};

#endif // TMYCONSTIT_H

