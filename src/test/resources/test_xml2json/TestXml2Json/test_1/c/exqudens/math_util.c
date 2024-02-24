#include "exqudens/math_util.h"

/*! @addtogroup EXQUDENS_MATH
* @{
*/

/*!
* @brief Private add int to int.
* @private
*/
static int exqudens_math_util_internal_add(int a, int b);

/*!
* @details Private sum of two integer values.
*/
static int exqudens_math_util_internal_add(int a, int b) {
  return a + b;
}

/*!
* @details Protected sum of two integer values.
* @protected
*/
int exqudens_math_util_add(int a, int b) {
  return exqudens_math_util_internal_add(a, b);
}

/*!
* @protected
*/
int exqudens_math_util_subtract(int a, int b) {
  return a - b;
}

//! @}
