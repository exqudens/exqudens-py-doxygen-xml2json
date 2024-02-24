#include "exqudens/math.h"
#include "exqudens/math_util.h"

/*!
* @addtogroup EXQUDENS_MATH
* @{
*/

/*!
* @private @memberof ExqudensMath
*/
static int add(int a, int b);

/*!
* @details Public sum of two integer values.
* @public @memberof ExqudensMath
*/
int exqudens_math_add(int a, int b) {
  return add(a, b);
}

/*!
* @private @memberof ExqudensMath
*/
static int add(int a, int b) {
  return exqudens_math_util_add(a, b);
}

//! @}
