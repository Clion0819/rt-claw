/* SPDX-License-Identifier: MIT */

#ifndef PLATFORM_LINUX_LOCAL_VOICE_BUTTON_H
#define PLATFORM_LINUX_LOCAL_VOICE_BUTTON_H

#ifdef __cplusplus
extern "C" {
#endif

int local_voice_button_init(void);
int local_voice_button_start(void);
void local_voice_button_stop(void);
int local_voice_button_running(void);

#ifdef __cplusplus
}
#endif

#endif /* PLATFORM_LINUX_LOCAL_VOICE_BUTTON_H */
