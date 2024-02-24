#ifndef EXQUDENS_MATH_H_INCLUDED
#define EXQUDENS_MATH_H_INCLUDED

#ifdef __cplusplus
extern "C" {
#endif

/*!
* @addtogroup EXQUDENS_MATH
* @{
*/

#ifndef DOXYGEN_SKIP_THIS

typedef struct ExqudensMath ExqudensMath;

#endif // DOXYGEN_SKIP_THIS

struct ExqudensMath {
  unsigned int versionMajor;
  unsigned int versionMinor;
  unsigned int versionBuild;
};

/*!
* @brief Public add int to int.
* @public @memberof ExqudensMath
* @see function math
* @todo fix this
*/
int exqudens_math_add(int a, int b);

//! @}

#ifdef __cplusplus
}
#endif

#endif
