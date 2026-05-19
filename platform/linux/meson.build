# SPDX-License-Identifier: MIT
# Linux native platform: link claw + osal + cjson → executable

platform_src = files(
    'main.c',
    'shell.c',
    'board.c',
    'ota_stub.c',
)

if get_option('tool_script')
    platform_src += files('scripting.c')
endif
if get_option('linux_web_voice')
    if not get_option('voice')
        error('linux_web_voice requires voice=true')
    endif
    platform_src += files('web_voice_server.c')
endif
if get_option('linux_local_voice')
    if not get_option('voice')
        error('linux_local_voice requires voice=true')
    endif
    platform_src += files('local_voice_endpoint.c')
endif

# ===== 新增：按钮和表情平台文件 =====
if get_option('linux_local_voice_button')
    if not get_option('linux_local_voice')
        error('linux_local_voice_button requires linux_local_voice=true')
    endif
    platform_src += files('local_voice_button.c')
endif

if get_option('tool_expression')
    platform_src += files('expression_display_linux.c')
endif
# ==================================

thread_dep = dependency('threads')
platform_c_args = platform_defs

if get_option('tool_script')
    platform_c_args += '-DCONFIG_RTCLAW_TOOL_SCRIPT'
endif
if get_option('voice')
    platform_c_args += '-DCONFIG_RTCLAW_VOICE_ENABLE'
endif
if get_option('linux_web_voice')
    platform_c_args += '-DCONFIG_RTCLAW_LINUX_WEB_VOICE_ENABLE'
endif
if get_option('linux_local_voice')
    platform_c_args += '-DCONFIG_RTCLAW_LINUX_LOCAL_VOICE_ENABLE'
endif

# ===== 新增：按钮和表情的编译定义 =====
if get_option('linux_local_voice_button')
    platform_c_args += '-DCONFIG_RTCLAW_LINUX_LOCAL_VOICE_BUTTON_ENABLE'
endif
if get_option('tool_expression')
    platform_c_args += '-DCONFIG_RTCLAW_TOOL_EXPRESSION'
endif
# ======================================

rtclaw_exe = executable('rtclaw',
    platform_src,
    include_directories: [claw_inc, claw_root_inc],
    c_args: platform_c_args,
    dependencies: [rtclaw_dep, osal_dep, cjson_dep, thread_dep],
    install: false,
)

# Unit test executable — links ota_stub.c for OTA symbol resolution
test_main_src = files('../../tests/unit/test_main_linux.c')
test_incs = include_directories('../../tests/unit')
test_platform_src = files('ota_stub.c')

if get_option('tool_script')
    test_platform_src += files('scripting.c')
endif
if get_option('linux_web_voice')
    test_platform_src += files('web_voice_server.c')
endif
if get_option('linux_local_voice')
    test_platform_src += files('local_voice_endpoint.c')
endif

# ===== 新增：测试也包含按钮和表情文件 =====
if get_option('linux_local_voice_button')
    test_platform_src += files('local_voice_button.c')
endif

if get_option('tool_expression')
    test_platform_src += files('expression_display_linux.c')
endif
# ==========================================

rtclaw_test_exe = executable('rtclaw_test',
    test_main_src + test_platform_src,
    include_directories: [claw_inc, claw_root_inc, test_incs],
    c_args: platform_c_args,
    link_with: [unittest_lib],
    dependencies: [rtclaw_dep, osal_dep, cjson_dep, thread_dep],
    install: false,
)