build_test_program(
  NAME OperatorTest
  SUFFIX .out
  SRCS PlusTest.cpp MinusTest.cpp
  LIBS plus minus
)
