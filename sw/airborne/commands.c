/*  $Id$
 *
 * (c) 2006 Pascal Brisset, Antoine Drouin
 *
 * This file is part of paparazzi.
 *
 * paparazzi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * paparazzi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with paparazzi; see the file COPYING.  If not, write to
 * the Free Software Foundation, 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 *
 */

/** \file commands.c
 *  \brief Hardware independent data structures for commands handling
 *
 */

#include "commands.h"

#ifndef COMMAND_ROLL_TRIM
#define COMMAND_ROLL_TRIM 0
#endif

#ifndef COMMAND_PITCH_TRIM
#define COMMAND_PITCH_TRIM 0
#endif

#ifndef COMMAND_YAW_TRIM
#define COMMAND_YAW_TRIM 0
#endif

pprz_t command_roll_trim = COMMAND_ROLL_TRIM;
pprz_t command_pitch_trim = COMMAND_PITCH_TRIM;
pprz_t command_yaw_trim = COMMAND_YAW_TRIM;


pprz_t commands[COMMANDS_NB];
const pprz_t commands_failsafe[COMMANDS_NB] = COMMANDS_FAILSAFE;