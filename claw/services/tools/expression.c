/* SPDX-License-Identifier: MIT */

#include <string.h>
#include "claw/services/tools/tools.h"
#include "claw/core/errno.h"
#include "platform/expression_display.h"
#include "cJSON.h"

#define TAG "tool_expr"

static const char schema_expression_set[] =
    "{\"type\":\"object\","
    "\"properties\":{"
    "\"expression\":{\"type\":\"string\","
    "\"enum\":[\"idle\",\"happy\",\"thinking\",\"sad\","
    "\"listening\",\"speaking\"],"
    "\"description\":\"Expression to show on the local display\"}},"
    "\"required\":[\"expression\"]}";

static claw_err_t tool_expression_set(struct claw_tool *tool,
                                      const cJSON *params,
                                      cJSON *result)
{
    cJSON *expr_j = cJSON_GetObjectItem(params, "expression");
    (void)tool;


    if (!expr_j || !cJSON_IsString(expr_j)) {
        cJSON_AddStringToObject(result, "error",
                                "missing expression parameter");
        CLAW_LOGW(TAG, "expression_set called without expression param");
        return CLAW_ERROR;
    }

    const char *expr = expr_j->valuestring;
    const char *prev = platform_expression_current();

    if (platform_expression_set(expr) != CLAW_OK) {
        cJSON_AddStringToObject(result, "error",
                                "failed to set expression");
        CLAW_LOGW(TAG, "platform_expression_set(%s) failed", expr);
        return CLAW_ERROR;
    }

    CLAW_LOGI(TAG, "expression %s -> %s",
              prev ? prev : "none", expr);

    cJSON_AddStringToObject(result, "status", "ok");
    cJSON_AddStringToObject(result, "expression", expr);
    cJSON_AddStringToObject(result, "previous",
                            prev ? prev : "none");

    return CLAW_OK;
}

static const struct claw_tool_ops expression_set_ops = {
    .execute = tool_expression_set,
};

static struct claw_tool expression_set_tool = {
    .name = "expression_set",
    .description = "Switch the local expression window to a named expression.",
    .input_schema_json = schema_expression_set,
    .ops = &expression_set_ops,
    .flags = CLAW_TOOL_LOCAL_ONLY,
};

CLAW_TOOL_REGISTER(expression_set, &expression_set_tool);
