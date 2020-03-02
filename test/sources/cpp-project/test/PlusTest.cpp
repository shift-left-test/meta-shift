#include <gtest/gtest.h>
#include "plus.hpp"

TEST(PlusTest, testShouldReturnExpectedValue) {
  ASSERT_EQ(3, arithmetic::plus(1, 2));
}
