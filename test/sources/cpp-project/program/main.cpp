#include <iostream>
#include "plus.hpp"
#include "minus.hpp"

int main(int argc, char *argv[]) {
  int result = arithmetic::plus(1, 2) + arithmetic::minus(1, 2);
  std::cout << "(1 + 2) + (1 - 2) = " << result << std::endl;
  return 0;
}
