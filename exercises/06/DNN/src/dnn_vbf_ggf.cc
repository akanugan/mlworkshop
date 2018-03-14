// ----------------------------------------------------------------------
// File:    dnn_vbf_ggf
// Created: Thu Mar 15 00:35:28 2018 by dnnwrite.py v1.0.0
// ----------------------------------------------------------------------
#ifdef WITH_PYTHON
#include <Python.h>
#endif
#include <iostream>
#include <algorithm>
#include <vector>
#include <cmath>
// ----------------------------------------------------------------------
struct dnn_vbf_ggf
{
  dnn_vbf_ggf()
    : ninputs(2),
      noutputs(1),
      maxwidth(10),
      outputs(std::vector<double>(noutputs)),
      I(std::vector<double>(maxwidth)),
      mean(std::vector<double>(ninputs)),
      scale(std::vector<double>(ninputs))
  {
    initialize();
  }

  ~dnn_vbf_ggf()
  {
  }

  double operator()(std::vector<double>& inputs)
  {
    std::copy(inputs.begin(), inputs.end(), I.begin());

    // standardize inputs
    for(size_t c=0; c < mean.size(); c++) I[c] = (I[c] - mean[c]) / scale[c];

    // compute network output
    for(size_t layer=0; layer < weights.size(); layer++) compute(layer);

    return outputs[0];
  }

#ifdef WITH_PYTHON
  //This is the function that is called from your python code
  double operator()(PyObject* o)
  {
    if ( PyList_Check(o) )
      {
        for(long c=0; c < PyList_Size(o); c++)
          I[c] = PyFloat_AsDouble(PyList_GetItem(o, c));
      }
    else if ( PyTuple_Check(o) ) 
      {
        for(long c=0; c < PyTuple_Size(o); c++)
          I[c] = PyFloat_AsDouble(PyTuple_GetItem(o, c));
      }
    else
      return -1;

   // standardize inputs
    for(size_t c=0; c < mean.size(); c++) I[c] = (I[c] - mean[c]) / scale[c];

    // compute network output
    for(size_t layer=0; layer < weights.size(); layer++) compute(layer);

    return outputs[0];    
  }
#endif
  
  struct Layer
  {
    double (*activation)(double); 
    std::vector<double> B;
    std::vector<std::vector<double> > W;    
  };

  int ninputs;
  int noutputs;
  int maxwidth;

  std::vector<double> outputs;
  std::vector<double> I;
  std::vector<double> mean;
  std::vector<double> scale;
  std::vector<Layer>  weights;

  inline
  static
  double identity(double x) { return x; }

  inline
  static
  double logistic(double x) { return 1.0/(1 + exp(-x)); }

  inline
  static
  double relu(double x) { return max<double>(0, x); }


  void compute(int layer)
  {
    std::vector<double>& B = weights[layer].B; // reference not a copy!
    std::vector<std::vector<double> >& W = weights[layer].W; // reference not a copy!

    for(size_t j=0; j < B.size(); j++)
      {
        outputs[j] = B[j];
        for(size_t i=0; i < W.size(); i++) outputs[j] += I[i] * W[i][j];
        outputs[j] = weights[layer].activation(outputs[j]);
      }
    for(size_t j=0; j < B.size(); j++) I[j] = outputs[j];
  }

