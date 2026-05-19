/* SPDX-License-Identifier: MIT */

#ifndef PLATFORM_EXPRESSION_DISPLAY_H
#define PLATFORM_EXPRESSION_DISPLAY_H

#include "claw/core/errno.h"

claw_err_t platform_expression_set(const char *name);
const char *platform_expression_current(void);
int platform_expression_launch(void);
void platform_expression_shutdown(void);

#endif /* PLATFORM_EXPRESSION_DISPLAY_H */
