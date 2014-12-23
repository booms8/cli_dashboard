#!/usr/bin/env python2.7

import time
import psutil
import sys
from progressbar import ProgressBar

cpus = []
cores = psutil.cpu_count()

mem = ProgressBar(1000, pos = 1, width = 0.5, ansi = True, fillchar = '#')
mem.set_bar_color('G')
mem.set_perc_color('B')
mem.set_msg_color('Y')

swp = ProgressBar(1000, pos = 2, width = 0.5, ansi = True, fillchar = '#')
swp.set_bar_color('G')
swp.set_perc_color('B')
swp.set_msg_color('Y')

tot = ProgressBar(1000, pos = (4 + cores), width = 0.5, ansi = True, fillchar = '#')
tot.set_bar_color('G')
tot.set_perc_color('B')
tot.set_msg_color('M')

mem.draw('RAM')
swp.draw('Swap')

for i in range(cores):
	cpus.append(ProgressBar(1000, pos = (4 + i), width = 0.5, ansi = True, fillchar = '#'))
	cpus[i].set_bar_color('G')
	cpus[i].set_perc_color('B')
	cpus[i].set_msg_color('M')
	cpus[i].draw('CPU #{}'.format(i + 1))

tot.draw('Total CPU')

print '\033[?25l'

try:
	while (True):
		mem.change_progress(psutil.virtual_memory().percent * 10)
		swp.change_progress(psutil.swap_memory().percent * 10)

		perc = psutil.cpu_percent(percpu = True)
		for i in range(cores):
			cpus[i].change_progress(perc[i] * 10)

		tot.change_progress(psutil.cpu_percent() * 10)

		time.sleep(1)

except KeyboardInterrupt:
	print '\033[?25h'
	pass