  void initialize()
  {
    // scale variables using y = (x  - mean) / scale
    mean[0]= 2.94192e+00; mean[1]= 4.32645e+02; 
    scale[0]= 1.90830e+00; scale[1]= 5.06946e+02; 

    weights.clear();

    {
      // layer 0
      weights.push_back(Layer());
      weights.back().activation = this->relu;

      weights.back().B = std::vector<double>(10);    
      std::vector<double>& B = weights.back().B;
      B[0]= 5.04315e-01; B[1]= 5.11969e-01; B[2]=-2.09208e-01; 
      B[3]= 6.16052e-01; B[4]= 3.08439e-01; B[5]= 9.80417e-01; 
      B[6]=-5.64693e-01; B[7]=-6.51875e-01; B[8]=-5.20387e-01; 
      B[9]= 6.85981e-01; 
      weights.back().W = std::vector<std::vector<double> >
       (2, std::vector<double>(10));
      std::vector<std::vector<double> >& W = weights.back().W;
      W[0][0]=-2.25951e-01; W[0][1]= 1.58378e-01; W[0][2]=-6.44026e-01; 
      W[0][3]=-3.29386e-01; W[0][4]=-4.14345e-01; W[0][5]=-6.64769e-01; 
      W[0][6]=-4.63539e-01; W[0][7]=3.02919e-288; W[0][8]=-1.10344e-02; 
      W[0][9]= 5.17905e-01; W[1][0]=-2.76761e-01; W[1][1]= 3.69815e-01; 
      W[1][2]=-1.09224e+00; W[1][3]= 8.78446e-01; W[1][4]=-1.10757e+00; 
      W[1][5]= 4.53269e-01; W[1][6]=-6.36596e-01; W[1][7]=-2.22594e-306; 
      W[1][8]=-1.23978e-02; W[1][9]=-2.11085e-01; 
    }

    {
      // layer 1
      weights.push_back(Layer());
      weights.back().activation = this->relu;

      weights.back().B = std::vector<double>(10);    
      std::vector<double>& B = weights.back().B;
      B[0]= 3.67625e-01; B[1]= 4.99798e-01; B[2]= 1.08657e-01; 
      B[3]=-5.45400e-01; B[4]= 3.19744e-01; B[5]=-3.34377e-01; 
      B[6]= 8.90920e-02; B[7]= 1.59920e-01; B[8]= 6.90704e-01; 
      B[9]= 3.55656e-01; 
      weights.back().W = std::vector<std::vector<double> >
       (10, std::vector<double>(10));
      std::vector<std::vector<double> >& W = weights.back().W;
      W[0][0]=-4.06259e-01; W[0][1]=-2.26093e-01; W[0][2]= 6.11559e-01; 
      W[0][3]=-2.29868e-310; W[0][4]= 2.95318e-01; W[0][5]= 1.98969e-01; 
      W[0][6]= 1.70158e-01; W[0][7]= 3.96421e-01; W[0][8]=-4.91287e-01; 
      W[0][9]= 3.52557e-01; W[1][0]= 5.92733e-01; W[1][1]= 6.83476e-02; 
      W[1][2]=-4.47654e-01; W[1][3]= 2.55918e-03; W[1][4]=-5.61903e-01; 
      W[1][5]=-2.11598e-02; W[1][6]= 4.79795e-01; W[1][7]=-1.26312e-01; 
      W[1][8]=-1.50593e-01; W[1][9]=-3.83178e-01; W[2][0]=-6.43111e-01; 
      W[2][1]= 1.03702e-01; W[2][2]=-5.94709e-01; W[2][3]=-2.12007e-280; 
      W[2][4]= 3.80258e-01; W[2][5]=-4.64941e-01; W[2][6]= 1.33523e-01; 
      W[2][7]=-4.90222e-01; W[2][8]=-2.40473e-02; W[2][9]= 3.01118e-01; 
      W[3][0]=-1.66327e-01; W[3][1]=-1.72976e-01; W[3][2]= 1.40666e-01; 
      W[3][3]=-1.01217e-04; W[3][4]=-1.51199e+00; W[3][5]= 2.49531e-01; 
      W[3][6]=-5.33461e-02; W[3][7]= 3.20322e-01; W[3][8]= 7.66520e-01; 
      W[3][9]= 7.10979e-02; W[4][0]= 2.74399e-01; W[4][1]=-5.54701e-01; 
      W[4][2]=-2.06677e-01; W[4][3]=-1.20050e-267; W[4][4]= 1.27725e-01; 
      W[4][5]=-1.69687e-02; W[4][6]= 5.44091e-01; W[4][7]=-3.12741e-01; 
      W[4][8]= 1.02381e-01; W[4][9]= 3.80835e-01; W[5][0]= 8.91036e-01; 
      W[5][1]= 3.80313e-01; W[5][2]= 4.73539e-01; W[5][3]= 1.90319e-37; 
      W[5][4]=-4.63054e-01; W[5][5]= 6.13247e-01; W[5][6]=-6.23837e-01; 
      W[5][7]= 9.61766e-01; W[5][8]= 6.63947e-01; W[5][9]= 2.31408e-01; 
      W[6][0]=-2.12783e-01; W[6][1]=-5.32680e-01; W[6][2]=-9.65762e-01; 
      W[6][3]=-1.15480e-307; W[6][4]= 3.62596e-01; W[6][5]=-7.93720e-01; 
      W[6][6]= 2.13225e-01; W[6][7]= 2.60068e-01; W[6][8]=-3.27197e-01; 
      W[6][9]=-6.85326e-02; W[7][0]=-2.29218e-291; W[7][1]=-2.43627e-308; 
      W[7][2]=-2.60327e-255; W[7][3]=-1.80863e-297; W[7][4]=-1.81602e-250; 
      W[7][5]=3.34573e-300; W[7][6]=3.47294e-239; W[7][7]=1.53982e-246; 
      W[7][8]=-1.40300e-289; W[7][9]=-7.84804e-238; W[8][0]= 1.14107e-41; 
      W[8][1]=-1.10736e-256; W[8][2]=7.68451e-248; W[8][3]=-2.11458e-287; 
      W[8][4]= 8.26483e-41; W[8][5]=9.71067e-277; W[8][6]= 1.12290e-14; 
      W[8][7]= 1.16897e-13; W[8][8]= 1.66950e-39; W[8][9]=-7.76930e-08; 
      W[9][0]=-4.13241e-01; W[9][1]=-8.78330e-01; W[9][2]=-5.64508e-01; 
      W[9][3]=-6.70288e-232; W[9][4]= 5.22618e-01; W[9][5]=-1.46880e-01; 
      W[9][6]= 6.68610e-02; W[9][7]= 4.72886e-01; W[9][8]=-2.80302e-01; 
      W[9][9]=-1.71857e-01; 
    }

    {
      // layer 2
      weights.push_back(Layer());
      weights.back().activation = this->logistic;

      weights.back().B = std::vector<double>(1);    
      std::vector<double>& B = weights.back().B;
      B[0]=-4.05795e-01; 
      weights.back().W = std::vector<std::vector<double> >
       (10, std::vector<double>(1));
      std::vector<std::vector<double> >& W = weights.back().W;
      W[0][0]= 4.09782e-01; W[1][0]=-1.31521e+00; W[2][0]=-1.39001e+00; 
      W[3][0]=-6.88532e-61; W[4][0]=-1.79317e+00; W[5][0]=-1.22647e+00; 
      W[6][0]=-6.31386e-01; W[7][0]= 7.18914e-01; W[8][0]= 4.46343e-01; 
      W[9][0]=-8.12445e-01; 
    }

  }
};
