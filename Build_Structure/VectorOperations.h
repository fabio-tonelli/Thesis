#ifndef VECTOR_OPERATIONS_H
#define VECTOR_OPERATIONS_H

#include <algorithm>  // se si vogliono usare algoritmi STL
#include <cassert>
#include <iostream>
#include <numeric>  // per inner_product
#include <vector>

using namespace std;

// ===============================================================================
// somma di due vettori : somma componente per componente
// ===============================================================================

template <typename T>
inline std::vector<T> operator+(const std::vector<T>& a,
                                const std::vector<T>& b) {
  //  if ( a.size() != b.size() ) throw "Trying to sum vectors with different
  //  size" ;

  if (a.size() != b.size()) {
    cout << "Trying to sum vectors with different size, exiting" << endl;
    exit(-1);
  };

  std::vector<T> result(a.size());

  for (int i = 0; i < static_cast<int>(a.size()); i++) result[i] = a[i] + b[i];

  // Alternativamente si puo' usare l'algoritmo transform della STL

  return result;
}

// ===============================================================================
// differenza di due vettori componente per componente
// [ preferisco re-implementarlo perche' si fanno meno operazioni rispetto
// result = a + (-1.*b) ]
// ===============================================================================
template <typename T>
inline std::vector<T> operator-(const std::vector<T>& a,
                                const std::vector<T>& b) {
  if (a.size() != b.size()) {
    cout << "Trying to sum vectors with different size, exiting" << endl;
    exit(-1);
  };

  std::vector<T> result(a.size());

  for (int i = 0; i < static_cast<int>(a.size()); i++) result[i] = a[i] - b[i];

  // Alternativamente si puo' usare l'algoritmo transform della STL

  return result;
}

// ===============================================================================
// prodotto scalare tra due vettori
// ===============================================================================

template <typename T>
inline T operator*(const std::vector<T>& a, const std::vector<T>& b) {
  if (a.size() != b.size()) {
    cout << "Trying to sum vectors with different size, exiting" << endl;
    exit(-1);
  };

  T sum = 0;
  for (int i = 0; i < static_cast<int>(a.size()); i++) sum += a[i] * b[i];

  // Alternativamente si puo' usare l'algoritmo inner_product della STL

  return sum;
}

// ===============================================================================
// prodotto tra uno scalare e un vettore
// ===============================================================================

template <typename T>
inline std::vector<T> operator*(T c, const std::vector<T>& a) {
  std::vector<T> result(a.size());

  for (int i = 0; i < static_cast<int>(a.size()); i++) result[i] = c * a[i];

  // Alternativamente si puo' usare l'algoritmo inner product

  return result;
}

// ===============================================================================
// prodotto tra un vettore e uno scalare
// ===============================================================================

template <typename T>
inline std::vector<T> operator*(const std::vector<T>& a, T c) {
  std::vector<T> result(a.size());

  for (int i = 0; i < static_cast<int>(a.size()); i++) result[i] = c * a[i];

  return result;
}

// ===============================================================================
// divisione tra un vettore e uno scalare
// ===============================================================================

template <typename T>
inline std::vector<T> operator/(const std::vector<T>& a, T c) {
  std::vector<T> result(a.size());
  for (int i = 0; i < static_cast<int>(a.size()); i++) result[i] = a[i] / c;

  return result;
}

// ===============================================================================
// somma ad a un vettore b e il risultato viene messo in a
// ===============================================================================

template <typename T>
inline std::vector<T>& operator+=(std::vector<T>& a, const std::vector<T>& b) {
  if (a.size() != b.size()) {
    cout << "Trying to sum vectors with different size, exiting" << endl;
    exit(-1);
  };

  for (int i = 0; i < static_cast<int>(a.size()); i++) a[i] += b[i];

  // Alternativamente si puo' usare l'algoritmo transform della STL

  return a;
}

// ===============================================================================
// sottrai ad a un vettore b e il risultato viene messo in a
// ===============================================================================

template <typename T>
inline std::vector<T>& operator-=(std::vector<T>& a, const std::vector<T>& b) {
  if (a.size() != b.size()) {
    cout << "Trying to sum vectors with different size, exiting" << endl;
    exit(-1);
  };

  for (int i = 0; i < static_cast<int>(a.size()); i++) a[i] -= b[i];

  // Alternativamente si puo' usare l'algoritmo transform della STL

  return a;
}

// ===============================================================================
// Possiamo usare funzioni generiche che agiscono sui vettori
// ===============================================================================

// metodo comodo per stampare il vettore

template <typename T>
inline void Print(const std::vector<T>& v) {
  std::cout << "Printing vector" << std::endl;
  for (auto it = v.begin(); it != v.end(); it++) std::cout << *it << " ";
  std::cout << std::endl;
  std::cout << "End of printing vector" << std::endl;
};

// ===============================================================================
// Possiamo costruire una classe che erediti da vector ed abbia gli operatori
// come data membri.
// ===============================================================================

#endif