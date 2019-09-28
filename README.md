# QRadarPersistentStorageMonitoring
Monitors The IBM QRadar Persistent Storage Folder to detect if there is a backlog of events being processed

Recently on at least two occasions, I encountered a problem whereby the IBM QRadar Persistent Storage Folder '/store/persistent_queue/ecs-ec-ingress.ecs-ec-ingress/' fills up and causes a backlog of events. This means, events shown on the events tabs have a date in the past, even though the log sources are streaming in real time.

To monitor this folder, I developed a script which I believe helps to detect this issue sooner rather than later.

Here is an example of the output from the email once the script runs successfully


Subject: [**] qradar.securitynik.local :: INFORMATIONAL - Monitoring of Persistent Queue [**]

[*] Running on host: qradar.securitynik.local

[*] Current QRadar Version: "7.3.2"

[*] Persistent Folder: /store/persistent_queue/ecs-ec-ingress.ecs-ec-ingress/

[*] Current Status as of 2019-09-27 16:35:26.033240

[*] Current Number of files: 3

[*] Current Directory Size in Bytes:104962873B

[*] Current Directory Size in MBs: 104M
[*] Current Directory Size in Gigs: 0G

 ***Powered By SecurityNik ***



