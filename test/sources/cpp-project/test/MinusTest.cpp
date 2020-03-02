#include <gtest/gtest.h>
#include "minus.hpp"

TEST(MinusTest, testShouldReturnExpectedValue) {
  ASSERT_EQ(-1, arithmetic::minus(1, 2));
}
