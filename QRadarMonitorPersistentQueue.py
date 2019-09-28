#!/usr/bin/env python

# This script monitors the QRadar Presistent Storage Folder
# QRadarMonitorPersistentQueue.py
# This tool was designed to monitor the QRadar Persistent Storage Folder because of all the heartaches it is causing
# Currently there is no simpler way to monitor this folder for backblog

__author__ = 'Nik Alleyne'
__author_blog__ = 'www.securitynik.com'
__copyright__ = 'SecuityNik'
__credits__ = 'Nik Alleyne'
__version__ = '1.0.1'
__email__ = 'nikalleyne at gmail dot com'
__status__ = 'Production Ready'


import datetime
import os
import sys
import subprocess as sp
from socket import gethostname as hostname
import smtplib
import email.utils
from email.mime.text import MIMEText as mt


# Verify Qradar and OS version
def verify_os_qradar_version():
	# Clear the screen
	sp.call(['clear'])
	if ( sys.platform == 'linux2' ):
		print('[*] Running on Linux ...')
		
		print('[*] Checking QRadar Version ...')
		qradar_version = sp.check_output(['/opt/qradar/bin/getHostVersion.sh']).split('\n')[2]

		if (qradar_version.startswith('qradar')):
			print('[*] Found QRadar Version:{} '.format(qradar_version.split('=')[1]))
		else:
			print('[!] Unable to determine QRadar Version!')

	else:
		print('[*] Not running on Linux. Exiting ...')
		sys.exit(0)


# Cheeck the directory size 
def check_directory(num_files, dir_size):
	# Declare variables
	persistent_directory_path = '/store/persistent_queue/ecs-ec-ingress.ecs-ec-ingress/'
	max_files = 10 #10 files
	max_dir_size = 10000000000 #10GB
	current_dir_size = 0


	# Check if the directory path exists
	print('[*] Checking for directory {} ...'.format(persistent_directory_path))
	if ( (os.path.exists) and ( os.path.isdir(persistent_directory_path)) ):
		print('\t[*] Directory found ...')

		# Get the directory size
		current_dir_size = sp.check_output(['du', '--bytes', '/store/persistent_queue/ecs-ec-ingress.ecs-ec-ingress/']).split('\t')[0]	
		
		# Check whether their are more than 10 files or the directory is larger than 10GB
		if (( len(os.listdir(persistent_directory_path)) < max_files ) or ( current_dir_size < max_dir_size )) :			
			print('\t[*] Current number of file is: {} '.format(len(os.listdir(persistent_directory_path))))
			print('\t[*] Directory size is: {} Bytes '.format(current_dir_size))
			print('[***] System looks ok! [***]:-)')
		else:
			print('\t[!] Current number of files in the directory: {} '.format(len(os.listdir(persistent_directory_path))))
			print('\t[!] Current Directory size is: {} Bytes '.format(current_dir_size))
			print('[!!!] Possible issue with the persistent queue!')
	else:
		print('[!] Error! Directory not found!')

	return len(os.listdir(persistent_directory_path)), current_dir_size


# Setup and send email
def mailer(num_files, dir_size):
	print('[*] In Mailer!!')

	#You will have to formal the email below properly
	send_to = ['Nik Alleyne <nik alleyne at gmail dot com>']
	send_from = email.utils.formataddr(('IBM QRadar' , 'IBMQRadar@securitynik.local'))
	
	qradar_version = sp.check_output(['/opt/qradar/bin/getHostVersion.sh']).split('\n')[2]


	# Read Qradar Device Hostname
	msg_body = '[*] Running on host: {} \n' .format(hostname())
	msg_body = msg_body + '\n[*] Current QRadar Version: {} \n'.format(qradar_version.split('=')[1])
	msg_body = msg_body + '\n[*] Persistent Folder: /store/persistent_queue/ecs-ec-ingress.ecs-ec-ingress/ \n'
	msg_body = msg_body + '\n[*] Current Status as of {} \n'.format(datetime.datetime.now())
	msg_body = msg_body + '\n[*] Current Number of files: {} \n'.format(num_files)
	msg_body = msg_body + '\n[*] Current Directory Size in Bytes:{}B \n'.format(dir_size)
	msg_body = msg_body + '\n[*] Current Directory Size in MBs: {}M'.format(int(dir_size)/1000000)
	msg_body = msg_body + '\n[*] Current Directory Size in Gigs: {}G'.format(int(dir_size)/1000000000)	
	msg_body = msg_body + '\n\n ***Powered By Sirius Computer Solutions *** \n\n'
	
	print('[*] Preparing to send mail ... ')
	msg = mt(msg_body)
	msg['To'] = ','.join(send_to)
	msg['From'] = send_from
	
	if ( (num_files < 10 ) and (int(dir_size) < 10000000000 ) ):
		msg['Subject'] = '[**] {} :: INFORMATIONAL - Monitoring of Persistent Queue [**]'.format(hostname())
	else:
		msg['Subject'] = '[!!] {} :: POTENTIAL PROBLEM - Persistent Queue is growing [!!]'.format(hostname())

	send_mail = smtplib.SMTP('localhost')

	try:
      # once again, you will have to properly format the email    
			send_mail.sendmail(send_from, 'nikalleyne at gmail dot com' , msg.as_string())
			print('[*] Mail sent successfully!')
	except:
		print('[!] Ooops! Looks like an error occurred while sending the mail.')	

	send_mail.quit()
	

# main function
def main():
	print('[*] In Main!')
	verify_os_qradar_version()
	num_files,dir_size = check_directory(0,0)
	mailer(num_files,dir_size)


if __name__ == '__main__':
	main()